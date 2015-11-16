import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


def is_in_list(list_element, text):
    for element in list_element:
        if text in element.text:
            return True
    return False


def element_exists(driver, css_selector=None, link_text=None, xpath=None):
    try:
        if css_selector is not None:
            driver.find_element_by_css_selector(css_selector)
        elif link_text is not None:
            driver.find_element_by_link_text(link_text)
        elif xpath is not None:
            driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    else:
        return True


def get_driver(site_url):
    driver = webdriver.Firefox()
    driver.maximize_window()
    driver.get(site_url)
    return driver


def login_nodeconductor(driver, username, password):
    element = driver.find_element_by_class_name('take-a-tour')
    element.click()
    time.sleep(2)
    username_field = driver.find_element_by_css_selector('[ng-model="auth.user.username"]')
    username_field.send_keys(username)
    password_field = driver.find_element_by_css_selector('[ng-model="auth.user.password"]')
    password_field.send_keys(password)
    login_field = driver.find_element_by_class_name('button-login')
    login_field.click()


def choose_organization(driver, nec_organization):
    organization_field = driver.find_element_by_css_selector('ul.nav-list span.customer-name')
    organization_field.click()
    organization = driver.find_element_by_link_text(nec_organization)
    organization.click()
    time.sleep(10)
    dashboard_field = driver.find_element_by_css_selector('[ui-sref="dashboard.index"]')
    dashboard_field.click()


def create_project(driver, project_name, project_description=''):
    add_new_project_field = driver.find_element_by_class_name('button-apply')
    add_new_project_field.click()
    time.sleep(5)
    project_name_field = driver.find_element_by_css_selector('[ng-model="ProjectAdd.project.name"]')
    project_name_field.send_keys(project_name)
    if project_description:
        project_description_field = driver.find_element_by_css_selector('[ng-model="ProjectAdd.project.description"]')
        project_description_field.send_keys(project_description)
    create_project_field = driver.find_element_by_class_name('button-apply')
    create_project_field.click()
    time.sleep(10)
    back_to_list_field = driver.find_element_by_class_name('back-to-list')
    back_to_list_field.click()


def delete_project(driver, project_name):
    dashboard_field = driver.find_element_by_css_selector('[ui-sref="dashboard.index"]')
    dashboard_field.click()
    time.sleep(5)
    projects = driver.find_element_by_link_text(project_name)
    projects.click()
    time.sleep(5)
    back_to_list_field = driver.find_element_by_class_name('back-to-list')
    back_to_list_field.click()
    time.sleep(5)
    project_search_field = driver.find_element_by_css_selector('[ng-model="generalSearch"]')
    project_search_field.send_keys(project_name)
    time.sleep(5)
    actions_field = driver.find_element_by_link_text('actions')
    actions_field.click()
    remove_field = driver.find_element_by_link_text('Remove')
    remove_field.click()
    time.sleep(5)
    alert = driver.switch_to_alert()
    alert.accept()


def create_ssh_key(driver, user_full_name, key_name):
    user_field = driver.find_element_by_link_text(user_full_name)
    user_field.click()
    profile_field = driver.find_element_by_link_text('Profile')
    profile_field.click()
    time.sleep(5)
    keys = driver.find_element_by_css_selector('[visible="keys"]')
    keys.click()
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
    dashboard_field = driver.find_element_by_css_selector('[ui-sref="dashboard.index"]')
    dashboard_field.click()
    time.sleep(5)
    user_field = driver.find_element_by_link_text(user_full_name)
    user_field.click()
    profile_field = driver.find_element_by_link_text('Profile')
    profile_field.click()
    time.sleep(5)
    keys = driver.find_element_by_css_selector('[visible="keys"]')
    keys.click()
    time.sleep(5)
    ssh_search_field = driver.find_element_by_css_selector('[ng-model="generalSearch"]')
    ssh_search_field.send_keys(key_name)
    time.sleep(5)
    ssh_key_remove_field = driver.find_element_by_link_text('Remove')
    ssh_key_remove_field.click()
    time.sleep(8)
    alert = driver.switch_to_alert()
    alert.accept()


