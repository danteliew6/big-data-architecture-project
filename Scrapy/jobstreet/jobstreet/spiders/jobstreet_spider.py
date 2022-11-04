import scrapy

class JobstreetSpider(scrapy.Spider):
    name = 'jobstreet'
    start_urls = [
        'https://www.jobstreet.com.sg/en/job-search/information-systems-jobs/8/?sort=createdAt&specialization=508',
    ]

    def parse(self, response):
        for listing in response.xpath('//h1[@class="sx2jih0 zcydq82q _18qlyvc0 _18qlyvcv _18qlyvc3 _18qlyvc8"]/a'):
            yield response.follow(listing.xpath('./@href').get(), self.parse_job)

        next_page = response.xpath('//a[@class="sx2jih0 zcydq872 zcydq862 zcydq88 zcydq82b zcydq832 zcydq8c6 zcydq824 zcydq82l zcydq82k _1ouuf_0"]/@href').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_job(self, response):
        job_title = response.xpath('//h1[@class="sx2jih0 _18qlyvc0 _18qlyvcd _1d0g9qk4 _18qlyvcj _18qlyvcv"]/text()').get()
        companyName = response.xpath('.//div[@class="sx2jih0 zcydq84i"][2]//text()').get()
        salary = response.xpath('.//div[@class="sx2jih0 zcydq846"][2]//text()').get() if len(response.xpath('.//div[@class="sx2jih0 zcydq846"]')) > 2 else None
        job_description = response.xpath('string(//div[@data-automation="jobDescription"])').get()
        yield {
            'job_title': job_title,
            'company':  companyName,
            'salary': salary,
            'job_description': job_description
        }