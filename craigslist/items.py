# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class CraigslistItem(Item):
	# define the fields for your item here like:
	# name = Field()
	title = Field()
	price = Field()
	link = Field()
	desc = Field()
	date = Field()
	location = Field()
	sellerType = Field()
