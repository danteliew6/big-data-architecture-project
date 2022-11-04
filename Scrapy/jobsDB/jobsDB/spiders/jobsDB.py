import scrapy


class JobsDBSpider(scrapy.Spider):
    name = 'jobsDB'

    start_urls = [
        'https://sg.jobsdb.com/j?sp=homepage&q=information+systems&l=singapore'
        #'https://sg.jobsdb.com/job/Information-Technology-Engineer-5d3a823f02ba60b8bfba9747b52b8089?from_url=https%3A%2F%2Fsg.jobsdb.com%2Fj%3Fsp%3Dhomepage%26q%3Dinformation%2Bsystems%26l%3Dsingapore&sl=singapore&sol_srt=cbcc66f8-7f39-488e-9b2d-519de2e9d0bf&sp=serp&sponsored=false&sq=information+systems&sr=1&tk=Dqpyay2LOId7kJ8lt9HT-GnxqpIfcX9M_8d6puNPU'
    ]

    def parse(self, response):
        
        for job in response.xpath('//article/div[@class="top-container"]/h3/a'):
            yield response.follow(job.xpath('@href').get(), self.parsePage)
        
        next_page = response.xpath('//div/a[contains(text(),"Next")]/@href').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
    
    def parsePage(self, response):
        
        # #Option 1 (Role and responsibilites seperate, some empty)
        # requirements = []
        # responsibilities = []
        # for listitem in response.xpath('//div[@id="job-description-container"]/div/ul/li'):
        #     if listitem.xpath('text()').get() != None:
        #         requirements.append(listitem.xpath('text()').get())
        # for listitem in response.xpath('//div[@id="job-description-container"]/ul/li'):
        #     if listitem.xpath('text()').get() != None:
        #         responsibilities.append(listitem.xpath('text()').get())
        # yield {
        #     'title': response.xpath('//h3/text()').get(),
        #     'requirements': requirements,
        #     'responsibilities': responsibilities,
        # }

        #Option 2 (Role and responsibilites together)
        skills = []
        for listitem in response.xpath('//ul/li'):
            if listitem.xpath('text()').get() != None:
                skills.append(listitem.xpath('text()').get())
        yield {
            'job_title': response.xpath('//h3/text()').get(),
            'company': response.xpath('//div[@class="heading-small"]/span/text()').get(),
            'job_description': skills,
        }
        

        