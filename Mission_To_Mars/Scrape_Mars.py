#!/usr/bin/env python
# coding: utf-8

# In[35]:


from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import pymongo
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
from pprint import pprint


# In[44]:
def scrape():


    #Splinter Setup
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)


    # In[6]:


    #NASA Mars News

    #Retrieve webpage and create an object
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html= browser.html

    response = requests.get(url)
    soup = bs(response.text, 'lxml')


    # In[7]:


    #Scrape site for news title and paragraph text
    news_heading = soup.find_all('div', class_="content_title")[1].text
    news_snip = soup.find("div", class_="rollover_description_inner").text

    # In[8]:


    #Mars Facts
    url = 'https://space-facts.com/mars/'


    # In[9]:


    #Retrieve webpage and create an object
    response = requests.get(url)
    soup = bs(response.text, 'lxml')


    # In[10]:


    #Convert the HTML into a df
    info_df = pd.read_html(url)
    mars_df = info_df[0]
    mars_df


    # In[11]:


    #Convert df to HTML table string
    htmltbl = mars_df.to_html()
    htmltbl.replace('\n','')


    # In[45]:


    #Mars Hemispheres
    image_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    main_url = 'https://astrogeology.usgs.gov'


    # In[46]:


    #Splinter Setup
    browser.visit(image_url)


    # In[47]:


    #Create object and parse
    html= browser.html
    soup = bs(html,'lxml')


    # In[48]:


    #Scrape the site for all mars info
    hemisphere = soup.find_all('div', class_="item")

    #Empty list full link
    all_info =[]

    for i in hemisphere:
        #find title
        title = i.find('h3').text
        browser.click_link_by_partial_text(title)
        title = title.strip("Enhanced")

        html= browser.html
        soup = bs(html,'lxml')
        
        img_url= soup.find("div", class_="downloads").find("ul").find('a')['href']
            
        marsdict={'title':title, 'img_url': img_url}
        all_info.append(marsdict)
        
        browser.back()
        
    browser.quit()

    #Create dict to scraped info
    output = {"newstitle":news_heading, "newspara":news_snip, "mfacts":htmltbl,"hemi":all_info}
    return output

