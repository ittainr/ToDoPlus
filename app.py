from flask import *
from database import init_db, db_session
from models import *

app = Flask(__name__)

# TODO: Change the secret key
app.secret_key = "Change Me"

# TODO: Fill in methods and routes
@app.route("/", methods=["GET", "POST"])
def login():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    return render_template("register.html")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)