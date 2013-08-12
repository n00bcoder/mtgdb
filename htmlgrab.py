#########################################################
#                                                       #
#       Magic: The Gathering Card Info Retriever        #
#                                                       #
#   Create a database to keep track of your inventory   #
#             from the Gatherer website!                #
#														#
#########################################################

import urllib2		#import url getter library
import MySQLdb		#import MySQL connection library

#list of certain sections in the html that are used to define start and stop search points
section_lookup = ['_nameRow"', '_manaRow"', '_cmcRow"', '_typeRow"', '_setRow"']

#empty string variables to pass to the functions - it tells me they need to be declared
card_value = ""
mana_cost = ""
card_name = ""
card_type = ""
main_type = ""
subtype = ""
card_text = ""
rarity = ""
card_set = ""
power_toughness = ""

#looks for info between certain tags using the section_lookup to start from
def get_info_after_value(block, card_value_read, card_value):
	read_start = block.find(card_value_read)
	card_value_start = block.find('ue">', read_start) + 4
	card_value_end = block.find('</div>', card_value_start)
	card_value = block[card_value_start:card_value_end]
	card_value = card_value.strip()
	return card_value

#gets the mana cost and formats it into single letter cost labels for colors
def get_mana_cost(block, mana_cost_read, mana_cost_end, mana_cost):
	mana_start = block.find(mana_cost_read)
	mana_end = block.find(mana_cost_end)
	mana_cost_start = block.find("alt=", mana_start) + 5
	mana_cost_stop = block.find('"', mana_cost_start)
	mana_cost = block[mana_cost_start:mana_cost_stop]
	str_cost = str(mana_cost)	
	if len(str_cost) != 2:								#looks for 2 digit cost, if it is, this is all skipped
		if str_cost == 'Blue':							#if not 2 digit, check for 'Blue' and change it
			mana_cost = 'U'
		elif str_cost == 'Variable Colorless':			#checks for X casting cost, and makes it X
			mana_cost = 'X'
		elif str_cost.find(' or ') != -1:								#checks for "either/or" casting cost
			or_pos_start = str_cost.find(' ')							
			or_pos_end = str_cost.find(' or ') + 4						
			if str_cost[:or_pos_start] == 'Blue':						#checks if the first part of the cost is Blue; knowing where Blue is is important
				first_color = 'U'										
				second_color = str_cost[or_pos_end:or_pos_end + 1]		
			elif str_cost[or_pos_end:] == 'Blue':						#checks if the second part of the cost is Blue if it wasn't first
				first_color = str_cost[0]								
				second_color = 'U'
			else:														
				first_color = str_cost[0]								# if blue isn't found, it just grabs the color letters
				second_color = str_cost[or_pos_end:or_pos_end + 1]		
			mana_cost = first_color + '/' + second_color				#combines the cost in an easy format
		else:
			mana_cost = str_cost[0]						#otherwise take the first character of the cost
	else:
		mana_cost = str_cost							#happens when a two digit cost is found, changed into a string for concatenation later
	while block.find('alt="', mana_cost_stop) < mana_end:
		mana_cost_start = block.find("alt=", mana_cost_stop) + 5
		mana_cost_stop = block.find('"', mana_cost_start)
		next_mana_cost = block[mana_cost_start:mana_cost_stop]
		if next_mana_cost == 'Blue':
			next_mana_cost = 'U'
		elif next_mana_cost == 'Variable Colorless':
			next_mana_cost = 'X'
		elif next_mana_cost.find(' or ') != -1:
			or_pos_start = next_mana_cost.find(' ')
			or_pos_end = next_mana_cost.find(' or ') + 4
			if next_mana_cost[:or_pos_start] == 'Blue':
				first_color = 'U'
				second_color = next_mana_cost[or_pos_end:or_pos_end + 1]
			elif next_mana_cost[or_pos_end:] == 'Blue':
				first_color = next_mana_cost[0]
				second_color = 'U'
			else:
				first_color = next_mana_cost[0]
				second_color = next_mana_cost[or_pos_end:or_pos_end + 1]
			next_mana_cost = ' ' + first_color + '/' + second_color
		else:
			next_mana_cost = next_mana_cost[0]
		mana_cost += next_mana_cost
	return mana_cost

#takes the card type and splits it into the main type and subtype, strips everything else off
def fix_card_type(card_type, main_type, subtype):
	main_type_end = card_type.find("\xe2")
	if main_type_end == -1:
		main_type = card_type
		return main_type
	main_type = card_type[:main_type_end].strip()
	subtype_start = main_type_end + 3
	subtype = card_type[subtype_start:].strip()
	return main_type, subtype
	
