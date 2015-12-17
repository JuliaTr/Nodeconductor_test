"""
1. Login NC
2. Choose organization
3. Create project
4. Create provider
5. Import resource
6. Unlink resource
7. Delete provider
8. Delete project
"""


import time
import unittest
import sys

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from helpers import (login_nodeconductor, get_driver, create_project, delete_project, choose_organization,
                     create_provider_amazon, import_resource, unlink_resource, delete_provider,
                     element_exists, go_to_main_page, make_screenshot)
from base import BaseSettings


class Settings(object):
    site_url = "http://web-test.nodeconductor.com"
    username = 'Alice'
    password = 'Alice'
    user_full_name = 'Alice Lebowski'
    organization = 'Test only org'
    project_name = 'Amazon test project'
    provider_type_name = 'Amazon'
    provider_name = 'AmazonTest provider'
    access_key_id_name = 'AKIAIHOQGSGNVO6SYFWA'
    secret_access_key_name = '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'
    category_name = 'VMs'
    resource_name = 'old.opennodecloud.com'
    resource_cost = '$9.67'


class NodeconductorTest(unittest.TestCase):

    def setUp(self):
        self.driver = get_driver(Settings.site_url)
        self.project_exists = False
        self.provider_exists = False
        self.resource_exists = False
        self.driver.implicitly_wait(BaseSettings.implicitly_wait)

    def test_create_delete_project_provider_resource(self):
        # Login NC
        print '%s is going to be loggedin.' % Settings.username
        login_nodeconductor(self.driver, Settings.username, Settings.password)
        username_idt_field = self.driver.find_element_by_class_name('user-name')
        assert username_idt_field.text == Settings.user_full_name, 'Error. Another username.'
        print '%s was loggedin successfully.' % Settings.username

        # Choose organization
        print 'Organization is going to be chosen.'
        choose_organization(self.driver, Settings.organization)
        print 'Organization was chosen successfully.'

        # Create project
        print 'Project is going to be created.'
        create_project(self.driver, Settings.project_name)
        time.sleep(BaseSettings.click_time_wait)
        xpath = '//span[@class="name" and contains(text(), "%s")]' % Settings.project_name
        assert bool(self.driver.find_elements_by_xpath(xpath)), 'Cannot create project "%s"' % Settings.project_name
        self.project_exists = True
        print 'Project was created successfully.'

        # Create provider
        print 'Provider is going to be created.'
        create_provider_amazon(self.driver, Settings.provider_name, Settings.provider_type_name,
                               Settings.access_key_id_name, Settings.secret_access_key_name)
        print 'Search created provider'
        search_field = self.driver.find_element_by_css_selector('[ng-model="generalSearch"]')
        search_field.clear()
        search_field.send_keys(Settings.provider_name)
        time.sleep(BaseSettings.search_time_wait)
        print 'Find provider in list'
        xpath = '//span[contains(text(), "%s")]' % Settings.provider_name
        assert element_exists(self.driver, xpath=xpath), 'Error: Provider with name "%s" is not found' % Settings.provider_name
        self.provider_exists = True
        print 'Find online state of created provider'
        try:
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".status-circle.online")))
        except TimeoutException as e:
            print 'Error: Provider is not online'
            raise e
        else:
            print 'Provider is in online status'
        print 'Provider was created successfully.'

        # Import resource
        print 'Resource is going to be imported.'
        import_resource(self.driver, Settings.project_name, Settings.provider_name, Settings.category_name,
                        Settings.resource_name)
        print 'Search imported resource'
        search_field = self.driver.find_element_by_css_selector('[ng-model="generalSearch"]')
        search_field.clear()
        search_field.send_keys(Settings.resource_name)
        time.sleep(BaseSettings.search_time_wait)
        print 'Go to resource page'
        resource = self.driver.find_element_by_link_text(Settings.resource_name)
        resource.click()
        time.sleep(BaseSettings.click_time_wait)
        print 'Check imported resource existence'
        xpath = '//span[@class="name" and contains(text(), "%s")]' % Settings.resource_name
        assert bool(self.driver.find_elements_by_xpath(xpath)), 'Cannot import resource "%s"' % Settings.resource_name
        self.resource_exists = True
        print 'Resource exists: ', self.resource_exists
        print 'Check imported resource state'
        xpath = '//dd[contains(text(), "Online")]'
        assert bool(self.driver.find_elements_by_xpath(xpath)), 'Error: Imported resource "%s" is not online.' % Settings.resource_name
        print 'Imported resource is in online state'
        print 'Resource was imported successfully.'

        print '----- Cost is going to be checked----- '
        go_to_main_page(self.driver)
        costs = self.driver.find_element_by_link_text('Costs')
        costs.click()
        time.sleep(BaseSettings.click_time_wait)
        print 'Select resources tab'
        resources_list = self.driver.find_element_by_css_selector('[ng-class="{\'active\': row.selected && row.activeTab==\'resources\'}"]')
        resources_list.click()
        time.sleep(BaseSettings.click_time_wait)
        print 'Find row with the resource in a resource table'
        rows_list = self.driver.find_elements_by_css_selector('[ng-repeat="resource in row.resources"]')
        resource_cost_exists = False
        for row in rows_list:
            if Settings.resource_name in row.text:
                assert Settings.resource_cost in row.text, 'Error: Cannot find resource cost "%s" ' % Settings.resource_cost
                resource_cost_exists = True
                print 'Resource cost "%s" was found on page' % Settings.resource_cost
        assert resource_cost_exists, 'Error: Cannot find resource with name "%s" to check cost' % Settings.resource_name
        time.sleep(BaseSettings.click_time_wait)
        print '----- Cost was checked successfully----- '

        # Unlink resource
        print 'Resource is going to be unlinked.'
        unlink_resource(self.driver, Settings.project_name, Settings.resource_name)
        print 'Search imported resource'
        search_field = self.driver.find_element_by_css_selector('[ng-model="generalSearch"]')
        search_field.clear()
        search_field.send_keys(Settings.resource_name)
        time.sleep(BaseSettings.search_time_wait)
        print 'Check unlinked resource existence'
        assert not element_exists(self.driver, xpath='//a[contains(text(), "%s")]' % Settings.resource_name), (
            'Error: Resource with name "%s" was not unlinked, it still exists' % Settings.resource_name)
        self.resource_exists = False
        print 'Resource exists: ', self.resource_exists
        print 'Resource was unlinked successfully.'

    def tearDown(self):
        print '\n\n\n --- TEARDOWN ---'
        if sys.exc_info()[0] is not None:
            make_screenshot(self.driver)
        print 'Provider exists: ', self.provider_exists
        if self.provider_exists:
            try:
                # Delete provider
                print 'Provider is going to be deleted.'
                delete_provider(self.driver, Settings.provider_name)
                self.provider_exists = False
                time.sleep(BaseSettings.click_time_wait)
                search_field = self.driver.find_element_by_css_selector('[ng-model="generalSearch"]')
                search_field.clear()
                search_field.send_keys(Settings.provider_name)
                time.sleep(BaseSettings.search_time_wait)
                assert not element_exists(self.driver, xpath='//span[contains(text(), "%s")]' % Settings.provider_name), (
                    'Error: Provider with name "%s" was not deleted, it still exists' % Settings.provider_name)
                print 'Provider was deleted successfully.'
            except Exception as e:
                print 'Provider cannot be deleted. Error: "%s"' % e

        if self.project_exists:
            try:
                # Delete project
                print 'Project is going to be deleted.'
                delete_project(self.driver, Settings.project_name)
                self.project_exists = False
                time.sleep(BaseSettings.click_time_wait)
                search_field = self.driver.find_element_by_css_selector('[ng-model="generalSearch"]')
                search_field.clear()
                search_field.send_keys(Settings.project_name)
                time.sleep(BaseSettings.search_time_wait)
                if element_exists(self.driver, xpath='//a[contains(text(), "%s")]' % Settings.project_name):
                    self.project_exists = True
                print 'Project was deleted successfully.'
            except Exception as e:
                print 'Project cannot be deleted. Error: "%s"' % e

        if self.resource_exists:
            print 'Warning! Test cannot unlink resource "%s". It has to be unlinked manually.' % Settings.resource_name
        if self.provider_exists:
            print 'Warning! Test cannot delete provider "%s". It has to be deleted manually.' % Settings.provider_name
        if self.project_exists:
            print 'Warning! Test cannot delete project "%s". It has to be delete manually.' % Settings.project_name

        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
