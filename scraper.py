from bs4 import BeautifulSoup
from selenium import webdriver
from os import mkdir,rmdir
from sys import exit
from time import sleep
from requests import get

def createFolder(download_location:str) -> None:
    """
    Creates a folder in the same directory as this program
    You might want to run this in Downloads
    """
    try:
        mkdir(download_location)
        return None
    except Exception as e:
        print(str(e))
        print(f"folder {download_location} already exists, exiting")
        sleep(5)
        exit()

def downloadImages(image_tags:list, folder:str) -> None:
    for image in image_tags:
        print(image)
        url = str(image).split("src=\"")[1].split("\"")[0]
        print(url)
        data = get(url).content
        path = folder + "/" + url.split("/")[-1]
        with open(path, "wb") as f:
            f.write(data)

def main():
    url = input("Please enter the url you want to scrape for photos: ")
    folder_name = url.replace(".","").replace("/","").replace("\"","").replace(":","")
    createFolder(folder_name)

    try:
        browser = webdriver.Firefox()

        browser.get(url)
        sleep(10)
        for _ in range(10):
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(1)
        

        scraper = BeautifulSoup(browser.page_source,"html.parser")
        images = scraper.find_all("img",{"class": "sm-image"})

        print("total images found: " + str(len(images)))

        downloadImages(images,folder_name)
    except:
        rmdir(folder_name)
    finally:
        browser.close()

        

main()