import http.client
import json
import os
import sys
import time

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

if __name__ == '__main__':
    # cred.json format
    # {
    #   "username": "",
    #   "password": "",
    #   "email": "",
    #   "ceePassword": ""
    # }
    print('Initializing...')
    hrmsUnavailable = False
    application_path = os.path.dirname(sys.executable)
    try:
        # cred = json.load(open(os.path.join(application_path, 'cred.json')))
        cred = json.load(open('cred.json'))
    except FileNotFoundError:
        print('cred.json not found')
        sys.exit(1)
    ceePassword = cred['ceePassword']
    email = cred['email']

    ContactLessSwipeUrl = 'https://cee-apac.exelatech.com/'
    service = Service('geckodriver.exe')
    options = webdriver.FirefoxOptions()
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    options.accept_insecure_certs = True
    options.set_preference("geo.enabled", True)
    # options.add_experimental_option("prefs", {"profile.default_content_setting_values.geolocation": 1})
    options.headless = True
    CEEDriver = webdriver.Firefox(options=options, service=service)


    # CEELogin
    CEEDriver.get(ContactLessSwipeUrl)
    time.sleep(1)
    CEEDriver.find_element(By.CSS_SELECTOR, 'input.col-12').send_keys(email)
    CEEDriver.find_element(By.ID, 'password-field').send_keys(ceePassword)
    CEEDriver.find_element(By.CSS_SELECTOR, 'input.form-control:nth-child(2)').click()
    while True:
        if CEEDriver.current_url == 'https://cee-apac.exelatech.com/Index':
            break
    # time.sleep(3)
    clock_in_btn = WebDriverWait(CEEDriver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.card_image > '
                                                                                                  'img:nth-child(1)')))
    # clock_in_btn = CEEDriver.find_element(By.XPATH, '/html/body/app/div[2]/div[3]/div[1]/div/div[1]/img')
    # clock_in_btn = CEEDriver.find_element(By.CSS_SELECTOR, '.card_image > img:nth-child(1)')
    # clock_in_btn_text = CEEDriver.find_element(By.XPATH, '/html/body/app/div[2]/div[3]/div[1]/div/div[2]/p').text
    clock_in_btn_text = CEEDriver.find_element(By.CSS_SELECTOR, 'div.card_title:nth-child(2) > p:nth-child(1)').text
    # End CEE Login
    print('\t***-Welcome to AutoPunchEla-***')
    print('1.Punch In\n2.Punch Out')
    choice = int(input('Enter your choice: '))
    if choice == 1:
        print('\n\t***-Please wait while we log you in-***')

        print("Logging in to Contactless EE")
        print("Trying to Clock In")
        if clock_in_btn_text == 'Click on the icon above to clock-OUT':
            print('You are already Clocked in to Contactless EE')
            print("___________________")
        else:
            clock_in_btn.click()
            while True:
                if CEEDriver.current_url == 'https://cee-apac.exelatech.com/complete':
                    break
            print("Clock In successful!")
            print("___________________")
    elif choice == 2:
        print("Trying to Clock Out")
        if clock_in_btn_text == 'Click on the icon above to clock-IN':
            print('You are already Clocked Out from Contactless EE')
            print("___________________")
        else:
            clock_in_btn.click()
            while True:
                if CEEDriver.current_url == 'https://cee-apac.exelatech.com/complete':
                    break
            print("Clock Out successful!")
            print("___________________")
    print("Cleaning up.....")
    CEEDriver.quit()
    print('\t***-Thank you for using AutoPunchEla-***')
    sys.exit(0)
