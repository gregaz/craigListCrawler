from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request

from craigslist.items import CraigslistItem

class CraigslistSpider(CrawlSpider):
   name = "craigslist"
   domain_name = "craigslist.org"
   allowed_domains = ["craigslist.org"]
   start_urls = [
       "http://newyork.craigslist.org/ela/",
   ]
   rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        #Rule(SgmlLinkExtractor(allow=('default\.aspx', ), deny=('subsection\.php', ))),

        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        Rule(SgmlLinkExtractor(allow=(),restrict_xpaths=('//p[@id="nextpage"]')), callback='parseList', follow= True),
        #Rule(SgmlLinkExtractor(allow=(),restrict_xpaths=('//p[@class="row"]/a')), callback='parseList', follow=False)
    )

   def parseItem(self, response):
       hxs = HtmlXPathSelector(response)
       item = response.meta['item']
       item['desc'] = hxs.select("//div[@id='userbody']/text()").extract()
       item['date'] = hxs.select("/html/body[@class='posting']/span[@class='postingdate']/text()").extract()
       item['location'] = hxs.select("/html/body[@class='posting']/div[@id='userbody']/ul[@class='blurbs']/li[1]/text()").extract()
       return item

   def parseList(self, response):

        requests = []
        hxs = HtmlXPathSelector(response)        
        titles = hxs.select('//p[@class="row"]/a/text()').extract()
        prices = hxs.select("//p[@class='row']/span[@class='itempp']").extract()
        links = hxs.select('//p[@class="row"]/a/@href').extract()
        sellerType = hxs.select("//p[@class='row']//small[@class='gc']/a/text()").extract()
        
        for n in range(0,100):
            item = CraigslistItem()
            item['title'] = titles[n]
            item['price'] = prices[n]
            item['link'] = links[n]
            item['sellerType'] = sellerType[n]
            request = Request(links[n], callback=self.parseItem)
            request.meta['item'] = item
            requests.append(request)
        
        return requests
        
            
#TODO: from list get:
#    title = Field()
#    price = Field()
#    link = Field()
#    sellerType = Field()

#from item get:
#    desc = Field()
#    date = Field()
#    location = Field()