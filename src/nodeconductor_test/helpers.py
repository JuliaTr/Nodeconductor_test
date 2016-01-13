import datetime
import os
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

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


def _search(driver, key):
    print 'Search by key: %s' % key
    search_field = driver.find_element_by_css_selector('[ng-model="generalSearch"]')
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


def go_to_main_page(driver):
    split = urlparse.urlsplit(driver.current_url)
    driver.get('%s://%s/' % (split.scheme, split.netloc))


def make_screenshot(driver, name=None):
    if name is None:
        name = str(datetime.datetime.now()) + '.png'
    name = name.replace(' ', '_')
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


def force_click(driver, css_selector=None, xpath=None, tries_left=3):
    """ Tries to get element and click on it several times. """
    try:
        if css_selector is not None:
            element = driver.find_element_by_css_selector(css_selector)
        elif xpath is not None:
            element = driver.find_element_by_xpath(xpath)
        element.click()
    except StaleElementReferenceException as e:
        tries_left -= 1
        if tries_left > 0:
            force_click(driver, css_selector=css_selector, xpath=xpath, tries_left=tries_left)
        else:
            raise e


def get_driver(site_url):
    driver = webdriver.Firefox()
    # driver.set_window_size(420, 580) # to test mobile version
    driver.maximize_window()  # to test mobile version comment this line
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
    _go_to_organization_details(driver)
    _back_to_list(driver)
    time.sleep(BaseSettings.click_time_wait)
    print 'Delete organization'
    search_field = driver.find_element_by_css_selector('[ng-change="entityList.search()"]')
    search_field.clear()
    search_field.send_keys(organization)
    time.sleep(BaseSettings.search_time_wait)
    print 'Open organization actions'
    force_click(driver, css_selector='[ng-click="openActionsListTrigger()"]')
    print 'Click on remove button'
    organization_remove = driver.find_element_by_link_text('Remove')
    organization_remove.click()
    _confirm_alert(driver, organization)
    print '----- Organization deletion process ended -----'


# Cannot complete, blocker SAAS-1101
def top_up_organization_balance(driver, top_up_balance, card_number, expiration_month_date, first_name, last_name,
                                expiration_year_date, csc_number, addresss_line, city_name, phone_number, email):
    print '----- Top up organization balance process started -----'
    go_to_main_page(driver)
    print 'Go to organization page'
    _go_to_organization_details(driver)
    print 'Top-up balance'
    top_up_button = driver.find_element_by_link_text('Top-up')
    top_up_button.click()
    add_amount_field = driver.find_element_by_css_selector('[ng-model="amount"]')
    add_amount_field.clear()
    add_amount_field.send_keys(top_up_balance)
    add_credit_button = driver.find_element_by_link_text('Add credit')
    add_credit_button.click()
    time.sleep(BaseSettings.click_time_wait)
    print 'Switch to payment process'
    # window_before = driver.window_handles[0]
    # window_after = driver.window_handles[1]
    # driver.switch_to_window(window_after)
    # print window_after
    # for handle in driver.window_handles:
    #     driver.switch_to.window(handle)
    card = driver.find_elements_by_id('cc_number')
    card.send_keys(card_number)
    expiration_month = driver.find_elements_by_id('expdate_month')
    expiration_month.send_keys(expiration_month_date)
    expiration_year = driver.find_elements_by_id('expdate_year')
    expiration_year.send_keys(expiration_year_date)
    csc = driver.find_elements_by_id('cvv2_number')
    csc.send_keys(csc_number)
    name_field = driver.find_elements_by_id('first_name')
    name_field.send_keys(first_name)
    last_name_field = driver.find_elements_by_id('last_name')
    last_name_field.send_keys(last_name)
    address_field = driver.find_elements_by_id('address1')
    address_field.send_keys(addresss_line)
    city_field = driver.find_elements_by_id('city')
    city_field.send_keys(city_name)
    phone_number_field = driver.find_elements_by_id('H_PhoneNumber')
    phone_number_field.send_keys(phone_number)
    email_field = driver.find_elements_by_id('email-address')
    email_field.send_keys(email)
    continue_button = driver.find_elements_by_id('submitBilling')
    continue_button.click()
    print '----- Top up organization balance process started -----'


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
    print 'Category selection'
    categories = driver.find_elements_by_class_name('appstore-template')
    for category in categories:
        if category.text == category_name:
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


def delete_resource(driver, resource_name, project_name, time_wait_after_resource_stopping,
                    time_wait_after_resource_removal):
    dashboard_field = driver.find_element_by_css_selector('[ui-sref="dashboard.index"]')
    dashboard_field.click()
    time.sleep(5)
    _go_to_project_page(driver, project_name)
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
        assert resource_name not in resource.text, 'Error: resource was not deleted, it still exists'


def create_provider_digitalocean(driver, provider_name, provider_type_name, token_name):
    print '----- Provider creation process started -----'
    print 'Go to organization page'
    _go_to_organization_details(driver)
    print 'Go to providers tab'
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
    token_name_field = driver.find_element_by_id('DigitalOcean_token')
    token_name_field.send_keys(token_name)
    print 'Click on add provider button'
    add_provider_button = driver.find_element_by_link_text('Add provider')
    add_provider_button.click()
    print '----- Provider creation process ended -----'


def create_provider_amazon(driver, provider_name, provider_type_name, access_key_id_name, secret_access_key_name):
    print '----- Provider creation process started -----'
    print 'Go to organization page'
    _go_to_organization_details(driver)
    print 'Go to providers tab'
    force_click(driver, css_selector='[visible="providers"]')
    print 'providers tab was successfully choosen'
    time.sleep(BaseSettings.click_time_wait)
    print 'Push button to create a provider'
    provider_creation = driver.find_element_by_xpath('//a[contains(@class, \'button\') and span[contains(text(), \'Create provider\')]]')
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
    access_key_id_name_field = driver.find_element_by_id('Amazon_username')
    access_key_id_name_field.send_keys(access_key_id_name)
    secret_access_key_name_field = driver.find_element_by_id('Amazon_token')
    secret_access_key_name_field.send_keys(secret_access_key_name)
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
    force_click(driver, xpath='//li[@visible="vms"]')
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
    application_creation = driver.find_element_by_xpath('//span[contains(text(), "Create")]')
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
    print 'Open application group actions'
    force_click(driver, css_selector='[ng-click="openActionsListTrigger()"]')
    print 'Click on remove button'
    remove_field = driver.find_element_by_link_text('Remove')
    remove_field.click()
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
    print 'Open application project actions'
    actions = driver.find_element_by_link_text('actions')
    actions.click()
    print 'Click on remove button'
    remove_field = driver.find_element_by_link_text('Remove')
    remove_field.click()
    _confirm_alert(driver, application_project_name)
    print '----- Application project deletion process ended -----'
