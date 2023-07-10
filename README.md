# Calories web site 

My solution for *Advanced Python Programming: Build 10 OOP Applications* Sections 21-25.  

## Description
One-page toy web app to calculate the number of calories you need based on some of your body characteristics (height, weight, age) and local (city, country).  It scrapes the temperature of your locale from the web.  It then predicts the number of calories you need to consume for the upcoming day.

The scraping source is timeanddate.com = but there is one weakness - forming a URL for an ambiguous city name (e.g., Albany NY vs Albany, GA) looks like it uses either some sort of lookup for geo position, or it can use postal code in some countries.  But none of this appears to be document.  Ardit depends only on (city, country),  So I'm going to allow the same limitation.  I'm also not going to check for whatever the valid country name might be, if they get it wrong I'll give them a link to try directly.

My classes are different from his, more logical to me.  Also, I'm doing a little above and beyond by:
  - checking inputs (possible duplication with Flask validators)
  - supporting both English and metric units
