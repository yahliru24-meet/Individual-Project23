from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase
import random

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

config = {
  "apiKey": "AIzaSyD_0XhSd7z02s2rnVH5hl00qrrIlFH2kfY",
  "authDomain": "citysearch-11ecd.firebaseapp.com",
  "databaseURL": "https://citysearch-11ecd-default-rtdb.europe-west1.firebasedatabase.app",
  "projectId": "citysearch-11ecd",
  "storageBucket": "citysearch-11ecd.appspot.com",
  "messagingSenderId": "315680174031",
  "appId": "1:315680174031:web:95b37b654ee89a5a576cba",
  "measurementId": "G-XB1ZE83SPK",
  "databaseURL": "https://citysearch-11ecd-default-rtdb.europe-west1.firebasedatabase.app/",
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

#Code goes below here


@app.route("/", methods = ["GET", "POST"])
def signin():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('home'))
        except:
            error = "Authentication failed"
    return render_template("signin.html")


@app.route("/signup", methods = ["GET", "POST"])
def signup():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        username = request.form["username"]
        full_name = request.form["full_name"]
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            UID = login_session['user']['localId']
            user = {"name": full_name, "username" : username}
            db.child("Users").child(UID).set(user)
            return redirect(url_for('home'))
        except:
            error = "Authentication failed"
    return render_template("signup.html", error = error)


@app.route("/home", methods = ["GET", "POST"])
def home():
    UID = login_session['user']['localId']
    cities = db.child("Cities").get().val().keys()
    username = db.child("Users").child(UID).child("username").get().val()
    print(username)
    try:
        fav_cities = db.child("Users").child(UID).child("favs").get().val().keys()
        return render_template("home.html", cities = cities, favs = fav_cities, username = username)
    except:
        return render_template("home.html", cities = cities, username = username)


@app.route("/c/<string:name>", methods = ["GET", "POST"])
def city(name):
    cities = db.child("Cities").get().val()
    if request.method == "POST":
        UID = login_session['user']['localId']
        db.child("Users").child(UID).child("favs").child(name).set("/")
    return render_template("city.html", city_name = name, cities = cities)


@app.route("/user", methods = ["GET", "POST"])
def user():
    try:
        UID = login_session['user']['localId']
        username = db.child("Users").child(UID).child("username").get().val()
        full_name = db.child("Users").child(UID).child("name").get().val()
        fav_cities = db.child("Users").child(UID).child("favs").get().val().keys()
        return render_template("user.html", favs = fav_cities, username = username, full_name = full_name)
    except:
        return render_template("user.html", username = username, full_name = full_name)


@app.route("/random_city")
def random_city():
    cities = list(db.child("Cities").get().val().keys())
    return redirect(url_for("city", name=random.choice(cities)))


# def init_app():
#     israel_cities = {
#     "Jerusalem": {
#         "summary": "Jerusalem is the capital and largest city of Israel. It holds great religious significance for Jews, Christians, and Muslims.",
#         "population": "Approximately 936,000",
#         "area": "125.1 square kilometers"
#     },
#     "Tel-Aviv": {
#         "summary": "Tel Aviv is a major city on Israel's Mediterranean coastline. It is known for its vibrant nightlife, beaches, and cultural scene.",
#         "population": "Approximately 460,000",
#         "area": "51.8 square kilometers"
#     },
#     "Haifa": {
#         "summary": "Haifa is a northern coastal city known for its port, industry, and the Bahá'í World Centre.",
#         "population": "Approximately 283,000",
#         "area": "63.67 square kilometers"
#     },
#     "Rishon LeZion": {
#         "summary": "Rishon LeZion is a city in the Tel Aviv District and is the fourth-largest city in Israel.",
#         "population": "Approximately 254,000",
#         "area": "58.8 square kilometers"
#     },
#     "Petah Tikva": {
#         "summary": "Petah Tikva is a city in the Central District, known for its high-tech industries and medical centers.",
#         "population": "Approximately 248,000",
#         "area": "35.9 square kilometers"
#     },
#     "Ashdod": {
#         "summary": "Ashdod is a major port city on the Mediterranean coast, known for its industrial and commercial significance.",
#         "population": "Approximately 224,000",
#         "area": "47.2 square kilometers"
#     },
#     "Netanya": {
#         "summary": "Netanya is a coastal city with beautiful beaches and a growing tourism industry.",
#         "population": "Approximately 222,000",
#         "area": "28.4 square kilometers"
#     },
#     "Beersheba": {
#         "summary": "Beersheba is the largest city in the Negev desert, known for its history and modern development.",
#         "population": "Approximately 217,000",
#         "area": "117.5 square kilometers"
#     },
#     "Holon": {
#         "summary": "Holon is a city in the Tel Aviv District, known for its industrial and cultural activities.",
#         "population": "Approximately 193,000",
#         "area": "18.2 square kilometers"
#     },
#     "Bnei Brak": {
#         "summary": "Bnei Brak is a city in the Tel Aviv District with a large ultra-Orthodox Jewish population.",
#         "population": "Approximately 196,000",
#         "area": "7.6 square kilometers"
#     },
#     "Ramat Gan": {
#         "summary": "Ramat Gan is a city in the Tel Aviv District, known for its diamond exchange and commercial activities.",
#         "population": "Approximately 159,000",
#         "area": "12.7 square kilometers"
#     },
#     "Ashkelon": {
#         "summary": "Ashkelon is a coastal city known for its historical significance and beaches.",
#         "population": "Approximately 139,000",
#         "area": "47.8 square kilometers"
#     },
#     "Rehovot": {
#         "summary": "Rehovot is a city in the Central District, known for its scientific research institutions.",
#         "population": "Approximately 138,000",
#         "area": "23.5 square kilometers"
#     },
#     "Bat Yam": {
#         "summary": "Bat Yam is a coastal city near Tel Aviv, known for its beaches and residential areas.",
#         "population": "Approximately 128,000",
#         "area": "8.9 square kilometers"
#     },
#     "Herzliya": {
#         "summary": "Herzliya is a city in the Tel Aviv District, known for its upscale residential areas and beaches.",
#         "population": "Approximately 97,000",
#         "area": "26.47 square kilometers"
#     }
# }
    
#     for city in israel_cities.keys():
#         city_info = israel_cities[city]
#         db.child("Cities").child(city).set(city_info)


#Code goes above here

if __name__ == '__main__':
    # init_app()
    app.run(debug=True)