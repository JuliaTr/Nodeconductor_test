import time
import unittest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

import settings
from helpers import (login_nodeconductor, get_driver, create_new_project, 
                    deletion_created_project, create_ssh_key, delete_ssh_key, 
                    choose_definite_organization, create_resource, delete_resource)


class NodeconductorTest(unittest.TestCase):

    def setUp(self):
        self.driver = get_driver(settings.site_url)

    def test_create_delete_project_key_resource(self):
        login_nodeconductor(self.driver, settings.username, settings.password)
        # Identify necessary username on loaded main page
        username_idt_field = self.driver.find_element_by_class_name('user-name')
        assert username_idt_field.text == settings.user_full_name, 'Warning'
        time.sleep(5)
        choose_definite_organization(self.driver, settings.nec_organization)
        time.sleep(5)
        create_new_project(self.driver, settings.project_name)
        time.sleep(5)
        create_ssh_key(self.driver, settings.user_full_name, settings.key_name)
        time.sleep(5)
        create_resource(self.driver, settings.project_name, settings.resource_name, settings.time_wait)
        time.sleep(5)
        delete_resource(self.driver, settings.resource_name, settings.project_name, settings.time_wait_again, 
                        settings.time_wait_remove)
        time.sleep(5)
        deletion_created_project(self.driver, settings.project_name)
        # Check deletion
        time.sleep(5)
        list_of_projects_field = self.driver.find_element_by_class_name('object-list')

        try:
            list_of_projects_field.find_element_by_link_text(settings.project_name)
        except NoSuchElementException:
            print 'I cannot find element. This is good.'
        else:
            print 'I found some element, test fails.'
        time.sleep(5)
        delete_ssh_key(self.driver, settings.key_name, settings.user_full_name)
        # Check deletion
        time.sleep(5)
        list_of_keys_field = self.driver.find_element_by_css_selector('html.ng-scope body.ng-scope.block-ui.'
            'block-ui-anim-fade div.app-wrap.ng-scope div.ng-scope div.ng-scope div.ng-scope div.profile'
            '-content.ng-scope div.container div.tabs-wrapper div.tab-content div#keys.tab.ng-scope.ng-isolate'
            '-scope.tab-active div.ng-scope div.ng-scope entitylist.ng-isolate-scope div.ng-scope div.ng-scope '
            'div.table')

        try:
            list_of_keys_field.find_element_by_tag_name('span')
        except NoSuchElementException:
            print 'I cannot find element. This is good.'
        else:
            print 'I found some element, test fails.'

    # def tearDown(self):
    #     # close browser
    #     self.driver.quit()


if __name__ == "__main__":
    unittest.main()