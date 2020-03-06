#-*- coding:utf-8 -*-

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from os import getcwd, mkdir
from shutil import move
from os.path import isdir
from time import sleep, time
from click import clear 
from sys import exit as terminate
from datetime import timedelta


PrintInfo = lambda info: print(f'[Temp-Mail-Service] {info}') 


def CheckDIR():
    directory = f'{getcwd()}\\tmp_mail\\'
    if not isdir(directory):
        mkdir(directory)
    return directory


def CreateCHROPT():

    options = Options() 
    options.add_argument("--disable-notifications") 

    options.add_experimental_option("prefs", { 
        "download.default_directory": getcwd() + '\\tmp_mail', 
        "download.prompt_for_download": False, 
        "download.directory_upgrade": True, 
        "safebrowsing_for_trusted_sources_enabled": False, 
        "safebrowsing.enabled": False 
    })
    options.add_argument("log-level=3")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument('--disable-software-rasterizer') 
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-dev-shm-usage")


    options.add_argument('--headless') 
    options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36") 

    return options


if __name__ == "__main__":
    StartTime = int(time())
    TempDIR = CheckDIR()


    driver = Chrome('chromedriver.exe', options=CreateCHROPT())
    driver.get('https://www.fakemail.net/expirace/604800')


    TempMailAddress = driver.find_element_by_xpath('//*[@id="email"]').text
    mailCount = 0

    clear()
    PrintInfo("종료하려면 Ctrl-C 를 입력하세요.")
    PrintInfo("현재 임시 메일 주소 : " + TempMailAddress)
    while True:
        try:
            driver.get(f'https://www.fakemail.net/window/id/{mailCount+1}')
            
            try:
                if driver.find_element_by_tag_name('p').text == 'OOPS! - Could not Find it':
                    sleep(3)
                    driver.refresh()


            except ( NoSuchElementException ):
                driver.get(f'https://www.fakemail.net/download-email/{mailCount+1}')
                mailCount += 1


            finally:
                TimeRemain = 60*60*24*7 - (int(time())-StartTime)
                
                if TimeRemain <= 0:
                    PrintInfo('시간이 만료되었습니다. Temp-mail 서비스를 종료합니다.')
                    break

                else:
                    print(f'\r[Temp-Mail-Service] 남은시간: {timedelta(seconds=TimeRemain)}', end='\r')


        except ( KeyboardInterrupt, EOFError ):
            PrintInfo('키보드 방해가 감지되었습니다. Temp-mail 서비스를 종료합니다.')
            break


    try:
        move(TempDIR, f'./{TempMailAddress}_temp_mails/')
        driver.close()

    except:
        pass
    
    finally:
        PrintInfo(f'{getcwd()}\\{TempMailAddress}_temp_mails\\ 에 저장되었습니다.')
        terminate()
