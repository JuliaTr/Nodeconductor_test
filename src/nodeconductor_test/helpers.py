import datetime
import os
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import urlparse

from base import BaseSettings


def get_private_parent(class_name):
    private_parent = object  # empty private parent if it is not defined
    try:
        import private_settings
    except ImportError:
        # private settings is not defined. Do nothing.
        pass
    else:
        if hasattr(private_settings, class_name):   # check if private settings is defined
            private_parent = getattr(private_settings, class_name)  # add settings to list of parents
    return private_parent


def _go_to_organization_details(driver):
    organization_field = driver.find_element_by_css_selector('ul.nav-list span.customer-name')
    organization_field.click()
    organization_details = driver.find_element_by_link_text('Details')
    organization_details.click()
    time.sleep(BaseSettings.click_time_wait)


def _search(driver, key, css_selector='[ng-model="controller.generalSearch"]'):
    print 'Search by key: %s' % key
    search_field = driver.find_element_by_css_selector(css_selector)
    search_field.clear()
    search_field.send_keys(key)
    time.sleep(BaseSettings.search_time_wait)


def _go_to_project_page(driver, key):
    print 'Go to project %s page' % key
    project = driver.find_element_by_link_text(key)
    project.click()
    time.sleep(BaseSettings.click_time_wait)


def _confirm_alert(driver, key):
    print 'Accept %s delete confirmation popup' % key
    alert = driver.switch_to_alert()
    alert.accept()


def _back_to_list(driver):
    print 'Go to list'
    back_to_list_button = driver.find_element_by_class_name('back-to-list')
    back_to_list_button.click()
    time.sleep(BaseSettings.click_time_wait)


def _remove_action(driver):
    print 'Select remove action'
    actions = driver.find_element_by_link_text('actions')
    actions.click()
    remove_field = driver.find_element_by_link_text('Remove')
    remove_field.click()


def go_to_main_page(driver):
    split = urlparse.urlsplit(driver.current_url)
    driver.get('%s://%s/' % (split.scheme, split.netloc))
    time.sleep(BaseSettings.click_time_wait)  # organization page isn't downloaded at once.


def make_screenshot(driver, name=None):
    if name is None:
        name = str(datetime.datetime.now()) + '.png'
    name = name.replace(' ', '_')
    print "Make screenshot with name " + name
    if not os.path.exists(BaseSettings.screenshots_folder):
        os.makedirs(BaseSettings.screenshots_folder)
    driver.save_screenshot(os.path.join(BaseSettings.screenshots_folder, name))


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


def force_click(driver, css_selector=None, xpath=None, link_text=None, tries_left=3):
    """ Tries to get element and click on it several times. """
    try:
        if css_selector is not None:
            element = driver.find_element_by_css_selector(css_selector)
        elif xpath is not None:
            element = driver.find_element_by_xpath(xpath)
        elif link_text is not None:
            element = driver.find_element_by_link_text(link_text)
        element.click()
    except StaleElementReferenceException as e:
        tries_left -= 1
        if tries_left > 0:
            force_click(driver, css_selector=css_selector, xpath=xpath, link_text=link_text, tries_left=tries_left)
        else:
            raise e


def get_driver(site_url):
    driver = webdriver.Firefox()
    # Tests should run on 1024x768 resolution until agreed otherwise.
    # If changing these numbers make sure to change screen size in Jenkins job configuration.
    # Use 420x580 resolution to test mobile version (work in progress).
    # TODO: read resolution value from method parameters or configuration file.
    driver.set_window_size(1366, 768)
    driver.get(site_url)
    return driver


def login_nodeconductor(driver, username, password):
    print '----- Logging in started -----'
    element = driver.find_element_by_class_name('take-a-tour')
    element.click()
    username_field = driver.find_element_by_css_selector('[ng-model="auth.user.username"]')
    username_field.send_keys(username)
    password_field = driver.find_element_by_css_selector('[ng-model="auth.user.password"]')
    password_field.send_keys(password)
    login_field = driver.find_element_by_class_name('button-login')
    login_field.click()
    print '----- Logging in ended -----'


def choose_organization(driver, organization):
    print '----- Organization selection process started -----'
    organization_field = driver.find_element_by_css_selector('ul.nav-list span.customer-name')
    organization_field.click()
    print 'Go to organization page'
    organization = driver.find_element_by_link_text(organization)
    organization.click()
    print '----- Organization selection process ended -----'


