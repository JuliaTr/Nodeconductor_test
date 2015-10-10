import time
import unittest
from selenium import webdriver

from helpers import login_nodeconductor, get_driver, create_new_project, deletion_created_project, create_ssh_key

class NodeconductorTest(unittest.TestCase):

    def setUp(self):
        # Open browser
        self.driver = get_driver()
 
    def test_login_nodeconductor(self):
        login_nodeconductor(self.driver)
        # Identify necessary username on loaded main page
        username_idt_field = self.driver.find_element_by_class_name('user-name')
        assert username_idt_field.text == 'Trygubniak', 'Warning'

    def test_create_new_project(self):
        login_nodeconductor(self.driver)
        create_new_project(self.driver, 'Julia_project', 'xcvgngbfr')
        # Identify created project
        project_name_field = self.driver.find_element_by_class_name('name')
        assert project_name_field.text == 'Julia_project', 'Warning'
        deletion_created_project(self.driver)
        # Check deletion
        project_search_field = self.driver.find_element_by_css_selector('[ng-model="entityList.searchInput"]')
        project_search_field.send_keys('Julia_project')
        time.sleep(5)
        list_of_projects_field = self.driver.find_element_by_class_name('object-list')

        try:
            list_of_projects_field.find_element_by_link_text('Julia_project')
        except NoSuchElementException:
            print 'I cannot find element. This is good.'
        else:
            print 'I found some element, test fails.'

    def test_create_ssh_key(self):
        # Create ssh key
        login_nodeconductor(self.driver)
        create_ssh_key(self.driver)
        delete_ssh_key(self.driver)
        # Check deletion
        ssh_search_field = self.driver.find_element_by_css_selector('[ng-model="UserDetailUpdate.searchInput"]')
        ssh_search_field.send_keys('vgbh')
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

    def tearDown(self):
        # close browser
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
