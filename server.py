from flask import Flask, render_template
from datetime import datetime
import requests
import random
from post import Post

app = Flask(__name__)


blog_url = "https://api.npoint.io/3be6d6bab3195f342ab1"
all_posts = requests.get(blog_url).json()
post_list = []
for post in all_posts:
    post_list.append(Post(post["id"], post["title"], post["subtitle"], post["body"]))




@app.route('/')
def home():
    return render_template("index.html", posts = post_list)


@app.route('/guess/<name>')
def guess(name):
    request_age = requests.get("https://api.agify.io", params={"name":name})
    age = request_age.json()["age"]

    request_gender = requests.get("https://api.genderize.io", params={"name":name})
    gender = request_gender.json()["gender"]

    nationallity_request = requests.get("https://api.nationalize.io", params={"name":name})
    nationallity = nationallity_request.json()["country"][0]["country_id"]

    return render_template("guesser.html", name=name, gender=gender, country=nationallity, age=age)


@app.route("/post/<int:index>")
def show_post(index:int):
    post = None
    for blog_post in post_list:
        if index == blog_post.id:
            post = blog_post
    return render_template("post.html", post=post)


@app.route("/blog")
def get_blog():
    blog_url = "https://api.npoint.io/3be6d6bab3195f342ab1"
    all_blogs = requests.get(blog_url).json()
    return render_template("blog.html", posts=all_blogs)



if __name__ == "__main__":
    app.run(debug=True)