def create_organization(driver, organization):
    print '----- Organization creation process started -----'
    _go_to_organization_details(driver)
    _back_to_list(driver)
    # time.sleep(20)  # without additional time it leads to 404 page. Manualy it doesn't lead to 404 page.
    print 'Create organization'
    add_organization_button = driver.find_element_by_xpath('//a[contains(@class, \'button\') and span[contains(text(), \'Add organization\')]]')
    add_organization_button.click()
    organization_name_field = driver. find_element_by_css_selector('[ng-model="CustomerAdd.instance.name"]')
    organization_name_field.send_keys(organization)
    create_organization_button = driver. find_element_by_link_text('Create organization')
    create_organization_button.click()
    print '----- Organization creation process ended -----'


def delete_organization(driver, organization):
    print '----- Organization deletion process started -----'
    go_to_main_page(driver)
    print 'Go to organization page'
    time.sleep(BaseSettings.click_time_wait)
    _go_to_organization_details(driver)
    _back_to_list(driver)
    print 'Delete organization'
    _search(driver, organization, css_selector='[ng-model="entityList.searchInput"]')
    print 'Open organization actions'
    _remove_action(driver)
    _confirm_alert(driver, organization)
    print '----- Organization deletion process ended -----'


def top_up_organization_balance(driver, top_up_balance, email, password_account):
    print '----- Top up organization balance process started -----'
    go_to_main_page(driver)
    print 'Top-up balance'
    time.sleep(7)   # because of alert over the button
    balance_button = driver.find_element_by_css_selector('i.fa-credit-card')
    balance_button.click()
    add_amount_field = driver.find_element_by_css_selector('[ng-model="amount"]')
    add_amount_field.clear()
    add_amount_field.send_keys(top_up_balance)
    add_credit_button = driver.find_element_by_css_selector('[submit-button="addCredit(amount)"]')
    add_credit_button.click()
    time.sleep(BaseSettings.click_time_wait)
    time.sleep(10)  # PayPal page loading
    print 'Switch to payment process'
    way_to_pay = driver.find_element_by_xpath('//input[@value="Pay with my PayPal account"]')
    way_to_pay.click()
    time.sleep(BaseSettings.click_time_wait)
    email_field = driver.find_element_by_id('login_email')
    email_field.clear()
    email_field.send_keys(email)
    password_field = driver.find_element_by_id('login_password')
    password_field.clear()
    password_field.send_keys(password_account)
    login_button = driver.find_element_by_id('submitLogin')
    login_button.click()
    time.sleep(BaseSettings.click_time_wait)
    continue_button = driver.find_element_by_id('continue_abovefold')
    continue_button.click()
    print '----- Top up organization balance process ended -----'


def create_project(driver, project_name, project_description=''):
    print '----- Project creation process started -----'
    go_to_main_page(driver)
    add_new_project_field = driver.find_element_by_class_name('button-apply')
    add_new_project_field.click()
    print 'Create a project'
    project_name_field = driver.find_element_by_css_selector('[ng-model="ProjectAdd.project.name"]')
    project_name_field.send_keys(project_name)
    if project_description:
        project_description_field = driver.find_element_by_css_selector('[ng-model="ProjectAdd.project.description"]')
        project_description_field.send_keys(project_description)
    print 'Click on create project button'
    create_project_field = driver.find_element_by_class_name('button-apply')
    create_project_field.click()
    print '----- Project creation process ended -----'


def delete_project(driver, project_name):
    print '----- Project deletion process started -----'
    go_to_main_page(driver)
    _go_to_project_page(driver, project_name)
    _back_to_list(driver)
    time.sleep(BaseSettings.click_time_wait)
    _search(driver, project_name)
    print 'Open project actions'
    force_click(driver, css_selector='[ng-click="openActionsListTrigger()"]')
    print 'Click on remove button'
    project_remove = driver.find_element_by_link_text('Remove')
    project_remove.click()
    _confirm_alert(driver, project_name)
    print '----- Project deletion process ended -----'


