from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import json
import time
import requests
import os
import delete_table

url = 'https://trendy-tiktok-api.herokuapp.com/trend-api/'

chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument('--headless')
#chrome_options.headless = True

driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
driver.create_options()

driver.get(os.getenv("TIKTOK_CREATIVE_CENTER_GERAL"))

#Config do mouse
mouse_driver = ActionChains(driver)

#Tratar a hastag vinda do site
def TratarHastag(hast):
    i = 0
    while hast[i] != '#':
        i+= 1
    hast = hast[i:]
    hast = "\n".join(hast.split("\n")[:1])
    hast = hast[:1] + '' + hast[1 + 1:]
    return hast

#Vincular as Foreigns Keys dos criadores as Hastags
def VincularForeignKeyHast(hastag):
    json_var = requests.get(url+'wsgeral/hastag').text
    inp_dict = json.loads(str(json_var))
    filtrar_por_id = [obj for obj in inp_dict if(obj['hastag'] == hastag)]
    return filtrar_por_id[0]['id']

#Vincular as Foreign Keys dos HotVideo do criador ao id do criador
def VincularForeignKeyCreator(creator):
    json_var = requests.get(url+'wsgeral/creator').text
    inp_dict = json.loads(str(json_var))
    filtrar_por_id = [obj for obj in inp_dict if(obj['creator'] == creator)]
    return filtrar_por_id[0]['id']





#Função que pega hastags e posta na API 
#NÃO CHAMAR ESSA FUNÇÃO
def PostHastag(quit_driver):
    i = 1
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="ccContentContainer"]/div[3]/div[2]/div/div[2]/div[1]/span[1]/span'))
        )
    finally:
        while i <= 5:
            data = {
                "hastag": TratarHastag(driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div[3]/div[2]/div/div[2]/div[2]/div['+str(i)+']').text),
                "position": driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div[3]/div[2]/div/div[2]/div[2]/div['+str(i)+']/div[1]/span').text,
            }
            requests.post(url+'wsgeral/hastag', json=data)
            i += 1
    if quit_driver == True:
        driver.quit()

#Funçao que pega os criadores das hastags e posta
def PostCreatorHastag(get_hast, quit_driver):
    try:
        if get_hast == True:
            try:
                delete_table.ApagarTabela(url+'wsgeral/hastag', url+'wsgeral/delete-hastag/')
                delete_table.ApagarTabela(url+'wsgeral/hastag-creator', url+'wsgeral/delete-hastag-creator/')
            finally:
                PostHastag(False)
        else: 
            element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="ccContentContainer"]/div[3]/div[2]/div/div[2]/div[1]/span[1]/span'))
        )
    finally:
        #config para pegar imagens
        back_ground_image_count = 20

        #Contadores
        i = 1
        j = 1
        
        while i <= 5:
            #Hastag dos criadores
            hast = TratarHastag(driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div[3]/div[2]/div/div[2]/div[2]/div['+str(i)+']').text)
            foreign_key = VincularForeignKeyHast(hast)

            while j <= 3:
                try:
                    #Elemento do criador
                    elmen = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div[3]/div[2]/div/div[2]/div[2]/div['+str(i)+']/div[4]/div/div['+str(j)+']/span/div')

                    #hover over element
                    mouse_driver.move_to_element(elmen).perform()
                    
                    #Pegar nome do criador
                    name = driver.find_element(By.XPATH, '/html/body/div['+str(back_ground_image_count)+']/div/div/div/div/span').text
                    back_ground_image_count += 1

                    #elemento da thumb
                    elm = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[2]/div[3]/div[2]/div/div[2]/div[2]/div['+str(i)+']/div[4]/div/div['+str(j)+']/span/div'))).value_of_css_property("background-image")

                    #Link da Thumb do criador
                    LinkThumb = elm.split('"')[1]

                    data = {
                        "hastag_creator_name": name,
                        "hastag_creator_thumbnail": LinkThumb,
                        "hastag_id": foreign_key
                    }
                    requests.post(url+'wsgeral/hastag-creator', json=data)
                    j += 1
                except NoSuchElementException:
                    pass
                    j += 1

            i += 1
            j = 1
    if quit_driver == True:
        driver.quit()
            
#Função que pega sons e posta na API
def PostSong(quit_driver):
    #Contador
    i = 1

    try:
        try:
            delete_table.ApagarTabela(url+'wsgeral/song', url+'wsgeral/delete-song/')
        finally:
            #Waiter
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[2]/div[3]/div[2]/div/div[2]/div[1]/span[2]/span'))
            )
    finally:
        #Clicar em "Songs"
        mouse_driver.click(driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div[3]/div[2]/div/div[2]/div[1]/span[2]/span')).perform()

        #Dormir por 4 segundos para dar tempo das imagens carregarem
        time.sleep(4)

        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="ccContentContainer"]/div[3]/div[2]/div/div[2]/div[2]/div[1]/div[2]/div[2]/div[1]/span'))
            )
        finally:
            while i <= 5:
                thumb = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div[3]/div[2]/div/div[2]/div[2]/div['+str(i)+']/div[2]/div[1]/img').get_attribute("src")
                song_title = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div[3]/div[2]/div/div[2]/div[2]/div['+str(i)+']/div[2]/div[2]/div[1]/span').text
                singer = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div[3]/div[2]/div/div[2]/div[2]/div['+str(i)+']/div[2]/div[2]/div[2]/div/span').text
                position = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div[3]/div[2]/div/div[2]/div[2]/div['+str(i)+']/div[1]/span').text
                data = {
                        "thumbnail": thumb,
                        "song_title": song_title,
                        "singer": singer,
                        "position": position
                    }
                post = requests.post(url+'wsgeral/song', json=data)
                i += 1
    if quit_driver == True:
        driver.quit()

