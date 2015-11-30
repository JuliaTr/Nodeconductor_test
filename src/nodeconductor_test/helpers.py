import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import urlparse

from base import BaseSettings


def go_to_main_page(driver):
    split = urlparse.urlsplit(driver.current_url)
    driver.get('%s://%s/' % (split.scheme, split.netloc))


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


def force_click(driver, css_selector=None, tries_left=3):
    """ Tries to get element and click on it several times. """
    try:
        element = driver.find_element_by_css_selector(css_selector)
        element.click()
    except StaleElementReferenceException as e:
        tries_left -= 1
        if tries_left > 0:
            force_click(driver, css_selector=css_selector, tries_left=tries_left)
        else:
            raise e


def get_driver(site_url):
    driver = webdriver.Firefox()
    driver.maximize_window()
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
    print 'Go to projects tab'
    projects = driver.find_element_by_link_text(project_name)
    projects.click()
    time.sleep(BaseSettings.click_time_wait)
    print 'Go to list of projects page'
    back_to_list_field = driver.find_element_by_class_name('back-to-list')
    back_to_list_field.click()
    time.sleep(BaseSettings.click_time_wait)
    print 'Put project name to search field'
    project_search_field = driver.find_element_by_css_selector('[ng-model="generalSearch"]')
    project_search_field.send_keys(project_name)
    time.sleep(BaseSettings.search_time_wait)
    print 'Open project actions'
    force_click(driver, css_selector='[ng-click="openActionsListTrigger()"]')
    print 'Click on remove button'
    remove_field = driver.find_element_by_link_text('Remove')
    remove_field.click()
    print 'Accept project delete confirmation popup'
    alert = driver.switch_to_alert()
    alert.accept()
    print '----- Project deletion process ended -----'


def create_ssh_key(driver, user_full_name, key_name):
    user_field = driver.find_element_by_link_text(user_full_name)
    user_field.click()
    profile_field = driver.find_element_by_link_text('Profile')
    profile_field.click()
    time.sleep(10)
    keys = driver.find_element_by_css_selector('[visible="keys"]')
    keys.click()
    time.sleep(15)
    keys_field = driver.find_element_by_link_text('Add SSH Key')
    keys_field.click()
    time.sleep(15)
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
    project = driver.find_element_by_link_text(project_name)
    project.click()

    vms = driver.find_element_by_css_selector('[visible="vms"]')
    vms.click()
    time.sleep(BaseSettings.click_time_wait)
    resource_vms_creation = driver.find_element_by_link_text('Create')
    resource_vms_creation.click()

    categories = driver.find_elements_by_class_name('appstore-template')
    for category in categories:
        if category.text == category_name:
            category.click()
            break

    providers = driver.find_elements_by_class_name('appstore-template')
    for provider in providers:
        if provider.text == provider_name_in_resource:
            provider.click()
            break

    resource_name_field = driver.find_element_by_css_selector('[ng-model="AppStore.instance[field.name]"]')
    resource_name_field.send_keys(resource_name)

    images = driver.find_elements_by_class_name('appstore-template-image')
    for image in images:
        if image.text == image_name:
            image.click()
            break

    flavors = driver.find_elements_by_class_name('title')
    for flavor in flavors:
        if flavor.text == flavor_name:
            flavor.click()
            break

    public_keys = driver.find_elements_by_class_name('description-ssh_public_key')
    for public_key in public_keys:
        if public_key.text == public_key_name:
            public_key.click()
            break

    purchase = driver.find_element_by_css_selector('[submit-button="AppStore.save()"]')
    purchase.click()


# To use this function it is necessary to be already on dashboard
def create_resource_azure(driver, project_name, resource_name, category_name, provider_name, image_name,
                          username, os_password, size_name):
    project = driver.find_element_by_link_text(project_name)
    project.click()
    # time.sleep(BaseSettings.click_time_wait)
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
        assert resource_name not in resource.text, 'Error: resource was not deleted, it still exists'


