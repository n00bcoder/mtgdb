mtgdb
=====

Magic card database to keep track of inventory

This will build a database of Magic: The Gathering cards so that you can keep an inventory of your own stock.

First, run the mtgdb.sql file to create the database and table to keep the card info in. You'll need to setup your own user to get access to it. You'll need to then add those credentials into the other python scripts to access the database.

Next, to get the actual card data, modify the htmlgrab.py file and put in your database creds that have write access to the mtgdb db.

Run the htmlgrab.py script. That will define all the necessary procedures to actually get the card info. When it's done, the console will tell which procedure to run and what to pass into it, which is the get_card_info() procedure. The start card ID and stop card ID will need to be passed into it. To acquire those, you'll need to get them from gatherer.wizards.com. Find a card in the set you want, and then find out the range by modifying the ID in the url until the card set changes. For example, the card ID range for the Magic 2014 set is 370577-370825, so run get_card_info(370577,370825) to get that set. Later on, I might include a lookup table so all you have to enter in is the card set you want, but for now, find the ID's, it goes fast.

That will run and print out the card ID's as it gets them. This is helpful in case any errors pop up.

After that, you'll want to run the getpic.py file to define those procedures. 

Run get_card_pic() to get the card images, again passing in the card ID range, for example, get_card_pic(370577, 370825) to get the images. Those currently will be saved to your working directory, so be warned. I haven't implemented directories for that yet.

Run the get_symbols() procedure to get all the various cards symbols: mana symbols, mana costs, and tap symbol. This procedure takes no arguments. Again, the symbols will be saved in your working directory. 

The singlecardgrab.py will define procedures that will go an get info for a single card ID and print the info it captures. Pass in a card ID to the get_card_info() procedure.

Things still being worked on -

As I mentioned, saving into subdirs for the images and symbols.

Also, the card text data pulled in htmlgrab.py will have broken links to any symbol images. I still need to write something that will go through and fix all the links in there to be local links and to the appropriate symbol. 

The biggest thing though is the front end, of which this project currently doesn't have one. Once I get the card text data modified, I will be starting work on the interface to actually show all this goodness and enter in a quantity for the card.
