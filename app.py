import secrets
import sqlite3
from flask import Flask
from flask import abort, flash, redirect, render_template, request, session
import config
import items
import users

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

def check_csrf():
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

@app.route("/")
def index():
    all_items = items.get_items()
    return render_template("index.html", items=all_items)

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    user_items = users.get_items(user_id)
    return render_template("show_user.html", user=user, items=user_items)

@app.route("/show_item/<int:item_id>")
def show_item(item_id):
    item = items.get_item(item_id)
    if not item:
        abort(404)
    classes = items.get_classes(item_id)
    sign_ups = items.get_sign_ups(item_id)
    user_id = session.get("user_id")
    is_owner = user_id is not None and user_id == item["user_id"]
    is_signed_up = any(s["user_id"] == user_id for s in sign_ups) if user_id else False

    return render_template("show_item.html", item=item, classes=classes,
            sign_ups=sign_ups, is_owner=is_owner, is_signed_up=is_signed_up)

@app.route("/new_item")
def new_item():
    require_login()
    classes = items.get_all_classes()
    return render_template("new_item.html", classes=classes)

@app.route("/create_item", methods=["POST"])
def create_item():
    require_login()
    check_csrf()

    title = request.form["title"]
    if not title or len(title) > 50:
        abort(403)
    description = request.form["description"]
    if not description or len(description) > 1000:
        abort(403)
    participants = request.form["participants"]
    try:
        participants_int = int(participants)
        if participants_int < 1 or participants_int > 99:
            abort(403)
    except ValueError:
        abort(403)
    user_id = session["user_id"]

    all_classes = items.get_all_classes()
    classes = []
    for entry in request.form.getlist("classes"):
        if entry:
            class_title, class_value = entry .split(":")
            if class_title not in all_classes:
                abort(403)
            if class_value not in all_classes[class_title]:
                abort(403)

            classes.append((class_title, class_value))

    items.add_item(title, description, participants, user_id, classes)

    return redirect("/")

@app.route("/create_sign_up", methods=["POST"])
def create_sign_up():
    require_login()
    check_csrf()

    application = request.form["application"]
    if not application or len(application) > 1000:
        abort(403)
    item_id = request.form["item_id"]
    item = items.get_item(item_id)
    if not item:
        abort(403)
    user_id = session["user_id"]

    maximum_participants = items.get_maximum_participants(item_id)
    sign_ups = items.get_sign_ups(item_id)
    if maximum_participants <= len(sign_ups):
        abort(403)

    items.add_sign_up(item_id, user_id, application)

    return redirect("/show_item/" + str(item_id))

@app.route("/remove_sign_up", methods=["POST"])
def remove_sign_up():
    require_login()
    check_csrf()

    item_id = request.form["item_id"]
    sign_up_id = request.form["sign_up_id"]

    items.remove_sign_up(sign_up_id)

    return redirect("/show_item/" + str(item_id))

@app.route("/edit_item/<int:item_id>")
def edit_item(item_id):
    require_login()
    item = items.get_item(item_id)
    if item["user_id"] != session["user_id"]:
        abort(403)

    all_classes = items.get_all_classes()
    classes = {}
    for my_class in all_classes:
        classes[my_class] = ""
    for entry in items.get_classes(item_id):
        classes[entry["title"]] = entry["value"]

    return render_template("edit_item.html", item=item,
                           classes=classes, all_classes=all_classes)

@app.route("/update_item", methods=["POST"])
def update_item():
    require_login()
    check_csrf()

    item_id = request.form["item_id"]
    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)

    title = request.form["title"]
    if not title or len(title) > 50:
        abort(403)
    description = request.form["description"]
    if not description or len(description) > 1000:
        abort(403)

    all_classes = items.get_all_classes()
    classes = []
    for entry in request.form.getlist("classes"):
        if entry:
            class_title, class_value = entry .split(":")
            if class_title not in all_classes:
                abort(403)
            if class_value not in all_classes[class_title]:
                abort(403)

            classes.append((class_title, class_value))

    items.update_item(item_id, title, description, classes)

    return redirect("/show_item/" + str(item_id))

@app.route("/remove_item/<int:item_id>", methods=["GET", "POST"])
def remove_item(item_id):
    require_login()

    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("remove_item.html", item=item)

    if request.method == "POST":
        check_csrf()
        if "remove" in request.form:
            items.remove_item(item_id)
            return redirect("/")

        return redirect("/show_item/" + str(item_id))

@app.route("/find_item")
def find_item():
    query = request.args.get("query")
    if query:
        results = items.find_items(query)
    else:
        query = ""
        results = []

    return render_template("find_item.html", query=query, results=results)

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create_user", methods=["POST"])
def create_user():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        flash("VIRHE: salasanat eivät ole samat")
        return redirect("/register")

    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        flash("VIRHE: tunnus on jo varattu")
        return redirect("/register")

    flash("Tunnus luotu")
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user_id = users.check_login(username, password)
        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")
        else:
            flash("VIRHE: väärä tunnus tai salasana")
            return redirect("/login")

@app.route("/logout")
def logout():
    require_login()
    del session["user_id"]
    del session["username"]
    return redirect("/")
