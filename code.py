# Allows the reading of an online file.
import requests as re
# Enables a few of Selenium different tools.
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# For the final submission.
import json

resulting_dict = {}

# This function gets the online file and appends the titles into a list.
def titles_retriever(file):
    clean_titles = []
    read_url = re.get(file)
    with open('article_titles_for_home_test.txt', 'wb') as file:
        file.write(read_url.content)
    with open('article_titles_for_home_test.txt', 'r', encoding='utf-8') as text_file:
        titles = text_file.readlines()

    # Removes the '/n' (indicating line drop) from each string.
    for title in titles:
        clean_titles.append(title.rstrip('\n'))
    return clean_titles

# This function creates titles-ids pairs, and stores them in a dictionary.
def articles_ids(titles, link):
    list_of_titles = titles_retriever(titles)

    # Iterates over every title
    for title in range(len(list_of_titles)):
        try:  # Prevents a potential crash.

            # Uses 'Chrome' browser.
            options = webdriver.ChromeOptions()
            driver = webdriver.Chrome(options=options)

            driver.get(link)  # reads the url

            search_box = driver.find_element('name', 'term')  # Retrieved from the html code
            search_box.clear()  # The box will most likely be empty, but it's better to avoid any possible error
            search_box.send_keys(list_of_titles[title])  # Writes the titles in the search box
            search_box.send_keys(Keys.RETURN)  # Presses 'enter'

            try:
                # Makes sure the page is fully loaded.
                pubmed_id = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'current-id')))
                resulting_dict[list_of_titles[title]] = pubmed_id.text  # Pairs the key-value as requested
                driver.quit()
            except:
                # This covers the case we get a few results, and uses the first one (probably the most accurate one)
                try:
                    # Makes sure the page is fully loaded.
                    pubmed_id = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'docsum-pmid')))
                    resulting_dict[list_of_titles[title]] = pubmed_id.text  # Pairs the key-value as requested
                    driver.quit()

                # 0 results.
                except:
                    resulting_dict[list_of_titles[title]] = "no results for article title"
                    driver.quit()

        # Any unseen error.
        except:
            print('error')

    return resulting_dict

titles_file = # Insert the file's link here.
url = # Insert the url here.

# Executes the function with the provided links
articles_ids(titles_file, url)

# Saves the dictionary as a json file
with open('result.json', 'w') as json_file:
    json.dump(resulting_dict, json_file)