#cycles through the card text group looking for multiple sections of it; captures flavor text as well
def get_card_text(block, card_text, text_area_end):
	text_block_start = block.find('Card Text:')								#start of the card text area
	if text_block_start == -1:												#check to see if there's any text
		card_text = ""
		return card_text
	if block.find('_markRow', text_block_start) != -1:						#searches for a Watermark area so as to not capture it as part of the card text
		text_block_end = block.find('_markRow', text_block_start)
	else:
		text_block_end = block.find(text_area_end)							#end of the card text area
	text_start = block.find('cardtextbox">', text_block_start) + 13			#search for the first occurrence of card text, add enough to to get to the beginning
	text_stop = block.find('</div>', text_start)							#search for the end of the card text
	card_text = block[text_start:text_stop]									#get the actual text
	while block.find('cardtextbox">', text_stop) < text_block_end:			#loop to check for more occurrences of card text
		if block.find('cardtextbox">', text_stop) == -1:
			return card_text
		text_start = block.find('cardtextbox">', text_stop) + 13			#set new start point to get text
		text_stop = block.find('</div>', text_start)						#set new stop point for text, searching from start point
		combine_with_breaks = "<br /><br />" + block[text_start:text_stop] 	#combine html breaks with actual card text
		card_text += combine_with_breaks									#combine html break added text with existing captured card text
	return card_text														#once done, return combined card text

#gets the rarity of the card along with the card set - combined into one function because it was easy
def get_rarity_and_set(block, rarity, card_set):
	rarity_pos = block.find("rarity=") + 7
	rarity = block[rarity_pos:rarity_pos + 1]
	card_set_start = block.find('alt="', rarity_pos) + 5
	card_set_end = block.find('(', card_set_start)
	card_set = block[card_set_start:card_set_end]
	return rarity, card_set
	
#gets power and toughness, pretty simple
def get_power_toughness(block,power_toughness):
	pt_read = block.find("P/T:")
	if pt_read == -1:
		#power_toughness = ""						#if there is no power/toughness, just return nothing. 
		return #power_toughness
	pt_start = block.find('ue">', pt_read) + 4
	pt_end = block.find('</div>', pt_start)
	power_toughness = block[pt_start:pt_end].strip()
	return power_toughness

#this runs all the functions, passes what needs to be passed to them, sends things to get fixed, and returns all the info as a tuple
def parse_the_info(block, card_value, card_name, mana_cost, card_type, main_type, subtype, card_text, rarity, card_set, power_toughness):
	card_name = get_info_after_value(block, section_lookup[0], card_value)
	mana_cost = get_mana_cost(block, section_lookup[1], section_lookup[2], card_value)
	card_type = get_info_after_value(block, section_lookup[3], card_value)
	main_type, subtype = fix_card_type(card_type, main_type, subtype)
	card_text = get_card_text(block, card_text, section_lookup[4])
	rarity, card_set = get_rarity_and_set(block,rarity, card_set)
	power_toughness = get_power_toughness(block, power_toughness)
	return card_name, mana_cost, main_type, subtype, card_text, card_set, rarity, power_toughness

#main function - initializes where the card ids start, connects to the db, then loops through all the web urls
#inserting the card ID as it goes through
#changes the returned tuple from parse_the_info to a list so it can add the card id into it
#then writes it all into the db
def get_card_info(card_id_start, card_id_end):		#M14 set is 370577 - 370825
	card_id = card_id_start
	config = {
		'user': 'carduser',
		'passwd': 'cardpassword',
		'host': 'localhost',
		'db': 'mtgdb',
	}
	cnx = MySQLdb.connect(**config)		#used a dictionary just for ease of changing info
	cur = cnx.cursor()
	statement = """INSERT INTO cards (id, name, castingCost, type, subtype, text, cardset, rarity, pt) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
	while card_id <= card_id_end:
		str_card_id = str(card_id)
		print "Gathering card ID " + str_card_id + "..."
		website = urllib2.urlopen("http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=" + str_card_id)
		website_html = website.read()
		search_start = website_html.find("smallGreyMono") + 1		#doing this gets a better start point
		block_start = website_html.find("smallGreyMono", search_start)
		block = website_html[block_start:]
		card = parse_the_info(block, card_value, card_name, mana_cost, card_type, main_type, subtype, card_text, rarity, card_set, power_toughness)
		card_list = list(card)
		card_list.insert(0, card_id)
		try:
			cur.execute(statement, (card_list))
			cnx.commit()
		except:
			cur.close()
		print "Card ID " + str_card_id + " done."
		card_id += 1
	print "All done!" #"Number of rows added = ", total_rows <- this only returned 1
	cur.close()
	cnx.close()

print "Run get_card_info() and pass in the starting card ID number and the ending card ID number you want to get info for."
