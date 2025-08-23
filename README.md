# Rubáiyát TESR Project

This repository is created for the **Text Encoding and Semantic Representation (TESR)** exam, part of the **Digital Humanities and Digital Knowledge (DHDK)** program at the University of Bologna.  
It focuses on a selection from *The Rubáiyát*, included in *The Persian Literature, Comprising The Shah Nameh, The Rubaiyat, The Divan, and The Gulistan, Volume 1* (Project Gutenberg).

<p align="center">
  <img src="https://github.com/user-attachments/assets/ebfe889f-17b7-41dd-aa35-5f00a1aa413e" width="600" />
</p>

📄 View the HTML version here: [https://mjavadf.github.io/gol-o-mey/](https://mjavadf.github.io/gol-o-mey/)


## About the Source
The digital text for this project is taken from Book *The Persian Literature, Comprising The Shah Nameh, The Rubaiyat, The Divan, and The Gulistan, Volume 1*, which is available at **Project Gutenberg**.
This set, created in the early part of the 20th century, gathered English translations of such perennially popular Persian works, serving not just a primary function as a means by which readers in the West could be introduced to Persian epic, lyric, and didactic traditions, but also a part-function toward their preservation and spread through readership in English.

### About the Rubáiyát
The *Rubáiyát* of Omar Khayyám is a well-known body of quatrains (rubā'īyāt in Persian) which address the concerns of time, fate, love, and the fleeting nature of life.
Even though Khayyám was himself a mathematician, astronomer, and philosopher, his poems came to be famous all across the globe primarily because of 19th-century English translations by Edward FitzGerald. The selected quatrains below demonstrate that dialogue between Persian philosophy and its modern-day reception.

### About the Cultural Object
To supplement the textual edition, this project also includes metadata for an image inspired by the *Rubáiyát*, preserved at the Smithsonian American Art Museum.
The painting—created in the late 19th to early 20th century—symbolizes the Western fascination with Khayyám's poetry and demonstrates how his words traveled across languages and media. Encoding both the literary work and the painting at the same time allows us to place in the foreground this cross-cultural traffic.


## Project Structure

```text
gol-o-mey/
│── main.ipynb              # Jupyter notebook used for testing and exploration
│── README.md               # Project documentation (this file)
│── requirements.txt        # Python dependencies for running scripts
│
├── data/                   # Metadata of the selected cultural object(s)
│   ├── artwork_metadata.csv
│   └── vedder_metadata.json
│
├── docs/                   # Published website (GitHub Pages)
│   └── index.html
│
├── rdf/                    # Final combined RDF dataset
│   └── graph.ttl
│
├── scripts/                # Python scripts for transformations
│   └── build_graph.py      # Converts TEI + object metadata into RDF
│
├── sources/                # Source texts
│   ├── pg10315.txt         # Original Project Gutenberg file
│   ├── the_rubaiyat_clean.txt
│   └── the_rubaiyat.txt
│
├── tei/                    # TEI-encoded version of the chosen text
│   └── rubaiyat.xml
│
└── xslt/                   # XSLT stylesheet for HTML transformation
└── rubaiyat.xsl

```

## Methodology
[] [TO BE COMPLETED]

## Tools & Standards Used

- **TEI P5 (Text Encoding Initiative)** → used to encode the selected quatrains in XML, ensuring scholarly conventions for representing literary texts.
    
- **XSLT (eXtensible Stylesheet Language Transformations)** → transforms the TEI-encoded XML into HTML for web publication.
    
- **HTML + GitHub Pages** → HTML is generated and published online through GitHub Pages for easy access and dissemination.
    
- **RDF (Resource Description Framework)** → used to represent both the encoded text and the cultural object metadata in a graph-based, machine-readable format.
    
- **rdflib (Python library)** → employed to build and serialize RDF graphs from XML/TEI and object metadata.
    
- **Ontologies reused**:
    
    - **Dublin Core (dcterms)** → for basic bibliographic and descriptive metadata.
        
    - **FOAF (Friend of a Friend)** → to describe persons and their relations.
        
    - **Schema.org** → for general cultural heritage object description.
        
- **Project Gutenberg** → source of the digital text, in the public domain.
    
- **Smithsonian American Art Museum** → provider of metadata for the chosen cultural object.

## License & Credits

- **Text Source**: The digital text of _The Rubáiyát_ is taken from _The Persian Literature, Comprising The Shah Nameh, The Rubaiyat, The Divan, and The Gulistan, Volume 1_, made freely available by **Project Gutenberg**. As with all Project Gutenberg works, the text is in the _public domain_.
    
- **Cultural Object**: The metadata describing the artwork is derived from the **Smithsonian American Art Museum** digital collections. Please refer to their site for rights and reproduction terms.
    
- **Code & Scripts**: The code in this repository is released under the **MIT License** (see the [LICENSE](https://github.com/mjavadf/gol-o-mey/blob/main/LICENSE) file for details).

- **Image**: The project banner illustration was created using **Gemini AI**.
    
- **Credits**:
    
    - Project developed by [Mohammad Javad Farokhi Darani](mohammad.farokhi2@studio.unibo.it) as part of the **Text Encoding and Semantic Representation (TESR)** exam in the **DHDK program** at the University of Bologna.
        
    - Supervised by Prof. _Marilena Daquino_.
