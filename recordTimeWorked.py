from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
import time, glob, os
import pandas as PD

files = glob.glob("C:/Users/[MODIFY THIS WITH YOUR MACHINE USERNAME]/Downloads/Toggl_time_entries*.csv")
files.sort(key=os.path.getmtime, reverse = True)
print(files[0])

columns = ['Description', 'Start date', 'Duration', 'Tags']
source_info = PD.read_csv(files[0], usecols = columns)
source_info.rename(columns={'Start date': 'Date'}, inplace=True)

url = r'https://liberty.service-now.com/task_time_worked.do?sys_id=-1&sysparm_stack=task_time_worked_list.do'
path = r'C:\[PATH TO YOU SELENIUM BROWSER DRIVER]'

browser = webdriver.Edge(path)
browser.get(url)
wait = WebDriverWait(browser, 10)
time.sleep(3)

def fill_form(description, date, duration, tags):
    #initialize url
    browser.get(url)
    WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.ID, 'sysverb_insert_bottom')))
    #find elements
    in_comments = browser.find_element_by_id('task_time_worked.comments')
    in_time_hours = browser.find_element_by_id('ni.task_time_worked.time_workeddur_hour')
    in_time_min = browser.find_element_by_id('ni.task_time_worked.time_workeddur_min')
    in_date = browser.find_element_by_id('task_time_worked.u_created_for')
    in_category = Select(browser.find_element_by_id('task_time_worked.u_category'))
    in_task = browser.find_element_by_id('sys_display.task_time_worked.task')
    submit = browser.find_element_by_id('sysverb_insert_bottom')
    #input data
    in_task.clear()
    if (tags == 'ooo'):
        in_category.select_by_index(1)
    elif (tags == 'pd'):
        in_category.select_by_index(2)
    elif (tags == 'conv'):
        in_category.select_by_index(3)
    elif (tags == 'cler'):
        in_category.select_by_index(4)
    else:
        in_task.send_keys(tags)
    time.sleep(1)
    in_date.clear()
    in_date.send_keys(date)
    time.sleep(1)
    in_time_hours.clear()
    in_time_hours.send_keys(duration[0:2])
    time.sleep(1)
    in_time_min.clear()
    in_time_min.send_keys(duration[3:5])
    time.sleep(1)
    in_comments.clear()
    in_comments.send_keys(description)
    time.sleep(1)
    #submit
    #submit.click()
    time.sleep(5)

for row in source_info.itertuples():
    fill_form(row.Description, row.Date, row.Duration, row.Tags)

print("Procedure Completed.")