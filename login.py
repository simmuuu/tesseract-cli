'''
Opens a Browser for the User to Login. Returns a UserData on success.
'''

from seleniumwire import webdriver
import chromedriver_autoinstaller
from db.dbPy import setDB
from yaspin import yaspin
import time
import json


def login(sp):
    sp.start()
    sp.text = "Loading Browser"
    
    try:
        chromedriver_autoinstaller.install()
    except ValueError as e:
        if "No chrome executable found" in str(e):
            sp.fail("❌ Chrome is missing. Please install Chrome to continue!")
            print("Chrome is missing. Please install Chrome to continue!")
            exit(1)
            
    driver = webdriver.Chrome()
    driver.maximize_window()
    
    url = 'https://tesseractonline.com/'
    driver.get(url)
    

    while driver.current_url != "https://tesseractonline.com/student":
        time.sleep(1)
        
    for request in driver.requests:
        if request.response:
            if request.url == "https://api.tesseractonline.com/auth/login":
                response_payload = request.response.body.decode('utf-8')
                user_details = json.loads(response_payload)
                
    setDB(user_details)
    sp.ok("✔️ Login Successful!")
    time.sleep(3)
    return 0
    
def Login():
    sp = yaspin()
    # try:
    login(sp)
    # except:
    #     sp.fail("❌ An Error has occured!")
    #     exit(1)