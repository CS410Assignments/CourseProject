# """Defines all the functions related to the database"""
from flask import render_template
from app import app
from webforms import SearchForm
import content_based_system as cb

@app.route('/content_based', methods=["POST"])
def search():
    print("wtf")
    form = SearchForm()
    data = form.searched.data #input value
    print(data)
    rec_movies = cb.get_recommendations('The Dark Knight Rises')
    targetItem = []
    for index, movie in rec_movies:
        item = {
            "movie_name" : movie
        }
        targetItem.append(item)
    return render_template(
        "content_based.html",
        form=form,
        targetItem=targetItem
    )

        # conn = db.connect()
        # print('SELECT * FROM Game WHERE name like "%{}%";'.format(data))
        # query = conn.execute('SELECT * FROM Game WHERE name like "{}";'.format(data))
        # conn.close()
        # query_result = [x for x in query]
        # targetItem = []
        # for ret in query_result:
        #     item = {
        #         "gameId": ret[0],
        #         "name": ret[1],
        #         "year": ret[2],
        #         "genre": ret[3]
        #     }
        #     targetItem.append(item)
        # return render_template("search.html", 
        #         form=form,
        #         targetItem=targetItem)