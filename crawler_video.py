from selenium.webdriver.firefox.options import Options
from selenium import webdriver
import time
import os
import requests
from unipd_login import *
import argparse

def main(dep, course, index_video):   

    dep_name = dep.upper()
    course_name = course.upper()
    
    video_tag = "Kaltura Video Resource"
    download_dir = os.getcwd()

    usr, pwd = input_data()

    # set some useful options, like download in the same directory
    firefoxOptions = Options()
    firefoxOptions.set_preference("browser.download.folderList", 2)
    firefoxOptions.set_preference("browser.download.manager.showWhenStarting", False)
    firefoxOptions.set_preference("browser.download.dir", download_dir)
    
    # automatically download .m3u8 files, without asking
    firefoxOptions.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/vnd.apple.mpegurl")

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
    course = driver.find_element_by_partial_link_text(course_name).click();

    # find and click over the selected video
    all_videos = driver.find_elements_by_xpath("//*[span[contains(text(),'"+video_tag+"')]]")
    
    all_videos[index_video].click()

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
    
    driver.close()


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Download the playlist .m3u8 of the video lecture selected")
    
    parser.add_argument("--dep", required=True, help="department of the course")
    parser.add_argument("--course", required=True, help="name of the course")
    parser.add_argument("--index", required=False, help="index of the video to be downloaded")
    
    args = parser.parse_args()
    
    main(dep=args.dep, course=args.course, index_video=args.index)    
    
