# -*- coding: utf-8 -*-
import scrapy
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from scrapy import Selector

class ReviewsSpider(scrapy.Spider):
    name = 'reviews'
    allowed_domains = ['https://www.tripadvisor.co.uk/Hotel_Review-g294209-d4293067-Reviews-Mahali_Mzuri_Sir_Richard_Branson_s_Kenyan_Safari_Camp-Maasai_Mara_National_Reserve_Rif.html']
    start_urls = ['https://www.tripadvisor.co.uk/Hotel_Review-g294209-d4293067-Reviews-Mahali_Mzuri_Sir_Richard_Branson_s_Kenyan_Safari_Camp-Maasai_Mara_National_Reserve_Rif.html/']
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.wait  = WebDriverWait(self.driver,timeout=20)

    def parse(self, response):
        self.driver.get(response.url) 
        self.driver.maximize_window()
        self.wait.until(EC.presence_of_all_elements_located((By.XPATH,'//p[@class="partial_entry"]/span[@class="taLnk ulBlueLinks"]')))
        self.wait.until(EC.presence_of_all_elements_located((By.XPATH,'//*[@id="taplc_location_reviews_list_hotels_0"]/div/div[12]/div/span[2]')))
        more = self.driver.find_element_by_xpath('//p[@class="partial_entry"]/span[@class="taLnk ulBlueLinks"]')
        more.click()
        time.sleep(1)
        source = self.driver.page_source
        sel  = Selector(text=source)
        for quote in sel.css('div.review-container'):
            yield {
                    'text': quote.css('p.partial_entry::text').extract_first(),
                    'title': quote.css('span.noQuotes::text').extract_first(),
                    'reviewed':quote.css('span.ratingDate.relativeDate::text').extract_first()} 

        break_value = 1

        while break_value == 1:
            try:
                next_page = self.driver.find_element_by_css_selector('span.nav.next.taLnk')
                next_page.click()
                time.sleep(1)
                more = self.driver.find_element_by_xpath('//p[@class="partial_entry"]/span[@class="taLnk ulBlueLinks"]')
                more.click()
                time.sleep(1)
                source = self.driver.page_source
                sel  = Selector(text=source)
                for quote in sel.css('div.review-container'):
                    yield {
                            'text': quote.css('p.partial_entry::text').extract_first(),
                            'title': quote.css('span.noQuotes::text').extract_first(),
                            'reviewed':quote.css('span.ratingDate.relativeDate::text').extract_first()} 

            except:
                print ("No more pages to scrape")
                break_value = 0
        self.driver.close()

       
         
             
        
