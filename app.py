from flask import *
from database import init_db, db_session
from models import *

app = Flask(__name__)

# TODO: Change the secret key
app.secret_key = "Change Me"
user = None

# TODO: Fill in methods and routes
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method=="GET":
        return render_template("index.html")
    elif request.method=="POST":
        username=request.form["username"]
        password=request.form["password"]
        for u in db_session.query(User).where(User.username==username and User.password==password).all():
            user = u
            return redirect(url_for("home"))
        return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method=="GET":
        return render_template("register.html")
    elif request.method=="POST":
        username=request.form["username"]
        password=request.form["password"]
        confirm_password=request.form["confirm-password"]
        if password==confirm_password and len(db_session.query(User).where(User.username==username).all())==0:
            user = User(username=username, password=password)
            db_session.add(user)
            db_session.commit()
            return redirect(url_for("home"))
        return render_template("register.html")

@app.route("/home", methods=["GET", "POST"])
def home():
    return render_template("home.html")

@app.route("/add", methods=["GET", "POST"])
def add():
    return render_template("add.html")

@app.route("/edit", methods=["GET", "POST"])
def edit():
    return render_template("edit.html")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