def create_resource_openstack(driver, project_name, resource_name, category_name, provider_name_in_resource,
                            image_name, flavor_name, public_key_name):
    dashboard_field = driver.find_element_by_css_selector('[ui-sref="dashboard.index"]')
    dashboard_field.click()
    time.sleep(5)
    project = driver.find_element_by_link_text(project_name)
    project.click()
    time.sleep(5)
    vms = driver.find_element_by_css_selector('[visible="vms"]')
    vms.click()
    time.sleep(5)
    resource_vms_creation = driver.find_element_by_link_text('Create')
    resource_vms_creation.click()
    time.sleep(5)
    categories = driver.find_elements_by_class_name('appstore-template')
    for category in categories:
        if category.text == category_name:
            category.click()
            break
    time.sleep(5)
    providers = driver.find_elements_by_class_name('appstore-template')
    for provider in providers:
        if provider.text == provider_name_in_resource:
            provider.click()
            break
    time.sleep(10)
    resource_name_field = driver.find_element_by_css_selector('[ng-model="AppStore.instance[field.name]"]')
    resource_name_field.send_keys(resource_name)
    time.sleep(5)
    images = driver.find_elements_by_class_name('appstore-template-image')
    for image in images:
        if image.text == image_name:
            image.click()
            break
    time.sleep(5)
    flavors = driver.find_elements_by_class_name('title')
    for flavor in flavors:
        if flavor.text == flavor_name:
            flavor.click()
            break
    time.sleep(5)
    public_keys = driver.find_elements_by_class_name('description-ssh_public_key')
    for public_key in public_keys:
        if public_key.text == public_key_name:
            public_key.click()
            break
    time.sleep(5)
    purchase = driver.find_element_by_css_selector('[submit-button="AppStore.save()"]')
    purchase.click()


def create_resource_azure(driver, project_name, resource_name, category_name, provider_name, image_name,
                        username, os_password, size_name):
    dashboard_field = driver.find_element_by_css_selector('[ui-sref="dashboard.index"]')
    dashboard_field.click()
    time.sleep(5)
    project = driver.find_element_by_link_text(project_name)
    project.click()
    time.sleep(5)
    vms = driver.find_element_by_css_selector('[visible="vms"]')
    vms.click()
    time.sleep(5)
    resource_vms_creation = driver.find_element_by_link_text('Create')
    resource_vms_creation.click()
    time.sleep(5)
    categories = driver.find_elements_by_class_name('appstore-template')
    for category in categories:
        if category.text == category_name:
            category.click()
            break
    time.sleep(5)
    providers = driver.find_elements_by_class_name('appstore-template')
    for provider in providers:
        if provider.text == provider_name:
            provider.click()
            break
    time.sleep(10)
    resource_os_username_field = driver.find_element_by_css_selector('[ng-model="AppStore.instance[field.name]"]')
    resource_os_username_field.send_keys(username)
    time.sleep(5)
    os_password_field = driver.find_element_by_class_name('appstore-password')
    os_password_field.send_keys(os_password)
    time.sleep(5)
    repeat_os_password_field = driver.find_element_by_css_selector('[ng-model="AppStore.instance[\'repeat_password\']"]')
    repeat_os_password_field.send_keys(os_password)
    time.sleep(5)
    repeat_os_password_field = driver.find_element_by_id('name')
    repeat_os_password_field.send_keys(resource_name)
    time.sleep(5)
    search_field = driver.find_element_by_css_selector('[ng-model="field.searchQuery"]')
    time.sleep(5)
    search_field.send_keys(image_name)
    time.sleep(10)
    images = driver.find_elements_by_class_name('appstore-template-image')
    for image in images:
        if image.text == image_name:
            image.click()
            break
    time.sleep(5)
    sizes = driver.find_elements_by_class_name('title')
    for size in sizes:
        if size.text == size_name:
            size.click()
            break
    time.sleep(5)
    purchase = driver.find_element_by_css_selector('[submit-button="AppStore.save()"]')
    purchase.click()


def delete_resource(driver, resource_name, project_name, time_wait_after_resource_stopping,
                    time_wait_after_resource_removal):
    dashboard_field = driver.find_element_by_css_selector('[ui-sref="dashboard.index"]')
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


def create_provider_digitalocean(driver, provider_name, provider_type_name, token_name):
    organization_field = driver.find_element_by_css_selector('ul.nav-list span.customer-name')
    organization_field.click()
    time.sleep(5)
    organization_details = driver.find_element_by_link_text('Details')
    organization_details.click()
    time.sleep(10)
    providers = driver.find_element_by_css_selector('[visible="providers"]')
    providers.click()
    time.sleep(5)
    provider_creation = driver.find_element_by_link_text('Create provider')
    provider_creation.click()
    time.sleep(5)
    provider_type = driver.find_element_by_class_name(provider_type_name)
    provider_type.click()
    time.sleep(5)
    provider_name_field = driver.find_element_by_css_selector('[ng-model="ServiceAdd.model.serviceName"]')
    provider_name_field.clear()
    provider_name_field.send_keys(provider_name)
    token_name_field = driver.find_element_by_id('DigitalOcean_token')
    token_name_field.send_keys(token_name)
    add_provider_button = driver.find_element_by_link_text('Add provider')
    add_provider_button.click()


