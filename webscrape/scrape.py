from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
import json

# Global Config
option = Options()
option.add_argument('window-size=800x841')
#option.add_argument('headless')
driver = webdriver.Edge(options=option)

url = 'https://eatigo.com/sg/singapore/en/view-all-a-z'
urls = 'https://eatigo.com/sg/singapore/en/r/ai-cafe-horne-road-5011786'


# Edit variable here
restaurantDict = {}
restaurantList = []  # store in list, output to json
nameList = [] 
locationList = []
imageList = []
ratingList = [] 
numOfRestaurant = 100  # set number of restaurant to scrape

class Restaurant():

    def __init__(self, driver, url) -> None:
        self.url = url
        self.driver = driver

    def startUrl(self):
        self.driver.get(self.url)

    def stopUrl(self):
        self.driver.close()


    def generateJSON(self, names, locations, images, ratings):
        restaurantList = [
            {"name": name, "location": location, "imageLink": imageLink, "rating": rating}
            for name, location, imageLink, rating in zip(names, locations, images, ratings)
        ]

        # Specify the output file name (change to your desired file name)
        filename = "restaurant_data.json"

        # Write the JSON data to the output file
        with open(filename, "w") as output_file:
            json.dump(restaurantList, output_file, indent=4)

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



    def nameLocationRating(self, url):

        for i in range(numOfRestaurant):
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
                WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, 'restaurant-section--header-info_rating')))

                # get all rating with the same class name
                rating = self.driver.find_element(By.CLASS_NAME, 'restaurant-section--header-info_rating').text
                
                ratingList.append(rating)

            except:
                print("skipping " + str(i))





restaurant = Restaurant(driver, url)
restaurant.nameLocationRating(url)
restaurant.generateJSON(nameList, locationList, imageList, ratingList)
restaurant.stopUrl()



# driver.get(urls)

# block = driver.find_element(By.CLASS_NAME, 'restaurant-section--header-info_rating').text
# print(block)

# driver.quit()
