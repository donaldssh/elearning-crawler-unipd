# Crawler elearning unipd

### SETUP
- The web crawler need to sign in the elearning, so you have to set you email and password inside `pwd.asd` as shown. In the first line you have to set the email, and in the second line you have to set the password.

### Installation
- Firefox geckodriver
 https://github.com/mozilla/geckodriver/releases
- Selenium:
    `pip install selenium`

### Usage
- crawler_slide.py : dowload all the slides of the selected course
- crawler.py : download the selected .m3u8 video lecture