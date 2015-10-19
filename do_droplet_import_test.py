import time
import unittest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

import settings
from helpers import (login_nodeconductor, get_driver, create_project, delete_project, create_ssh_key, 
                    delete_ssh_key, choose_organization, create_resource, delete_resource, create_provider, 
                    import_resource, unlink_resource, delete_provider)


class NodeconductorTest(unittest.TestCase):

    def setUp(self):
        self.driver = get_driver(settings.site_url)
        self.is_project_created = False
      

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
        print 'Project was created successfully'
        print 'Provider is going to be created.'
        create_provider(self.driver, settings.project_name, settings.provider_name)
        time.sleep(5)
        list_of_providers_field = self.driver.find_element_by_css_selector('[ng-model="generalSearch"]')

        try:
            list_of_providers_field.find_element_by_link_text(settings.provider_name)
        except NoSuchElementException:
            print 'Created provider is found. This is good.'
        else:
            print 'I cannot find created provider, test fails.'
        
        print 'Provider was created successfully.'
        time.sleep(10)
        print 'Resource is going to be imported.'
        import_resource(self.driver, settings.project_name, settings.provider_name, settings.resource_name)
        time.sleep(5)
        list_of_resource_field = self.driver.find_element_by_css_selector('[ng-model="generalSearch"]')

        try:
            list_of_resource_field.find_element_by_link_text(settings.resource_name)
        except NoSuchElementException:
            print 'Imported resource is found. This is good.'
        else:
            print 'I cannot find imported resource, test fails.'
        print 'Resource was imported successfully.'
        time.sleep(10)
        print 'Resource is going to be unlinked.'
        unlink_resource(self.driver, settings.project_name, settings.resource_name)
        time.sleep(10)
        list_of_resource_field = self.driver.find_element_by_css_selector('[ng-model="generalSearch"]')

        try:
            list_of_resource_field.find_element_by_link_text(settings.resource_name)
        except NoSuchElementException:
            print 'I cannot find unlinked resource. This is good.'
        else:
            print 'Unlinked resource is found, test fails.'
        print 'Resource was unlinked successfully.'
        print 'Provider is going to be removed.'
        delete_provider(self.driver, settings.project_name, settings.provider_name)
        time.sleep(10)
        list_of_provider_field = self.driver.find_element_by_css_selector('[ng-model="generalSearch"]')

        try:
            list_of_provider_field.find_element_by_link_text(settings.provider_name)
        except NoSuchElementException:
            print 'I cannot find removed provider. This is good.'
        else:
            print 'Removed provider is found, test fails.'
        print 'Provider was removed successfully.'

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
        
        # close browser
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()