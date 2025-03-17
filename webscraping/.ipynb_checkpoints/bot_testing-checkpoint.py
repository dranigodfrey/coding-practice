import os
import json
import csv
import time
import argparse
import traceback
from datetime import datetime
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException


class LinkedInJobScraper:
    """LinkedIn Job Scraper that can search and extract job listings"""
    
    def __init__(self, headless=False, output_dir="output"):
        """
        Initialize the LinkedIn Job Scraper
        
        Args:
            headless (bool): Run browser in headless mode
            output_dir (str): Directory to save output files
        """
        self.base_url = "https://www.linkedin.com"
        self.jobs = []
        self.number_of_jobs = 0
        self.headless = headless
        self.output_dir = output_dir
        
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Initialize the Chrome driver
        self._initialize_driver()
    
    def _initialize_driver(self):
        """Set up and initialize the Chrome driver"""
        print("Initializing Chrome driver...")
        
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--start-maximized")
        
        # Add user agent to avoid detection
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36")
        
        # Install or use existing ChromeDriver
        try:
            service = Service(executable_path='chromedriver.exe')
            self.driver = Chrome(service=service, options=chrome_options)
        except Exception as e:
            print(f"Error initializing Chrome driver: {str(e)}")
            print("Attempting to use system ChromeDriver...")
            self.driver = Chrome(options=chrome_options)
        
        # Set implicit wait time
        self.driver.implicitly_wait(10)
        print("Chrome driver initialized successfully")
    
    def login(self, username, password):
        """
        Login to LinkedIn
        
        Args:
            username (str): LinkedIn username/email
            password (str): LinkedIn password
            
        Returns:
            bool: True if login successful, False otherwise
        """
        print("Logging in to LinkedIn...")
        self.driver.get(f"{self.base_url}/login")
        
        try:
            # Wait for the login page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            
            # Enter username/email
            username_field = self.driver.find_element(By.ID, "username")
            username_field.clear()
            username_field.send_keys(username)
            
            # Enter password
            password_field = self.driver.find_element(By.ID, "password")
            password_field.clear()
            password_field.send_keys(password)
            
            # Click login button
            login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            login_button.click()
            
            # Wait for login to complete
            WebDriverWait(self.driver, 15).until(
                EC.url_contains("feed")
            )
            
            print("Successfully logged in to LinkedIn")
            return True
            
        except Exception as e:
            print(f"Login failed: {str(e)}")
            return False
    
    def search_jobs(self, keywords, location, remote_only=False, experience_level=None, limit=None):
        """
        Search for jobs on LinkedIn
        
        Args:
            keywords (str): Job search keywords
            location (str): Job location
            remote_only (bool): Filter for remote jobs only
            experience_level (str): Filter by experience level 
                                   (Entry, Associate, Mid-Senior, Director, Executive)
            limit (int): Maximum number of job listings to process
            
        Returns:
            bool: True if search successful, False otherwise
        """
        print(f"Searching for jobs with keywords: '{keywords}' in '{location}'")
        
        try:
            # Navigate to LinkedIn Jobs page
            self.driver.get(f"{self.base_url}/jobs/")
            
            # Wait for the search form to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[role='combobox']"))
            )
            
            # Find and fill the keyword and location fields
            # LinkedIn has multiple inputs, so we'll try to find the right ones
            input_fields = self.driver.find_elements(By.CSS_SELECTOR, "input[role='combobox']")
            
            if len(input_fields) >= 2:
                # Clear and fill keyword field
                keyword_field = input_fields[0]
                keyword_field.clear()
                keyword_field.send_keys(keywords)
                
                # Clear and fill location field
                location_field = input_fields[1]
                for _ in range(50):  # Clear the field
                    location_field.send_keys(Keys.BACKSPACE)
                location_field.send_keys(location)
                location_field.send_keys(Keys.RETURN)
            else:
                print("Could not locate search fields, trying alternative method")
                # Alternative approach - navigate directly to search URL
                search_url = f"{self.base_url}/jobs/search/?keywords={keywords.replace(' ', '%20')}&location={location.replace(' ', '%20')}"
                self.driver.get(search_url)
            
            # Wait for search results to load
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, "jobs-search__results-list"))
            )
            
            # Apply filters if specified
            if remote_only or experience_level:
                self._apply_filters(remote_only, experience_level)
            
            # Wait for results to refresh after applying filters
            time.sleep(3)
            
            print("Job search completed successfully")
            return True
            
        except Exception as e:
            print(f"Job search failed: {str(e)}")
            traceback.print_exc()
            return False
    
    def _apply_filters(self, remote_only, experience_level):
        """Apply job search filters"""
        try:
            print("Applying job filters...")
            
            # Click the filter button
            filter_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Filter by']"))
            )
            filter_button.click()
            
            # Apply remote filter if specified
            if remote_only:
                print("Applying remote filter...")
                try:
                    remote_checkbox = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, "//label[contains(., 'Remote')]"))
                    )
                    remote_checkbox.click()
                except Exception as e:
                    print(f"Failed to apply remote filter: {str(e)}")
            
            # Apply experience level filter if specified
            if experience_level:
                print(f"Applying experience level filter: {experience_level}")
                try:
                    # Click experience level dropdown
                    exp_dropdown = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Experience level')]"))
                    )
                    exp_dropdown.click()
                    
                    # Select the specified experience level
                    exp_option = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, f"//label[contains(., '{experience_level}')]"))
                    )
                    exp_option.click()
                    
                    # Close the dropdown
                    exp_dropdown.click()
                except Exception as e:
                    print(f"Failed to apply experience level filter: {str(e)}")
            
            # Apply filters by clicking the Show results button
            show_results = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Show results')]"))
            )
            show_results.click()
            
            # Wait for results to refresh
            time.sleep(3)
            
        except Exception as e:
            print(f"Error applying filters: {str(e)}")
    
    def extract_job_info(self, limit=None):
        """
        Extract job information from LinkedIn job search results and export to CSV/JSON
        
        Args:
            limit (int): Maximum number of job listings to process
            
        Returns:
            list: List of dictionaries containing job information
        """
        # Clear previous job data
        self.jobs = []
        
        try:
            print("Starting job extraction...")
            # Wait for job list to load using explicit wait
            job_list_selector = By.CLASS_NAME, "jobs-search__results-list"
            job_cards_selector = By.CSS_SELECTOR, ".job-search-card"
            
            # Add debug prints
            print("Waiting for job listings to load...")
            
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(job_list_selector)
            )
            
            job_list = self.driver.find_element(*job_list_selector)
            job_fetch = job_list.find_elements(*job_cards_selector)
            
            print(f'Found {len(job_fetch)} job listings')
            self.number_of_jobs = len(job_fetch)
            
            # Check if job listings are found
            if self.number_of_jobs == 0:
                print("No job listings found. Check the page structure or search parameters.")
                return []
            
            # Apply limit if specified
            if limit and limit < self.number_of_jobs:
                print(f"Limiting to {limit} job listings")
                job_fetch = job_fetch[:limit]
            
            # Store initial window handle
            main_window = self.driver.current_window_handle
            
            for index, job in enumerate(job_fetch):
                try:
                    print(f"Processing job {index + 1}/{len(job_fetch)}")
                    
                    # Extract job data with safer approach
                    job_data = self._extract_single_job_data(job, index)
                    
                    if job_data:
                        self.jobs.append(job_data)
                        print(f"Successfully extracted job {index + 1}: {job_data.get('title', 'Unknown title')}")
                    else:
                        print(f"Failed to extract data for job {index + 1}")
                    
                    # Add short pause between processing jobs
                    time.sleep(1)
                    
                except Exception as e:
                    print(f"Error processing job {index + 1}: {str(e)}")
                    traceback.print_exc()  # Print stack trace for debugging
        
        except Exception as e:
            print(f"Fatal error in job extraction: {str(e)}")
            traceback.print_exc()
        
        finally:
            # Print debugging information
            print(f"Total jobs extracted: {len(self.jobs)}")
            
            # Return to main results page if necessary
            try:
                if self.driver.current_window_handle != main_window:
                    self.driver.switch_to.window(main_window)
            except Exception:
                pass
            
            # Save extracted data to files if we have data
            if self.jobs:
                self._save_extracted_data()
            else:
                print("No job data to save")
            
            return self.jobs
    
    def _extract_single_job_data(self, job, index):
        """
        Extract data for a single job listing with improved error handling
        
        Args:
            job: WebElement representing the job card
            index: Index of the job in the list
            
        Returns:
            dict: Dictionary containing job information
        """
        job_data = {}
        
        try:
            # First extract data from the card without clicking
            try:
                job_link = job.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                job_data["url"] = job_link
            except NoSuchElementException:
                job_data["url"] = "URL not available"
                print(f"Warning: Could not extract URL for job {index + 1}")
            
            # Extract title (try multiple potential selectors)
            try:
                selectors = [
                    ".base-search-card__title", 
                    ".job-card-container__link",
                    ".job-card-list__title",
                    "h3"
                ]
                for selector in selectors:
                    try:
                        job_title = job.find_element(By.CSS_SELECTOR, selector).text.strip()
                        if job_title:
                            job_data["title"] = job_title
                            break
                    except NoSuchElementException:
                        continue
                
                if "title" not in job_data:
                    job_data["title"] = "Title not available"
                    print(f"Warning: Could not extract title for job {index + 1}")
            except Exception as e:
                job_data["title"] = "Title not available"
                print(f"Error extracting title: {str(e)}")
            
            # Extract company name (try multiple potential selectors)
            try:
                selectors = [
                    ".base-search-card__subtitle", 
                    ".job-card-container__company-name",
                    ".job-card-container__primary-description",
                    ".job-card-list__company-name"
                ]
                for selector in selectors:
                    try:
                        company = job.find_element(By.CSS_SELECTOR, selector).text.strip()
                        if company:
                            job_data["company"] = company
                            break
                    except NoSuchElementException:
                        continue
                
                if "company" not in job_data:
                    job_data["company"] = "Company not available"
            except Exception as e:
                job_data["company"] = "Company not available"
                print(f"Error extracting company: {str(e)}")
            
            # Extract location (try multiple potential selectors)
            try:
                selectors = [
                    ".job-search-card__location", 
                    ".job-card-container__metadata-item",
                    ".job-card-list__location"
                ]
                for selector in selectors:
                    try:
                        location = job.find_element(By.CSS_SELECTOR, selector).text.strip()
                        if location:
                            job_data["location"] = location
                            break
                    except NoSuchElementException:
                        continue
                
                if "location" not in job_data:
                    job_data["location"] = "Location not available"
            except Exception as e:
                job_data["location"] = "Location not available"
                print(f"Error extracting location: {str(e)}")
            
            # Now click the job to get more details
            print(f"Clicking job {index + 1} to view details...")
            try:
                # Try using JavaScript click which is more reliable
                self.driver.execute_script("arguments[0].click();", job)
            except Exception:
                # Fallback to traditional click methods
                try:
                    actions = ActionChains(self.driver)
                    actions.move_to_element(job).click().perform()
                except Exception:
                    try:
                        job.click()
                    except Exception as e:
                        print(f"Failed to click job {index + 1}: {str(e)}")
                        # Return basic job data we've gathered so far
                        return job_data
            
            # Wait for job details pane to load
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".top-card-layout__title, .jobs-unified-top-card__title"))
                )
                print(f"Job {index + 1} details loaded")
            except TimeoutException:
                print(f"Timeout waiting for job {index + 1} details to load")
                # Return basic job data we've gathered so far
                return job_data
            
            # Handle potential login popup
            try:
                dismiss_button = WebDriverWait(self.driver, 3).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "contextual-sign-in-modal__modal-dismiss"))
                )
                dismiss_button.click()
                print("Dismissed login popup")
            except TimeoutException:
                # No popup appeared, continue
                pass
            
            # Try to get more detailed information
            # Title from details
            try:
                selectors = [
                    ".top-card-layout__title",
                    ".jobs-unified-top-card__title"
                ]
                for selector in selectors:
                    try:
                        job_title_detail = self.driver.find_element(By.CSS_SELECTOR, selector).text.strip()
                        if job_title_detail:
                            job_data["title"] = job_title_detail
                            break
                    except NoSuchElementException:
                        continue
            except Exception:
                pass  # Keep existing title if detail view fails
            
            # Company from details
            try:
                selectors = [
                    ".topcard__org-name-link",
                    ".jobs-unified-top-card__company-name"
                ]
                for selector in selectors:
                    try:
                        company_detail = self.driver.find_element(By.CSS_SELECTOR, selector).text.strip()
                        if company_detail:
                            job_data["company"] = company_detail
                            break
                    except NoSuchElementException:
                        continue
            except Exception:
                pass  # Keep existing company if detail view fails
            
            # Location from details
            try:
                selectors = [
                    ".topcard__flavor--bullet",
                    ".jobs-unified-top-card__bullet"
                ]
                for selector in selectors:
                    try:
                        location_detail = self.driver.find_element(By.CSS_SELECTOR, selector).text.strip()
                        if location_detail:
                            job_data["location"] = location_detail
                            break
                    except NoSuchElementException:
                        continue
            except Exception:
                pass  # Keep existing location if detail view fails
            
            # Description
            try:
                selectors = [
                    ".description__text",
                    ".jobs-description-content__text",
                    ".jobs-unified-description__text"
                ]
                for selector in selectors:
                    try:
                        description = WebDriverWait(self.driver, 5).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                        ).get_attribute("innerText").strip()
                        if description:
                            job_data["description"] = description
                            break
                    except (TimeoutException, NoSuchElementException):
                        continue
                
                if "description" not in job_data:
                    job_data["description"] = "Description not available"
            except Exception:
                job_data["description"] = "Description not available"
            
            # Salary
            try:
                selectors = [
                    ".compensation__salary",
                    ".jobs-unified-top-card__salary-info",
                    ".jobs-unified-top-card__job-insight"
                ]
                for selector in selectors:
                    try:
                        salary_elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        for element in salary_elements:
                            text = element.text.strip()
                            if '$' in text or 'salary' in text.lower() or 'compensation' in text.lower():
                                job_data["salary"] = text
                                break
                    except NoSuchElementException:
                        continue
                
                if "salary" not in job_data:
                    job_data["salary"] = "Not disclosed"
            except Exception:
                job_data["salary"] = "Not disclosed"
            
            # Try to get job type/employment type
            try:
                selectors = [
                    ".job-criteria__item[aria-label='Employment type'] .job-criteria__text",
                    ".jobs-unified-top-card__job-insight"
                ]
                for selector in selectors:
                    try:
                        job_type_elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        for element in job_type_elements:
                            text = element.text.strip()
                            # Look for common employment type indicators
                            if any(type_keyword in text.lower() for type_keyword in 
                                ['full-time', 'part-time', 'contract', 'temporary', 'internship']):
                                job_data["job_type"] = text
                                break
                    except NoSuchElementException:
                        continue
                
                if "job_type" not in job_data:
                    job_data["job_type"] = "Not specified"
            except Exception:
                job_data["job_type"] = "Not specified"
            
            # Experience level
            try:
                selectors = [
                    ".job-criteria__item[aria-label='Experience level'] .job-criteria__text",
                    ".jobs-unified-top-card__job-insight"
                ]
                for selector in selectors:
                    try:
                        exp_elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        for element in exp_elements:
                            text = element.text.strip()
                            # Look for common experience level indicators
                            if any(exp_keyword in text.lower() for exp_keyword in 
                                ['entry', 'associate', 'mid-senior', 'director', 'executive']):
                                job_data["experience_level"] = text
                                break
                    except NoSuchElementException:
                        continue
                
                if "experience_level" not in job_data:
                    job_data["experience_level"] = "Not specified"
            except Exception:
                job_data["experience_level"] = "Not specified"
            
            # Add date posted if available
            try:
                selectors = [
                    ".job-search-card__listdate",
                    ".job-posted-time"
                ]
                for selector in selectors:
                    try:
                        posted_date = job.find_element(By.CSS_SELECTOR, selector).get_attribute("datetime").strip()
                        if posted_date:
                            job_data["date_posted"] = posted_date
                            break
                    except (NoSuchElementException, AttributeError):
                        continue
            except Exception:
                pass  # Date posted is optional
            
            # Add extraction timestamp
            job_data["extraction_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            return job_data
            
        except Exception as e:
            print(f"Error in _extract_single_job_data for job {index + 1}: {str(e)}")
            traceback.print_exc()
            # Return whatever data we were able to gather
            return job_data if job_data else None
    
    def _save_extracted_data(self):
        """
        Save the extracted job information to CSV and JSON files
        
        Returns:
            dict: Dictionary with file paths and job count
        """
        if not self.jobs:
            print("No job data to save")
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save as JSON
        json_filename = os.path.join(self.output_dir, f"linkedin_jobs_{timestamp}.json")
        try:
            with open(json_filename, 'w', encoding='utf-8') as f:
                json.dump(self.jobs, f, indent=4, ensure_ascii=False)
            print(f"Job data saved to {json_filename}")
        except Exception as e:
            print(f"Error saving JSON: {str(e)}")
        
        # Save as CSV
        csv_filename = os.path.join(self.output_dir, f"linkedin_jobs_{timestamp}.csv")
        try:
            # Get all possible field names from all job dictionaries
            fieldnames = set()
            for job in self.jobs:
                fieldnames.update(job.keys())
            
            with open(csv_filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=list(fieldnames))
                writer.writeheader()
                writer.writerows(self.jobs)
            print(f"Job data saved to {csv_filename}")
        except Exception as e:
            print(f"Error saving CSV: {str(e)}")
        
        # Print summary of extraction
        print(f"Successfully extracted {len(self.jobs)} job listings")
        
        # Return the location of saved files
        return {
            "json_file": json_filename,
            "csv_file": csv_filename,
            "job_count": len(self.jobs)
        }
    
    def close(self):
        """Close the browser and clean up resources"""
        print("Closing the browser...")
        try:
            self.driver.quit()
            print("Browser closed successfully")
        except Exception as e:
            print(f"Error closing browser: {str(e)}")


def main():
    """Main function to run the LinkedIn job scraper from command line"""
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description='LinkedIn Job Scraper')
    
    # Required arguments
    parser.add_argument('-k', '--keywords', type=str, required=True, 
                        help='Job search keywords (e.g. "python developer")')
    parser.add_argument('-l', '--location', type=str, required=True, 
                        help='Job location (e.g. "New York" or "Remote")')
    
    # Optional arguments
    parser.add_argument('-u', '--username', type=str, 
                        help='LinkedIn username/email (optional, provides better results when logged in)')
    parser.add_argument('-p', '--password', type=str, 
                        help='LinkedIn password')
    parser.add_argument('-r', '--remote', action='store_true', 
                        help='Filter for remote jobs only')
    parser.add_argument('-e', '--experience', type=str, choices=['Entry', 'Associate', 'Mid-Senior', 'Director', 'Executive'], 
                        help='Filter by experience level')
    parser.add_argument('-n', '--number', type=int, default=None, 
                        help='Maximum number of job listings to process')
    parser.add_argument('--headless', action='store_true', 
                        help='Run browser in headless mode')
    parser.add_argument('-o', '--output', type=str, default='output', 
                        help='Directory to save output files')
    
    args = parser.parse_args()
    
    # Initialize the scraper
    scraper = LinkedInJobScraper(headless=args.headless, output_dir=args.output)
    
    try:
        # Login if credentials provided
        if args.username and args.password:
            scraper.login(args.username, args.password)
        
        # Search for jobs
        search_success = scraper.search_jobs(
            keywords=args.keywords,
            location=args.location,
            remote_only=args.remote,
            experience_level=args.experience
        )
        
        if search_success:
            # Extract job information
            job_data = scraper.extract_job_info(limit=args.number)
            print(f"Extracted {len(job_data)} job listings")
        else:
            print("Job search failed, unable to extract job listings")
    
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        traceback.print_exc()
    
    finally:
        # Clean up
        scraper.close()


if __name__ == "__main__":
    main()