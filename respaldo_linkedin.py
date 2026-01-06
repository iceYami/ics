from linkedin_scraper import Person, actions
from selenium import webdriver

driver = webdriver.Chrome()

email = "your_linkedin_email"
password = "your_linkedin_password"
actions.login(driver, email, password)

# Search for employees
company = "Company Name"
people = []

# Search URL
search_url = f"https://www.linkedin.com/search/results/people/?keywords={company}%20SCADA"
driver.get(search_url)

# Extract profiles (simplified)
# ... (scraping logic)

driver.quit()
