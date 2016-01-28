"""
1. Login NC
2. Choose organization
3. Create project
4. Create application group
5. Create application project
6. Delete application project
7. Delete application group
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
                     create_application_group, element_exists, delete_application_group, create_application_project,
                     delete_application_project, make_screenshot, _search)
from base import BaseSettings


class Settings(BaseSettings):
    site_url = "http://web-test.nodeconductor.com"
    username = 'Alice'
    password = 'Alice'
    user_full_name = 'Alice Lebowski'
    organization = 'Test only org'
    project_name = 'GitLab test project'
    category_name = 'APPLICATIONS'
    resource_type_name = 'Group'
    resource_type_name1 = 'Project'
    path_name = 'test-group'
    application_group_name = 'Test group'
    visibility_level_name = 'The project can be cloned by any logged in user.'
    application_project_name = 'Test project'
    time_wait_for_application_state = 10
    time_wait_to_delete_application = 60


class ApplicationCreationTest(unittest.TestCase):

    def setUp(self):
        self.driver = get_driver(Settings.site_url)
        self.project_exists = False
        self.application_group_exists = False
        self.application_project_exists = False
        self.driver.implicitly_wait(BaseSettings.implicitly_wait)

    def test_create_delete_application(self):
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

        # Create application group
        print 'Application group is going to be created.'
        create_application_group(self.driver, Settings.project_name, Settings.category_name, Settings.resource_type_name,
                                 Settings.path_name, Settings.application_group_name)
        xpath = '//span[@class="name" and contains(text(), "%s")]' % Settings.application_group_name
        assert bool(self.driver.find_elements_by_xpath(xpath)), 'Cannot create application group "%s"' % Settings.application_group_name
        self.application_group_exists = True
        print 'Application group exists: ', self.application_group_exists
        print 'Find online state of created application group'
        try:
            WebDriverWait(self.driver, Settings.time_wait_for_application_state).until(
                EC.presence_of_element_located((By.XPATH, '//dd[contains(text(), "Online")]')))
        except TimeoutException as e:
            print 'Error: Application group is not online'
            raise e
        else:
            print 'Application group is in online status'
        print 'Application group was created successfully'

        # Create application project
        print 'Application project is going to be created.'
        create_application_project(self.driver, Settings.project_name, Settings.category_name, Settings.resource_type_name1, Settings.application_project_name,
                                   Settings.visibility_level_name, Settings.application_group_name)
        xpath = '//span[@class="name" and contains(text(), "%s")]' % Settings.application_project_name
        assert bool(self.driver.find_elements_by_xpath(xpath)), 'Cannot create application group "%s"' % Settings.application_project_name
        self.application_project_exists = True
        print 'Application project exists: ', self.application_project_exists
        print 'Find online state of created application group'
        try:
            WebDriverWait(self.driver, Settings.time_wait_for_application_state).until(
                EC.presence_of_element_located((By.XPATH, '//dd[contains(text(), "Online")]')))
        except TimeoutException as e:
            print 'Error: Application project is not online'
            raise e
        else:
            print 'Application project is in online status'
        print 'Application project was created successfully'

    def tearDown(self):
        print '\n\n\n --- TEARDOWN ---'
        if sys.exc_info()[0] is not None:
            make_screenshot(self.driver)
        if self.application_project_exists:
            try:
                # Delete application project
                print 'Application project is going to be deleted.'
                delete_application_project(self.driver, Settings.project_name, Settings.application_project_name)
                self.application_project_exists = False
                _search(self.driver, Settings.application_project_name)
                print 'Wait till application project will be deleted'
                try:
                    WebDriverWait(self.driver, Settings.time_wait_to_delete_application).until(
                        EC.invisibility_of_element_located((By.XPATH, '//a[contains(text(), "%s")]' % Settings.application_project_name)))
                except TimeoutException as e:
                    print 'Error: Application project with name "%s" was not deleted, it still exists' % Settings.application_project_name
                    raise e
                else:
                    print 'Application project was deleted successfully.'
            except Exception as e:
                print 'Application project cannot be deleted. Error: %s' % e

        if self.application_group_exists:
            try:
                # Delete application group
                print 'Application group is going to be deleted.'
                delete_application_group(self.driver, Settings.project_name, Settings.application_group_name)
                self.application_group_exists = False
                _search(self.driver, Settings.application_group_name)
                print 'Wait till application group will be deleted'
                try:
                    WebDriverWait(self.driver, Settings.time_wait_to_delete_application).until(
                        EC.invisibility_of_element_located((By.XPATH, '//a[contains(text(), "%s")]' % Settings.application_group_name)))
                except TimeoutException as e:
                    print 'Error: Application group with name "%s" was not deleted, it still exists' % Settings.application_group_name
                    raise e
                else:
                    print 'Application group was deleted successfully.'
            except Exception as e:
                print 'Application group cannot be deleted. Error: %s' % e

        if self.project_exists:
            try:
                # Delete project
                print 'Project is going to be deleted.'
                delete_project(self.driver, Settings.project_name)
                self.project_exists = False
                time.sleep(BaseSettings.click_time_wait)
                _search(self.driver, Settings.project_name)
                if element_exists(self.driver, xpath='//a[contains(text(), "%s")]' % Settings.project_name):
                    self.project_exists = True
                print 'Project was deleted successfully.'
            except Exception as e:
                print 'Project cannot be deleted. Error: "%s"' % e

        if self.application_project_exists:
            print 'Warning! Test cannot delete application project %s. It has to be deleted manually.' % Settings.application_project_name
        if self.application_group_exists:
            print 'Warning! Test cannot delete application group %s. It has to be deleted manually.' % Settings.application_group_name
        if self.project_exists:
            print 'Warning! Test cannot delete project %s. It has to be delete manually.' % Settings.project_name

        self.driver.quit()


if __name__ == "__main__":
    try:
        import xmlrunner
        unittest.main(testRunner=xmlrunner.XMLTestRunner(output=Settings.test_reports_dir))
    except ImportError as e:
        unittest.main()
