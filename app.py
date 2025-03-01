from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, current_user
from model import db, Dish
from scraper import scrape_dishes
from auth import auth

app = Flask(__name__)
app.config.from_object("config.Config")
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.init_app(app)

app.register_blueprint(auth)


@app.route("/")
def home():
    dishes = Dish.query.all()
    return render_template("home.html", dishes=dishes)


@app.route("/search")
def search():
    query = request.args.get("query")
    results = Dish.query.filter(Dish.name.ilike(f"%{query}%")).all()
    return render_template("home.html", dishes=results)


@app.route("/scrape")
@login_required
def scrape():
    dishes = scrape_dishes()
    for dish in dishes:
        new_dish = Dish(name=dish["name"], image=dish["image"], calories=dish["calories"], recipe=dish["recipe"],
                        category=dish["category"])
        db.session.add(new_dish)
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
