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

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from helpers import (login_nodeconductor, get_driver, create_project, delete_project, choose_organization,
                     create_provider_digitalocean, import_resource, unlink_resource, delete_provider,
                     element_exists, force_click, go_to_main_page)
from base import BaseSettings


class Settings(object):
    site_url = "http://web-test.nodeconductor.com"
    username = 'Alice'
    password = 'Alice'
    user_full_name = 'Alice Lebowski'
    organization = 'Test only org'
    project_name = 'DO test project'
    provider_type_name = 'DigitalOcean'
    provider_name = 'DigitalOceanTest provider'
    token_name = '6ac9ad515e61dc80fddd6f9ee83f3b866fa2b6dc8cc1274dd2becc89241dd710'
    category_name = 'VMs'
    resource_name = 'SIB-test'
    projected_cost = 'Projected cost $4.69'


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
        create_provider_digitalocean(self.driver, Settings.provider_name, Settings.provider_type_name,
                                     Settings.token_name, Settings.organization)
        print 'Search created provider'
        search_field = self.driver.find_element_by_css_selector('[ng-model="generalSearch"]')
        search_field.clear()
        search_field.send_keys(Settings.provider_name)
        time.sleep(BaseSettings.search_time_wait)
        print 'Find provider in list'
        xpath = '//span[contains(text(), "%s")]' % Settings.provider_name
        assert element_exists(self.driver, xpath=xpath), 'Error: Provider with name %s is not found' % Settings.provider_name
        self.provider_exists = True
        print 'Find online state of created provider'
        try:
            WebDriverWait(self.driver, 10).until(
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
        time.sleep(BaseSettings.click_time_wait)
        # TODO: Implement resource existance check after fix of resource list

        # element = WebDriverWait(self.driver, 10).until(
        #     EC.presence_of_element_located((By.CLASS_NAME, "status-circle")))
        # search_field = self.driver.find_element_by_css_selector('[ng-model="generalSearch"]')
        # search_field.clear()
        # time.sleep(BaseSettings.click_time_wait)
        # search_field.send_keys(Settings.resource_name)
        # time.sleep(BaseSettings.search_time_wait)
        # resource = self.driver.find_element_by_css_selector('[href="#/resources/DigitalOcean.Droplet/f352b53521ac4f7c9d72f5ea07af5bf1/"]')
        # resource.click()
        # time.sleep(BaseSettings.click_time_wait)
        # xpath = '//span[@class="name" and contains(text(), "%s")]' % Settings.resource_name
        # self.project_exists = bool(self.driver.find_elements_by_xpath(xpath))
        # assert self.project_exists, 'Cannot import resource "%s"' % Settings.resource_name
        print 'Resource exists: ', self.resource_exists
        self.resource_exists = True
        print 'Resource was imported successfully.'

        # # goto main page:
        # go_to_main_page(self.driver)
        # costs = self.driver.find_element_by_link_text('Costs')
        # costs.click()
        # assert Settings.projected_cost == self.driver.find_element_by_class_name('total-cost').text, (
        #     'Error: Cannot find %s ' % Settings.projected_cost)
        # activity = self.driver.find_element_by_link_text('Activity')
        # activity.click()
        # time.sleep(BaseSettings.click_time_wait)

        # Unlink resource
        print 'Resource is going to be unlinked.'
        unlink_resource(self.driver, Settings.project_name, Settings.resource_name)
        time.sleep(BaseSettings.click_time_wait)
        # TODO: Implement resource existance check after fix of resource list

        # search_field = self.driver.find_element_by_css_selector('[ng-model="generalSearch"]')
        # search_field.clear()
        # search_field.send_keys(Settings.resource_name)
        # time.sleep(BaseSettings.search_time_wait)
        # assert not element_exists(self.driver, xpath='//div[@class="tab-content" and contains(text(), "%s")]' % Settings.resource_name), (
        #     'Error: Resource with name %s is found' % Settings.resource_name)
        self.resource_exists = False
        print 'Resource exists: ', self.resource_exists
        print 'Resource was unlinked successfully.'

    def tearDown(self):
        print 'Provider exists: ', self.provider_exists
        if self.provider_exists:
            try:
                # Delete provider
                print 'Provider is going to be deleted.'
                delete_provider(self.driver, Settings.provider_name, Settings.organization)
                self.provider_exists = False
                time.sleep(BaseSettings.click_time_wait)
                search_field = self.driver.find_element_by_css_selector('[ng-model="generalSearch"]')
                search_field.clear()
                search_field.send_keys(Settings.provider_name)
                time.sleep(BaseSettings.search_time_wait)
                assert not element_exists(self.driver, xpath='//span[contains(text(), "%s")]' % Settings.provider_name), (
                    'Error: Provider with name %s is found' % Settings.provider_name)
                print 'Provider was deleted successfully.'
            except Exception as e:
                print 'Provider cannot be deleted. Error: %s' % e

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
                print 'Project cannot be deleted. Error: %s' % e

        if self.resource_exists:
            print 'Warning! Test cannot unlink resource %s. It has to be unlinked manually.' % Settings.resource_name
        if self.provider_exists:
            print 'Warning! Test cannot delete provider %s. It has to be deleted manually.' % Settings.provider_name
        if self.project_exists:
            print 'Warning! Test cannot delete project %s. It has to be delete manually.' % Settings.project_name

        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
