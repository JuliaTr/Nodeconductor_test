import time

from selenium import webdriver

# def page_scroll(driver):
#     driver.execute_script("window.scrollTo(0, 50);")
#     time.sleep(5)

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
    username_field.send_keys(username)
    # Type password
    password_field = driver.find_element_by_css_selector('[ng-model="auth.user.password"]')
    password_field.send_keys(password)
    # Click to login
    login_field = driver.find_element_by_class_name('button-login')
    login_field.click()

def choose_organization(driver, nec_organization):
    organization_field = driver.find_element_by_css_selector('ul.nav-list span.customer-name')
    organization_field.click()
    organization = driver.find_element_by_link_text(nec_organization)
    organization.click()
    time.sleep(5)
    dashboard_field = driver.find_element_by_link_text('Dashboard')
    dashboard_field.click()

def create_project(driver, project_name, project_description=''):
    # Create new project by clicking on the button
    add_new_project_field = driver.find_element_by_class_name('button-apply')
    add_new_project_field.click()
    time.sleep(5)
    project_name_field = driver.find_element_by_css_selector('[ng-model="ProjectAdd.project.name"]')
    project_name_field.send_keys(project_name)
    # project_description_field = driver.find_element_by_css_selector('[ng-model="ProjectAdd.project.description"]')
    # project_description_field.send_keys(project_description)
    create_project_field = driver.find_element_by_class_name('button-apply')
    create_project_field.click()
    time.sleep(5)
    dashboard_field = driver.find_element_by_link_text('Dashboard')
    dashboard_field.click()

def delete_project(driver, project_name):
    dashboard_field = driver.find_element_by_link_text('Dashboard')
    dashboard_field.click()
    time.sleep(5)
    # Delete created project
    projects = driver.find_element_by_link_text(project_name)
    projects.click()
    time.sleep(5)
    back_to_list_field = driver.find_element_by_class_name('back-to-list')
    back_to_list_field.click()
    time.sleep(5)
    project_search_field = driver.find_element_by_css_selector('[ng-model="entityList.searchInput"]')
    project_search_field.send_keys(project_name)
    time.sleep(5)
    actions_field = driver.find_element_by_link_text('actions')
    actions_field.click()
    remove_field = driver.find_element_by_link_text('Remove')
    remove_field.click()
    # Confirm deletion
    alert = driver.switch_to_alert()
    alert.accept()

def create_ssh_key(driver, user_full_name, key_name):
    user_field = driver.find_element_by_link_text(user_full_name)
    user_field.click()
    profile_field = driver.find_element_by_link_text('Profile')
    profile_field.click()
    time.sleep(5)
    keys_field = driver.find_element_by_link_text('Add SSH Key')
    keys_field.click()
    time.sleep(5)
    key_name_field = driver.find_element_by_css_selector('[ng-model="KeyAdd.instance.name"]')
    key_name_field.send_keys(key_name)
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

def delete_ssh_key(driver, key_name, user_full_name):    
    dashboard_field = driver.find_element_by_link_text('Dashboard')
    dashboard_field.click()
    time.sleep(5)
    user_field = driver.find_element_by_link_text(user_full_name)
    user_field.click()
    profile_field = driver.find_element_by_link_text('Profile')
    profile_field.click()
    time.sleep(5)
    # Delete ssh key
    ssh_search_field = driver.find_element_by_css_selector('[ng-model="UserDetailUpdate.searchInput"]')
    ssh_search_field.send_keys(key_name)
    time.sleep(5)
    ssh_key_remove_field = driver.find_element_by_link_text('Remove')
    ssh_key_remove_field.click()
    # Confirm deletion
    alert = driver.switch_to_alert()
    alert.accept()

