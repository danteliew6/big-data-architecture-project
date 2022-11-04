import scrapy
import time

class grabJobsSpider(scrapy.Spider):
    name = 'grabJobs'


    start_urls = [
        'https://grabjobs.co/singapore/jobs?c=technology&q=information+systems&p=93&req_id=8628d4c830d76c09dbae4fcaef5bc613',
    ]

    def parse(self, response):
        for joblist in response.xpath('//*[@class="col-xl-6 col-lg-8 col-md-8"]'):
            for job in joblist.xpath('//*[@class="has-text-black link-card"]'):
                job_link = job.xpath('@href').get()
                if job_link is not None:
                    yield response.follow(job_link, self.innerparse)

        next_page = response.xpath('//ul[@class="pagination justify-content-center"]/li[6]/a/@href').get()
        if next_page is not None:
            time.sleep(4)
            yield response.follow(next_page, self.parse)


    def innerparse(self,response):
        description = response.xpath('//div[@class="card shadow-sm mb-3 mobile-view-card"][2]/div[contains(@class,"card-body")]//text()').getall()
        description_joined = ' '.join(description)
        description = description_joined.replace('\n', '')
        
        company = response.xpath('//*[@class="has-text-dark"]/text()').get()
        company = company.replace('\n', '')

        yield {
            'job_title': response.xpath('//*[@class="card-title h5 fw-bold d-block mb-3"]/text()').get(),
            'company': company,
            'salary': response.xpath('//*[@class="is-grabjobs-color normal-text fw-bold"]/text()').get(),
            'job_description': description
        }        

#https://grabjobs.co/singapore/jobs?c=technology&q=information+systems&p=38&req_id=a7d7eb9bf44bd3bd63cb5e716ed0ca16
#https://grabjobs.co/singapore/jobs?c=technology&q=information%20systems
#https://grabjobs.co/singapore/jobs?c=technology&q=information+systems&p=49&req_id=8c46f39e9efc5a2ac0bb6b0d8117c9da
#https://grabjobs.co/singapore/jobs?c=technology&q=information+systems&p=78&req_id=088f2d404ab818c74eca27c7b53c0918
#https://grabjobs.co/singapore/jobs?c=technology&q=information+systems&p=80&req_id=f8996129a3dc33f32ef70e131d83321f
#https://grabjobs.co/singapore/jobs?c=technology&q=information+systems&p=87&req_id=c8d1eabab3edcabe85a6eb0146c4e9f3
#https://grabjobs.co/singapore/jobs?c=technology&q=information+systems&p=93&req_id=8628d4c830d76c09dbae4fcaef5bc613