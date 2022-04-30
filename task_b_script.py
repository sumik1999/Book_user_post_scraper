import requests
import sqlite3
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1",
           "DNT": "1", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate"}

con = sqlite3.connect('booksdata.db')
cur = con.cursor()
cur.execute(f'''CREATE TABLE IF NOT EXISTS books( id INTEGER PRIMARY KEY AUTOINCREMENT,title text,price real, star_rating text , available text )''')
con.commit()

URL = 'https://books.toscrape.com/catalogue/'


def create_books_database():
    """A function to scrape and create the books database over 50 pages """

    for index in range(1,51):

        req = requests.get(URL+f'page-{index}.html', headers=headers)
        soup = BeautifulSoup(req.content, "html.parser")
        products = soup.find_all("article", attrs={"class": "product_pod"})

        for product in products:
            title = product.find('h3').find('a')['title']
            price = product.find('p', attrs={"class": "price_color"}).text
            star_rating = product.find('p')['class'][-1]+'/Five'
            available = product.find(
                'p', attrs={"class": "instock availability"}).text.strip()

            cur.execute("INSERT INTO books(title, price, star_rating, available) VALUES(?, ?, ?, ?)",
                        ( title, price, star_rating, available))
            con.commit()
        
        print(f'{index} page scraped')


if __name__=="__main__":

    create_books_database()
    
