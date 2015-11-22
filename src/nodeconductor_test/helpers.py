import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException


# deprecated - do not use this function. It has to be replaced with exement exists checks in tests.
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

    username_field = driver.find_element_by_css_selector('[ng-model="auth.user.username"]')
    username_field.send_keys(username)
    password_field = driver.find_element_by_css_selector('[ng-model="auth.user.password"]')
    password_field.send_keys(password)
    login_field = driver.find_element_by_class_name('button-login')
    login_field.click()


def choose_organization(driver, organization):
    organization_field = driver.find_element_by_css_selector('ul.nav-list span.customer-name')
    organization_field.click()
    organization = driver.find_element_by_link_text(organization)
    organization.click()

    dashboard_field = driver.find_element_by_css_selector('[ui-sref="dashboard.index"]')
    dashboard_field.click()


def create_project(driver, project_name, project_description=''):
    add_new_project_field = driver.find_element_by_class_name('button-apply')
    add_new_project_field.click()

    project_name_field = driver.find_element_by_css_selector('[ng-model="ProjectAdd.project.name"]')
    project_name_field.send_keys(project_name)
    if project_description:
        project_description_field = driver.find_element_by_css_selector('[ng-model="ProjectAdd.project.description"]')
        project_description_field.send_keys(project_description)
    create_project_field = driver.find_element_by_class_name('button-apply')
    create_project_field.click()

    back_to_list_field = driver.find_element_by_class_name('back-to-list')
    back_to_list_field.click()


def delete_project(driver, project_name):
    dashboard_field = driver.find_element_by_css_selector('[ui-sref="dashboard.index"]')
    dashboard_field.click()

    projects = driver.find_element_by_link_text(project_name)
    projects.click()

    back_to_list_field = driver.find_element_by_class_name('back-to-list')
    back_to_list_field.click()

    project_search_field = driver.find_element_by_css_selector('[ng-model="generalSearch"]')
    project_search_field.send_keys(project_name)

    actions_field = driver.find_element_by_link_text('actions')
    actions_field.click()
    remove_field = driver.find_element_by_link_text('Remove')
    remove_field.click()

    alert = driver.switch_to_alert()
    alert.accept()


def create_ssh_key(driver, user_full_name, key_name):
    user_field = driver.find_element_by_link_text(user_full_name)
    user_field.click()
    profile_field = driver.find_element_by_link_text('Profile')
    profile_field.click()

    keys = driver.find_element_by_css_selector('[visible="keys"]')
    keys.click()

    keys_field = driver.find_element_by_link_text('Add SSH Key')
    keys_field.click()

    key_name_field = driver.find_element_by_css_selector('[ng-model="KeyAdd.instance.name"]')
    key_name_field.send_keys(key_name)
    public_key_field = driver.find_element_by_css_selector('[ng-model="KeyAdd.instance.public_key"]')
    public_key_field.send_keys(
        'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC/TUNt44JCGCtRyGL/7hb+98YRkZesFRjIdgNtIBwmJ0W1Ikqa3sMn'
        '+Oho4I8+jFEGppLPN3UAZEU+KxnrPNCGfClSWeij9BJWDBmWzAikLFnyYUvJ99Exx3cv/YdYU1PynhwOf0oxpcwi025t'
        'chlYlSPX56e9U4o7q9gR0mkbAUfZN27VaZL7AVe8TXTqYaF8Zg8pB+ru0u0M5xaqTY6nLqps/LClePXKx3HdKVw5wEOf'
        'YNSdqWUFUHr4L7poe1hgzk4M0ZVMVGTXxs7FlUhOb6RxkvgmNC/saU3PWhAQK777iIMmA1OPr2QJkooIYEw4i4crCULy'
        'U9Bm1ehDsvuB marchukpavelp@gmail.com')

    add_key_field = driver.find_element_by_class_name('button-apply')
    add_key_field.click()


def delete_ssh_key(driver, key_name, user_full_name):
    dashboard_field = driver.find_element_by_css_selector('[ui-sref="dashboard.index"]')
    dashboard_field.click()

    user_field = driver.find_element_by_link_text(user_full_name)
    user_field.click()
    profile_field = driver.find_element_by_link_text('Profile')
    profile_field.click()

    keys = driver.find_element_by_css_selector('[visible="keys"]')
    keys.click()

    ssh_search_field = driver.find_element_by_css_selector('[ng-model="generalSearch"]')
    ssh_search_field.send_keys(key_name)

    ssh_key_remove_field = driver.find_element_by_link_text('Remove')
    ssh_key_remove_field.click()

    alert = driver.switch_to_alert()
    alert.accept()


