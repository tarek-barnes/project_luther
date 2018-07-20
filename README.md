Exploring Zillow's House Prices

For this project, I explored the different features which affected house prices in the San Francisco Bay Area.


zip_by_county_scraper.py -- This is the scraper which compiles a list of ZIP codes by county from Zillow's website.
zip_by_county_parser.py -- This parses the ZIP codes from HTML into a dictionary of a list of ZIP codes by county.
zillow_scraper.py -- This is the primary scraper for Zillow, mapping ZIP codes for counties to raw HTML to be parsed.
zillow_parser.py -- This is the primary parser for Zillow data, returning lists of tuple entries representing housing data for each county.
PresentationNotes.txt -- This is the notes for my presentation.
Zillow.pdf -- This is my presentation.


Here is a brief overview of my process:

1) Scraping Zillow:

This was a difficult project because of the constant CAPCHA walls. I found some ways to optimize my scraping script (Poisson distributed sleeps), but I could only get through 5-10 ZIP codes at a time, realistically.

2) Parsing Zillow data:

This was easier once I figured out that most of the information was in a JSON format. I had to throw away a lot of my data because it didn't contain the information I needed. I ended up scraping about 16,000 households, resulting in about 8,000 usable households.

3) Scraping Zillow for ZIP codes!

This was a lot easier than scraping Zillow for house data.

4) Modeling:

I started by analyzing the data I had by building some preliminary models, but quickly realized that I needed to log my dependent variable (price) and normalize everything else (the square footage was throwing everything else off). I didn't regularize immediately because I had a low r^2 value when optimizing my models, but eventually used Lasso just to see the degree of overfitting (not much). I also played around with GridSearchCV, although it was perhaps overkill, and found that cross-validation was optimized with an alpha of about 4000. Then for a quick sanity check, I looked at Robert's helpful diagnostic plots and double-checked the quality of my models by running a standard LinearRegression(). Finally, since OLS seemed not to be the best model for my dataset, I tested a variety of other models including RandomForest and GradientBoostedTrees, both of which seemed to have better results, but didn't generalize nearly as well as my mediocre OLS.