def create_provider_azure(driver, provider_name, provider_type_name, subscription_id_name):
    organization_field = driver.find_element_by_css_selector('ul.nav-list span.customer-name')
    organization_field.click()
    time.sleep(5)
    organization_details = driver.find_element_by_link_text('Details')
    organization_details.click()
    time.sleep(10)
    providers = driver.find_element_by_css_selector('[visible="providers"]')
    providers.click()
    time.sleep(5)
    provider_creation = driver.find_element_by_link_text('Create provider')
    provider_creation.click()
    time.sleep(5)
    provider_type = driver.find_element_by_class_name(provider_type_name)
    provider_type.click()
    time.sleep(5)
    provider_name_field = driver.find_element_by_css_selector('[ng-model="ServiceAdd.model.serviceName"]')
    provider_name_field.clear()
    provider_name_field.send_keys(provider_name)
    token_name_field = driver.find_element_by_id('Azure_username')
    token_name_field.send_keys(subscription_id_name)
    upload_file = driver.find_element_by_link_text('Browse')
    upload_file.click()
    time.sleep(5)
    # certificate = driver.switch_to_window('File Upload')
    certificate = driver.switch_to_active_element()
    certificate.send_keys('home\julia\azure_cert.pem')
    certificate.submit()
    # certificate = driver.find_element_by_name('azure_cert.pem')
    # certificate.open()
    # driver.current_window_handle
    # element = driver.switch_to_window("File Upload")
    # driver.navigate()
    # element.send_keys("home\julia\azure_cert.pem")
    # alert = driver.switch_to_alert()
    # alert.accept()
    time.sleep(5)
    add_provider_button = driver.find_element_by_link_text('Add provider')
    add_provider_button.click()


def import_resource(driver, project_name, provider_name, resource_name):
    dashboard_field = driver.find_element_by_css_selector('[ui-sref="dashboard.index"]')
    dashboard_field.click()
    time.sleep(10)
    project = driver.find_element_by_link_text(project_name)
    project.click()
    time.sleep(8)
    vms = driver.find_element_by_css_selector('[visible="vms"]')
    vms.click()
    time.sleep(5)
    resource_import = driver.find_element_by_link_text('Import')
    resource_import.click()
    time.sleep(5)
    category_list = driver.find_elements_by_class_name('appstore-template')
    for category in category_list:
        if category.text == 'VMs':
            category.click()
            break
    time.sleep(5)
    provider_list = driver.find_elements_by_class_name('appstore-template')
    for provider in provider_list:
        if provider.text == provider_name:
            provider.click()
            break
    time.sleep(5)
    resource = driver.find_element_by_link_text(resource_name)
    resource.click()
    time.sleep(5)
    import_button = driver.find_element_by_link_text('Import')
    import_button.click()


def unlink_resource(driver, project_name, resource_name):
    dashboard_field = driver.find_element_by_css_selector('[ui-sref="dashboard.index"]')
    dashboard_field.click()
    time.sleep(10)
    project = driver.find_element_by_link_text(project_name)
    project.click()
    time.sleep(10)
    vms = driver.find_element_by_css_selector('[visible="vms"]')
    vms.click()
    time.sleep(5)
    resource_search_field = driver.find_element_by_css_selector('[ng-model="generalSearch"]')
    resource_search_field.send_keys(resource_name)
    time.sleep(5)
    actions = driver.find_element_by_link_text('actions')
    actions.click()
    unlink_field = driver.find_element_by_link_text('Unlink')
    unlink_field.click()


def delete_provider(driver, provider_name):
    organization_field = driver.find_element_by_css_selector('ul.nav-list span.customer-name')
    organization_field.click()
    time.sleep(5)
    organization_details = driver.find_element_by_link_text('Details')
    organization_details.click()
    time.sleep(10)
    providers = driver.find_element_by_css_selector('[visible="providers"]')
    providers.click()
    time.sleep(5)
    provider_search_field = driver.find_element_by_css_selector('[ng-model="generalSearch"]')
    provider_search_field.send_keys(provider_name)
    time.sleep(10)
    remove_provider = driver.find_element_by_link_text('Delete')
    remove_provider.click()
    time.sleep(5)
    alert = driver.switch_to_alert()
    alert.accept()
