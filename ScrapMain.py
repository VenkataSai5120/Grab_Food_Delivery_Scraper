import requests
from bs4 import BeautifulSoup
import json
import time
import RestaurantList
from selenium import webdriver

# Function to scrape restaurant data from Grab's website
def scrape_restaurants():
    # URL of the Grab's restaurants page
    url = "https://food.grab.com/sg/en/restaurants"

    driver = webdriver.Chrome()
    driver.get(url)
    last_height = driver.execute_script("return document.body.scrollHeight")
    print(last_height)
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(15)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    
    # Get the HTML source from Selenium's WebDriver
    html_source = driver.page_source

    # Print the HTML source to check if it's obtained correctly
    # print(html_source)

    # Parsing the HTML source with BeautifulSoup
    soup = BeautifulSoup(html_source, "html.parser")

    # Finding the script tag containing the data we need
    script_tag = soup.find("script", id="__NEXT_DATA__")
    
    # Check if the script tag exists and has content
    if script_tag:
        # Extracting the content of the script tag
        script_content = script_tag.string.strip()

        # Writing the script content to a JSON file
        with open('resultJSON.json', 'w', encoding='utf-8') as json_file:
            json_file.write(script_content)
        
        # Logging that scraping is finished
        print("Grabber has finished scraping")
        
        # Adding a delay before calling RestaurantList.main()
        print("Waiting for 5 seconds before making the Restaurant List...")
        time.sleep(5)
        
        # Calling the main function from RestaurantList module to process the scraped data
        RestaurantList.main()
    else:
        # Logging an error if the script tag is not found
        print("Error: Script tag with id='__NEXT_DATA__' not found.")

    # Close the WebDriver instance to release resources
    driver.quit()

# Entry point of the script
if __name__ == "__main__":
    # Calling the main scraping function
    scrape_restaurants()

# import requests
# from bs4 import BeautifulSoup
# import json
# import time
# import RestaurantList
# from selenium import webdriver

# # Function to scrape restaurant data from Grab's website
# def scrape_restaurants():
#     # Read proxies from proxies_list.txt
#     with open('proxies_list.txt', 'r') as f:
#         proxies = f.readlines()

#     # Loop through proxies
#     for proxy in proxies:
#         proxy = proxy.strip()  # Remove leading/trailing whitespace
#         chrome_options = webdriver.ChromeOptions()
#         chrome_options.add_argument('--proxy-server=%s' % proxy)

#         # URL of the Grab's restaurants page
#         url = "https://food.grab.com/sg/en/restaurants"

#         try:
#             driver = webdriver.Chrome(options=chrome_options)
#             driver.get(url)
#             last_height = driver.execute_script("return document.body.scrollHeight")
#             print(last_height)
#             while True:
#                 driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#                 time.sleep(15)
#                 new_height = driver.execute_script("return document.body.scrollHeight")
#                 if new_height == last_height:
#                     break
#                 last_height = new_height
            
#             # Get the HTML source from Selenium's WebDriver
#             html_source = driver.page_source

#             # Parsing the HTML source with BeautifulSoup
#             soup = BeautifulSoup(html_source, "lxml")

#             # Finding the script tag containing the data we need
#             script_tag = soup.find("script", id="__NEXT_DATA__")
            
#             # Check if the script tag exists and has content
#             if script_tag:
#                 # Extracting the content of the script tag
#                 script_content = script_tag.string.strip()

#                 # Writing the script content to a JSON file
#                 with open('resultJSON.json', 'w', encoding='utf-8') as json_file:
#                     json_file.write(script_content)
                
#                 # Logging that scraping is finished
#                 print("Grabber has finished scraping")
                
#                 # Adding a delay before calling RestaurantList.main()
#                 print("Waiting for 5 seconds before making the Restaurant List...")
#                 time.sleep(5)
                
#                 # Calling the main function from RestaurantList module to process the scraped data
#                 RestaurantList.main()
#                 break  # Break the loop if successful
#             else:
#                 # Logging an error if the script tag is not found
#                 print("Error: Script tag with id='__NEXT_DATA__' not found.")

#         except Exception as e:
#             print(f"Proxy {proxy} failed. Trying next one...")
#             continue  # Try next proxy

#         finally:
#             if 'driver' in locals():
#                 driver.quit()

# # Entry point of the script
# if __name__ == "__main__":
#     # Calling the main scraping function
#     scrape_restaurants()