#Função que pega os Criadores e posta na API
#NÃO CHAMAR ESSA FUNÇÃO
def PostCreators(quit_driver):
    i = 1
    
    try:
        #Waiter
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[2]/div[3]/div[2]/div/div[2]/div[1]/span[3]/span'))
        )
    finally:
        #Clicar em "Songs"
        mouse_driver.click(driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div[3]/div[2]/div/div[2]/div[1]/span[3]/span')).perform()

        #Dormir por 4 segundos para dar tempo das imagens carregarem
        time.sleep(4)

        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[2]/div[3]/div[2]/div/div[2]/div[2]/div[1]'))
            )
        finally:
            while i <= 5:
                creator = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div[3]/div[2]/div/div[2]/div[2]/div['+str(i)+']/div[1]/div/div[1]/span').text
                followers = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div[3]/div[2]/div/div[2]/div[2]/div['+str(i)+']/div[2]/div[1]/span[1]').text
                likes = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div[3]/div[2]/div/div[2]/div[2]/div['+str(i)+']/div[2]/div[2]/span[1]').text
                creator_profile_link = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div[3]/div[2]/div/div[2]/div[2]/div['+str(i)+']/div[1]/div/div[2]/a[2]').get_attribute('href')
                creator_thumbnail = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div[3]/div[2]/div/div[2]/div[2]/div['+str(i)+']/div[1]/a/img').get_attribute("src")
                data = {
                        "creator": creator,
                        "followers": followers,
                        "likes": likes,
                        "creator_profile_link": creator_profile_link,
                        "creator_thumbnail": creator_thumbnail
                    }
                post = requests.post(url+'wsgeral/creator', json=data)
                i += 1

    if quit_driver == True:
        driver.quit()

#Função que pega os videos hots do criador e posta na API
def PostCreatorHotVideo(get_creator, quit_driver):
    i = 1
    j = 1

    try: 
        try:
            delete_table.ApagarTabela(url+'wsgeral/creator', url+'wsgeral/delete-creator/')
            delete_table.ApagarTabela(url+'wsgeral/creator-hot-video', url+'wsgeral/delete-creator-hot-video/')
        finally:
            if get_creator == True:
                PostCreators(False)
            else: 
                #Waiter
                element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[2]/div[3]/div[2]/div/div[2]/div[1]/span[3]/span'))
                )
    finally:
        try:
            #Clicar em Creators 
            mouse_driver.click(driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div[3]/div[2]/div/div[2]/div[1]/span[3]/span')).perform()
            #Waiter
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[2]/div[3]/div[2]/div/div[2]/div[2]/div[1]'))
            )
        finally: 
            while i <= 5:
                #Criador atual
                criador = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div[3]/div[2]/div/div[2]/div[2]/div['+str(i)+']/div[1]/div/div[1]/span').text

                #Vincular id do hotvideo ao criador pela função VincularForeignKeyCreator()
                creator_id = VincularForeignKeyCreator(criador)

                while j <= 3:
                    creator_hot_video_views = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div[3]/div[2]/div/div[2]/div[2]/div['+str(i)+']/div[3]/div['+str(j)+']/div/span[2]').text
                    creator_hot_video_link = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div[3]/div[2]/div/div[2]/div[2]/div['+str(i)+']/div[3]/div['+str(j)+']/a').get_attribute('href')
                    creator_hot_video_thumbnail = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div[3]/div[2]/div/div[2]/div[2]/div['+str(i)+']/div[3]/div['+str(j)+']/img').get_attribute("src")
                    data = {
                            "creator_hot_video_views": creator_hot_video_views,
                            "creator_hot_video_link": creator_hot_video_link,
                            "creator_hot_video_thumbnail": creator_hot_video_thumbnail,
                            "creator_id": creator_id
                        }
                    post = requests.post(url+'wsgeral/creator-hot-video', json=data)
                    j += 1
                i += 1
                j = 1

    if quit_driver == True:
        driver.quit()

#Função que pega os vídeos do tiktok e posta na API
def PostVideo(quit_driver): 
    i = 1

    try:
        try:
            delete_table.ApagarTabela(url+'wsgeral/video', url+'wsgeral/delete-video/')
        finally:

            element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[2]/div[3]/div[2]/div/div[2]/div[1]/span[4]/span'))
                )
    finally:
        try:
            mouse_driver.click(driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div[3]/div[2]/div/div[2]/div[1]/span[4]/span')).perform()
            element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[2]/div[3]/div[2]/div/div[2]/div[2]/div[1]/div'))
                )
        finally:
            while i <= 5:
                thumbnail = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div[3]/div[2]/div/div[2]/div[2]/div['+str(i)+']/div/a').value_of_css_property("background-image").split('"')[1]
                link = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div[3]/div[2]/div/div[2]/div[2]/div['+str(i)+']/div/a').get_attribute('href')
                data = {
                            "thumbnail": thumbnail,
                            "link": link
                        }
                post = requests.post(url+'wsgeral/video', json=data)
                i += 1
    if quit_driver == True:
        driver.quit()



def PostAllTables():
    PostCreatorHastag(True, False)
    PostSong(False)
    PostCreatorHotVideo(True, False)
    PostVideo(True)

PostAllTables()