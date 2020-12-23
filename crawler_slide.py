from selenium.webdriver.firefox.options import Options
from selenium import webdriver
import time
import os
import requests
from unipd_login import *


def main():   
    
    # input parameters: department, course and download dir
    dep_name = "SET HERE THE DPT"
    course_name = "SET HERE THE COURSE NAME"
    download_dir = os.getcwd()+"/slides"

    mime_types = "application/pdf,application/vnd.adobe.xfdf,application/vnd.fdf,application/vnd.adobe.xdp+xml"

    firefoxOptions = Options()
    firefoxOptions.set_preference("browser.download.folderList",2)
    firefoxOptions.set_preference("browser.download.manager.showWhenStarting", False)
    firefoxOptions.set_preference("browser.download.dir", download_dir)
    firefoxOptions.set_preference("browser.helperApps.neverAsk.saveToDisk", mime_types)
    firefoxOptions.set_preference("pdfjs.disabled", True) 

    # load firefox geckodriver with dowload options
    driver = webdriver.Firefox(options=firefoxOptions)
    
    #wait 10 seconds when doing a find_element before carrying on
    driver.implicitly_wait(10) 
    
    usr, pwd = input_data()

    # find the login button based on the department
    department(dep_name, driver)
    
    # wait some more seconds for the loading
    time.sleep(5)
    
    # get the input box of username and password
    username = driver.find_element_by_id("j_username_js")
    password = driver.find_element_by_id("password")

    username.send_keys(usr)
    password.send_keys(pwd)

    # sign in
    driver.find_element_by_id("login_button_js").click()
    
    # find and click over the selected course
    course = driver.find_element_by_partial_link_text(course_name).click()

    
    # find all the slides
    slides = driver.find_elements_by_xpath("//*[span[contains(text(),'File')]]")
    print(str(len(slides)) + ' slides are goind to be downloaded')

    for i in range(len(slides)):

        slides[i].click()
        
        driver.find_element_by_id("download").click()

        time.sleep(1)

        driver.execute_script("window.history.go(-1)")

    # driver.close()


if __name__ == "__main__":
    main()
