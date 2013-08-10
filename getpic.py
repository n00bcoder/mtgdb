import urllib2

#Should put in a way to save to an /images directory, that way where ever this is run from, it saves into a subdir of that

def get_card_pic(card_id_start, card_id_end):
	#card_id = card_id_start
	while card_id_start <= card_id_end:
		str_card_id = str(card_id_start)
		link = urllib2.urlopen('http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=' + strCardID + '&type=card')
		file = open(str_card_id + '.jpg', 'wb')
		file.write(link.read())
		file.close()
		print 'Card ID ' + str_card_id + ' saved.'
		card_id_start += 1
	print "All done!"
	return

#Should put in a way to save to an /symbols directory, that way where ever this is run from, it saves into a subdir of that
	
def get_symbols():
	name = ['B','U','G','R','W','X','Tap','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','BG','BR','UB','UR','GU','GW','WB','WU']
	size = ['small','medium','large']
	name_pos = 0
	size_pos = 0
	while size_pos < len(size):
		while name_pos < len(name):
			link = urllib2.urlopen('http://gatherer.wizards.com/Handlers/Image.ashx?size=' + size[size_pos] + '&name=' + name[name_pos] + '&type=symbol')
			file = open(size[size_pos] + name[name_pos] + '.gif', 'wb')
			file.write(link.read())
			file.close()
			print size[size_pos] + name[name_pos] + '.gif saved'
			name_pos += 1
		size_pos += 1
		name_pos = 0
	print 'All done!'
	return
	