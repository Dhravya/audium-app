from functools import cache
import random
from datetime import datetime
from os import environ as env
import requests

from dotenv import load_dotenv
from appwrite import query
from appwrite.client import Client
from appwrite.services.users import Users
from appwrite.services.storage import Storage
from appwrite.services.database import Database

load_dotenv()

appwrite_client = Client()

(
    appwrite_client.set_endpoint(env.get("APPWRITE_ENDPOINT"))
    .set_project(env.get("APPWRITE_PROJECT_ID"))
    .set_key(env.get("APPWRITE_API_KEY"))
    .set_self_signed()
)

users = Users(appwrite_client)
storage = Storage(appwrite_client)
database = Database(appwrite_client)


@cache
def get_date(post_id):
    return datetime.fromtimestamp(float(post_id[:10] + "." + post_id[10:])).strftime(
        "%Y-%m-%d %H:%M:%S"
    )


class StorageHandler:
    @staticmethod
    def upload_audio(audio_filepath):
        fileid = random.randint(1, 99999999)
        file = storage.create_file("audios", file=audio_filepath, file_id=fileid)

        return f"{env.get('APPWRITE_ENDPOINT')}/storage/buckets/audios/files/{fileid}/view?project={env.get('APPWRITE_PROJECT_ID')}"


class AuthHandler:
    def __init__(self) -> None:
        pass

    @staticmethod
    @cache
    def get_user(id_=None):
        """gets the user object"""
        url = (
            "https://"
            + env.get("AUTH0_DOMAIN")
            + f"/api/v2/users?q=user_id:{id_}&search_engine=v3"
        )
        headers = {"Authorization": f"Bearer {env.get('AUTH0_MGMT_TOKEN')}"}

        res = requests.get(url, headers=headers)

        if res.status_code == 200 and len(res.json()) > 0:
            return res.json()[0]

        return None

    @staticmethod
    def filter_post(post):
        post["date"] = get_date(post["$id"])

        uploader = AuthHandler.get_user(post["uploader"])
        if uploader:
            post["uploader"] = uploader["given_name"]
            post["picture"] = uploader["picture"]
        else:
            post["uploader"] = "Unknown"
            post["picture"] = f"https://avatars.dicebear.com/api/human/{random.randint(1, 1000)}.svg"
        
        return post
         

class DataBaseHandler:
    @staticmethod
    def add_audio_to_db(description, audio_url, uploader, colour, hashtag):

        aud_obj = {
            "description": description,
            "hashtag": hashtag,
            "audio": audio_url,
            "colour": colour,
            "uploader": uploader,
        }

        # ID is the unix timestamp
        id_ = str(datetime.now().timestamp()).replace(".", "")

        database.create_document("posts", id_, aud_obj)

        return id_

    @staticmethod
    def get_stream(n: int = 5, offset: int = 0):
        """Returns n posts from the database"""
        posts = database.list_documents(
            "posts", limit=n, offset=offset, order_types=["DESC"]
        )

        for post in posts["documents"]:
            AuthHandler.filter_post(post)

        return posts

    @staticmethod
    @cache
    def get_post(id_: str):
        """Returns a post from the database"""
        post = database.get_document("posts", str(id_))
        AuthHandler.filter_post(post)

        return post

    @staticmethod
    def get_user_posts(username: str):
        """Returns all posts from a user"""
        posts = database.list_documents(
            "posts",
            queries=[query.Query.equal("uploader", username)],
            order_types=["DESC"],
        )

        for post in posts["documents"]:
            AuthHandler.filter_post(post)

        return posts["documents"]

    @staticmethod
    def like_post(id_: str, user_id):
        """Likes a post"""
        doc = database.get_document("posts", str(id_)) 
        
        likers = doc["likers"]
    
        if user_id not in likers:
            likers.append(user_id)
        else:
            likers.remove(user_id)
        
        database.update_document("posts", str(id_), {"likers": likers})