def create_resource_openstack(driver, project_name, resource_name, category_name, provider_name_in_resource,
                              image_name, flavor_name, public_key_name):
    dashboard_field = driver.find_element_by_css_selector('[ui-sref="dashboard.index"]')
    dashboard_field.click()

    project = driver.find_element_by_link_text(project_name)
    project.click()

    vms = driver.find_element_by_css_selector('[visible="vms"]')
    vms.click()

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


def create_resource_azure(driver, project_name, resource_name, category_name, provider_name, image_name,
                          username, os_password, size_name):
    dashboard_field = driver.find_element_by_css_selector('[ui-sref="dashboard.index"]')
    dashboard_field.click()

    project = driver.find_element_by_link_text(project_name)
    project.click()

    vms = driver.find_element_by_css_selector('[visible="vms"]')
    vms.click()

    resource_vms_creation = driver.find_element_by_link_text('Create')
    resource_vms_creation.click()

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

    project = driver.find_element_by_link_text(project_name)
    project.click()

    vms = driver.find_element_by_css_selector('[visible="vms"]')
    vms.click()

    resource_search_field = driver.find_element_by_css_selector('[ng-model="generalSearch"]')
    resource_search_field.send_keys(resource_name)

    resource_list = driver.find_elements_by_class_name('list-box')
    for resource in resource_list:
        assert 'Online' in resource.text, 'Error: cannot stop resource that is not online or does not exist'

    actions = driver.find_element_by_link_text('actions')
    actions.click()
    stop_field = driver.find_element_by_link_text('Stop')
    stop_field.click()
    time.sleep(time_wait_after_resource_stopping)
    driver.refresh()

    vms = driver.find_element_by_css_selector('[visible="vms"]')
    vms.click()

    resource_field = driver.find_element_by_css_selector('[ng-model="generalSearch"]')
    resource_field.send_keys(resource_name)

    resource_list = driver.find_elements_by_class_name('list-box')
    for state in resource_list:
        assert 'Offline' in state.text, ('Error: cannot delete resource that is not offline, '
                                         'was not stopped, or does not exist')

    actions = driver.find_element_by_link_text('actions')
    actions.click()
    remove_field = driver.find_element_by_link_text('Remove')
    remove_field.click()
    alert = driver.switch_to_alert()
    alert.accept()
    time.sleep(time_wait_after_resource_removal)
    driver.refresh()

    vms = driver.find_element_by_css_selector('[visible="vms"]')
    vms.click()

    resource_field = driver.find_element_by_css_selector('[ng-model="generalSearch"]')
    resource_field.send_keys(resource_name)

    resource_list = driver.find_elements_by_class_name('list-box')
    for resource in resource_list:
        assert resource_name not in resource.text, 'Error: resource was not deleted, it still exists'


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


def create_provider_digitalocean(driver, provider_name, provider_type_name, token_name, organization):
    organization_field = driver.find_element_by_xpath(
        '//span[contains(@class, "customer-name") and contains(text(), "%s")]' % organization)
    organization_field.click()

    organization_details = driver.find_element_by_link_text('Details')
    organization_details.click()

    force_click(driver, css_selector='[visible="providers"]')
    print 'providers tab was successfully created'

    time.sleep(2)  # something is wrong with "create provider" button - it is not clickable for short period of time
    provider_creation = driver.find_element_by_link_text('Create provider')
    provider_creation.click()
    print 'I should be on provider creation page'

    provider_type = driver.find_element_by_class_name(provider_type_name)
    provider_type.click()

    provider_name_field = driver.find_element_by_css_selector('[ng-model="ServiceAdd.model.serviceName"]')
    provider_name_field.clear()
    provider_name_field.send_keys(provider_name)
    token_name_field = driver.find_element_by_id('DigitalOcean_token')
    token_name_field.send_keys(token_name)
    add_provider_button = driver.find_element_by_link_text('Add provider')
    add_provider_button.click()


# Method isn't completed yet.
# TODO: Add certificate.
def create_provider_azure(driver, provider_name, provider_type_name, subscription_id_name):
    organization_field = driver.find_element_by_css_selector('ul.nav-list span.customer-name')
    organization_field.click()

    organization_details = driver.find_element_by_link_text('Details')
    organization_details.click()

    providers = driver.find_element_by_css_selector('[visible="providers"]')
    providers.click()

    provider_creation = driver.find_element_by_link_text('Create provider')
    provider_creation.click()

    provider_type = driver.find_element_by_class_name(provider_type_name)
    provider_type.click()

    provider_name_field = driver.find_element_by_css_selector('[ng-model="ServiceAdd.model.serviceName"]')
    provider_name_field.clear()
    provider_name_field.send_keys(provider_name)
    token_name_field = driver.find_element_by_id('Azure_username')
    token_name_field.send_keys(subscription_id_name)
    upload_file = driver.find_element_by_link_text('Browse')
    upload_file.click()

    # TODO: Add certificate.
    add_provider_button = driver.find_element_by_link_text('Add provider')
    add_provider_button.click()


