from bs4 import BeautifulSoup
import datetime
from random import randint
from random import shuffle
import requests
from time import sleep

def get_html(url):
    
    html_content = ''
    try:
        page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        html_content = BeautifulSoup(page.content, "html.parser")
    except: 
        pass
    
    return html_content

def get_details(url, category):
    
    stamp = {}
    
    try:
        html = get_html(url)
    except:
        return stamp

    try:
        price = html.select('#product-price')[0].get_text().strip()
        stamp['price'] = price.replace('$', '').replace(',', '').strip()
    except: 
        stamp['price'] = None
        
    try:
        title = html.select('#details .title')[0].get_text().strip()
        stamp['title'] = title
    except:
        stamp['title'] = None
        
    try:
        number = html.select('#quantity-available')[0].get_text().strip()
        stamp['number'] = number
    except:
        stamp['number'] = None        

    try:
        raw_text_cont = html.find_all('div', attrs={'itemprop':'description'})[0]
        raw_text = raw_text_cont.get_text().strip()
        stamp['raw_text'] = raw_text.replace('"',"'")
    except:
        stamp['raw_text'] = None  
        
    stamp['category'] = category     
    
    try:
        subcategory = html.select('.breadcrumb-item')[-1].get_text().strip()
        stamp['subcategory'] = subcategory
    except:
        stamp['subcategory'] = None      
        
    stamp['currency'] = 'USD'
    
    # image_urls should be a list
    images = []                    
    try:
        image_items = html.select('.img-thumbnail')
        for image_item in image_items:
            img = 'https://www.ipdastore.com' + image_item.get('src')
            if img not in images:
                images.append(img)
    except:
        pass
    
    stamp['image_urls'] = images 
        
    # scrape date in format YYYY-MM-DD
    scrape_date = datetime.date.today().strftime('%Y-%m-%d')
    stamp['scrape_date'] = scrape_date

    stamp['url'] = url
    print(stamp)
    print('+++++++++++++')
    sleep(randint(25, 65))
           
    return stamp

def get_page_items(url):
    
    items = []
    next_url = ''

    try:
        html = get_html(url)
    except:
        return items, next_url

    try:
        for item_cont in html.select('.card-title'):
            item_link = item_cont.select('a')[0].get('href')
            if item_link not in items:
                items.append(item_link)
    except:
        pass
    
    try:
        for next_item in html.select('.page-link'):
            next_item_text = next_item.get_text()
            if 'Next' in next_item_text:
                next_url = next_item.get('href')
                break
    except:
        pass
    
    shuffle(list(set(items)))
    
    return items, next_url

def get_categories():
    
    url = 'https://www.ipdastore.com/'
    
    items = {}

    try:
        html = get_html(url)
    except:
        return items

    try:
        for item_cont in html.select('.dropdown-menu .categories-item a'):
            item_link = item_cont.get('href')
            item_name = item_cont.get_text().strip()
            if item_link not in items: 
                items[item_name] = item_link
    except: 
        pass
    
    shuffle(list(set(items)))
    
    return items

categories = get_categories()
for category_name in categories:
    category = categories[category_name]
    page_url = category
    while(page_url):
        page_items, page_url = get_page_items(page_url)
        for page_item in page_items:
            stamp = get_details(page_item, category_name)

