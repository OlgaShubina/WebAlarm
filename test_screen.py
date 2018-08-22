from selenium import webdriver
from depot.manager import DepotManager

browser = webdriver.Chrome('/chromedriver')
browser.get('localhost:8000/status_page.html')
browser.save_screenshot('screenie.png')
browser.quit()
