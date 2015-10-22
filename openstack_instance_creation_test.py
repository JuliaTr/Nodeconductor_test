import time
import unittest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

import settings
from helpers import (login_nodeconductor, get_driver, create_project, 
                    delete_project, create_ssh_key, delete_ssh_key, 
                    choose_organization, create_resource, delete_resource)


class Settings(object):
    site_url = "http://web-test.nodeconductor.com"
    username = 'Alice'
    password = 'Alice'
    user_full_name = 'Alice Lebowski'
    nec_organization = 'Ministry of Bells'
    project_name = 'OpenStack test project'
    key_name = 'Openstack test key'
    resource_name = 'OpenStack test instance'
    time_after_resource_creation = 180
    time_wait_after_resource_stopping = 60
    time_wait_after_resource_removal = 30


class NodeconductorTest(unittest.TestCase):

    def setUp(self):
        self.driver = get_driver(Settings.site_url)
        self.project_exists = False
        self.ssh_key_exists = False
        self.resource_exists = False

    def test_create_delete_project_key_resource(self):
        print '%s is going to be loggedin.' % Settings.username
        login_nodeconductor(self.driver, Settings.username, Settings.password)
        time.sleep(5)
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
        print 'Prject was created successfully'

        print 'Ssh key is going to be created.'
        create_ssh_key(self.driver, Settings.user_full_name, Settings.key_name)
        time.sleep(10)
        self.ssh_key_exists = True
        print 'Ssh key was created successfully'

        print 'Resource is going to be created.'
        create_resource(self.driver, Settings.project_name, Settings.resource_name,
                         Settings.time_after_resource_creation)
        time.sleep(10)
        self.resource_exists = True
        print 'Resource was created successfully'

        print 'Resource is going to be deleted.'

        delete_resource(self.driver, Settings.resource_name, Settings.project_name, 
                        Settings.time_wait_after_resource_stopping, Settings.time_wait_after_resource_removal)
        time.sleep(10)
        self.resource_exists = False
        print 'Resource was deleted successfully'


    def tearDown(self):
        if self.project_exists:
            try:
                print 'Project is going to be removed.'
                delete_project(self.driver, Settings.project_name)
                self.project_exists = False
                # # Check deletion
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
        
        time.sleep(10)
        if self.ssh_key_exists:
            try:
                delete_ssh_key(self.driver, Settings.key_name, Settings.user_full_name)
                self.ssh_key_exists = False
                # # Check deletion
                # time.sleep(10)
                # list_of_keys_field = self.driver.find_element_by_css_selector('html.ng-scope body.ng-scope.block-ui.'
                # 'block-ui-anim-fade div.app-wrap.ng-scope div.ng-scope div.ng-scope div.ng-scope div.profile'
                # '-content.ng-scope div.container div.tabs-wrapper div.tab-content div#keys.tab.ng-scope.ng-isolate'
                # '-scope.tab-active div.ng-scope div.ng-scope entitylist.ng-isolate-scope div.ng-scope div.ng-scope '
                # 'div.table')

                # try:
                #     list_of_keys_field.find_element_by_tag_name('span')
                # except NoSuchElementException:
                #     print 'I cannot find ssh key. This is good.'
                # else:
                #     print 'Ssh key is found, test fails.'
            except Exception as e:
                print 'Ssh key cannot be deleted. Error: %s' % e

        if self.resource_exists:
            print 'Warning! Test cannot delete resource %s. It has to be deleted manually.' % Settings.resource_name
        if self.project_exists:
            print 'Warning! Test cannot delete project %s. It has to be delete manually.' % Settings.project_name
        if self.ssh_key_exists:
            print 'Warning! Test cannot delete ssh key %s. It has to be deleted manually.' % Settings.key_name

        # # close browser
        # self.driver.quit()


if __name__ == "__main__":
    unittest.main()