def import_resource(driver, project_name, provider_name, resource_name):
    dashboard_field = driver.find_element_by_css_selector('[ui-sref="dashboard.index"]')
    dashboard_field.click()

    project = driver.find_element_by_link_text(project_name)
    project.click()

    vms = driver.find_element_by_css_selector('[visible="vms"]')
    vms.click()

    resource_import = driver.find_element_by_link_text('Import')
    resource_import.click()

    category_list = driver.find_elements_by_class_name('appstore-template')
    for category in category_list:
        if category.text == 'VMs':
            category.click()
            break

    provider_list = driver.find_elements_by_class_name('appstore-template')
    for provider in provider_list:
        if provider.text == provider_name:
            provider.click()
            break

    resource = driver.find_element_by_link_text(resource_name)
    resource.click()

    import_button = driver.find_element_by_link_text('Import')
    import_button.click()


def unlink_resource(driver, project_name, resource_name):
    dashboard_field = driver.find_element_by_css_selector('[ui-sref="dashboard.index"]')
    dashboard_field.click()

    project = driver.find_element_by_link_text(project_name)
    project.click()

    vms = driver.find_element_by_css_selector('[visible="vms"]')
    vms.click()

    resource_search_field = driver.find_element_by_css_selector('[ng-model="generalSearch"]')
    resource_search_field.send_keys(resource_name)

    actions = driver.find_element_by_link_text('actions')
    actions.click()
    actions_dropdown = driver.find_element_by_class_name('actions-dropdown')
    unlink_field = actions_dropdown.find_element_by_link_text('Unlink')
    unlink_field.click()


def delete_provider(driver, provider_name):
    organization_field = driver.find_element_by_css_selector('ul.nav-list span.customer-name')
    organization_field.click()

    organization_details = driver.find_element_by_link_text('Details')
    organization_details.click()

    providers = driver.find_element_by_css_selector('[visible="providers"]')
    providers.click()

    provider_search_field = driver.find_element_by_css_selector('[ng-model="generalSearch"]')
    provider_search_field.send_keys(provider_name)

    remove_provider = driver.find_element_by_link_text('Delete')
    remove_provider.click()

    alert = driver.switch_to_alert()
    alert.accept()


def create_application(driver, project_name, category_name, resource_type_name, path_name, application_name):
    dashboard_field = driver.find_element_by_css_selector('[ui-sref="dashboard.index"]')
    dashboard_field.click()

    project = driver.find_element_by_link_text(project_name)
    project.click()

    vms = driver.find_element_by_css_selector('[visible="applications"]')
    vms.click()

    provider_creation = driver.find_element_by_link_text('Create')
    provider_creation.click()

    categories = driver.find_elements_by_class_name('appstore-template')
    for category in categories:
        if category.text == category_name:
            category.click()
            break

    resource_types = driver.find_elements_by_class_name('appstore-template')
    for resource_type in resource_types:
        if resource_type.text == resource_type_name:
            resource_type.click()
            break

    path_field = driver.find_element_by_css_selector('[ng-if="field.name !== \'password\'"]')
    path_field.send_keys(path_name)

    application_name_field = driver.find_element_by_id('name')
    application_name_field.send_keys(application_name)

    purchase = driver.find_element_by_css_selector('[submit-button="AppStore.save()"]')
    purchase.click()


def delete_application(driver, project_name, time_wait_after_resource_removal, application_name):
    dashboard_field = driver.find_element_by_css_selector('[ui-sref="dashboard.index"]')
    dashboard_field.click()

    project = driver.find_element_by_link_text(project_name)
    project.click()

    applications = driver.find_element_by_css_selector('[visible="applications"]')
    applications.click()

    resource_search_field = driver.find_element_by_css_selector('[ng-model="generalSearch"]')
    resource_search_field.send_keys(application_name)

    actions = driver.find_element_by_link_text('actions')
    actions.click()
    remove_field = driver.find_element_by_link_text('Remove')
    remove_field.click()
    alert = driver.switch_to_alert()
    alert.accept()
    time.sleep(time_wait_after_resource_removal)
    driver.refresh()

    applications = driver.find_element_by_css_selector('[visible="applications"]')
    applications.click()

    resource_field = driver.find_element_by_css_selector('[ng-model="generalSearch"]')
    resource_field.send_keys(application_name)

    application_list = driver.find_elements_by_class_name('list-box')
    for application in application_list:
        assert application_name not in application.text, 'Error: application was not deleted, it still exists'
