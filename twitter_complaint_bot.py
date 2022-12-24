import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


#initialize global variables
PROMISED_DOWN = 600
PROMISED_UP = 0
PATH = '~/.local/bin/chromedriver'
OPTIONS = Options()
OPTIONS.add_experimental_option("detach", True)
DRIVER = webdriver.Chrome(PATH, options=OPTIONS)
TWITTER_EMAIL = os.getenv('TWITTER_EMAIL')
TWITTER_UNAME = os.getenv('TWITTER_UNAME')
TWITTER_PW = os.getenv('TWITTER_PW')


class InternetSpeedTwitterBot:
    def __init__(self, driver_path):
        self.driver = DRIVER
        self.up = 0
        self.down = 0


    def get_internet_speed(self):
        '''Obtain relevant internet speed data.'''
        self.driver.get("https://www.google.com/search?client=firefox-b-1-e&q=speed+test")
        run_speed_test = self.driver.find_element(By.XPATH, '//*[@id="knowledge-verticals-internetspeedtest__test_button"]/div')
        run_speed_test.click()

          
        sleep(20)
        self.up = self.driver.find_element(By.XPATH, '//*[@id="knowledge-verticals-internetspeedtest__download"]/p[1]').text
        self.down = self.driver.find_element(By.XPATH, '//*[@id="knowledge-verticals-internetspeedtest__upload"]/p[1]').text

    
    def tweet_at_provider(self):
        '''Send tweet about poor internet speeds.'''
        self.driver.get("https://twitter.com/login")
        sleep(4)

        email = self.driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input')
        email.send_keys(TWITTER_EMAIL)
        email.send_keys(Keys.ENTER)
        sleep(2)

        enter_twitter_username = self.driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input')
        sleep(2)
        enter_twitter_username.send_keys(TWITTER_UNAME)
        enter_twitter_username.send_keys(Keys.ENTER)
        sleep(3)

        password = self.driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input')
        password.send_keys(TWITTER_PW)
        password.send_keys(Keys.ENTER)
        sleep(6)

        tweet_compose = self.driver.find_element(By.CLASS_NAME, 'public-DraftStyleDefault-block')
        tweet = f"~TEST~ Hey Internet Provider, why is my internet speed {self.down}down/{self.up}up when I pay for {PROMISED_DOWN}down/{PROMISED_UP}up?"
        tweet_compose.send_keys(tweet)
        sleep(4)

        tweet_button = self.driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[3]/div/div/div[2]/div/div/span/span')
        tweet_button.click()
        sleep(3)
        self.driver.quit()
        

#create bot from InternetSpeedTwitterBot Class
BOT = InternetSpeedTwitterBot(PATH)


#initiate program functionality
try:
    BOT.get_internet_speed()
    BOT.tweet_at_provider()

except KeyboardInterrupt:
    print('See you later.')