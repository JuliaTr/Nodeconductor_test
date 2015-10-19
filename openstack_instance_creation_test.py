import time
import unittest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

import settings
from helpers import (login_nodeconductor, get_driver, create_project, 
                    delete_project, create_ssh_key, delete_ssh_key, 
                    choose_organization, create_resource, delete_resource)


class NodeconductorTest(unittest.TestCase):

    def setUp(self):
        self.driver = get_driver(settings.site_url)
        self.is_project_created = False
        self.is_ssh_key_created = False

    def test_create_delete_project_key_resource(self):
        print '%s is going to be loggedin.' % settings.username
        login_nodeconductor(self.driver, settings.username, settings.password)
        time.sleep(5)
        # Identify necessary username on loaded main page
        username_idt_field = self.driver.find_element_by_class_name('user-name')
        assert username_idt_field.text == settings.user_full_name, 'Error. Another username.'
        time.sleep(10)
        print '%s was loggedin successfully.' % settings.username
        print 'Organization is going to be chosen.'
        choose_organization(self.driver, settings.nec_organization)
        time.sleep(10)
        print 'Organization was chosen successfully.'
        print 'Project is going to be created.'
        create_project(self.driver, settings.project_name)
        time.sleep(10)
        self.is_project_created = True
        print 'Prject was created successfully'
        print 'Ssh key is going to be created.'
        create_ssh_key(self.driver, settings.user_full_name, settings.key_name)
        time.sleep(10)
        self.is_ssh_key_created = True
        print 'Ssh key was created successfully'
        print 'Resource is going to be created.'
        create_resource(self.driver, settings.project_name, settings.resource_name,
                         settings.time_after_resource_creation)
        time.sleep(10)
        print 'Resource was created successfully'
        print 'Resource is going to be deleted.'
        delete_resource(self.driver, settings.resource_name, settings.project_name, 
                        settings.time_wait_after_resource_stopping, settings.time_wait_after_resource_removal)
        time.sleep(10)
        print 'Resource was deleted successfully'


    def tearDown(self):
        if self.is_project_created:
            try:
                delete_project(self.driver, settings.project_name)
                # Check deletion
                time.sleep(10)
                list_of_projects_field = self.driver.find_element_by_class_name('object-list')

                try:
                    list_of_projects_field.find_element_by_link_text(settings.project_name)
                except NoSuchElementException:
                    print 'I cannot find project. This is good.'
                else:
                    print 'Project is found, test fails.'
            except Exception as e:
                print 'Project cannot be deleted. Error: %s' % e
        
        time.sleep(10)
        if self.is_ssh_key_created:
            try:
                delete_ssh_key(self.driver, settings.key_name, settings.user_full_name)
                # Check deletion
                time.sleep(10)
                list_of_keys_field = self.driver.find_element_by_css_selector('html.ng-scope body.ng-scope.block-ui.'
                'block-ui-anim-fade div.app-wrap.ng-scope div.ng-scope div.ng-scope div.ng-scope div.profile'
                '-content.ng-scope div.container div.tabs-wrapper div.tab-content div#keys.tab.ng-scope.ng-isolate'
                '-scope.tab-active div.ng-scope div.ng-scope entitylist.ng-isolate-scope div.ng-scope div.ng-scope '
                'div.table')

                try:
                    list_of_keys_field.find_element_by_tag_name('span')
                except NoSuchElementException:
                    print 'I cannot find ssh key. This is good.'
                else:
                    print 'Ssh key is found, test fails.'
            except Exception as e:
                print 'Ssh key cannot be deleted. Error: %s' % e
        # close browser
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()