def create_resource(driver, project_name, resource_name, time_after_resource_creation):
    dashboard_field = driver.find_element_by_link_text('Dashboard')
    dashboard_field.click()
    time.sleep(5)
    project = driver.find_element_by_link_text(project_name)
    project.click()
    # organization = driver.find_element_by_link_text('Manage projects')
    # organization.click()
    # time.sleep(5)
    # project_search_field = driver.find_element_by_css_selector('[ng-model="entityList.searchInput"]')
    # project_search_field.send_keys(project_name)
    # time.sleep(5)
    # project = driver.find_element_by_link_text(project_name)
    # project.click()
    time.sleep(5)
    vms = driver.find_element_by_css_selector('[visible="vms"]')
    vms.click()
    time.sleep(5)
    resource_vms_creation = driver.find_element_by_link_text('Create')
    resource_vms_creation.click()
    time.sleep(5)
    category = driver.find_element_by_class_name('desktop')
    category.click()
    time.sleep(5)
    provider = driver.find_element_by_class_name('openstack')
    provider.click()
    time.sleep(5)
    resource_name_field = driver.find_element_by_css_selector('[ng-model="AppStore.instance[field.name]"]')
    resource_name_field.send_keys(resource_name)
    time.sleep(5)
    images = driver.find_elements_by_class_name('appstore-template-image')
    for image in images:
        if image.text == 'Ubuntu 14.04 x86_64':
            image.click()
            break
    time.sleep(5)        
    flavors = driver.find_elements_by_class_name('title')
    for flavor in flavors:
        if flavor.text == 'm1.small':
            flavor.click()
            break
    time.sleep(5)
    public_keys = driver.find_elements_by_class_name('description-ssh_public_key')
    for public_key in public_keys:
        if public_key.text == 'Openstack test key':
            public_key.click()
            break  
    time.sleep(5)
    purchase = driver.find_element_by_css_selector('[ng-click="AppStore.save()"]')
    purchase.click()
    time.sleep(time_after_resource_creation)
    driver.refresh()

def delete_resource(driver, resource_name, project_name, time_wait_after_resource_stopping, 
                    time_wait_after_resource_removal):
    dashboard_field = driver.find_element_by_link_text('Dashboard')
    dashboard_field.click()
    time.sleep(5)
    project = driver.find_element_by_link_text(project_name)
    project.click()
    time.sleep(5)
    vms = driver.find_element_by_css_selector('[visible="vms"]')
    vms.click()
    time.sleep(5)
    resource_search_field = driver.find_element_by_css_selector('[ng-model="generalSearch"]')
    resource_search_field.send_keys(resource_name)
    time.sleep(5)
    resource_list = driver.find_elements_by_class_name('list-box')
    for resource in resource_list:
        assert 'Online' in resource.text, 'Error: cannot stop resource that is not online or does not exist'
    time.sleep(5)
    actions = driver.find_element_by_link_text('actions')
    actions.click()
    stop_field = driver.find_element_by_link_text('Stop')
    stop_field.click()
    time.sleep(time_wait_after_resource_stopping)
    driver.refresh()
    time.sleep(5)
    vms = driver.find_element_by_css_selector('[visible="vms"]')
    vms.click()
    time.sleep(5)
    resource_field = driver.find_element_by_css_selector('[ng-model="generalSearch"]')
    resource_field.send_keys(resource_name)
    time.sleep(5)
    resource_list = driver.find_elements_by_class_name('list-box')
    for state in resource_list:
        assert 'Offline' in state.text, ('Error: cannot delete resource that is not offline, '
                                        'was not stopped, or does not exist')
    time.sleep(5)
    actions = driver.find_element_by_link_text('actions')
    actions.click()
    remove_field = driver.find_element_by_link_text('Remove')
    remove_field.click()
    alert = driver.switch_to_alert()
    alert.accept()
    time.sleep(time_wait_after_resource_removal)
    driver.refresh()
    time.sleep(5)
    vms = driver.find_element_by_css_selector('[visible="vms"]')
    vms.click()
    time.sleep(5)
    resource_field = driver.find_element_by_css_selector('[ng-model="generalSearch"]')
    resource_field.send_keys(resource_name)
    time.sleep(5)
    resource_list = driver.find_elements_by_class_name('list-box')
    for resource in resource_list:
        assert resource_name not in resource.text, 'Error: resource was not deleted resource, it still exist'






