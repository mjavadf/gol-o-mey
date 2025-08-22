from pathlib import Path
import csv
from urllib.parse import quote
from lxml import etree
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, XSD, DCTERMS, FOAF, Namespace

XML = Namespace("http://www.w3.org/XML/1998/namespace")
BASE = Namespace("https://mjavadf.github.io/gol-o-mey/rdf/graph.ttl#")
SCHEMA = Namespace("http://schema.org/")
OWL = Namespace("http://www.w3.org/2002/07/owl#")

ROOT = Path(__file__).resolve().parents[1]
TEI_FILE = ROOT / "tei" / "rubaiyat.xml"
CSV_FILE = ROOT / "data" / "artwork_metadata.csv"
OUT_FILE = ROOT / "rdf" / "graph.ttl"

NS = {"tei": "http://www.tei-c.org/ns/1.0"}

def mint(kind: str, label: str) -> URIRef:
    slug = quote(label.strip().replace(" ", "_"), safe="_-")
    return BASE[slug]

def add_if(g: Graph, s, p, o):
    if o is None:
        return
    if isinstance(o, str) and not o.strip():
        return
    g.add((s, p, o if isinstance(o, (URIRef, Literal)) else Literal(o)))

# --- helpers (put above tei_to_rdf) ---------------------------------------
def index_list(g, root, list_xpath, name_xpath, kind, rdf_type, label_prop):
    """Build entities from listPerson/listPlace and return a {#id: URI} index."""
    idx = {}
    for el in root.findall(list_xpath, NS):
        xmlid = el.get(f"{{{str(XML)}}}id")
        name_el = el.find(name_xpath, NS)
        label = (getattr(name_el, "text", None) or xmlid or "").strip()
        if not label:
            continue
        uri = mint(kind, label)
        g.add((uri, RDF.type, rdf_type))
        g.add((uri, label_prop, Literal(label)))
        if xmlid:
            idx[f"#{xmlid}"] = uri
        for attr in ("sameAs", "ref"):
            for v in (el.get(attr) or "").split():
                add_if(g, uri, OWL.sameAs, URIRef(v))
    return idx

def resolve_mentions(g, root, work_uri, xpath, idx, kind, rdf_type, label_prop):
    """Link body mentions to indexed URIs or mint new ones; add owl:sameAs if ref is http(s)."""
    for el in root.findall(xpath, NS):
        ref = (el.get("ref") or "").strip()
        label = ("".join(el.itertext()).strip() or el.get("key") or ref)
        uri = idx.get(ref)
        if not uri:
            uri = mint(kind, label)
            g.add((uri, RDF.type, rdf_type))
            add_if(g, uri, label_prop, Literal(label))
            if ref.startswith("http"):
                add_if(g, uri, OWL.sameAs, URIRef(ref))
        g.add((work_uri, SCHEMA.mentions, uri))

# --- compact tei_to_rdf ----------------------------------------------------
def tei_to_rdf(g: Graph):
    root = etree.parse(str(TEI_FILE)).getroot()

    work_uri = mint("work", "rubaiyat")
    g.add((work_uri, RDF.type, SCHEMA.CreativeWork))

    title_el = root.find(".//tei:fileDesc/tei:titleStmt/tei:title", NS)
    if title_el is not None and (title := title_el.text):
        g.add((work_uri, DCTERMS.title, Literal(title)))

    auth_el = root.find(".//tei:fileDesc/tei:titleStmt/tei:author", NS)
    if auth_el is not None and (aname := auth_el.text):
        a = mint("person", aname)
        g.add((a, RDF.type, FOAF.Person)); g.add((a, FOAF.name, Literal(aname)))
        g.add((work_uri, DCTERMS.creator, a))

    date_el = root.find(".//tei:profileDesc//tei:creation//tei:date[@when]", NS) \
              or root.find(".//tei:date[@when]", NS)
    if date_el is not None and (when := date_el.get("when")):
        dt = XSD.date if len(when) == 10 and when[4] == "-" else (XSD.gYear if len(when) == 4 else None)
        g.add((work_uri, DCTERMS.date, Literal(when, datatype=dt) if dt else Literal(when)))

    # build authority indexes
    person_idx = index_list(g, root, ".//tei:listPerson/tei:person", ".//tei:persName", "person", FOAF.Person, FOAF.name)
    place_idx  = index_list(g, root, ".//tei:listPlace/tei:place",  ".//tei:placeName", "place",  SCHEMA.Place, RDFS.label)

    # link body mentions (reusing indexes)
    resolve_mentions(g, root, work_uri, ".//tei:persName[@ref]", person_idx, "person", FOAF.Person, FOAF.name)
    resolve_mentions(g, root, work_uri, ".//tei:placeName[@ref]", place_idx,  "place",  SCHEMA.Place, RDFS.label)

    # optional: keywords
    for t in root.findall(".//tei:textClass//tei:keywords//tei:term", NS):
        kw = (t.text or "").strip()
        if kw:
            g.add((work_uri, SCHEMA.keywords, Literal(kw)))

def csv_to_rdf(g: Graph):
    with open(CSV_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            title = row.get("Title") or "Untitled"
            obj_uri = mint("object", title)
            g.add((obj_uri, RDF.type, SCHEMA.CreativeWork))
            g.add((obj_uri, DCTERMS.title, Literal(title)))

            # Artist
            artist = row.get("Artist")
            if artist:
                a_uri = mint("person", artist)
                g.add((a_uri, RDF.type, FOAF.Person))
                g.add((a_uri, FOAF.name, Literal(artist)))
                g.add((obj_uri, SCHEMA.creator, a_uri))

            # Date / Location / Mediums / Description / Rights
            if row.get("Date"):
                g.add((obj_uri, SCHEMA.dateCreated, Literal(row["Date"])))
            if row.get("Location"):
                g.add((obj_uri, SCHEMA.locationCreated, Literal(row["Location"])))
            # Prefer detailed description if present, else Mediums
            med_desc = row.get("MediumsDescription") or row.get("Mediums")
            if med_desc:
                g.add((obj_uri, SCHEMA.material, Literal(med_desc)))
            if row.get("CreditLine"):
                g.add((obj_uri, DCTERMS.provenance, Literal(row["CreditLine"])))
            if row.get("Classification"):
                g.add((obj_uri, SCHEMA.artform, Literal(row["Classification"])))
            if row.get("Subjects"):
                g.add((obj_uri, SCHEMA.keywords, Literal(row["Subjects"])))
            if row.get("rights"):
                g.add((obj_uri, DCTERMS.rights, Literal(row["rights"])))

            # Links & image
            for k in ("URL", "source_uri", "lod_uri"):
                val = row.get(k)
                if val:
                    g.add((obj_uri, FOAF.page, URIRef(val)))
            if row.get("image_uri"):
                g.add((obj_uri, SCHEMA.image, URIRef(row["image_uri"])))

def main():
    g = Graph()
    g.bind("dcterms", DCTERMS)
    g.bind("foaf", FOAF)
    g.bind("schema", SCHEMA)
    g.bind("owl", OWL)
    g.bind("", BASE)

    tei_to_rdf(g)
    csv_to_rdf(g)

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    g.serialize(destination=str(OUT_FILE), format="turtle")
    print(f"Wrote {OUT_FILE} with {len(g)} triples.")

if __name__ == "__main__":
    main()
