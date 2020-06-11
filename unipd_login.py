from selenium import webdriver

def department(dep, driver):
    switcher = {
        "DEI": lambda : dei_login(driver),
        "MATH": lambda : math_login(driver)
    }
    return switcher.get(dep, lambda :  "Department not implemented")()


def dei_login(driver):
    
    # base url for the elearning dei
    url = "https://elearning.dei.unipd.it/mod/page/view.php?id=1673"

    # load the url
    driver.get(url)

    # go to the login page
    shib = driver.find_element_by_id("shibbox")
    img = shib.find_element_by_css_selector(".img-responsive").click()
    return


def math_login(driver):
    
    url = "https://elearning.unipd.it/math/my/?myoverviewtab=courses"
    
    # load the url
    driver.get(url)
    
    # go to the login page
    shib = driver.find_element_by_id("shib_si")
    img = shib.find_elements_by_tag_name("a")[0].click()
    return
    

def read_pwd_from_asd():
    
    lines = open("pwd.asd").readlines()
    usr = lines[0].replace("\n", "")
    pwd = lines[1].replace("\n", "")
    
    return usr, pwd
    
      
def main():
    pass

if __name__ == "__main__":
   main()
