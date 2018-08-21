import pyautogui
import time
import urllib.request 
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException



websitelogin = "https://login.yahoo.com/?.src=ym&.lang=en-US&.intl=us&.done=https%3A%2F%2Fmail.yahoo.com%2Fd"

#to read email list and proxies list
F = open("EmailListPsw.txt","r")
proxies = open("ProxyYahoo.txt","r")
list = F.readlines()
PROXY = proxies.readlines()
count = 0
countproxy = 0
#To clean the List !DO NOT REMOVE IT!
for word in list:
    if "\n" in word:
        list[count] = word[:len(word)-1]
    count+=1

for prox in PROXY:
    if "\n" in prox:
        PROXY[countproxy] = prox[:len(prox)-1]
    countproxy+=1
    
#!!!



def signINmail(username):
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('del')
    pyautogui.typewrite(username, interval=0.1)
    pyautogui.press('enter')
    return 0

def signINpsw(passw):
    pyautogui.typewrite(passw, interval=0.1)
    pyautogui.press('enter')
    return 0

def is_bad_proxy(pip):    
    try:        
        proxy_handler = urllib.request.ProxyHandler({'http': pip})        
        opener = urllib.request.build_opener(proxy_handler)
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)        
        req=urllib.request.Request('http://www.google.com')
        sock=urllib.request.urlopen(req)
    except urllib.request.HTTPError as e:        
        return e.code
    except Exception as detail:
        return 1
    return 0
    

def main(proxy, user, psw):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--proxy-server=http://%s' % proxy)
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(websitelogin)
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "username-country-code-field"))
        )
    finally:
        print("founded")
        signINmail(user)
        try:
            element_2 = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "password-challenge"))
            )        
        finally:
            print("Psw founded")
            signINpsw(psw)
            try:
                element_3 = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "spam-count"))
                )        
            finally:
                print("spam folder founded")
                bool =driver.find_elements_by_xpath('//*[@title="Spam - 0 emails"]')
                if(len(bool) > 0):
                    print("spam folder is Empty")
                    time.sleep(3)
                    driver.quit()
                    return 0
                else:
                    spam_x = 0
                    spam_y = 0
                    count_1 = 0
                    while(spam_x==0):
                        try:
                            spam_x,spam_y = pyautogui.locateCenterOnScreen('spamexist.png')
                        except TypeError:
                            spam_x = 0
                            count_1+=1
                            print(count_1)
                            if(count_1>=5):
                                sys.exit()
                    pyautogui.moveTo(spam_x,spam_y,2)
                    pyautogui.click()
                    x = 1
                    while(len(bool) == 0):
                        try:
                            element_4 = WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located((By.XPATH, '//*[@class="list-view-item-container ml-bg   "]'))
                            )
                        except TimeoutException:
                            break
                        finally:
                            print("spam folder elements founded")
                            #just ones
                            if(x):
                                pyautogui.press('down')
                                x=0
                            #Not spam
                            time.sleep(2)
                            pyautogui.press('enter')
                            Notspam_x = 0
                            Notspam_y = 0
                            count_2 = 0
                            while(Notspam_x==0):
                                try:
                                    Notspam_x,Notspam_y = pyautogui.locateCenterOnScreen('notSpamBtn.png')
                                except TypeError:
                                    Notspam_x = 0
                                    count_2+=1
                                    print(count_2)
                                    if(count_2>=5):
                                        sys.exit()
                            pyautogui.moveTo(Notspam_x,Notspam_y,2)
                            pyautogui.click()
                            pyautogui.moveTo(Notspam_x+50,Notspam_y+50,2)
                            time.sleep(1)
                            bool =driver.find_elements_by_xpath('//*[@title="Spam - 0 emails"]')
                    #Done with this email; NExT->
                    print("spam folder is Empty")
                    driver.quit()
                    return 0


###############

if __name__ == "__main__":
    NumProxy = 0
    for i in range(0,len(list),2):
        if(len(PROXY)>NumProxy):
            while(is_bad_proxy(PROXY[NumProxy])):
                print("Bad Proxy", PROXY[NumProxy])
                if(len(PROXY)>NumProxy):
                    NumProxy += 1
                else:
                    print("add more Proxies")
                    sys.exit()
            print("Proxy was fine")
            main(PROXY[NumProxy], list[i], list[i+1])
            NumProxy += 1
        else:
            print("add more Proxies")
            sys.exit()
        




    
    
