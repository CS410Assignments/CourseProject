from flask import Flask, redirect, url_for, render_template, request
from ranker import ranker

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def home():
	request_method = request.method
	if request.method == "POST":
		user = request.form["nm"]
		if user:
			return redirect(url_for("results", name=user))
		else:
			return render_template("main.html")
	else:
		return render_template("main.html")
@app.route("/results/<string:name>", methods=["GET"])
def results(name):
	x = ranker(name)
	y = []

	for subreddit in x:
		if subreddit[0] not in y:
			y.append(subreddit[0])

	return render_template("results.html", name=y)
	

if __name__ == "__main__":
	app.run()