import requests
from bs4 import BeautifulSoup
import csv

def get_html(url):
    response = requests.get(url)
    return response.text 

def get_total_pages(html):  #сколько страниц с объявлениями выдается по запросу (для числа повторов цикла в main)
    soup = BeautifulSoup(html,'lxml')
    pages = soup.find('div', class_ = 'pagination-root-2oCjZ').find_all('span', class_ = 'pagination-item-1WyVp')[-2]
    return int(pages.text)

def get_page_data(html): #извлечение названия объявления, ссылки, цены
    soup = BeautifulSoup(html, 'lxml')
    ads = soup.find('div',class_='js-catalog_serp').find_all('div',class_='snippet-horizontal item item_table clearfix js-catalog-item-enum item-with-contact js-item-extended')
    for ad in ads:        
        try:
            title = ad.find('h3',class_='snippet-title').text.strip()        
        except:
            title = ''        
        try: #приведение укороченной ссылки на объявление к полному виду
            link = 'https://avito.ru' + ad.find('h3',class_='snippet-title').find('a').get('href')        
        except:
            link=''        
        try:
            price = ad.find('span',class_='snippet-price').text.strip()
        except:
            price = ''
        ad_data = {'title':title,
                    'link':link,
                    'price':price}
        write_csv(ad_data)  #добавление полученного словаря в csv файл
 
def write_csv(data): #создаст файл (при его отсутствии) или допишет данные (но с дубликатами), если вызов не первый 
    with open('./miavito.csv', 'a') as f:    #адрес - директория, где находится скрипт
        writer = csv.writer(f)
        writer.writerow((data['title'], data['link'], data['price']))        

   
def main():
    url = 'https://www.avito.ru/moskva?q=Miband&p=1'
    base_url = url[:-1]
    total_pages = get_total_pages(get_html(url))
    for i in range(1, total_pages + 1):
        urlgen = base_url + str(i) 
        html = get_html(urlgen)
        get_page_data(html)

if __name__ == '__main__':
    main()