def create_ssh_key(driver, user_full_name, key_name):
    print '----- SSH key creation process started -----'
    print 'Go to profile page'
    user_field = driver.find_element_by_class_name('user-name')
    user_field.click()
    profile = driver.find_element_by_link_text('Profile')
    profile.click()
    print 'Go to keys tab'
    force_click(driver, css_selector='[visible="keys"]')
    print 'keys tab was successfully choosen'
    time.sleep(BaseSettings.click_time_wait)
    print 'Push button to add SSH key'
    keys_field = driver.find_element_by_link_text('Add SSH Key')
    keys_field.click()
    time.sleep(BaseSettings.click_time_wait)
    print 'Give a name to a key'
    key_name_field = driver.find_element_by_css_selector('[ng-model="KeyAdd.instance.name"]')
    key_name_field.send_keys(key_name)
    print 'Give a public key '
    public_key_field = driver.find_element_by_css_selector('[ng-model="KeyAdd.instance.public_key"]')
    public_key_field.send_keys(
        'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC/TUNt44JCGCtRyGL/7hb+98YRkZesFRjIdgNtIBwmJ0W1Ikqa3sMn'
        '+Oho4I8+jFEGppLPN3UAZEU+KxnrPNCGfClSWeij9BJWDBmWzAikLFnyYUvJ99Exx3cv/YdYU1PynhwOf0oxpcwi025t'
        'chlYlSPX56e9U4o7q9gR0mkbAUfZN27VaZL7AVe8TXTqYaF8Zg8pB+ru0u0M5xaqTY6nLqps/LClePXKx3HdKVw5wEOf'
        'YNSdqWUFUHr4L7poe1hgzk4M0ZVMVGTXxs7FlUhOb6RxkvgmNC/saU3PWhAQK777iIMmA1OPr2QJkooIYEw4i4crCULy'
        'U9Bm1ehDsvuB marchukpavelp@gmail.com')
    print 'Click on add key button'
    add_key_field = driver.find_element_by_class_name('button-apply')
    add_key_field.click()
    print '----- SSH key creation process ended -----'


def delete_ssh_key(driver, key_name, user_full_name):
    print '----- SSH key deletion process started -----'
    print 'Go to profile page'
    user_field = driver.find_element_by_class_name('user-name')
    user_field.click()
    profile = driver.find_element_by_link_text('Profile')
    profile.click()
    print 'Go to keys tab'
    force_click(driver, css_selector='[visible="keys"]')
    print 'keys tab was successfully choosen'
    time.sleep(BaseSettings.click_time_wait)
    _search(driver, key_name)
    print 'Click on remove button'
    ssh_key_remove = driver.find_element_by_link_text('Remove')
    ssh_key_remove.click()
    _confirm_alert(driver, key_name)
    print '----- SSH key deletion process ended -----'


# Blocker SAAS-1141
def create_resource_openstack(driver, project_name, resource_name, category_name, provider_name_in_resource,
                              image_name, flavor_name, public_key_name):
    print '----- Resource creation process started -----'
    go_to_main_page(driver)
    _go_to_project_page(driver, project_name)
    print 'Go to vms tab'
    force_click(driver, css_selector='[visible="vms"]')
    print 'vms tab was successfully choosen'
    time.sleep(BaseSettings.click_time_wait)
    print 'Create a resource'
    resource_vms_creation = driver.find_element_by_link_text('Create')
    resource_vms_creation.click()
    time.sleep(BaseSettings.click_time_wait)
    print 'Category selection'
    categories = driver.find_elements_by_class_name('appstore-template')
    for category in categories:
        if category_name in category.text:
            category.click()
            break
    print 'Provider selection'
    providers = driver.find_elements_by_class_name('appstore-template')
    for provider in providers:
        if provider.text == provider_name_in_resource:
            provider.click()
            break
    print 'Put resource name'
    resource_name_field = driver.find_element_by_css_selector('[ng-model="AppStore.instance[field.name]"]')
    resource_name_field.send_keys(resource_name)
    print 'Image selection'
    images = driver.find_elements_by_class_name('appstore-template-image')
    for image in images:
        if image.text == image_name:
            image.click()
            break
    print 'Flavor selection'
    flavors = driver.find_elements_by_class_name('title')
    for flavor in flavors:
        if flavor.text == flavor_name:
            flavor.click()
            break
    print 'Public key selection'
    public_keys = driver.find_elements_by_class_name('description-ssh_public_key')
    for public_key in public_keys:
        if public_key.text == public_key_name:
            public_key.click()
            break
    print 'Click on purchase button'
    purchase = driver.find_element_by_css_selector('[submit-button="AppStore.save()"]')
    purchase.click()
    print '----- Resource creation process ended -----'


