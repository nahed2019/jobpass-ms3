import os
import json
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


# Route for index
@app.route("/")
@app.route("/profile")
def profile():
    data_skill = []
    with open("data/skills.json", "r") as json_data:
        data_skill = json.load(json_data)
    data_projects = []
    with open("data/projects.json", "r") as json_data:
        data_projects = json.load(json_data)
    basics = mongo.db.basic_info.find()
    projects = mongo.db.projects.find()
    skills = mongo.db.skills.find()
    works = mongo.db.work_experience.find()
    return render_template(
        "profile.html", basics=basics, projects=projects,
        skills=skills, works=works,
        data_skill=data_skill, data_projects=data_projects)


# Route for contact form in my profile
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        flash("Thanks {}, we have received your message!".format(
            request.form.get("name")))

    return render_template("profile.html")


# Route for profile shop
@app.route("/shop")
def shop():
    basics = mongo.db.basic_info.find()
    return render_template(
        "shop.html", basics=basics)


@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    basics = list(mongo.db.basic_info.find({"$text": {"$search": query}}))
    return render_template("shop.html", basics=basics)


# Route for register
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        # if username not exists in db
        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
        return redirect(url_for("add_profile", username=session["user"]))
    return render_template("register.html")


# Route for login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                flash("Welcome, {}".format(request.form.get("username")))
                return redirect(
                    url_for("manage_profile", username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


# Route for add profile
@app.route("/add_profile/<username>", methods=["GET", "POST"])
def add_profile(username):
    # grab the session user's username from db
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    if session["user"]:
        return render_template("add_profile.html", username=username)
    return redirect(url_for("login"))


# Route for add basic info in add profile
@app.route("/basic_info", methods=["GET", "POST"])
def basic_info():
    if request.method == "POST":
        basic = {
            "first_name": request.form.get("first_name"),
            "last_name": request.form.get("last_name"),
            "phone": request.form.get("phone"),
            "email": request.form.get("email"),
            "cur_title": request.form.get("cur_title"),
            "education": request.form.get("education"),
            "adress": request.form.get("adress"),
            "about_me": request.form.get("about_me"),
            "created_by": session["user"]
        }
        mongo.db.basic_info.insert_one(basic)
        flash(
            "Basic Information Successfully Added, Add Your Projects Info")

    return render_template("add_profile.html")


# Route for add project info in add profile
@app.route("/add_project", methods=["GET", "POST"])
def add_project():
    if request.method == "POST":
        project = {
            "project_name": request.form.get("project_name"),
            "project_desc": request.form.get("project_desc"),
            "project_link": request.form.get("project_link"),
            "created_by": session["user"]
        }
        mongo.db.projects.insert_one(project)
        flash(
            "Projects Info Successfully Added,Move to Experience section")

    return render_template("add_profile.html")


# Route for add work experience in add profile
@app.route("/work_experience", methods=["GET", "POST"])
def work_experience():
    if request.method == "POST":
        work_experience = {
            "job_title": request.form.get("job_title"),
            "company_name": request.form.get("company_name"),
            "from_date": request.form.get("from_date"),
            "to_date": request.form.get("to_date"),
            "created_by": session["user"]
        }
        mongo.db.work_experience.insert_one(work_experience)
        flash(
            "Experience Information Successfully Added, Add more Experience")

    return render_template("add_profile.html")


# Route for add skills in add profile
@app.route("/skills", methods=["GET", "POST"])
def skills():
    if request.method == "POST":
        skills = {
            "skill_name": request.form.get("skill_name"),
            "percent": request.form.get("percent"),
            "created_by": session["user"]
        }
        mongo.db.skills.insert_one(skills)
        flash(
            "skills Information Successfully Added, Add more skills")

    return render_template("add_profile.html")


# Route for add languges in add profile
@app.route("/languages", methods=["GET", "POST"])
def languages():
    if request.method == "POST":
        languages = {
            "language_name": request.form.get("language_name"),
            "language_level": request.form.get("language_level"),
            "created_by": session["user"]
        }
        mongo.db.languages.insert_one(languages)
        flash(
            "Languages Information Successfully Added, Add more languages")

    return render_template("add_profile.html")


# Route for manage profile
@app.route("/manage_profile/<username>", methods=["GET", "POST"])
def manage_profile(username):
    if session["user"]:
        # grab the session user's username from db
        username = mongo.db.users.find_one(
            {"username": session["user"]})["username"]
        basic_info = list(mongo.db.basic_info.find())
        projects = mongo.db.projects.find()
        skills = mongo.db.skills.find()
        works = mongo.db.work_experience.find()
        languages = mongo.db.languages.find()
        return render_template(
            "manage_profile.html", username=username,
            basic_info=basic_info, projects=projects,
            skills=skills, works=works, languages=languages)
    return redirect(url_for("login"))


# Route for edit projects in manage profile
@app.route("/edit_project/<project_id>", methods=["GET", "POST"])
def edit_project(project_id):
    if request.method == "POST":
        projects = {
            "project_name": request.form.get("project_name"),
            "project_desc": request.form.get("project_desc"),
            "project_link": request.form.get("project_link"),
            "created_by": session["user"]
        }
        mongo.db.projects.update({"_id": ObjectId(project_id)}, projects)
        flash(
            "Projects Info Successfully updated")
    project = mongo.db.projects.find_one({"_id": ObjectId(project_id)})
    return render_template("edit_project.html", project=project)


# Route for delete projects in manage profile
@app.route("/delete_project/<project_id>")
def delete_project(project_id):
    if session["user"]:
        # grab the session user's username from db
        username = mongo.db.users.find_one(
                {"username": session["user"]})["username"]
        mongo.db.projects.remove({"_id": ObjectId(project_id)})
        flash("Projects Info Successfully deleted")
        return redirect(url_for("manage_profile", username=username))


# Route for edit experience in manage profile
@app.route("/edit_experience/<experience_id>", methods=["GET", "POST"])
def edit_experience(experience_id):
    if request.method == "POST":
        works = {
            "job_title": request.form.get("job_title"),
            "company_name": request.form.get("company_name"),
            "from_date": request.form.get("from_date"),
            "to_date": request.form.get("to_date"),
            "created_by": session["user"]
        }
        mongo.db.work_experience.update({"_id": ObjectId(
            experience_id)}, works)
        flash(
            "Work Experience Information Successfully updated")
    work = mongo.db.work_experience.find_one(
        {"_id": ObjectId(experience_id)})
    return render_template("edit_experience.html", work=work)


# Route for delete Work Experience in manage profile
@app.route("/delete_experience/<experience_id>")
def delete_experience(experience_id):
    if session["user"]:
        # grab the session user's username from db
        username = mongo.db.users.find_one(
                {"username": session["user"]})["username"]
        mongo.db.work_experience.remove({"_id": ObjectId(experience_id)})
        flash("Work Experience Info Successfully deleted")
        return redirect(url_for("manage_profile", username=username))


# Route for edit skills in manage profile
@app.route("/edit_skill/<skill_id>", methods=["GET", "POST"])
def edit_skill(skill_id):
    if request.method == "POST":
        skills = {
            "skill_name": request.form.get("skill_name"),
            "percent": request.form.get("percent"),
            "created_by": session["user"]
        }
        mongo.db.skills.update({"_id": ObjectId(skill_id)}, skills)
        flash(
            " Skill Information Successfully updated")
    skill = mongo.db.skills.find_one({"_id": ObjectId(skill_id)})
    return render_template("edit_skill.html", skill=skill)


# Route for delete skill in manage profile
@app.route("/delete_skill/<skill_id>")
def delete_skill(skill_id):
    if session["user"]:
        # grab the session user's username from db
        username = mongo.db.users.find_one(
                {"username": session["user"]})["username"]
        mongo.db.skills.remove({"_id": ObjectId(skill_id)})
        flash("Skill Information Successfully deleted")
        return redirect(url_for("manage_profile", username=username))


@app.route("/logout")
def logout():
    # remove user from session cookie
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
