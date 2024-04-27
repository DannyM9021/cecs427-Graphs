# Daniel Moreno
# CECS 427 - 01 Dynamic Networks
# Due Data: April 26, 2024

# Creating web crawler spider using scrapy
import scrapy 
import os
import logging
from scrapy.utils.reactor import install_reactor
import json

# Using as main help for setting up the spider
# https://www.youtube.com/watch?v=s4jtkzHhLzY
# as well as from the documentation

class www_spider(scrapy.Spider):
    name = 'www_spider'
    install_reactor("twisted.internet.asyncioreactor.AsyncioSelectorReactor")

    # Helped define initialization of spider with urls
    # https://stackoverflow.com/questions/11594485/scrapy-cant-override-init-function
    def __init__(self, *args, **kwargs):
        super(www_spider, self).__init__(*args, **kwargs)
        file_parse = self.parse_input_file()
        self.start_urls = file_parse[1:]
        self.vertices = file_parse[0]
        self.dict = {}

    def parse(self, response):
        try:
            self.dict.update({response.url:response.css('span[itemprop="author"] a::attr(href)').getall()})
            for links in response.css('span[itemprop="author"] a::attr(href)').getall():
                print(links)
                try:
                    yield{"link":links}
                except Exception as e:
                    yield{"link":"NONE"}
        except Exception as e:
            self.logger.error("Error parsing response: %s", e)
    def parse_input_file(self):
        curr_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(curr_dir, '..', '..', '..', 'crawlingFile')

        items = []
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    items.append(line.split("\n")[0])
                file.close()
                print(items)
                return items
        except Exception as e:
            print("Error:", e)

    # When spider is done executing, this funciton will be called, will output the file
    # https://stackoverflow.com/questions/12394184/scrapy-call-a-function-when-a-spider-quits
    def closed(self, reason):
        curr_dir = os.path.dirname(os.path.abspath(__file__))
        out_path = os.path.join(curr_dir, '..', '..', '..', 'output.json')
        with open(out_path, 'w') as out:
            json.dump(self.dict, out)

