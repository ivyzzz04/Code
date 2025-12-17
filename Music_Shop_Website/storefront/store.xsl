<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:output method="html" indent="yes"/>

<!-- root template -->
<xsl:template match="/">
<html>
    <head>
		<title>Store | Rustic Rhythms</title>
		<link rel="stylesheet" type="text/css" href="../styles.css" />
    </head>
	
    <body class="store">
	
<!-- top bar -->
<div style="z-index:1000; position: relative; padding: 0.9rem 0.5rem; background:#432818; border-bottom: 1px solid #FFE6A7; height: 60px; display: flex; align-items: center; justify-content: space-between;">
  <img src="../images/logo.png" style="height: 40px; margin-left: 60px;" />
  
  <div style="display: flex; align-items: center; gap: 10px; margin-right: 20px;">
	<img src="../images/search.png" style="height: 60px; margin-left:10px;" />
    <input type="text" placeholder="Search..." style="padding: 0.5rem; border: 1px solid #2C1A0f; border-radius: 6px 0 0 6px; width: 150px;" />
    <a href="../login.html"><img src="../images/profile.png" style="height: 30px; margin-left:10px;" /></a>
	<a href="../checkout.html"><img src="../images/cart.png" style="height: 30px; margin-left:10px;" /></a>

  </div>
</div>


<!-- nav bar -->
<nav style="padding: 0.4rem 2rem; background: rgba(255, 255, 240, 0.35); position: sticky; top: 0; z-index: 900; box-shadow: 0 0 15px rgba(0, 0, 0, 0.1); backdrop-filter: blur(2px); -webkit-backdrop-filter: blur(2px);">
  <ul style="display: flex; justify-content: center; align-items: center; gap: 6rem; list-style: none; margin: 0; padding: 0;">
    <li><a href="#" style="color: #2C1A0f; text-decoration: none; padding: 0.9rem;">What's New</a></li>
    <li><a href="store.xml" style="color: #2C1A0f; text-decoration: none; padding: 0.9rem;">Store</a></li>
    <li>
      <a href="../index.html" style="font-family: 'Arial Black', sans-serif; color: #2C1A0f; font-size: 1.8rem; font-weight: 900; letter-spacing: 2px; padding: 0.9rem 1rem; text-decoration: none;">
        <strong>RUSTIC RHYTHMS</strong>
      </a>
    </li>
    <li><a href="../about.html" style="color: #2C1A0f; text-decoration: none; padding: 0.9rem;">About Us</a></li>
    <li><a href="../contact.html" style="color: #2C1A0f; text-decoration: none; padding: 0.9rem;">Contact Us</a></li>
  </ul>
</nav>	
	

<!-- categories section & raw XSL file -->
<div class="store-field">
		<div class="category-field">
		<h3 style="line-height: 3.0;">Category</h3>
		<div class="category-item">□ Pop</div>
		<div class="category-item">□ Hip Hop</div>
		<div class="category-item">□ R'n'B</div>
		<div class="category-item">□ Rock</div>
		<div class="category-item">□ K-Pop</div>
		<div class="category-item">□ Jazz</div>
	<div style="margin-top: 20px;">
	  <a href="../albumlist/album.xml" 
		 style="display: inline-block; padding: 8px 12px; background-color: #99582a; color: #FFFFF0; text-decoration: none; border-radius: 4px; font-size: 0.9rem; border: 1px solid #2C1A0f;">
		Show All Albums
	  </a>
	</div>
</div>
        
<!-- album display -->
        <div class="album-content-field">
			<div class="content-text">
			<h1 style="color: #99582a; font-size: 27.6px; font-weight: bold; line-height: 2.0;">Store</h1>
			<p style="font-size: 15.4px; line-height: 1.8;">Discover a harmonious universe of vinyl records spanning Pop, Rock, Hip Hop &amp; RnB, Jazz &amp; Blues, Classical &amp; Opera, and the rich melodies of Arabic music.</p>
			</div>
		
		<!-- album display based on genre -->	
		<xsl:for-each select="store/genre">
		<div class="genre-field">
			<h2 style="font-size: 20.6px; font-weight: bold;"><xsl:value-of select="@name"/></h2>
			<p style="font-size: 14.6px; line-height: 1.8; margin-top: 10px; margin-bottom: 15px;"><xsl:value-of select="details"/></p>
		
		<!-- display of album details -->
		<xsl:for-each select="album">
		<div class="album-cell">
			<img src="{ cover }" alt="album cover" class="album-cover-cell" />
			<div>

		<h2 class="album-name-cell">
		  <xsl:value-of select="title"/> | <xsl:value-of select="artist"/>
		</h2>
			
			<!-- add to cart button -->	
			<div class="add-to-cart-field">
			<p class="album-price-cell"><xsl:value-of select="price"/></p>
			<div class="add-to-cart">
				<button class="quantity-button">-</button>
				<h6 style="font-size: 22.5px; text-align: center; padding: 0; margin: 0;"><b>1</b> QTY</h6>
				<button class="quantity-button">+</button>
			</div>
			</div>
			
			<!-- album description -->	
			<div class="album-description">
				<h3 style="font-size: 16.4px; font-weight: bold; margin-bottom: 15px; color: #99582a;">Album Description</h3>
				<p style="font-size: 14.4px; line-height: 1.8;"><xsl:value-of select="description"/></p>
			</div>
			
			<!-- quantity button -->	
			<div style="text-align: center; margin-top: 20px;">
				<a href="../checkout.html" style="background-color: #99582a; color: white; padding: 12px 24px; border-radius: 8px; text-decoration: none; display: block; width: 100%; max-width: 500px; margin-left: auto; margin-right: auto;">
					Add to Cart
				</a>
			</div>

		</div>
		</div>
		</xsl:for-each>
		</div>
		</xsl:for-each>
		</div>
	</div>

<!-- footer -->
<footer style="background:#120D0A; color:#FFFFF0; padding: 3rem 2rem; display: grid; grid-template-columns: 1fr 1fr; gap: 2rem;align-items:center;">

  <div>
    <p style="margin-bottom:15px;"><strong>Rustic Rhythms</strong></p>
	
    <p>123 Melody Lane, Harmony District, Music City, MC 45678, United Arab Emirates</p>
  </div>
  <div style="display: flex; justify-content: flex-end;width:100%;">
  <div style="display: flex; gap: 1.5rem; flex-wrap: wrap; justify-content: flex-end; align-items:center; margin-top: -50px; margin-right: 100px;">
      <a href="#"><img src="../images/insta.png" alt="Instagram" width="70" height="70" style="display: block; "/></a>
      <a href="#"><img src="../images/facebook.png" alt="Instagram" width="70" height="70" style="display: block;"/></a>
	  <a href="#"><img src="../images/youtube.png" alt="Instagram" width="70" height="70" style="display: block;"/></a>
      <a href="#"><img src="../images/twitter.png" alt="Instagram" width="70" height="70" style="display: block;"/></a>
      <a href="#"><img src="../images/linkedin.png" alt="Instagram" width="70" height="70" style="display: block;"/></a>

  
  </div>
  </div>

<div style="grid-column: 1 / -1;text-align: center;padding-top: 2rem;	border-top: 1px solid #444;">
		<p>Copyright Rustic Rhythms 2025</p>
</div>

</footer>


</body>
</html>
</xsl:template>
</xsl:stylesheet>
