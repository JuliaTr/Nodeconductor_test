import time

from selenium import webdriver

def get_driver(site_url):
    # Open browser
    driver = webdriver.Firefox()
    driver.maximize_window()
    # Go to start page
    driver.get(site_url)
    return driver

def login_nodeconductor(driver, username, password):
    # Click on take a tour button
    element = driver.find_element_by_class_name('take-a-tour')
    element.click()
    # Necessary time for reloading page
    time.sleep(2)
    # Type username
    username_field = driver.find_element_by_css_selector('[ng-model="auth.user.username"]')
    username_field.send_keys('Julia')
    # Type password
    password_field = driver.find_element_by_css_selector('[ng-model="auth.user.password"]')
    password_field.send_keys('123')
    # Click to login
    login_field = driver.find_element_by_class_name('button-login')
    login_field.click()
    # Necessary time for reloading page
    time.sleep(5)

def create_new_project(driver, project_name, project_description):
    # Create new project by clicking on the button
    add_new_project_field = driver.find_element_by_css_selector('.button-apply[ui-sref="projects.create"]')
    add_new_project_field.click()
    time.sleep(5)
    project_name_field = driver.find_element_by_css_selector('[ng-model="ProjectAdd.project.name"]')
    project_name_field.send_keys(project_name)
    project_description_field = driver.find_element_by_css_selector('[ng-model="ProjectAdd.project.description"]')
    project_description_field.send_keys(project_description)
    create_project_field = driver.find_element_by_class_name('button-apply')
    create_project_field.click()
    time.sleep(5)

def deletion_created_project(driver):
    # Delete created project
    back_to_list_field = driver.find_element_by_class_name('back-to-list')
    back_to_list_field.click()
    time.sleep(5)
    project_search_field = driver.find_element_by_css_selector('[ng-model="entityList.searchInput"]')
    project_search_field.send_keys('Julia_project')
    time.sleep(5)
    actions_field = driver.find_element_by_link_text('actions')
    actions_field.click()
    remove_field = driver.find_element_by_link_text('Remove')
    remove_field.click()
    # Confirm deletion
    alert = driver.switch_to_alert()
    alert.accept()
    time.sleep(5)

def create_ssh_key(driver):
    user_field = driver.find_element_by_link_text('Trygubniak')
    user_field.click()
    profile_field = driver.find_element_by_link_text('Profile')
    profile_field.click()
    time.sleep(5)
    keys_field = driver.find_element_by_link_text('Add SSH Key')
    keys_field.click()
    time.sleep(5)
    key_name_field = driver.find_element_by_css_selector('[ng-model="KeyAdd.instance.name"]')
    key_name_field.send_keys('vgbh')
    public_key_field = driver.find_element_by_css_selector('[ng-model="KeyAdd.instance.public_key"]')
    public_key_field.send_keys(
        'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC/TUNt44JCGCtRyGL/7hb+98YRkZesFRjIdgNtIBwmJ0W1Ikqa3sMn'
        '+Oho4I8+jFEGppLPN3UAZEU+KxnrPNCGfClSWeij9BJWDBmWzAikLFnyYUvJ99Exx3cv/YdYU1PynhwOf0oxpcwi025t'
        'chlYlSPX56e9U4o7q9gR0mkbAUfZN27VaZL7AVe8TXTqYaF8Zg8pB+ru0u0M5xaqTY6nLqps/LClePXKx3HdKVw5wEOf'
        'YNSdqWUFUHr4L7poe1hgzk4M0ZVMVGTXxs7FlUhOb6RxkvgmNC/saU3PWhAQK777iIMmA1OPr2QJkooIYEw4i4crCULy'
        'U9Bm1ehDsvuB marchukpavelp@gmail.com')
    time.sleep(5)
    add_key_field = driver.find_element_by_class_name('button-apply')
    add_key_field.click()
    time.sleep(5)

def delete_ssh_key(driver):    
    # Delete ssh key
    ssh_search_field = driver.find_element_by_css_selector('[ng-model="UserDetailUpdate.searchInput"]')
    ssh_search_field.send_keys('vgbh')
    time.sleep(5)
    ssh_key_remove_field = driver.find_element_by_link_text('Remove')
    ssh_key_remove_field.click()
    # Confirm deletion
    alert = driver.switch_to_alert()
    alert.accept()

