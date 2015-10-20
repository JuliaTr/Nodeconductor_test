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
        self.is_provider_created = False

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
        
        self.is_provider_created = True 
        print 'Provider is going to be created.'
        create_provider(self.driver, settings.project_name, settings.provider_name)
        time.sleep(5)
        search_provider = self.driver.find_element_by_class_name('object-list')
        time.sleep(5)        
        try:
            self.driver.find_element_by_link_text(settings.provider_name)
        except NoSuchElementException:
            print 'I cannot find created provider, test fails.'
        else:
            print 'Created provider is found. This is good.'  
        print 'Provider was created successfully.'
        time.sleep(10)
        
        print 'Resource is going to be imported.'
        import_resource(self.driver, settings.project_name, settings.provider_name, settings.resource_name)
        time.sleep(5)
        search_resource = self.driver.find_element_by_class_name('list-item')
        time.sleep(5)
        try:
            self.driver.find_element_by_link_text(settings.resource_name)
        except NoSuchElementException:
            print 'I cannot find imported resource, test fails.'
        else:
            print 'Imported resource is found. This is good.'
        print 'Resource was imported successfully.'
        time.sleep(10)
        
        print 'Resource is going to be unlinked.'
        unlink_resource(self.driver, settings.project_name, settings.resource_name)
        time.sleep(10)
        search_field = self.driver.find_element_by_css_selector('[ng-model="generalSearch"]')
        search_field.clear()
        search_field.send_keys(settings.resource_name)
        time.sleep(5)
        try:
            self.driver.find_element_by_link_text(settings.resource_name)
        except NoSuchElementException:
            print 'I cannot find unlinked resource. This is good.'
        else:
            print 'Unlinked resource is found, test fails.'
        print 'Resource was unlinked successfully.'
       
    def tearDown(self):
        print 'Is provider created: ', self.is_provider_created
        if self.is_provider_created:
            try:
                print 'Provider is going to be removed.'
                time.sleep(10)
                self.driver.refresh()       
                delete_provider(self.driver, settings.project_name, settings.provider_name)
                time.sleep(10)
                search_field = self.driver.find_element_by_css_selector('[ng-model="generalSearch"]')
                search_field.clear()
                search_field.send_keys(settings.provider_name)
                time.sleep(5)
                try:
                    self.driver.find_element_by_link_text(settings.provider_name)
                except NoSuchElementException:
                    print 'I cannot find removed provider. This is good.'
                else:
                    print 'Removed provider is found, test fails.'
            except Exception as e:
                print 'Provider cannot be removed. Error: %s' % e
                
        if self.is_project_created:
            try:
                print 'Project is going to be removed.'
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