# To use this function it is necessary to be already on dashboard
def create_resource_azure(driver, project_name, resource_name, category_name, provider_name, image_name,
                          username, os_password, size_name):
    _go_to_project_page(driver, project_name)
    force_click(driver, css_selector='[visible="vms"]')
    print 'vms tab was successfully choosen'
    time.sleep(BaseSettings.click_time_wait)
    resource_vms_creation = driver.find_element_by_link_text('Create')
    resource_vms_creation.click()
    time.sleep(BaseSettings.click_time_wait)
    categories = driver.find_elements_by_class_name('appstore-template')
    for category in categories:
        if category.text == category_name:
            category.click()
            break

    providers = driver.find_elements_by_class_name('appstore-template')
    for provider in providers:
        if provider.text == provider_name:
            provider.click()
            break

    resource_os_username_field = driver.find_element_by_css_selector('[ng-model="AppStore.instance[field.name]"]')
    resource_os_username_field.send_keys(username)

    os_password_field = driver.find_element_by_class_name('appstore-password')
    os_password_field.send_keys(os_password)

    repeat_os_password_field = driver.find_element_by_css_selector('[ng-model="AppStore.instance[\'repeat_password\']"]')
    repeat_os_password_field.send_keys(os_password)

    repeat_os_password_field = driver.find_element_by_id('name')
    repeat_os_password_field.send_keys(resource_name)

    search_field = driver.find_element_by_css_selector('[ng-model="field.searchQuery"]')
    time.sleep(BaseSettings.search_time_wait)
    search_field.send_keys(image_name)

    images = driver.find_elements_by_class_name('appstore-template-image')
    for image in images:
        if image.text == image_name:
            image.click()
            break

    sizes = driver.find_elements_by_class_name('title')
    for size in sizes:
        if size.text == size_name:
            size.click()
            break

    purchase = driver.find_element_by_css_selector('[submit-button="AppStore.save()"]')
    purchase.click()


def delete_resource(driver, resource_name, project_name, time_wait_after_resource_stopping):
    print '----- Resource deletion process started -----'
    go_to_main_page(driver)
    print 'Go to project page'
    _go_to_project_page(driver, project_name)
    print 'Go to vms tab'
    force_click(driver, css_selector='[visible="vms"]')
    print 'Search resource in the list'
    _search(driver, resource_name)
    print 'Check online state existence of the resource'
    xpath = '//a[@class="status-circle online"]'
    assert element_exists(driver, xpath=xpath), (
        'Error: cannot stop resource "%s" that is not online or does not exist' % resource_name)
    print 'Stop resource'
    actions = driver.find_element_by_link_text('actions')
    actions.click()
    stop_field = driver.find_element_by_link_text('Stop')
    stop_field.click()
    print 'Wait for stop of created resource'
    try:
        WebDriverWait(driver, time_wait_after_resource_stopping).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".status-circle.offline")))
    except TimeoutException as e:
        print 'Error: Resource was not stopped'
        raise e
    else:
        print 'Resource is stopped'
    print 'Go to vms tab'
    force_click(driver, css_selector='[visible="vms"]')
    print 'Search resource in the list'
    _search(driver, resource_name)
    xpath = '//a[@class="status-circle offline"]'
    assert element_exists(driver, xpath=xpath), (
        'Error: cannot delete resource "%s" that is not offline, was not stopped,'
        'or does not exist' % resource_name)
    _remove_action(driver)
    _confirm_alert(driver, resource_name)
    print '----- Resource deletion process ended -----'


def create_provider_digitalocean(driver, provider_name, provider_type_name, access_token):
    print '----- Provider creation process started -----'
    print 'Go to organization page'
    _go_to_organization_details(driver)
    print 'Go to providers tab'
    time.sleep(BaseSettings.click_time_wait)  # sometimes doesn't want to go to providers tab
    force_click(driver, css_selector='[visible="providers"]')
    print 'providers tab was successfully choosen'
    time.sleep(BaseSettings.click_time_wait)
    print 'Push button to create a provider'
    provider_creation = driver.find_element_by_link_text('Create provider')
    provider_creation.click()
    print 'To be on provider creation page'
    time.sleep(BaseSettings.click_time_wait)
    print 'Provider type selection'
    provider_type_list = driver.find_elements_by_class_name('appstore-template')
    for provider_type in provider_type_list:
        if provider_type.text == provider_type_name:
            provider_type.click()
            break
    time.sleep(BaseSettings.click_time_wait)
    print 'Give a name to provider'
    provider_name_field = driver.find_element_by_css_selector('[ng-model="ServiceAdd.model.serviceName"]')
    provider_name_field.clear()
    provider_name_field.send_keys(provider_name)
    print 'Put a name of the token'
    access_token_field = driver.find_element_by_id('DigitalOcean_token')
    access_token_field.send_keys(access_token)
    print 'Click on add provider button'
    add_provider_button = driver.find_element_by_link_text('Add provider')
    add_provider_button.click()
    print '----- Provider creation process ended -----'


