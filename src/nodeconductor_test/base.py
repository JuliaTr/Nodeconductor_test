from selenium import webdriver

driver = webdriver.Firefox()
driver.implicitly_wait(1000)  # seconds
driver.get("http://ted.com/")
driver.maximize_window()
myDynamicElement = driver.find_elements_by_xpath("//span[contains(text(), 'Ideas worth spreading')]")
driver.quit()
