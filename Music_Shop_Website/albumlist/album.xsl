<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:music="http://RusticRhythmsXML.com/XML">

<xsl:output method="html" indent="yes"/>

<!-- root template -->
    <xsl:template match="/">
        <html>
            <head>
                <title>Raw XSL Data | All Albums | Rustic Rhythms</title>
            </head>
            <body>
			
				<!-- button to back to exit album list -->
				<a href="../storefront/store.xml" 
				style="position: fixed; top: 10px; right: 10px; padding: 10px; background-color: #950606; color: white; border: none; text-decoration: none;">
					Go Back to Store
				</a>
                <xsl:for-each select="store/music:genre">
                    <h2><xsl:value-of select="@name"/></h2>
                    <p><xsl:value-of select="music:details"/></p>
					
					<!-- table for each genre -->
                    <table border="1" cellspacing="0" cellpadding="8">
                        <tr>
                            <th style="background-color: #EADDCA;">Title</th>
                            <th style="background-color: #EADDCA;">Artist</th>
                            <th style="background-color: #EADDCA;">Price</th>
                            <th style="background-color: #EADDCA;">Tracklist</th>
                            <th style="background-color: #EADDCA;">Description</th>
                        </tr>
						
						<!-- album details from XML file to insert into table -->
                        <xsl:for-each select="music:album">
                            <tr>
                                <td><xsl:value-of select="music:title"/></td>
                                <td><xsl:value-of select="music:artist"/></td>
                                <td><xsl:value-of select="music:price"/></td>
                                <td>
                                    <ul>
                                        <xsl:for-each select="music:tracklist/music:track">
                                            <li><xsl:value-of select="."/></li>
                                        </xsl:for-each>
                                    </ul>
                                </td>
                                <td><xsl:value-of select="music:description"/></td>
                            </tr>
                        </xsl:for-each>
                    </table>
                    <br/>
                </xsl:for-each>
            </body>
        </html>
    </xsl:template>

</xsl:stylesheet>
