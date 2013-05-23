# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

class CraigslistPipeline(object):
    def process_item(self, item, spider):
        if item['location'] == "it's NOT ok to contact this poster with services or other commercial interests":
            item['location'] = 'unknown'
        return item
