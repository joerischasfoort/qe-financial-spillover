from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import numpy as np
import pandas as pd
import time
import traceback
#from send_email import sendEmail


browser = webdriver.Chrome()

browser.get('https://www.ecb.europa.eu/stats/financial_markets_and_interest_rates/euro_area_yield_curves/html/index.en.html')
time.sleep(2)
browser.find_elements_by_xpath("//*[contains(text(), 'I understand and I accept the use of cookies')]")[0].click()
time.sleep(2)


years = np.array(range(6))+2008
months = range(12)



#span parameters
browser.find_elements_by_xpath("//*[contains(text(), 'Parameters')]")[1].click()

browser.find_element_by_id("all").click()
browser.find_element_by_id("AAA").click()



last_beta0 = 0
data = pd.DataFrame([])
date = []
for year in years:
    if year==2008:
        months = months[11:]
    else:
        months = range(12)

    for month in months:

        try:
            calb = browser.find_element_by_id("calendarButton").click()
        except:
            print('calendar already activated')

        browser.find_element_by_class_name('ui-datepicker-year').click()
        select_y = Select(browser.find_element_by_class_name('ui-datepicker-year'))
        select_y.select_by_value(str(2008))

        #select month
        browser.find_element_by_class_name('ui-datepicker-year').click()
        select_y = Select(browser.find_element_by_class_name('ui-datepicker-year'))

        select_y.select_by_value(str(year))

        #select month
        browser.find_element_by_class_name('ui-datepicker-month').click()
        select_m = Select(browser.find_element_by_class_name('ui-datepicker-month'))
        select_m.select_by_index(month)


        #select day
        days_loop = []
        c_bug = 0
        days = []
        tds=browser.find_elements_by_tag_name('TD')
        for td in tds:
            if td.get_attribute('data-handler')=="selectDay":
                days_loop.append(td)
        for day in range(len(days_loop)):
            if c_bug==1:
                break
            while True:
                if len(days_loop)!=len(days) and days != []:
                    c_bug = 1
                    break
                try:
                    calb = browser.find_element_by_id("calendarButton").click()
                    select_y = Select(browser.find_element_by_class_name('ui-datepicker-year'))
                    select_y.select_by_value(str(2008))
                    select_y = Select(browser.find_element_by_class_name('ui-datepicker-year'))
                    select_y.select_by_value(str(year))
                    browser.find_element_by_class_name('ui-datepicker-month').click()
                    select_m = Select(browser.find_element_by_class_name('ui-datepicker-month'))
                    if select_m.first_selected_option.text != select_m.options[month].get_attribute("text"):
                        select_m.select_by_index(month)
                    days=[]
                    tds = browser.find_elements_by_tag_name('TD')
                    for td in tds:
                        if td.get_attribute('data-handler') == "selectDay":
                            days.append(td)

                    d = days[day].get_attribute('innerHTML')
                    days[day].click()

                    txt_to_click=browser.find_elements_by_xpath("//*[contains(text(), 'The euro area yield curve')]")[0].click()
                    time.sleep(1)
                    #close all but one calendar item
                    if day==0 and month == months[0] and year == years[0]:
                        calit=browser.find_elements_by_class_name('calendarItem')
                        while len(calit)>1:
                            calit[1].click()
                            calit = browser.find_elements_by_class_name('calendarItem')
                    else:
                        calit=browser.find_elements_by_class_name('calendarItem')
                        while len(calit)>1:
                            calit[0].click()
                            time.sleep(0.2)
                            calit = browser.find_elements_by_class_name('calendarItem')

                    #store table
                    while True:
                        try:
                            main_table = browser.find_elements_by_tag_name("TBODY")
                            time.sleep(1)
                            test=main_table[0].get_attribute('innerHTML')
                        except:
                            print(year, month, day)
                            continue
                        break
                    x=main_table[0].get_attribute('innerHTML')
                    xs = str(x).split("</td><td>")
                    a=[year,month+1,int(str(d).split(">")[1].split("<")[0])]
                    sv_index=0
                    for v in range(1,7):
                        if last_beta0==xs[v].split('<')[0]:
                            sv_index+=1
                    if sv_index==6:
                        print("same value")
                        produce_error=xs[1000]
                except:
                    print("big loop error, try again")
                    continue
                break
            data=data.append({"date":str(a[2])+'.'+ str(a[1])+'.'+ str(a[0]), "beta0":xs[1].split('<')[0],"beta1": xs[2].split('<')[0],"beta2": xs[3].split('<')[0],"beta3": xs[4].split('<')[0],"tau1": xs[5].split('<')[0],"tau2": xs[6].split('<')[0]}, ignore_index=True)
            data.to_excel("yield_curve_data_allBonds01.xls")
            last_beta0=xs[1].split('<')[0]