# SAAS-1120
def create_provider_aws(driver, provider_name, provider_type_name, access_key_id, secret_access_key):
    print '----- Provider creation process started -----'
    print 'Go to organization page'
    _go_to_organization_details(driver)
    print 'Go to providers tab'
    force_click(driver, css_selector='[visible="providers"]')
    print 'providers tab was successfully choosen'
    time.sleep(BaseSettings.click_time_wait)
    time.sleep(3)  # sometimes click isn't executed without additional time click. There is no problem using the button manually
    print 'Push button to create a provider'
    provider_creation = driver.find_element_by_link_text('Create provider')
    provider_creation.click()
    print 'To be on provider creation page'
    time.sleep(BaseSettings.click_time_wait)
    print 'Provider type selection'
    provider_type_list = driver.find_elements_by_class_name('appstore-template')
    for provider_type in provider_type_list:
        if provider_type.text == provider_type_name:
            provider_type.click()
            break
    time.sleep(BaseSettings.click_time_wait)
    print 'Give a name to provider'
    provider_name_field = driver.find_element_by_css_selector('[ng-model="ServiceAdd.model.serviceName"]')
    provider_name_field.clear()
    provider_name_field.send_keys(provider_name)
    print 'Put a name of the access key id'
    access_key_id_field = driver.find_element_by_id('Amazon_username')
    access_key_id_field.send_keys(access_key_id)
    secret_access_key_field = driver.find_element_by_id('Amazon_token')
    secret_access_key_field.send_keys(secret_access_key)
    print 'Click on add provider button'
    add_provider_button = driver.find_element_by_link_text('Add provider')
    add_provider_button.click()
    print '----- Provider creation process ended -----'


# Method isn't completed yet.
# TODO: Add certificate.
def create_provider_azure(driver, provider_name, provider_type_name, subscription_id_name):
    _go_to_organization_details(driver)
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
    # TODO: Add certificate.
    add_provider_button = driver.find_element_by_link_text('Add provider')
    add_provider_button.click()


def import_resource(driver, project_name, provider_name, category_name, resource_name):
    print '----- Resource import process started -----'
    go_to_main_page(driver)
    _go_to_project_page(driver, project_name)
    print 'Go to resource tab'
    force_click(driver, css_selector='[visible="vms"]')
    time.sleep(BaseSettings.click_time_wait)
    print 'Import a resource'
    resource_import = driver.find_element_by_link_text('Import')
    resource_import.click()
    print 'Category selection'
    category_list = driver.find_elements_by_class_name('appstore-template')
    for category in category_list:
        if category.text == category_name:
            category.click()
            break
    print 'Provider selection'
    provider_list = driver.find_elements_by_class_name('appstore-template')
    for provider in provider_list:
        if provider.text == provider_name:
            provider.click()
            break
    print 'Select resource name'
    time.sleep(BaseSettings.click_time_wait)
    time.sleep(7)  # cannot find resource to import
    resource = driver.find_element_by_link_text(resource_name)
    resource.click()
    print 'Click on import button'
    import_button = driver.find_element_by_link_text('Import')
    import_button.click()
    print '----- Resource import process ended -----'


def unlink_resource(driver, project_name, resource_name):
    print '----- Resource unlink process started -----'
    go_to_main_page(driver)
    _go_to_project_page(driver, project_name)
    print 'Go to resource tab'
    force_click(driver, css_selector='[visible="vms"]')
    time.sleep(BaseSettings.click_time_wait)
    _search(driver, resource_name)
    print 'Open project actions'
    force_click(driver, css_selector='[ng-click="openActionsListTrigger()"]')
    print 'Click on remove button'
    unlink_field = driver.find_element_by_link_text('Unlink')
    unlink_field.click()
    print '----- Resource unlink process ended -----'


def delete_provider(driver, provider_name):
    print '----- Provider deletion process started -----'
    print 'Go to organization page'
    _go_to_organization_details(driver)
    print 'Go to providers tab'
    force_click(driver, css_selector='[visible="providers"]')
    print 'Providers tab was successfully choosen'
    time.sleep(BaseSettings.click_time_wait)
    _search(driver, provider_name)
    print 'Click on delete button'
    force_click(driver, css_selector='[ng-class="{\'disabled\': button.isDisabled(buttonModel)}"]')
    _confirm_alert(driver, provider_name)
    print '----- Provider deletion process ended -----'


