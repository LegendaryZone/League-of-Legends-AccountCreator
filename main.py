from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.chrome.options import Options
import string
from random import *
import random
import requests
from pprint import pprint
import json
options = Options()
options.add_argument('no-sandbox')
options.add_argument('headless')
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Enable Debugging~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
debuggingi = input('Debugging? (y/n): ')
if debuggingi == 'y' or debuggingi == 'Y':
    debugging = 'enabled'
else:
    debugging = 'disabled'

def asterisks(x):
    xa = ''
    for i in range(len(x)):
      xa += '*'
    return xa
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Enter your 2Captcha Key~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
api_key = input('Enter your 2Captcha API Key: ')
if debugging == 'enabled':
    api_key = ''
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~AURORA-BOT USERNAME & PASSWORD DECLARATION~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print('Would you like your accounts to be ported to Aurora?')
print('[1] Yes')
print('[2] No')
ans = input('Type the number of your choice: ')
if ans == '1':
    aurorausername = input('Type your Aurora-Bot username: ')
    aurorapassword = input('Type your Aurora-Bot password: ')
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~SERVER SELECTION & USER INPUT~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print("Select Server from one of the following:")
print("[1] EUN")
print("[2] EUW")
print("[3] NA")
CH = input("Type the number of the server you desire: ")
print(" ")
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Iteration Selection~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
accounts = input('Account Number: ')
print()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Combo Creation~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def combocr():
    f = open("userpass.txt", "a")
    combos = {"1": "EUN", "2": "EUW", "3": "NA"}
    f.write(combos[CH] + ':' + tempuser + ":" + temppass + "\n")
    return 'Combo Created'
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Main Program~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
account_number = 0
for account in range(int(accounts)):
    account_number = account_number + 1
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Account Number: ', account_number,'~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    def emailgen():
        lines = open('emails.txt').read().splitlines()
        line =random.choice(lines)
        tempuser = username_grabber()
        email = tempuser + '@' + line
        print('E-Mail = ', asterisks(tempuser) +'@' + line)
        return email
    def username_grabber():
        characters = string.ascii_letters
        username = "".join(choice(characters) for x in range(randint(6, 13)))
        return username
    def passwordgen():
        characters = string.ascii_letters + string.digits
        for x in range(len(characters)):
            if x != string.digits:
                characters = string.ascii_letters + string.digits
        password = "".join(choice(characters) for x in range(randint(7, 15)))
        password += choice(string.digits)
        return password
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Drivers~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    driver = webdriver.Chrome(options= options)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~URL Picking~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    url = ""
    cookie = " "
    if CH == '1':
        url = "https://signup.eune.leagueoflegends.com/en/signup/"
        mainurl = "https://signup.eune.leagueoflegends.com/en/signup/"
        print('Server = EUNE')
        region = 'EUN1'
    elif CH == '2':
        url = "https://signup.euw.leagueoflegends.com/en/signup/"
        print('Server = EUW')
        mainurl = "https://signup.euw.leagueoflegends.com/en/signup/"
        region = 'EUW1'
    elif CH == '3':
        url = "https://signup.na.leagueoflegends.com/en/signup/"
        mainurl = "https://signup.na.leagueoflegends.com/en/signup/"
        print('Server = NA')
        region = 'NA1'
    driver.get(url)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Field Completion~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    email = emailgen()
    mail = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.NAME, 'email')))
    mail = driver.find_element_by_name('email').send_keys(email)
    driver.find_element_by_class_name('next-button').click()
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div/div[2]/div[1]/form/div[1]/div[2]/select/option[9]')))
    driver.find_element_by_xpath("/html/body/div[3]/div/div/div[2]/div[1]/form/div[1]/div[2]/select/option[9]").click()
    driver.find_element_by_xpath("//select[@name='dob-month']//option[3]").click()
    driver.find_element_by_xpath("//select[@name='dob-year']//option[contains(text(),'1993')]").click()
    driver.find_element_by_xpath("//button[contains(text(),'next')]").click()
    tempuser = email.split('@')[0]
    temppass = passwordgen()
    print('Username = ', asterisks(tempuser))
    print('Password = ', asterisks(temppass))
    combocr()
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.NAME, 'username')))
    driver.find_element_by_name('username').send_keys(tempuser)
    driver.find_element_by_name('password').send_keys(temppass)
    driver.find_element_by_name('confirm_password').send_keys(temppass)
    driver.find_element_by_css_selector('#root > div > div > div.registration-component.scene-component.mounted > div.scene-content > form > div:nth-child(4) > label > div').click()
    driver.find_element_by_css_selector("#root > div > div > div.registration-component.scene-component.mounted > div.scene-content > form > div.next-button > button").click()
    print('Acquiring Token..')
    time.sleep(0.3)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Captcha Key~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    url=driver.find_element_by_css_selector("iframe[role='presentation']").get_attribute('src')
    keygoogle = url[52:92]
    if debugging == 'enabled':
        print(keygoogle)
    driver.close()
    driver.quit()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Captcha Solve~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    answer = ""
    answer_id = 0
    data_post = {'key': api_key, 'method': 'userrecaptcha', 'googlekey': keygoogle, "pageurl": mainurl}
    response = requests.post(url = 'https://2captcha.com/in.php', data = data_post )
    response = response.text[3:]
    print("Waiting for server response.")
    for x in range(30):
        time.sleep(1)
        if x == 8:
            print('Downloading info..')
        elif x == 15:
            print('Processing info..')
    data_request = {'key': api_key,'id': int(response),'action': 'get'}
    response = requests.get(url='https://2captcha.com/res.php', params=data_request)
    token = response.text[3:]
    ctr = 0
    while response.text == 'CAPCHA_NOT_READY':
        time.sleep(5)
        print('Waiting for Captcha..', '[',ctr,']', 'seconds passed')
        ctr = ctr + 5
        response = requests.get(url='https://2captcha.com/res.php', params=data_request)
        token = response.text[3:]
    if debugging == 'enabled':
        print(token)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~REQUEST TO RIOT SIGNUP API ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    request_body = {
        'username': tempuser,
        'password': temppass,
        'confirm_password': temppass,
        'date_of_birth': '1985-07-07',
        'email': email,
        'tou_agree': True,
        'newsletter': False,
        'region': region,
        'campaign': 'league_of_legends',
        'locale': 'en',
        'token': 'Captcha {}'.format(token),
    }
    api_url = 'https://signup-api.leagueoflegends.com/v1/accounts'
    json_data = json.dumps(request_body)
    responselol = requests.post(url=api_url, data=json_data, headers={'Content-Type': 'application/json'})
    if debugging == 'enabled':
        #pprint(json.loads(responselol.text))
        break
    if responselol.ok:
        print('Account Successfully Created')
    else:
        account_number = account_number - 1
        print('Account Was Not Successfully Created, Retrying..')
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~PORT TO AURORA~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
driveraccport = webdriver.Chrome(options=options)
time.sleep(2)
def accountport():
    with open('userpass.txt') as combos:
        combo = combos.readline()
        cnt = 1
        while combo:
            combo = combos.readline()
            print('~~~~Importing Account Number: ', cnt, ' ~~~~')
            cnt += 1
            driveraccport.find_element_by_xpath("//textarea[1]").send_keys(combo)
    driveraccport.find_element_by_xpath("//input[@placeholder='Your aurorabot password']").send_keys(aurorapassword)
    driveraccport.find_element_by_xpath("//button[contains(text(),'Create')]").click()
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Account Port = Successful ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    return
if ans == '1':
    url = 'https://aurora-bot.com/'
    time.sleep(1)
    driveraccport.get(url)
    WebDriverWait(driveraccport, 30).until(EC.presence_of_element_located((By.XPATH, "//input[@name='username']")))
    driveraccport.find_element_by_xpath("//input[@name='username']").send_keys(aurorausername)
    driveraccport.find_element_by_xpath("//input[@name='password']").send_keys(aurorapassword)
    driveraccport.find_element_by_xpath("//button[@class='rs-btn rs-btn-primary']").click()
    WebDriverWait(driveraccport, 30).until(EC.presence_of_element_located((By.XPATH, "//i[@class='rs-icon rs-icon-user-info']")))
    driveraccport.find_element_by_xpath("//i[@class='rs-icon rs-icon-user-info']").click()
    WebDriverWait(driveraccport, 30).until(EC.presence_of_element_located((By.XPATH, "//input[@name='password']")))
    driveraccport.find_element_by_xpath("//input[@name='password']").send_keys(aurorapassword)
    time.sleep(0.1)
    driveraccport.find_element_by_xpath("//button[contains(text(),'unlock')]").click()
    time.sleep(0.5)
    driveraccport.find_element_by_xpath("//button[contains(text(),'Add accounts')]").click()
    accountport()

end = '''
  _____                  _          _  ___          _ 
 / ____|                | |        | |/ (_)        (_)
| (___  _ __   ___  __ _| | ___   _| ' / ___      ___ 
 \___ \| '_ \ / _ \/ _` | |/ / | | |  < | \ \ /\ / / |
 ____) | | | |  __/ (_| |   <| |_| | . \| |\ V  V /| |
|_____/|_| |_|\___|\__,_|_|\_\\__, |_|\_\_| \_/\_/ |_|
                               __/ |                  
                              |___/                   
'''
print(end)