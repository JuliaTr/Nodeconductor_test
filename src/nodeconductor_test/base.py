import os

project_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


class BaseSettings(object):
    click_time_wait = 3  # time between normal user clicks
    search_time_wait = 8  # time for search
    implicitly_wait = 20  # time to wait for element appears on the page
    screenshots_folder = os.path.join(project_path, 'screenshots')
    test_reports_dir = os.path.join(project_path, 'test_reports')  # unittest-xml-reporting must be installed
