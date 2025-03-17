import os
import argparse
import traceback    
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import datetime
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException


class LinkedinScraper:
    def __init__(self, keywords='Senior Software Engineer', location='Uganda'):
        self.driver = webdriver.Chrome()
        self.keywords = keywords
        self.location = location
        # Configure Chrome
        self.options = Options()
        # self.options.add_argument("--window-size=1920,1080")
        self.service = Service('chromedriver.exe')
        load_dotenv()
        self.jobs = []
        self.number_of_jobs = 0
    

    # def login(self, username, password):
    #     self.driver = webdriver.Chrome(service=self.service, options=self.options)
    #     self.driver.get("https://www.linkedin.com/login")
    #     self.driver.implicitly_wait(10)
    #     self.driver.find_element(By.ID, 'username').send_keys(username)
    #     self.driver.find_element(By.ID, 'password').send_keys(password)
    #     self.driver.find_element(By.XPATH, '//button[@type="submit"]').click()
        
    #     # Wait for login to complete
    #     WebDriverWait(self.driver, 10).until(
    #         EC.presence_of_element_located((By.CSS_SELECTOR, ".feed-outlet"))
    #     )

     # def search_jobs(self):
    #      # Navigate to jobs page
    #     self.driver.find_element(By.XPATH, "//a[@href='https://www.linkedin.com/jobs/?']").click()
    #     self.driver.find_element(By.XPATH, "//a[@href='https://www.linkedin.com/jobs/search?origin=JOBS_HOME_JYMBII']").click()
    #     jobs = self.driver.find_element(By.CLASS_NAME, "scaffold-layout__list-detail-container")
    #     print('printing job listings')
    #     print(jobs)
        
    #     # Enter search criteria
    #     self.driver.find_element(By.ID, "jobs-search-box-keyword-id-ember453").send_keys(self.keywords)
    #     # self.driver.find_element(By.ID, "jobs-search-box-location-id-ember453").clear()
    #     # self.driver.find_element(By.ID, "jobs-search-box-location-id-ember453").send_keys(self.location)
    #     # self.driver.find_element(By.CSS_SELECTOR, ".jobs-search-box__submit-button").click()
        
    #     # Wait for search results
    #     WebDriverWait(self.driver, 10).until(
    #         EC.presence_of_element_located((By.CLASS_NAME, "scaffold-layout__list-detail-container"))
    #     )


    def open_linkedin(self):
        self.driver.get("https://www.linkedin.com/")
        self.driver.implicitly_wait(10)
    
    def search_jobs(self):
        # Navigate to the jobs page
        try:
            self.driver.find_element(By.XPATH, "//a[@href='https://www.linkedin.com/jobs/search?trk=guest_homepage-basic_guest_nav_menu_jobs']").click()
            self.driver.find_element(By.CLASS_NAME, "modal__dismiss").click()
            # Enter search criteria
            self.driver.find_element(By.ID, "job-search-bar-keywords").send_keys(self.keywords)
            self.driver.find_element(By.ID, "job-search-bar-location").clear()
            self.driver.find_element(By.ID, "job-search-bar-location").send_keys(self.location + Keys.ENTER)
            self.driver.find_element(By.CLASS_NAME, "base-search-bar__submit-btn").click()
        except Exception as e:
           print('Error searching for jobs' + str(e))
       
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "jobs-search__results-list"))
        )

    def etract_job_info(self):
        job_fetch = self.driver.find_element(By.CLASS_NAME, "jobs-search__results-list").find_elements(
            By.CLASS_NAME, "job-search-card"
        )
        # job_fetch = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".jobs-search__results-list")))
        # print(job_fetch)
        print('printing job listings')
        self.number_of_jobs = len(job_fetch)
        for job in job_fetch:
            try:
                # Click on the job card to view details
                job.click()
                time.sleep(3)  # Wait for job details to load
                # self.driver.find_element(By.CLASS_NAME, "contextual-sign-in-modal__modal-dismiss").click()
                # self.driver.implicitly_wait(3)
                # Extract job information
                job_title = self.driver.find_element(By.CSS_SELECTOR, ".top-card-layout__title").get_attribute("innerText")
                company = self.driver.find_element(By.CLASS_NAME, "topcard__org-name-link").text
                location = self.driver.find_element(By.CLASS_NAME, "topcard__flavor--bullet").text
                
                try:
                    description = self.driver.find_element(By.CLASS_NAME, "description__text").get_attribute("innerText")
                except:
                    description = "Description not available"
                
                self.jobs.append({
                    "title": job_title,
                    "company": company,
                    "location": location,
                    "description": description
                })
                # self.driver.back
                # time.sleep(50)
            
            except Exception as e:
                print(f"Error processing job: {str(e)}")

    def save_job_info(self):
        pass

    def close(self):
        if hasattr(self, 'driver'):
            self.driver.quit()


    def run(self):
        try:
            # self.login('angeltechno7@gmail.com', '.n@100%L#')
            self.open_linkedin()
            self.search_jobs()
            self.etract_job_info()
            # time.sleep(100)
            print(self.jobs)
            print('------------------------------------------')
            print(f"Found {self.number_of_jobs} jobs")
            print('------------------------------------------')
        finally:
            #    time.sleep(10)
            self.close()

if __name__ == '__main__':
    linkedin_scraper = LinkedinScraper()
    linkedin_scraper.run()