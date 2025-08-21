<!-- File: xslt/rubaiyat.xsl -->
<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:tei="http://www.tei-c.org/ns/1.0"
  exclude-result-prefixes="tei">

  <xsl:output method="html" encoding="UTF-8" indent="yes" />

  <!-- Root: build an HTML5 page -->
  <xsl:template match="/tei:TEI">
    <html lang="en">
      <head>
        <meta charset="utf-8" />
        <title>
          <xsl:value-of select="normalize-space(tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:title)"/>
        </title>
        <style>
          /* Minimal, readable CSS */
          :root { font-family: ui-serif, Georgia, "Times New Roman", serif; line-height: 1.6; }
          body { max-width: 72ch; margin: 2rem auto; padding: 0 1rem; }
          header h1 { margin: 0 0 .25rem; font-size: 1.8rem; }
          header p  { margin: .1rem 0; color: #444; }
          .rubai  { margin: 1.2rem 0; padding: .8rem 1rem; background: #fafafa; border: 1px solid #eee; border-radius: .5rem; }
          .rubai .num { font-variant-numeric: tabular-nums; color: #666; float: right; }
          .l { display: block; white-space: pre-wrap; }
          .persName { background: #fff3; border-bottom: 1px dotted #999; }
          .placeName { background: #fff3; border-bottom: 1px dashed #999; }
          .rs.object { background: #fff3; }
          footer { margin: 2rem 0; font-size: .9rem; color: #666; }
          .meta { color:#666; }
        </style>
      </head>
      <body>
        <header>
          <h1>
            <xsl:value-of select="normalize-space(tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:title)"/>
          </h1>
          <p class="meta">
            <strong>Author:</strong>
            <xsl:value-of select="normalize-space(tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:author)"/>
            • <strong>Translator:</strong>
            <xsl:value-of select="normalize-space(tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:editor[@role='translator'])"/>
          </p>
        </header>

        <!-- Body: render each rubā‘ī -->
        <main>
          <xsl:apply-templates select="tei:text/tei:body/tei:div[@type='rubaiyat']"/>
        </main>

        <footer>
          Generated from TEI via XSLT.
        </footer>
      </body>
    </html>
  </xsl:template>

  <!-- A single rubā‘ī (div) -->
  <xsl:template match="tei:div[@type='rubaiyat']">
    <section class="rubai">
      <span class="num">
        <xsl:value-of select="@n"/>
      </span>
      <xsl:apply-templates select="tei:lg"/>
    </section>
  </xsl:template>

  <!-- The stanza (lg) and lines (l) -->
  <xsl:template match="tei:lg">
    <xsl:for-each select="tei:l">
      <span class="l">
        <xsl:apply-templates/>
      </span>
    </xsl:for-each>
  </xsl:template>

  <!-- Inline entity rendering -->
  <xsl:template match="tei:persName">
    <span class="persName">
      <xsl:apply-templates/>
    </span>
  </xsl:template>

  <xsl:template match="tei:placeName">
    <span class="placeName">
      <xsl:apply-templates/>
    </span>
  </xsl:template>

  <xsl:template match="tei:rs">
    <span>
      <xsl:attribute name="class">
        <xsl:text>rs</xsl:text>
        <xsl:if test="@type"><xsl:text> </xsl:text><xsl:value-of select="@type"/></xsl:if>
      </xsl:attribute>
      <xsl:apply-templates/>
    </span>
  </xsl:template>

  <!-- Fallback: copy text only for anything unhandled -->
  <xsl:template match="text()">
    <xsl:value-of select="."/>
  </xsl:template>
</xsl:stylesheet>
