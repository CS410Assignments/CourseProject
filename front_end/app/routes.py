""" Specifies routing for the application"""
from flask import render_template, request, jsonify
from app import app
from webforms import SearchForm
import content_based_system as cb
# from app import database

app.config['SECRET_KEY'] = 'any secret string'

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", title='Home Page')

@app.route("/user_content")
def user_content():
    return render_template("user_content.html", title='User Based Recommendation')    

# @app.route("/content_based")
# def content_based():
#     return render_template("content_based.html", title='Contant Based Recommendation') 

# @app.route("/content_result")
# def content_based():
#     return render_template("content_based.html", title='Contant Based Recommendation') 

# @app.route('/content_based', methods=["POST","GET"])
# def search():
#     print("wtf")
#     form = SearchForm()
#     data = form.searched.data #input value
#     print(data)
#     rec_movies = cb.get_recommendations('The Dark Knight Rises')
#     targetItem = []
#     for index, movie in rec_movies:
#         item = {
#             "movie_name" : movie
#         }
#         targetItem.append(item)
#     return render_template(
#         "content_based.html",
#         form=form,
#         targetItem=targetItem
#     )
@app.route('/content_based', methods=['GET', 'POST'])
def content_based():
    form = SearchForm()
    targetItem = []
    if request.method == 'POST':
         print("what do you mean???")
         form = SearchForm()
         data = form.searched.data #input value
         print(data)
         rec_movies = cb.get_recommendations(data)
        #  print(rec_movies)
         for index, movie in rec_movies:
            item = {
                "movie_name" : movie
            }
            targetItem.append(item)
    print(targetItem)
    return render_template(
        "content_based.html",
        form=form,
        targetItem=targetItem
    )
@app.route("/autoencoder_based")
def autoencoder_based():
    return render_template("autoencoder_based.html", title='Autoencoder Recommendation') 