import scrapy

class IndeedSpider(scrapy.Spider):
    name = 'indeed'

    start_urls = [
        'https://sg.indeed.com/jobs?q=information%20systems&l=Singapore&filter=0&sort=date',
    ]

    def parse(self, response):
        for listing in response.xpath('//div[@id="mosaic-provider-jobcards"]/a'):
            yield response.follow(listing.xpath('./@href').get(), self.parse_job)


        next_page = response.xpath('//a[@aria-label="Next"]/@href').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_job(self, response):
        job_headers = response.xpath('//div[@class="jobsearch-DesktopStickyContainer"]')
        job_title = job_headers.xpath('.//div[1]/div[1]/h1/text()').get()
        companyName = job_headers.xpath('.//div[starts-with(@class,"jobsearch-InlineCompanyRating")]/div[1]//text()').get()
        salary = job_headers.xpath('.//span[@class="icl-u-xs-mr--xs"]//text()').get()
        job_description = response.xpath('string(//div[@id="jobDescriptionText"])').get()
        yield {
            'job_title': job_title,
            'company':  companyName,
            'salary': salary,
            'job_description': job_description
        }