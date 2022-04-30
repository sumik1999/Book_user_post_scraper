import sqlite3
import requests
from pymongo import MongoClient

from pprint import pprint

app_id = '626bbcdf43f56774571db143'
headers = {"app-id": app_id, 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1",
           "DNT": "1", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate"}


def create_user_request(users):
    """Function to fetch and insert users into the database"""

    query_params = {'limit': 20, 'page': 0}
    first_req = requests.get(
        'https://dummyapi.io/data/v1/user', headers=headers, params=query_params)
    data = first_req.json()

    for index,item in enumerate(data["data"]):
        print(f"{index+1} user created")
        users.insert_one(item)


def create_post_request(users, posts):
    """Function to fetch posts for each user and insert it into database"""
    for user_index, user in enumerate(users.find()):
        id = user['id']
        req = requests.get(
            f'https://dummyapi.io/data/v1/user/{id}/post', headers=headers)
        data = req.json()

        for post_index, item in enumerate(data["data"]):
            posts.insert_one(item)
            print(f" for user: {user_index+1} inserted post: {post_index+1}")


if __name__ == "__main__":
    client = MongoClient()
    db = client['users-database']
    collection = db['users-collection']
    users = db.users
    posts = db.posts

    create_user_request(users)
    create_post_request(users, posts)

