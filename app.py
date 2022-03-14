from flask import Flask, json, render_template, redirect, request, jsonify
from db import DataBase
import re


app = Flask(__name__, static_url_path="/static/", template_folder="templates")
app.config["TEMPLATES_AUTO_RELOAD"] = True
route = app.route
db = DataBase("films_cleared.db")
COUNT_FILMS_ON_PAGE = 20


def film_card_handler(info):
    # f'<img src="{info[3] if info[3] else "null"}" class="film-cover">' \
    return  f'<a href="/film/{info[0]}"><div class="film-card">' \
                f'<img src="{info[4]}" class="film-cover">' \
                f'<p class="film-title">{info[1]}</p>' \
            f'</div></a>'



@route("/", methods=["GET"])
def index():
    return render_template("index.html")


@route("/film/<_id>", methods=["GET"])
def film_page(_id):
    info = db.get_film(int(_id))
    print(eval(info[10]))
    return render_template("film_page.html", 
                           cover_link = info[4],
                           title = info[1],
                           date_year = info[7],
                           director = info[5],
                           actors = info[6],
                           description = info[8],
                           players_link = [[num, x] for num, x in enumerate(eval(info[10]), 1)],
                           link = info[9],
                           genre = info[3]
                           )


@route("/api/getFilmsList/<page>", methods=["GET"])
def films_list(page):
    page = int(page)
    if page <= 0: page = 0
    films_list = db.get_films([page*COUNT_FILMS_ON_PAGE+1, page*COUNT_FILMS_ON_PAGE+COUNT_FILMS_ON_PAGE])
    return "\n".join([film_card_handler(info) for info in films_list])


@route("/api/getMaxPage", methods=["GET"])
def get_max_page():
    count_films = db.get_count_films()[0]
    return str(int((count_films / COUNT_FILMS_ON_PAGE) + 0.5))


@route("/api/searchByTitle/<query>", methods=["GET"])
def search_by_title(query):
    return "\n".join([film_card_handler(info) for info in db.find_by_title(query)])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=52125)
