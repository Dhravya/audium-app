import json
import random
import requests

from flask import Flask, jsonify, render_template, request, redirect, url_for, session

from urllib.parse import quote_plus, urlencode

from authlib.integrations.flask_client import OAuth

from constants import  hashtags
from handlers import (
    AuthHandler,
    StorageHandler,
    DataBaseHandler,
    env,
)

app = Flask(__name__)
app.config["SECRET_KEY"] = env["APP_SECRET_KEY"]

oauth = OAuth(app)
oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration',
)

auth_handler = AuthHandler()

@app.route('/test')
def test():
    return jsonify(session.get("user")["userinfo"])

@app.route("/")
def index():
    posts = DataBaseHandler.get_stream(n=100)

    session_ = session.get("user")
    if not session_:
        return redirect(url_for("login"))

    new_posts = DataBaseHandler.get_stream(n=3)['documents']
    
    return render_template(
        "index.html",
        hashtags=["#" + hashtag for hashtag in hashtags],
        posts=posts["documents"],
        trending_posts=new_posts,
        user=session.get("user"),
    )


@app.route("/trending")
def trending():
    print(DataBaseHandler.get_stream())
    return render_template(
        "trending.html",
        hashtags=hashtags,
        posts=DataBaseHandler.get_stream()['documents'],
        user=session.get("user"),
    )


@app.route("/a/<id_>")
def post(id_):
    post = DataBaseHandler.get_post(id_)

    return render_template("post.html", post=post, user=session.get("user"))


@app.route("/new", methods=["GET", "POST"])
def new_post():

    session_ = session.get("user")
    if not session_:
        return redirect(url_for("login"))

    if request.method == "POST":
        audio = request.files["audio"]
        audio_bytes = audio.read()
        audio_num = random.randint(0, 10)

        if not audio_bytes:
            audio_url = request.form.get("audio_url")
            audio_bytes = requests.get(audio_url).content

        with open(f"temp/audio-{audio_num}.mp3", "wb") as f:
            f.write(audio_bytes)

        audio_url = StorageHandler.upload_audio(f"temp/audio-{audio_num}.mp3")

        id_ = DataBaseHandler.add_audio_to_db(
            description=request.form.get("description"),
            audio_url=audio_url,
            uploader=session.get("user")["userinfo"]["sub"],
            colour=request.form.get("colour"),
            hashtag=request.form.get("hashtag"),
        )

        return redirect(f"/a/{id_}")

    return render_template("new_post.html", hashtags=hashtags, user=session.get("user"))


@app.route("/me")
def me():
    session_ = session.get("user")
    if not session_:
        return redirect(url_for("login"))
    return render_template(
        "user.html",
        posts=DataBaseHandler.get_user_posts(session.get("user")["userinfo"]["sub"]),
        user=session.get("user")
    )

# Like post endpoint
@app.route('/a/<id_>/like')
def like_post(id_):
    session_ = session.get("user")
    if not session_:
        return redirect(url_for("login"))

    DataBaseHandler.like_post(id_, user_id = session.get("user")["userinfo"]["sub"])

    return None

"""
!_____________________________________________
    AUTH ROUTES
!_____________________________________________
"""


@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://"
        + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("index", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )


if __name__ == "__main__":
    app.run(debug=True)
