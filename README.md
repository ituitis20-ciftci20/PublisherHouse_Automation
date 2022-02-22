# PublishingHouse_Automation
This project is about updating price of books in an automatic way.

Problem:
Publishing house has a web site, which has 767 books in it. Every time they update the price of books from excel, they need to update every price in the web site and it takes huge amount of time. 

So, I design a program that takes an Excel file -which includes book names, new prices and other stuff- as an input, then updates the prices on the web site automaticly. 

I used mainly selenium, beautiful soup, pandas, numpy, difflib libraries in python.

Web site: http://www.kaknus.com.tr/

Table of Contents:
*Part1 is about scrapping data from web site. Especially, book ids which are associated with every book in the HTML file.
*Part2 is about comparing excel data and web data. Some books names are undermatching because of the typos.
*Part3 is about fixing typos in our input excel file.
*Part4 is about updating prices. Try to implement some one to one dictionary for every book in excel and every book in web site.
