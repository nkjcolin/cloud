from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
import json
import threading

# Global Config
option = Options()
option.add_argument('window-size=800x841')
#option.add_argument('headless')
driver = webdriver.Edge(options=option)

url = 'https://eatigo.com/sg/singapore/en/view-all-a-z'

# Edit variable here
restaurantDict = {}
restaurantList = []  # store in list, output to json
nameList = [] 
locationList = []
imageList = []
ratingList = []
numOfRatingList = []
descriptionList = []
reviewList = [] 
startRange = 200
numOfRestaurant = 250  # set number of restaurant to scrape

class Restaurant():

    def __init__(self, driver, url) -> None:
        self.url = url
        self.driver = driver

    def startUrl(self):
        self.driver.get(self.url)

    def stopDriver(self):
        self.driver.close()


    def generateJSON(self, names, locations, images, ratings, numOfRatings, descriptions, reviews):
        restaurantList = [
            {"name": name, 
             "location": location, 
             "imageLink": imageLink, 
             "rating": rating, 
             "numOfRating": numOfRating, 
             "description": description, 
             "review": review
             }
            for name, 
                location, 
                imageLink, 
                rating, 
                numOfRating, 
                description, 
                review 
                in zip(names, 
                       locations, 
                       images, 
                       ratings, 
                       numOfRatings, 
                       descriptions, 
                       reviews
                       )
        ]

        # Specify the output file name (change to your desired file name)
        filename = "restaurant_data.json"
        json_data = json.dumps(restaurantList, ensure_ascii=False, indent=7)

        # Write the JSON data to the output file
        with open(filename, "w", encoding='utf-8') as output_file:
            output_file.write(json_data)

        print(f"Data written to {filename}")


    def nameAndLocation(self, url):
        
        self.driver.get(url)

        for i in range(numOfRestaurant):
            # get all info with the same class name
            block = self.driver.find_elements(By.CLASS_NAME, 'minimal-card__info')

            # get all image link with the same class name
            image = self.driver.find_elements(By.CLASS_NAME, 'minimal-card__thumb')

            place = block[i].find_element(By.CLASS_NAME, 'minimal-card__title').text            # get text value
            location = block[i].find_element(By.CLASS_NAME, 'minimal-card__description').text   # get text value
            imageLink = image[i].find_element(By.TAG_NAME, 'img').get_attribute('src')          # get value in src

            nameList.append(place)
            locationList.append(location)
            imageList.append(imageLink)



    def rating(self, url):

        for i in range(numOfRestaurant):
            self.driver.get(url)
            WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, 'minimal-card__title')))
            block = self.driver.find_elements(By.CLASS_NAME, 'minimal-card__info')
            try:
                place = block[i].find_element(By.CLASS_NAME, 'minimal-card__title').click()
                WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, 'restaurant-section--header-info_rating')))

                # get all rating with the same class name
                rating = self.driver.find_element(By.CLASS_NAME, 'restaurant-section--header-info_rating').text
                ratingList.append(rating)

            except:
                print("skipping " + str(i))


    def nameLocationRatingDesc(self, url):

        for i in range(startRange,numOfRestaurant):
            self.driver.get(url)
            WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, 'minimal-card__title')))

            block = self.driver.find_elements(By.CLASS_NAME, 'minimal-card__info')
            image = self.driver.find_elements(By.CLASS_NAME, 'minimal-card__thumb')

            try:
                place = block[i].find_element(By.CLASS_NAME, 'minimal-card__title').text            # get text value
                location = block[i].find_element(By.CLASS_NAME, 'minimal-card__description').text   # get text value
                imageLink = image[i].find_element(By.TAG_NAME, 'img').get_attribute('src')          # get value in src

                nameList.append(place)
                locationList.append(location)
                imageList.append(imageLink)

                place = block[i].find_element(By.CLASS_NAME, 'minimal-card__title').click()

                self.getRating()
                self.getDescription()
                self.getReview()
                

            except:
                print("skipping " + str(i))

    def getRating(self):
        WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, 'restaurant-section--header-info_rating')))
        rating = self.driver.find_element(By.CLASS_NAME, 'restaurant-section--header-info_rating').text
        ratingList.append(rating)

    def getDescription(self):
        WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/div[1]/section/div[4]/div[1]/div[2]')))
        block = self.driver.find_element(By.XPATH, '/html/body/div[1]/main/div[1]/section/div[4]/div[1]/div[2]')
        block.click()
        WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/div[1]/section/div[4]/div[3]/div[1]/p')))
        desc = self.driver.find_element(By.XPATH, '/html/body/div[1]/main/div[1]/section/div[4]/div[3]/div[1]/p').text
        descriptionList.append(desc)

    def getReview(self):
        perReview = []
        WebDriverWait(self.driver, 1).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/div[1]/section/div[4]/div[1]/div[3]')))
        block = self.driver.find_element(By.XPATH, '/html/body/div[1]/main/div[1]/section/div[4]/div[1]/div[3]')
        block.click()
        WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/div[1]/section/div[4]/div[4]/div[1]/div[2]/div[1]/div[3]')))
        num = self.driver.find_element(By.XPATH, '/html/body/div[1]/main/div[1]/section/div[4]/div[4]/div[1]/div[2]/div[1]/div[3]').text
        numOfRatingList.append(num)

        WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, 'restaurant-content--tabs-feedback-comment--item')))
        reviews = self.driver.find_elements(By.CLASS_NAME, 'restaurant-content--tabs-feedback-comment--text')
        for review in reviews:
            perReview.append(review.text)
        
        reviewList.append(perReview)





restaurant = Restaurant(driver, url)
restaurant.nameLocationRatingDesc(url)
restaurant.generateJSON(nameList, locationList, imageList, ratingList, numOfRatingList, descriptionList, reviewList)
restaurant.stopDriver()





# driver.get(urls)
# block = driver.find_element(By.CLASS_NAME, 'restaurant-section--header-info_rating').text
# print(block)
# driver.quit()
