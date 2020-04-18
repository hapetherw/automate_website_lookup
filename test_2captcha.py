from selenium import webdriver
from time import sleep
import pandas as pd
import requests

url = 'https://bulkdacheck.com/'
# browser = webdriver.Chrome('chromedriver.exe')
# browser.maximize_window()
# browser.get(url)

API_KEY = '2e54538b3f77870c2cd4587af61e8114'
site_key = '6LeRhdEUAAAAAE1pEHO4cWBIn449rYsablgcSQ6A'

s = requests.Session()
# here we post site key to 2captcha to get captcha ID (and we parse it here too)
captcha_id = s.post("http://2captcha.com/in.php?key={}&method=userrecaptcha&googlekey={}&pageurl={}".format(
    API_KEY, site_key, url)).text.split('|')[1]
# then we parse gresponse from 2captcha response
recaptcha_answer = s.get(
    "http://2captcha.com/res.php?key={}&action=get&id={}".format(API_KEY, captcha_id)).text
print("solving ref captcha...")
while 'CAPCHA_NOT_READY' in recaptcha_answer:
    sleep(5)
    recaptcha_answer = s.get(
        "http://2captcha.com/res.php?key={}&action=get&id={}".format(API_KEY, captcha_id)).text
recaptcha_answer = recaptcha_answer.split('|')[1]
print(recaptcha_answer)

# we make the payload for the post data here, use something like mitmproxy or fiddler to see what is needed
payload = {
    'token': recaptcha_answer
}

# then send the post request to the url
response = s.post(url+'validate_recaptcha.php', payload)
print(response)
file = open('Example Website List.txt', 'r+')
website_list = file.readlines()
website_divisible_list = []
for index, site in enumerate(website_list):
    website_divisible_list.append(site)
    if (index+1) % 50 is 0:
        print(website_divisible_list)
        website_divisible_list.clear()
        break
# print(file.readlines())