def create_application_group(driver, project_name, category_name, resource_type_name, path_name, application_group_name):
    print '----- Application group creation process started -----'
    go_to_main_page(driver)
    _go_to_project_page(driver, project_name)
    print 'Go to applications tab'
    force_click(driver, css_selector='[visible="applications"]')
    print 'Applications tab was successfully choosen'
    time.sleep(BaseSettings.click_time_wait)
    time.sleep(5)  # create button isn't selected without additional time wait
    print 'Create an application'
    application_creation = driver.find_element_by_link_text('Create')
    application_creation.click()
    print 'To be on provider creation page'
    time.sleep(BaseSettings.click_time_wait)
    print 'Category selection'
    categories = driver.find_elements_by_class_name('appstore-template')
    for category in categories:
        if category.text == category_name:
            category.click()
            break
    print 'Resource type selection'
    resource_types = driver.find_elements_by_class_name('appstore-template')
    for resource_type in resource_types:
        if resource_type.text == resource_type_name:
            resource_type.click()
            break
    print 'Put path name'
    path_field = driver.find_element_by_css_selector('[ng-if="field.name !== \'password\'"]')
    path_field.send_keys(path_name)
    print 'Put application group name'
    application_name_field = driver.find_element_by_id('name')
    application_name_field.send_keys(application_group_name)
    print 'Purchase an application group'
    purchase = driver.find_element_by_css_selector('[submit-button="AppStore.save()"]')
    purchase.click()
    print '----- Application group creation process ended -----'


def create_application_project(driver, project_name, category_name, resource_type_name1,
                               application_project_name, visibility_level_name, application_group_name):
    print '----- Application project creation process started -----'
    go_to_main_page(driver)
    _go_to_project_page(driver, project_name)
    print 'Go to applications tab'
    force_click(driver, css_selector='[visible="applications"]')
    print 'Applications tab was successfully choosen'
    time.sleep(BaseSettings.click_time_wait)
    print 'Create an application'
    application_creation = driver.find_element_by_link_text('Create')
    application_creation.click()
    time.sleep(BaseSettings.click_time_wait)
    print 'Category selection'
    categories = driver.find_elements_by_class_name('appstore-template')
    for category in categories:
        if category.text == category_name:
            category.click()
            break
    print 'Resource type selection'
    resource_types = driver.find_elements_by_class_name('appstore-template')
    for resource_type in resource_types:
        if resource_type.text == resource_type_name1:
            resource_type.click()
            break
    time.sleep(BaseSettings.click_time_wait)
    print 'Group selection'
    groups = driver.find_elements_by_class_name('appstore-template')
    for group in groups:
        if group.text == application_group_name:
            group.click()
            break
    print 'Visibility selection'
    visibility_levels = driver.find_elements_by_class_name('appstore-template')
    for visibility_level in visibility_levels:
        if visibility_level.text == visibility_level_name:
            visibility_level.click()
            break
    print 'Put application project name'
    application_name_field = driver.find_element_by_css_selector('[ng-model="AppStore.instance[field.name]"]')
    application_name_field.send_keys(application_project_name)
    print 'Purchase an application project'
    purchase = driver.find_element_by_css_selector('[submit-button="AppStore.save()"]')
    purchase.click()
    print '----- Application project creation process ended -----'


def delete_application_group(driver, project_name, application_group_name):
    print '----- Application group deletion process started -----'
    go_to_main_page(driver)
    _go_to_project_page(driver, project_name)
    print 'Go to applications tab'
    force_click(driver, css_selector='[visible="applications"]')
    print 'Applications tab was successfully choosen'
    time.sleep(BaseSettings.click_time_wait)
    _search(driver, application_group_name)
    _remove_action(driver)
    _confirm_alert(driver, application_group_name)
    print '----- Application group deletion process ended -----'


def delete_application_project(driver, project_name, application_project_name):
    print '----- Application project creation process started -----'
    go_to_main_page(driver)
    _go_to_project_page(driver, project_name)
    print 'Go to applications tab'
    force_click(driver, css_selector='[visible="applications"]')
    print 'Applications tab was successfully choosen'
    time.sleep(BaseSettings.click_time_wait)
    _search(driver, application_project_name)
    _remove_action(driver)
    _confirm_alert(driver, application_project_name)
    print '----- Application project deletion process ended -----'
