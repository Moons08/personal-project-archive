import scrapy

from Metacrawler.items import MetacrawlerItem

class MetaSpider(scrapy.Spider):
    name = "metacritic"
    allow_domain = ["metacritic.com"]
    # 크롤링의 시작 URL
    start_urls = [
        "http://www.metacritic.com/browse/movies/release-date/theaters/date"
    ]

    # table/tbody/tr 일 경우, tbody생략....
    # link 리스트를 가져옴
    def parse(self, response):
        movies = response.xpath('//*[@class="browse_list_wrapper wide"]/table/tr')
        for movie in movies:
            link = 'http://www.metacritic.com'+movie.xpath('./*/div[@class="title"]/a/@href').extract()[0]
            print(link)
            yield scrapy.Request(link, callback=self.parse_page_contents)

    # 각페이지의 link로 접속하여 데이터를 가져옴
    def parse_page_contents(self, response):
        item = MetacrawlerItem()
        item["title"] = response.xpath('//*[@class="product_page_title oswald"]/h1/text()')[0].extract()
        item["metascore"] = response.xpath('//*[@id="nav_to_metascore"]/div[1]/div[2]/div[1]/a/div/text()')[0].extract()
        item["userscore"] = response.xpath('//*[@id="nav_to_metascore"]/div[2]/div[2]/div[1]/a/div/text()')[0].extract()
        yield item
