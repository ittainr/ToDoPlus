from flask import *
from database import init_db, db_session
from models import *
from datetime import datetime

app = Flask(__name__)

app.secret_key = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'

# TODO: Fill in methods and routes
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method=="GET":
        return render_template("index.html")
    elif request.method=="POST":
        username=request.form["username"]
        password=request.form["password"]
        for u in db_session.query(User).where(User.username==username and User.password==password).all():
            session["user"] = {"username":username, "password":password}
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
            session["user"] = {"username":username, "password":password}
            db_session.add(User(username=username, password=password))
            db_session.commit()
            return redirect(url_for("home"))
        return render_template("register.html")

@app.route("/home", methods=["GET", "POST"])
def home():
    if request.method=="GET":
        user = session.get("user")
        if user:
            username = user["username"]
            tasks = db_session.query(Task).where(Task.user_username==username).all()
            return render_template("home.html", tasks=tasks)
        else:
            return redirect(url_for("login"))
    elif request.method=="POST":
        task_id = request.form["task-id"]
        db_session.delete(db_session.query(Task).where(Task.id==task_id).all()[0])
        db_session.commit()
        return render_template("home.html", tasks=db_session.query(Task).where(Task.user_username==session.get("user")["username"]).all())

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method=="GET":
        return render_template("add.html")
    elif request.method=="POST":
        user = db_session.query(User).where(User.username==session.get("user")["username"] and User.password==session.get("user")["password"]).all()[0]
        new_task = Task(task_name=request.form["task-name"], due_date=datetime.strptime(request.form["due-date"], "%Y-%m-%d").date(), time_needed=request.form["time-needed"], user_username=user.username)
        db_session.add(new_task)
        user.tasks.append(new_task)
        db_session.commit()
        return redirect(url_for("home"))

@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method=="GET":
        task_id = request.args["task-id"]
        return render_template("edit.html", task_id=task_id)
    elif request.method=="POST":
        task_id = request.form["task-id"]
        task = db_session.query(Task).where(Task.id==task_id).all()[0]
        task.task_name=request.form["task-name"]
        task.due_date=datetime.strptime(request.form["due-date"], "%Y-%m-%d").date()
        task.time_needed=request.form["time-needed"]
        db_session.commit()
        return redirect(url_for("home"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
