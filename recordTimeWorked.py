from toggl.TogglPy import Toggl
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from urllib.request import urlopen, Request
import time, configparser, sys, json, pprint

#Generate ConfigParser to read inputs from config.ini file
config = configparser.ConfigParser()
config.read("config.ini")

#Toggl object for interacting with Toggl's API
toggl = Toggl()
toggl.setAPIKey(config['DEFAULT']['TogglApiKey'])
workspace_id = toggl.request("https://api.track.toggl.com/api/v8/workspaces")[0]['id']

#Create dict object to store URLs for API calls/Selenium
urls = {
    'source_info' : str("https://api.track.toggl.com/reports/api/v2/details?workspace_id=%s&user_agent=%s") % (workspace_id, config['DEFAULT']['TogglEmail']),
    'service_now' : r'https://liberty.service-now.com/task_time_worked.do?sys_id=-1&sysparm_stack=task_time_worked_list.do',
    'time_entries' : r'https://api.track.toggl.com/api/v8/time_entries'
}

#Generate source info from Toggl
source_info = toggl.request(urls['source_info'])['data']

#Initialize Selenium browser based on config.ini browser preference
if (config['DEFAULT']['Browser'] == 'Edge'):
    browser = webdriver.Edge(config['DEFAULT']['BrowserDriverPath'])
elif (config['DEFAULT']['Browser'] == 'Chrome'):
    browser = webdriver.Chrome(config['DEFAULT']['BrowserDriverPath'])
elif (config['DEFAULT']['Browser'] == 'Firefox'):
    browser = webdriver.Firefox(config['DEFAULT']['BrowserDriverPath'])
elif (config['DEFAULT']['Browser'] == 'Safari'):
    browser = webdriver.Safari(config['DEFAULT']['BrowserDriverPath'])
else:
    sys.exit("No supported browser included in config.ini. Browser must be: Chrome, Edge, Safari, or Firefox")

browser.get(urls['service_now'])
wait = WebDriverWait(browser, 10)
time.sleep(3)

def fill_form(description, date, duration, tags):
    if ('Tracked' not in tags):
        #Load time tracking webpage
        browser.get(urls['service_now'])
        WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.ID, 'sysverb_insert_bottom')))
        
        #Find html elements
        in_comments = browser.find_element_by_id('task_time_worked.comments')
        in_time_hours = browser.find_element_by_id('ni.task_time_worked.time_workeddur_hour')
        in_time_min = browser.find_element_by_id('ni.task_time_worked.time_workeddur_min')
        in_date = browser.find_element_by_id('task_time_worked.u_created_for')
        in_category = Select(browser.find_element_by_id('task_time_worked.u_category'))
        in_task = browser.find_element_by_id('sys_display.task_time_worked.task')
        submit = browser.find_element_by_id('sysverb_insert_bottom')
        
        #Input task data
        in_task.clear()
        if (tags[0] == 'ooo'):
            in_category.select_by_index(1)
        elif (tags[0] == 'pd'):
            in_category.select_by_index(2)
        elif (tags[0] == 'conv'):
            in_category.select_by_index(3)
        elif (tags[0] == 'cler'):
            in_category.select_by_index(4)
        else:
            in_task.send_keys(tags[0])
        time.sleep(1)

        #Input date data
        in_date.clear()
        in_date.send_keys(date[0:10])
        time.sleep(1)

        #Input hours
        in_time_hours.clear()
        hours = int(duration/1000/60/60)
        in_time_hours.send_keys(hours)
        time.sleep(1)

        #Input minutes
        in_time_min.clear()
        min = int(duration/1000/60%60)
        in_time_min.send_keys(min)
        time.sleep(1)

        #Input comments data
        in_comments.clear()
        in_comments.send_keys(description)
        time.sleep(1)
        
        #Submit form
        #submit.click()
        time.sleep(5)

#To-do: create function to update the tags for an entry after it has been tracked
def update_tags(entry_id):
    endpoint = str('%s/%s') % (urls['time_entries'], entry_id)
    binary_data = json.JSONEncoder().encode({
        'time_entry' : {
            'id' : entry_id,
            'tags' : ['tracked']
        }
    }).encode('utf-8')
    request = Request(endpoint, data=binary_data, headers=toggl.headers, method='PUT')
    urlopen(request)

for record in source_info:
    fill_form(record['description'], record['start'], record['dur'], record['tags'])
    update_tags(record['id'])

print("Procedure Completed.")