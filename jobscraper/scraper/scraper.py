from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

from .models import Job


class LinkedInScraper:
    excutable_path = "chromedriver/chromedriver"
    
    def __init__(self):
        self.chrome_service = Service()
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--window-size=1920,1080")
        self.chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
        self.driver = self.start_driver()
        self.wait = WebDriverWait(self.driver, 10)

        
    def start_driver(self):
        return webdriver.Chrome(service=self.chrome_service, options=self.chrome_options)


    def navigate_to_job_page(self):
        self.driver.get("https://www.linkedin.com/")
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "nav")))
        self.driver.find_element(By.XPATH, "//a[@href='https://www.linkedin.com/jobs/search?trk=guest_homepage-basic_guest_nav_menu_jobs']").click()
        try:
            self.driver.find_element(By.CLASS_NAME, "modal__dismiss").click()
        except Exception as e:
            print(f"Model {e}")

    
    def scrape_job(self, number_of_jobs): 
        self.navigate_to_job_page()
              
        jobs_found = []
        
        try:
            self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "job-search-card")))
            # locate the list of jobs 
            jobs = self.driver.find_elements(By.CLASS_NAME, "job-search-card")
            
            # loop through each job
            for job_counter in range(number_of_jobs):  
                # re-locate the list of jobs of to avoid stale elements
                jobs = self.driver.find_elements(By.CLASS_NAME, "job-search-card")
                jobs_loaded = len(jobs)
                
                # click on the current job 
                job = jobs[job_counter]
                job.find_element(By.CLASS_NAME, "base-card__full-link").click()
            
                # wait for the detailed page to load 
                time.sleep(random.uniform(3, 5))
                self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "two-pane-serp-page__detail-view"))) 
                           
                # Extract detailed information 
                job_title = self.driver.find_element(By.CLASS_NAME, "top-card-layout__title").text
                company_name = self.driver.find_element(By.CLASS_NAME, "topcard__org-name-link").text
                job_location = self.driver.find_element(By.CLASS_NAME, "topcard__flavor--bullet").text
                job_description= self.driver.find_element(By.CLASS_NAME, "decorated-job-posting__details").get_attribute("innerText")
        
                job_detail = {
                    "title": job_title,
                    "company": company_name,
                    "location": job_location,
                    "description": job_description
                }
                jobs_found.append(job_detail)
                
                # Go back to the list of jobs 
                self.driver.back
                
                try:
                    if job_counter == jobs_loaded-1:
                        time.sleep(2)
                        try:
                            see_more_jobs = self.driver.find_element(By.XPATH, "//button[@aria-label='See more jobs']")
                            if see_more_jobs.is_displayed():
                                see_more_jobs.click()
                                time.sleep(2)
                        except:
                            pass
                            
                        finally:
                            # Scroll down to load more results
                            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                            time.sleep(2)
                            
                except:
                    pass
            
                try:
                    see_more_jobs = self.driver.find_element(By.XPATH, "//button[@aria-label='See more jobs']")
                    if see_more_jobs.is_displayed():
                        see_more_jobs.click()
                        time.sleep(2)
                       
                except:
                    pass
            
                # # wait for the list to load again 
                self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "job-search-card")))
            
        except Exception as e:
            print(f'Scraped {job_counter} jobs, there are no more jobs in the search results: {e}')
        
        finally: 
            print(f'Scraped {len(jobs_found)} jobs sucessfully')
            # close the brower
            self.driver.quit()

        return jobs_found


    def save_jobs_to_db(self, jobs_data):
        new_jobs_count = 0
        
        for job_data in jobs_data:
            # Check if job already exists by job_id
            # if not Job.objects.filter(job_id=job_data['job_id']).exists():
                # Create new job record
            Job.objects.create(
                title=job_data['title'],
                company=job_data['company'],
                location=job_data['location'],
                description=job_data['description'],
            )
            new_jobs_count += 1
        
        return new_jobs_count
