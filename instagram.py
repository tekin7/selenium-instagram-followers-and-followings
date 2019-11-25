from selenium import webdriver
from instagramUserInfo import username, password
from selenium.webdriver.common.keys import Keys
import time
#import argparse
from selenium.webdriver.chrome.options import Options

class instagram:
    def __init__(self,username,password):
        self.browserProfile = webdriver.ChromeOptions()
        self.browserProfile.add_experimental_option('prefs', {'intl.accept_languages':'en,en_US'})
        self.browserProfile.add_argument('--user-agent="Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 640 XL LTE) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Mobile Safari/537.36 Edge/12.10166"')
        self.browser = webdriver.Chrome('chromedriver.exe', chrome_options=self.browserProfile)
        self.username = username
        self.password = password
        
    def signIn(self):
        self.browser.get("https://www.instagram.com/accounts/login/")
        time.sleep(2)
        
        usernameInput =self.browser.find_element_by_name("username")
        passwordInput = self.browser.find_element_by_name("password")
        
        usernameInput.send_keys(self.username)
        passwordInput.send_keys(self.password)
        passwordInput.send_keys(Keys.ENTER)
        time.sleep(2)
        
    def getFollowers(self):
        self.browser.get(f"https://www.instagram.com/{self.username}")
        time.sleep(1)
        self.browser.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[2]/a").click()
        time.sleep(1)
        dialog = self.browser.find_element_by_css_selector("div[role=dialog] ul")
        followercount = len(dialog.find_elements_by_css_selector("li"))
        action = webdriver.ActionChains(self.browser)
        
        while True:
            dialog.click()
            action.send_keys(Keys.SPACE).perform()
            time.sleep(1)
            
            newcount = len(dialog.find_elements_by_css_selector("li"))
            
            if followercount != newcount :
                followercount = newcount
                print(f"second count : {newcount}")
                time.sleep(1)
            else:
                break
        
        
        followers = dialog.find_elements_by_css_selector("li")
        
        followerList = []
        
        for user in followers:
            link = user.find_element_by_css_selector("a").get_attribute("href")
            followerList.append(link)
            
        with open("followers.txt", "w", encoding ="UTF-8") as file:
            for item in followerList:
                file.write(item+ "\n")
                
    def following(self):
        time.sleep(1)
        self.browser.get(f"https://www.instagram.com/{self.username}")
        time.sleep(2)
        self.browser.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[3]").click()
        time.sleep(1)
        dialog = self.browser.find_element_by_css_selector("div[role=dialog] ul")
        followingcount = len(dialog.find_elements_by_css_selector("li"))
        action = webdriver.ActionChains(self.browser)
        
        while True:
            dialog.click()
            action.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
            time.sleep(2)
            newcount = len(dialog.find_elements_by_css_selector("li"))
            if followingcount != newcount :
                followingcount = newcount
                print(f"second count : {newcount}")
                time.sleep(1)
            else:
                break
            
            
        following = dialog.find_elements_by_css_selector("li")
        
        followingList = []
        
        for user in following:
            link = user.find_element_by_css_selector("a").get_attribute("href")
            followingList.append(link)
            
        with open("following.txt", "w", encoding ="UTF-8") as file:
            for item in followingList:
                
                file.write(item+ "\n")
                
                
parser = argparse.ArgumentParser(add_help=True)
parser.add_argument("-u", type=str, help="username")
parser.add_argument("-p", type=str, help="password")
args = parser.parse_args()   
    
instgrm = instagram(username,password)
instgrm.signIn()
instgrm.getFollowers()
instgrm.following()