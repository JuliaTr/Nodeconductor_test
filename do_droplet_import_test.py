import time
import unittest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

import settings
from helpers import (login_nodeconductor, get_driver, create_project, delete_project, create_ssh_key, 
                    delete_ssh_key, choose_organization, create_resource, delete_resource, create_provider, 
                    import_resource, unlink_resource, delete_provider)


class Settings(object):
    site_url = "http://web-test.nodeconductor.com"
    username = 'Alice'
    password = 'Alice'
    user_full_name = 'Alice Lebowski'
    nec_organization = 'Ministry of Bells'
    project_name = 'DO test project'
    provider_name = 'DigitalOceanTest'
    resource_name = 'FFW3'


class NodeconductorTest(unittest.TestCase):

    def setUp(self):
        self.driver = get_driver(Settings.site_url)
        self.project_exists = False
        self.provider_exists = False
        self.resource_exists = False

    def test_create_delete_project_key_resource(self):
        print '%s is going to be loggedin.' % Settings.username
        login_nodeconductor(self.driver, Settings.username, Settings.password)
        time.sleep(10)
        # Identify necessary username on loaded main page
        username_idt_field = self.driver.find_element_by_class_name('user-name')
        assert username_idt_field.text == Settings.user_full_name, 'Error. Another username.'
        time.sleep(10)
        print '%s was loggedin successfully.' % Settings.username
        
        print 'Organization is going to be chosen.'
        choose_organization(self.driver, Settings.nec_organization)
        time.sleep(10)
        print 'Organization was chosen successfully.'
        
        print 'Project is going to be created.'
        create_project(self.driver, Settings.project_name)
        time.sleep(10)
        self.project_exists = True
        print 'Project was created successfully'
        
        print 'Provider is going to be created.'
        create_provider(self.driver, Settings.project_name, Settings.provider_name)
        self.provider_exists = True
        # time.sleep(10)        
        # try:
        #     self.driver.find_element_by_link_text(Settings.provider_name)
        # except NoSuchElementException:
        #     print 'I cannot find created provider, test fails.'
        # else:
        #     print 'Created provider is found. This is good.'  
        print 'Provider was created successfully.'
        time.sleep(10)
        
        print 'Resource is going to be imported.'
        import_resource(self.driver, Settings.project_name, Settings.provider_name, Settings.resource_name)
        self.resource_exists = True
        # time.sleep(10)
        # try:
        #     self.driver.find_element_by_link_text(Settings.resource_name)
        # except NoSuchElementException:
        #     print 'I cannot find imported resource, test fails.'
        # else:
        #     print 'Imported resource is found. This is good.'
        print 'Resource was imported successfully.'
        time.sleep(10)
        
        print 'Resource is going to be unlinked.'
        unlink_resource(self.driver, Settings.project_name, Settings.resource_name)
        time.sleep(10)
        # search_field = self.driver.find_element_by_css_selector('[ng-model="generalSearch"]')
        # search_field.clear()
        # search_field.send_keys(Settings.resource_name)
        # time.sleep(5)
        # try:
        #     self.driver.find_element_by_link_text(Settings.resource_name)
        # except NoSuchElementException:
        #     print 'I cannot find unlinked resource. This is good.'
        # else:
        #     print 'Unlinked resource is found, test fails.'
        self.resource_exists = False
        print 'Resource was unlinked successfully.'
       
    def tearDown(self):
        print 'Provider exists: ', self.provider_exists
        if self.provider_exists:
            try:
                print 'Provider is going to be removed.'
                time.sleep(10)
                self.driver.refresh()       
                delete_provider(self.driver, Settings.project_name, Settings.provider_name)
                self.provider_exists = False
                time.sleep(10)
                # search_field = self.driver.find_element_by_css_selector('[ng-model="generalSearch"]')
                # search_field.clear()
                # search_field.send_keys(Settings.provider_name)
                # time.sleep(5)
                # try:
                #     self.driver.find_element_by_link_text(Settings.provider_name)
                # except NoSuchElementException:
                #     print 'I cannot find removed provider. This is good.'
                # else:
                #     print 'Removed provider is found, test fails.'
            except Exception as e:
                print 'Provider cannot be removed. Error: %s' % e
        
        if self.project_exists:
            try:
                print 'Project is going to be removed.'
                delete_project(self.driver, Settings.project_name)
                self.project_exists = False
                # Check deletion
                # time.sleep(10)
                # list_of_projects_field = self.driver.find_element_by_class_name('object-list')

                # try:
                #     list_of_projects_field.find_element_by_link_text(Settings.project_name)
                # except NoSuchElementException:
                #     print 'I cannot find project. This is good.'
                # else:
                #     print 'Project is found, test fails.'
            except Exception as e:
                print 'Project cannot be deleted. Error: %s' % e       
        
        if self.resource_exists:
            print 'Warning! Test cannot unlink resource %s. It has to be unlinked manually.' % Settings.resource_name
        if self.provider_exists:
            print 'Warning! Test cannot delete provider %s. It has to be deleted manually.' % Settings.provider_name
        if self.project_exists:
            print 'Warning! Test cannot delete project %s. It has to be delete manually.' % Settings.project_name

        # # close browser
        # self.driver.quit()


if __name__ == "__main__":
    unittest.main()