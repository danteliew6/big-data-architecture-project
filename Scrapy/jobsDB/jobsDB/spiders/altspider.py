import scrapy


class JobsDBSpider(scrapy.Spider):
    name = 'jobsDB'

    start_urls = [
        'https://sg.jobsdb.com/j?sp=search&q=information+systems&l=Singapore',
    ]

    def parse(self, response):


        for joblist in response.xpath('//*[@id="jobresults"]'):
            for job in joblist.xpath('//*[@class="job-card result organic-job"]'):
                job_link = job.xpath('div/h3/a/@href').get()
                if job_link is not None:
                    yield response.follow(job_link, self.parse)


        yield {
            'job_title': response.xpath('//*[@id="job-info-container"]/h3/text()').get(),
            'company': response.xpath('//*[@id="company-location-container"]/span[1].text()').get(),
            'job_description': response.xpath('//*[@id="job-description-container"].text()').get()
        }        

        next_page = response.xpath('//a[@class="next-page-button"]/@href').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