def create_provider_digitalocean(driver, provider_name, provider_type_name, token_name, organization):
    print '----- Provider creation process started -----'
    print 'Go to organization page'
    organization_field = driver.find_element_by_xpath(
        '//span[contains(@class, "customer-name") and contains(text(), "%s")]' % organization)
    organization_field.click()
    organization_details = driver.find_element_by_link_text('Details')
    organization_details.click()
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
    print 'Give provider a name'
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


# Method isn't completed yet.
# TODO: Add certificate.
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
    # TODO: Add certificate.
    add_provider_button = driver.find_element_by_link_text('Add provider')
    add_provider_button.click()


def import_resource(driver, project_name, provider_name, category_name, resource_name):
    print '----- Resource import process started -----'
    go_to_main_page(driver)
    print 'Go to project page'
    project = driver.find_element_by_link_text(project_name)
    project.click()
    print 'Go to resource tab'
    vms = driver.find_element_by_css_selector('[visible="vms"]')
    vms.click()
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
    print 'Put resource name'
    resource = driver.find_element_by_link_text(resource_name)
    resource.click()
    print 'Click on import button'
    import_button = driver.find_element_by_link_text('Import')
    import_button.click()
    print '----- Resource import process ended -----'


def unlink_resource(driver, project_name, resource_name):
    print '----- Resource unlink process started -----'
    go_to_main_page(driver)
    print 'Go to project page'
    project = driver.find_element_by_link_text(project_name)
    project.click()
    print 'Go to resource tab'
    vms = driver.find_element_by_css_selector('[visible="vms"]')
    vms.click()
    time.sleep(BaseSettings.click_time_wait)
    print 'Put resource name to search field'
    resource_search_field = driver.find_element_by_css_selector('[ng-model="generalSearch"]')
    resource_search_field.send_keys(resource_name)
    time.sleep(BaseSettings.search_time_wait)
    print 'Open project actions'
    force_click(driver, css_selector='[ng-click="openActionsListTrigger()"]')
    print 'Click on remove button'
    unlink_field = driver.find_element_by_link_text('Unlink')
    unlink_field.click()
    print '----- Resource unlink process ended -----'


def delete_provider(driver, provider_name, organization):
    print '----- Provider deletion process started -----'
    print 'Go to organization page'
    organization_field = driver.find_element_by_xpath(
        '//span[contains(@class, "customer-name") and contains(text(), "%s")]' % organization)
    organization_field.click()
    organization_details = driver.find_element_by_link_text('Details')
    organization_details.click()
    print 'Go to providers tab'
    force_click(driver, css_selector='[visible="providers"]')
    print 'Providers tab was successfully choosen'
    time.sleep(BaseSettings.click_time_wait)
    print 'Put provider name to search field'
    provider_search_field = driver.find_element_by_css_selector('[ng-model="generalSearch"]')
    provider_search_field.send_keys(provider_name)
    time.sleep(BaseSettings.search_time_wait)
    print 'Click on delete button'
    force_click(driver, css_selector='[ng-class="{\'disabled\': button.isDisabled(buttonModel)}"]')
    print 'Accept project delete confirmation popup'
    alert = driver.switch_to_alert()
    alert.accept()
    print '----- Provider deletion process ended -----'


def create_application_group(driver, project_name, category_name, resource_type_name, path_name, application_name_for_group):
    dashboard_field = driver.find_element_by_css_selector('[ui-sref="dashboard.index"]')
    dashboard_field.click()
    time.sleep(15)
    project = driver.find_element_by_link_text(project_name)
    project.click()
    time.sleep(10)
    vms = driver.find_element_by_css_selector('[visible="applications"]')
    vms.click()
    time.sleep(5)
    provider_creation = driver.find_element_by_link_text('Create')
    provider_creation.click()
    time.sleep(5)
    categories = driver.find_elements_by_class_name('appstore-template')
    for category in categories:
        if category.text == category_name:
            category.click()
            break
    time.sleep(5)
    resource_types = driver.find_elements_by_class_name('appstore-template')
    for resource_type in resource_types:
        if resource_type.text == resource_type_name:
            resource_type.click()
            break
    time.sleep(5)
    path_field = driver.find_element_by_css_selector('[ng-if="field.name !== \'password\'"]')
    path_field.send_keys(path_name)
    time.sleep(5)
    application_name_field = driver.find_element_by_id('name')
    application_name_field.send_keys(application_name_for_group)
    time.sleep(5)
    purchase = driver.find_element_by_css_selector('[submit-button="AppStore.save()"]')
    purchase.click()


