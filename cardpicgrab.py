import urllib2

pic_url = "http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=370655&type=card"
filename = "370655.jpg"
urllib2.urlretreive(pic_url, filename)
