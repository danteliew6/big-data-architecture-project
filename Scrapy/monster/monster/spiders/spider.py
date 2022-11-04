

class MonsterSpider(scrapy.Spider):
    name = 'monster'

    start_urls = [
        'https://sg.jobsdb.com/j?sp=homepage&q=information+systems&l=Singapore',
    ]

    def parse(self, response):
        
        for titles in response.xpath('//div[@class="structItem-title"]/a'):
            click_in = titles.xpath('@href').get()
            yield response.follow(click_in,self.inner_parse)

        next_page =response.xpath('//a[@class="pageNav-jump pageNav-jump--next"]/@href').get() 
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def inner_parse(self, response):

        topic = response.xpath('//h1[@class="p-title-value"]/text()').get()
        for post in response.xpath('//article[starts-with(@id,"js-post")]'):
            yield {
                'topic':topic,
                'author': post.xpath('div/div[1]/section/div[2]/h4/a/text()').get(),
                'content': post.xpath('normalize-space(string(div/div[2]/div/div/div[1]/article/div[1]))').get(),
                'time':post.xpath('div/div[2]/div/header/ul[1]/li/a/time/@datetime').get(),
            }

        next_page =response.xpath('//a[@class="pageNav-jump pageNav-jump--next"]/@href').get() 
        if next_page is not None:
            yield response.follow(next_page, self.inner_parse)


#link
#https://webcache.googleusercontent.com/search?q=cache:2JhpnuUJxQcJ:https://www.monster.com.sg/search/information-systems-jobs+&cd=1&hl=en&ct=clnk&gl=sg&searchId=dcc986ae-5d6c-4941-862b-a4aef18364ee

# use to get all the job elements in the page
# x = response.xpath('//*[@class="card-panel apply-panel job-apply-card"]').getall()
# i.e x[0] is one job card

#for i in x
#i.xpath('//h3[@class="medium"]/a/text()').get()
#'//h3[@class="medium"]/a/text()' -> job title

#i.xpath('//span[@class="company-name"]/a/text()').get()
#'//span[@class="company-name"]/a/text()' -> company name


#'//span[@class="loc"]
#[//i@class="mqfi-location-v2"]/small/text() -> location
#[//*@class="mqfi-bag"]/small/text() -> years of exp
#[//*@class="mqfi-coin-stack fs-18"]/small/text() -> pay range
