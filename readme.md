# lego-by-pound: List LEGO by the pound

Here's what this application does:

1. Grabs the upcoming US Ebay listings for "LEGO lbs".
2. Keeps only results for which it can determine the number of pounds in the listing from the title.
3. Calculates total price including shipping.
4. Calculates price per pound.
5. Keeps only results that have a price per pound less than $10.
6. Displays the results by soonest end time.

You can view live results here: http://joncraton.org/lego-by-pound

# Getting started

Run __main__.py. 

This is configured to output a static list of items to stdout. It is actually a small web.py applications with only a single page. It could easily be expanded to run as a proper web application.