def create_application_project(driver, project_name, category_name, resource_type_name1, application_name_for_project, visibility_level_name):
    dashboard_field = driver.find_element_by_css_selector('[ui-sref="dashboard.index"]')
    dashboard_field.click()
    time.sleep(15)
    project = driver.find_element_by_link_text(project_name)
    project.click()
    time.sleep(10)
    vms = driver.find_element_by_css_selector('[visible="applications"]')
    vms.click()
    time.sleep(5)
    provider_creation = driver.find_element_by_link_text('Create')
    provider_creation.click()
    time.sleep(5)
    categories = driver.find_elements_by_class_name('appstore-template')
    for category in categories:
        if category.text == category_name:
            category.click()
            break
    time.sleep(5)
    resource_types = driver.find_elements_by_class_name('appstore-template')
    for resource_type in resource_types:
        if resource_type.text == resource_type_name1:
            resource_type.click()
            break
    time.sleep(5)
    visibility_levels = driver.find_elements_by_class_name('appstore-template')
    for visibility_level in visibility_levels:
        if visibility_level.text == visibility_level_name:
            visibility_level.click()
            break
    time.sleep(5)
    application_name_field = driver.find_element_by_id('name')
    application_name_field.send_keys(application_name_for_project)
    time.sleep(5)
    purchase = driver.find_element_by_css_selector('[submit-button="AppStore.save()"]')
    purchase.click()


def delete_application_group(driver, project_name, time_wait_after_resource_removal, application_name_for_group):
    dashboard_field = driver.find_element_by_css_selector('[ui-sref="dashboard.index"]')
    dashboard_field.click()
    time.sleep(5)
    project = driver.find_element_by_link_text(project_name)
    project.click()
    time.sleep(5)
    applications = driver.find_element_by_css_selector('[visible="applications"]')
    applications.click()
    time.sleep(5)
    resource_search_field = driver.find_element_by_css_selector('[ng-model="generalSearch"]')
    resource_search_field.send_keys(application_name_for_group)
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
    applications = driver.find_element_by_css_selector('[visible="applications"]')
    applications.click()
    time.sleep(5)
    resource_field = driver.find_element_by_css_selector('[ng-model="generalSearch"]')
    resource_field.send_keys(application_name_for_group)
    time.sleep(5)
    application_list = driver.find_elements_by_class_name('list-box')
    for application in application_list:
        assert application_name_for_group not in application.text, 'Error: application was not deleted, it still exists'


def delete_application_project(driver, project_name, time_wait_after_resource_removal, application_name_for_project):
    dashboard_field = driver.find_element_by_css_selector('[ui-sref="dashboard.index"]')
    dashboard_field.click()
    time.sleep(5)
    project = driver.find_element_by_link_text(project_name)
    project.click()
    time.sleep(5)
    applications = driver.find_element_by_css_selector('[visible="applications"]')
    applications.click()
    time.sleep(5)
    resource_search_field = driver.find_element_by_css_selector('[ng-model="generalSearch"]')
    resource_search_field.send_keys(application_name_for_project)
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
    applications = driver.find_element_by_css_selector('[visible="applications"]')
    applications.click()
    time.sleep(5)
    resource_field = driver.find_element_by_css_selector('[ng-model="generalSearch"]')
    resource_field.send_keys(application_name_for_project)
    time.sleep(5)
    application_list = driver.find_elements_by_class_name('list-box')
    for application in application_list:
        assert application_name_for_project not in application.text, 'Error: application was not deleted, it still exists'
