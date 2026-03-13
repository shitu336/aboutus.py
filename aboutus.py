 from flask import Flask, render_template_string, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret"

def db():
    return sqlite3.connect("ngo.db")

# create table
conn = db()
conn.execute("CREATE TABLE IF NOT EXISTS content(id INTEGER PRIMARY KEY, story TEXT, values TEXT, programs TEXT)")
conn.commit()

cur = conn.execute("SELECT * FROM content")
if not cur.fetchone():
    conn.execute("INSERT INTO content(story,values,programs) VALUES('Our NGO helps communities','Integrity,Empathy','Education,Health')")
    conn.commit()

# ABOUT PAGE
@app.route("/")
def about():
    conn = db()
    data = conn.execute("SELECT * FROM content").fetchone()

    html = """
    <h1>Welcome to Our NGO</h1>

    <h2>Our Story</h2>
    <p>{{story}}</p>

    <h2>Core Values</h2>
    <p>{{values}}</p>

    <h2>Programs</h2>
    <p>{{programs}}</p>

    <br>
    <a href="/admin">Admin Login</a>
    """

    return render_template_string(html,
    story=data[1],
    values=data[2],
    programs=data[3])

# ADMIN LOGIN
@app.route("/admin", methods=["GET","POST"])
def admin():

    if request.method=="POST":
        if request.form["username"]=="admin" and request.form["password"]=="admin":
            session["admin"]=True
            return redirect("/dashboard")

    html = """
    <h2>Admin Login</h2>
    <form method="post">
    Username <input name="username"><br><br>
    Password <input name="password" type="password"><br><br>
    <button>Login</button>
    </form>
    """
    return render_template_string(html)

# DASHBOARD
@app.route("/dashboard", methods=["GET","POST"])
def dashboard():

    if "admin" not in session:
        return redirect("/admin")

    conn = db()

    if request.method=="POST":
        story=request.form["story"]
        values=request.form["values"]
        programs=request.form["programs"]

        conn.execute("UPDATE content SET story=?,values=?,programs=? WHERE id=1",
                     (story,values,programs))
        conn.commit()

    data = conn.execute("SELECT * FROM content").fetchone()

    html = """
    <h2>Admin Dashboard</h2>

    <form method="post">

    Story<br>
    <textarea name="story">{{story}}</textarea><br><br>

    Core Values<br>
    <textarea name="values">{{values}}</textarea><br><br>

    Programs<br>
    <textarea name="programs">{{programs}}</textarea><br><br>

    <button>Save</button>
    </form>

    <br>
    <a href="/">View Website</a>
    """

    return render_template_string(html,
    story=data[1],
    values=data[2],
    programs=data[3])

app.run(debug=True)