import requests

import time
from bs4 import BeautifulSoup
import os
from selenium import webdriver

import pprint

import face_recognition
import concurrent.futures

user = 'sadikbot123'
passw = 'happy12345'
google_api = 'AIzaSyD2WFZcHj_ghcrTUD5HKOdezXrnk-HdzlE'

def insta_scrape(username):

    #Use Selenium to grab page source
    #Navigate to instagram page
    try:
        driver = webdriver.Chrome('/Users/vinhyard/Desktop/projects/Hacker/emailspam/chromedriver')
        driver.get(f'https://www.instagram.com/{username}/')
        time.sleep(3)

        driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input').send_keys(user)

        driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input').send_keys(passw)

        driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]').click()


        time.sleep(8)


        #Login
        driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input').send_keys(username)

        time.sleep(1)

        driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/div[3]/div/div[2]/div/div[1]/a/div').click()
    except:

        pass


    time.sleep(18)
    driver.implicitly_wait(30)
    #Parse page source
    soup = BeautifulSoup(driver.page_source, 'lxml')


    #Find the name of the instagram user
    insta_user = driver.find_element_by_class_name('rhpdm').text


    #Create a folder with the name of instagram user
    os.mkdir('./Known/'+ username)

    #Initialize count variable
    count = 0

    time.sleep(18)

    driver.implicitly_wait(30)

    #Find all images on the page
    img = soup.findAll("img", class_="FFVAD")

    #Check to see if user has posts on instagram page
    if len(img) != 0:

        for i, image in enumerate(img):

            try:
                image_link = image['data-srcset']

            except:

                try:
    
                    image_link = image['data-src']

                except:

                    try:

                        image_link = image['data-fallback-src']

                    except:

                        try:

                            image_link = image['src']

                        except:

                            pass


            try:
                r = requests.get(image_link).content

                try:

                    r = str(r, 'utf-8')

                except UnicodeDecodeError:
                #write image to folder
                    with open(f"./Known/{username}/{insta_user}{i+1}.jpg", "wb+") as f:

                        f.write(r)


                    count += 1

            except:

                pass




        driver.close()
        
        if count == len(img):

            return "All images downloaded"

        else:

            return 'Download failed'
         





#Facial-Recognition


def facial_rec(username):

    path = f'/Users/vinhyard/Desktop/Instacrawl/Known/{username}'

    unknown_face = face_recognition.load_image_file(f'/Users/vinhyard/Desktop/Instacrawl/Unknown/kimk.jpg')
    unknown_face_encoding = face_recognition.face_encodings(unknown_face)[0]
    folder = os.fsencode(path)
    match_found = 0

    not_match = 0
    for file in os.listdir(folder):

        filename = os.fsdecode(file)
        
        known_face = face_recognition.load_image_file(path+'/'+filename)
        
        try:
            known_face_encoding = face_recognition.face_encodings(known_face)[0]
            
            try:
                results = face_recognition.compare_faces([known_face_encoding], unknown_face_encoding)

                if results[0]:

                    match_found += 1
                else:
                    not_match += 1
            except:

                pass
            
        except:

            pass

    if match_found > not_match:

        print(f'Unknown person is {username}')

        return True

    elif match_found < not_match:

        print(f'Unknown person is not {username}')

        return False
    else:

        print(f'Face Recognition Inconclusive for {username}')

        return False




#multi-process img scrape

def multiprocess_download(username_list):

    with concurrent.futures.ProcessPoolExecutor() as executor:
        time.sleep(.5)
        results = executor.map(insta_scrape, username_list)






#facial features

#ask_account = str(input('Enter an Instagram Username: '))
if __name__ == '__main__':

    s = ['kyliejenner', 'kimkardashian'] 
    


    multiprocess_download(s)

    time.sleep(5)


    for i in range(len(s)):
        facial_rec(s[i])

        


