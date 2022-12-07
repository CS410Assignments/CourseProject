from flask import Flask, request
from flask_cors import CORS, cross_origin
import re
import os
from statistics import mean

app = Flask(__name__)
CORS(app)

currentDir = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(currentDir, 'Food_Dict.csv')) as f:
    food_dictionary = [line.rstrip().lower() for line in f]

with open(os.path.join(currentDir, 'AFINN_EMOTION.txt')) as afinnfile:
    scores = {}  # initialize an empty dictionary
    for line in afinnfile:
        # The file is tab-delimited. "\t" means "tab character"
        term, score = line.split("\t")
        scores[term] = int(score)  # Convert the score to an integer.


@app.route("/", methods=["POST"])
@cross_origin()
def review():
    # data received from frontend
    data = request.json

    # list containing only reviews
    review = list(review_retrieval(data))

    # list containing only reviews (small)
    review_s = [line.rstrip().lower() for line in review]

    best_selling_food, foodhere, final_review = food_showing_in_review(
        review, review_s, food_dictionary)

    sorted_food = sorted(best_selling_food.items(),
                         key=lambda x: x[1], reverse=True)

    # Sentimental Analysis
    reviewlist = list(final_review)  # make a copy to modify
    sentiment_scores = []

    for i in range(len(reviewlist)):
        tmpReview = []
        tmpReview.append(reviewlist[i])
        reviewlist[i] = re.compile("[^\w']|_").sub(" ", reviewlist[i]).split()
        sentiment = 0
        for words in reviewlist[i]:
            if words in scores:
                sentiment += scores[words]
        tmpReview.append(sentiment)
        sentiment_scores.append(tmpReview)

    final_score = mean([x[1] for x in sentiment_scores])

    # sorted_food: [ [dishNname, count], [dishNname, count], ... ]
    # final_score: sentiment review score for this restaurant
    # sentiment_scores: [ [review, score], [review, score], ... ]

    return {"sorted_food": sorted_food, "final_score": final_score, "sentiment_scores": sentiment_scores}


def review_retrieval(data):
    review = []
    for i in range(len(data)):
        if "text" in data[i]:
            review.append(data[i]["text"])
    return review


def food_showing_in_review(review, review_s, food_dictionary):
    best_selling_food = {}
    foodhere = set()
    final_review = set()

    for i in range(len(review)):
        for j in range(len(food_dictionary)):
            # Only select reviews that mention food
            x = review_s[i].find(food_dictionary[j])

            if (x != -1):
                best_selling_food[food_dictionary[j]] = best_selling_food.setdefault(
                    food_dictionary[j], 0) + 1
                foodhere.add(food_dictionary[j])

                final_review.add(review[i])

    return best_selling_food, foodhere, final_review
