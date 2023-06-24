from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchAttributeException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
from django.shortcuts import render
from django.http import HttpResponse
from bs4 import BeautifulSoup
import sys

import time

from selenium import webdriver



def index(request):
    return render(request, 'instabotapp/index.html')

def instareact(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        listofusernames = request.POST['listofusernames'].split(',')
        listoflocations = request.POST['listoflocations'].split(',')
        listofhashtags = request.POST['listofhashtags'].split(',')
        
        driver = webdriver.Chrome()  # Use appropriate WebDriver here
        driver.implicitly_wait(10)
        try:
            # Perform login using Selenium
            driver.get('https://www.instagram.com/accounts/login/')

            # # Find the login elements and enter the username and password
            username_input = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="username"]')))
            username_input.send_keys(username)

            password_input = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="password"]')))
            password_input.send_keys(password)

            # # Submit the form to log in
            login_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[type="submit"]')))
            login_button.click()
            
            try: 
                Notnow_2fadiv = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(),'Not Now')]")))
                Notnow_2fadiv.click()
                Notnow_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'Not Now')]")))
                Notnow_button.click()
            except Exception as e:
                print(f"An error occurred: {str(e)}")

            def performactionsonusernames(_username):
                # Enter username account
                driver.get(f'https://www.instagram.com/{_username}/')
                
                time.sleep(10)  # Add a small delay to allow the page to load

                try:

                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'h1')))
                    followers_link = driver.find_element(By.PARTIAL_LINK_TEXT, 'follower')
                    
                    followers_link.click()
                    time.sleep(10)
                    
                    followers_usernames_list = []
                    followers_list = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'x9f619') and contains(@class, 'xjbqb8w') and contains(@class, 'x1rg5ohu') and contains(@class, 'x168nmei') and contains(@class, 'x13lgxp2') and contains(@class, 'x5pf9jr')]")))
                    
                    time.sleep(10)

                    if len(followers_list) > 0:
                        for username in followers_list:
                            followers_usernames_list.append(username.text)
                            time.sleep(2)

                        showfollowersposts(followers_usernames_list)

                except Exception as e:
                    print(f"An error occurred: {str(e)}")
                
            def showfollowersposts(followers_usernames_list):
                for followerusername in followers_usernames_list:
                    driver.get(f'https:www.instagram.com/{followerusername}')
                    time.sleep(5)
                    count = 5
                    try:
                        followers_posts = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@href,'/p/') and contains(@role,'link')]")))
                        for post_like_btn in followers_posts:
                            post_href = post_like_btn.get_attribute('href')
                            driver.get(post_href)
                            time.sleep(10)
                            like_button = driver.find_element(By.XPATH, "//span/button[contains(@class,'_abl-') and contains(@type,'button')]")
                            like_button.click()
                            time.sleep(5)



                    except Exception as e:
                        # Handle the exception
                        print(f"An error occurred: {str(e)}")
                   
            def performactionsonhashtags(_hashtag):    
                
                try:
                    driver.get('https://www.instagram.com/explore/tags/{}/'.format(_hashtag))
                    time.sleep(15)
                    hashtagposts = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@href,'/p/') and contains(@role,'link')]")))
                    
                    for hashtagpost_link in hashtagposts:
                        hashtagpost_href = hashtagpost_link.get_attribute('href')
                        driver.get(hashtagpost_href)
                        # like
                        time.sleep(3)
                        driver.find_element(By.XPATH,"//span/button[contains(@class,'_abl-') and contains(@type,'button')]").click()
                        time.sleep(5)

                except Exception as e:
                    print(f"An error occurred: {str(e)}")


            def performactionsonlocations(_locationid):    
                
                    try:
                        driver.get('https://www.instagram.com/explore/locations/{}/'.format(_locationid))
                        time.sleep(15)
                        
                        locationposts = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@href,'/p/') and contains(@role,'link')]")))
                        
                        for locationpost_link in locationposts:
                            locationpost_href = locationpost_link.get_attribute('href')
                            driver.get(locationpost_href)
                            # like
                            time.sleep(3)
                            driver.find_element(By.XPATH,"//span/button[contains(@class,'_abl-') and contains(@type,'button')]").click()
                            time.sleep(5)

                    except Exception as e:
                        print(f"An error occurred: {str(e)}")


                    

            if len(listofusernames) != 0:
                for _username in listofusernames:
                    performactionsonusernames(_username)
            else:
                print(len(listoflocations))
            
            if len(listofhashtags) != 0:
                for _hashtag in listofhashtags:
                    performactionsonhashtags(_hashtag)
            else:
                print(len(listofhashtags))
                
            
            if len(listoflocations) != 0:
                for _locationid in listoflocations:
                    performactionsonlocations(_locationid)
            else:
                print(len(listoflocations))


            # Wait for the login process to complete (you can use a specific condition here)
            # WebDriverWait(driver, 20).until(EC.url_contains('/accounts/login/'))

            # Perform actions on Instagram after logging in
            # Example: Like a post
            # first_post = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='_9AhH0']")))
            # first_post.click()
            # like_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[@class='fr66n']/button")))
            # like_button.click()

    #  scp -r C:\xampp\htdocs\instabot root@185.211.4.40:/path/to/remote/directory

        except Exception as e:
            print(f"An error occurred: {str(e)}")

        # finally:
            # Close the WebDriver
            # driver.quit()

    return render(request, 'instabotapp/index.html')


