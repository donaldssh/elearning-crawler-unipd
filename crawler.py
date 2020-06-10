from selenium.webdriver.firefox.options import Options
from selenium import webdriver
import time
import os
import requests


def department(dep, driver):
    switcher = {
        "DEI": dei_login(driver),
        "MATH": math_login(driver)
    }
    return switcher.get(dep, "Department not implemented")


def dei_login(driver):
    
    # base url for the elearning dei
    url = "https://elearning.dei.unipd.it/mod/page/view.php?id=1673"

    # load the url
    driver.get(url)

    # go to the login page
    shib = driver.find_element_by_id("shibbox")
    img = shib.find_element_by_css_selector(".img-responsive").click()


def math_login(driver):
    
    url = "https://elearning.unipd.it/math/my/?myoverviewtab=courses"
    
    # load the url
    driver.get(url)
    
    # go to the login page
    shib = driver.find_element_by_id("shib_si")
    img = shib.find_elements_by_tag_name("a")[0].click()
    
    
def main():    


    # input parameters: department, course and video
    dep_name = "DEI"
    course_name = "COURSE NAME"
    video_name = "VIDEO NAME"
    # instead of video_name i can search also for kaltura video resource.., if i want to dowload all

    # read the username and password of elearning dei unipd
    lines = open("pwd.asd").readlines()
    usr = lines[0].replace("\n", "");
    pwd = lines[1].replace("\n", "");

    # set some useful options, like download in the same directory
    firefoxOptions = Options()
    firefoxOptions.set_preference("browser.download.folderList",2)
    firefoxOptions.set_preference("browser.download.manager.showWhenStarting", False)
    firefoxOptions.set_preference("browser.download.dir", os.getcwd())
    firefoxOptions.set_preference("browser.helperApps.neverAsk.saveToDisk", True)

    # load firefox geckodriver with dowload options
    driver = webdriver.Firefox(options=firefoxOptions)

    #wait 10 seconds when doing a find_element before carrying on
    driver.implicitly_wait(10) 


    # find the login button based on the department
    department(dep_name, driver)


    # wait some more seconds for the loading
    time.sleep(5)

    # get the input box of username and password
    username = driver.find_element_by_id("j_username_js")
    password = driver.find_element_by_id("password")

    # type their values, read from the pwd.asd
    username.send_keys(usr)
    password.send_keys(pwd)

    # sign in
    driver.find_element_by_id("login_button_js").click()

    # find and click over the selected course
    driver.find_element_by_partial_link_text(course_name).click();

    # find and click over the selected video
    driver.find_element_by_xpath("//span[contains(text(),'"+video_name+"')]").click()

    #all_cookies = driver.get_cookies()
    #print(all_cookies)

    # find the src of the kaltura video only
    url_videobase = driver.find_element_by_id("contentframe").get_attribute("src")
    driver.get(url_videobase)

    # wait some more seconds for the loading
    time.sleep(5)

    # find the iframe dynamically generated tag and search inside it
    driver.switch_to.default_content()
    frame = driver.find_element_by_xpath('//iframe')
    driver.switch_to.frame(frame)

    # find the src for the a.m3u8
    url_video2 = driver.find_element_by_id("pid_kplayer").get_attribute("src")

    # get the a.m3u8 file
    r = requests.get(url_video2)

    # write the a.m3u8 as txt
    with open("./a.txt", 'wb') as f:
        f.write(r.content)

    # read all the video links inside the a.txt
    video_links = open("./a.txt").readlines()

    # select one video (ie line 5, typically the HD, but check the a.txt and feel free to change it)
    choosen_index = video_links[4]

    # download the index.m3u8 file (which is the video stream of the lecture)
    driver.get(choosen_index)


if __name__ == "__main__":
    main()
