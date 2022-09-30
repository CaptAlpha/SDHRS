import scrapy
from selenium import webdriver
from items import Profile, Reviews
from scrapy.loader import ItemLoader

class Scrape(scrapy.Spider):
    name='reviews'
    allowed_domains = ['healthgrades.com']
    start_urls = ['https://www.healthgrades.com/physician/dr-jeffrey-lee-2y8xg/reviews']

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
    
    def parse(self, response):
        page_info=ItemLoader(item=Profile(), response=response)
        page_info.add_xpath('name', '//h1[@class="h2"]/text()')
        page_info.add_xpath('specialty', '//div[@class="specialty"]/text()')
        page_info.add_xpath('address', '//div[@class="address"]/text()')
        page_info.add_xpath('phone', '//div[@class="phone"]/text()')
        page_info.add_xpath('website', '//div[@class="website"]/a/text()')
        page_info.add_xpath('rating', '//div[@class="rating"]/text()')
        page_info.add_xpath('reviews', '//div[@class="reviews"]/text()')
        
        yield page_info.load_item()

        self.driver.get(response.url)
        for i in range(1, 10):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.driver.implicitly_wait(10)
            self.driver.find_element_by_xpath('//button[text()="Load More"]').click()
            self.driver.implicitly_wait(10)

        reviews = self.driver.find_elements_by_xpath('//div[@class="review"]')
        for review in reviews:
            review_info = ItemLoader(item=Reviews(), selector=review)
            review_info.add_xpath('date', './/div[@class="date"]/text()')
            review_info.add_xpath('rating', './/div[@class="rating"]/text()')
            review_info.add_xpath('review', './/div[@class="review-text"]/text()')
            yield review_info.load_item()

        self.driver.quit()

if __name__ == '__main__':
    from scrapy.cmdline import execute
    execute('scrapy crawl reviews'.split())
