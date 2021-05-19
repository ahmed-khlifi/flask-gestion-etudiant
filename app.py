from flask import Flask, render_template, request,redirect, session
from flask_session import Session
from db import db_connection

app = Flask(__name__)

# Configure sessions
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/admin", methods=['POST', "GET"])
def index():
    conn = db_connection()
    cusrsor = conn.cursor()
    if request.method == "POST":
        cusrsor.execute("SELECT cin, login, password FROM Administrateur WHERE login='admin' AND password='admin'")
        admin = cusrsor.fetchone()
        if request.form.get("login") and request.form.get("password") in admin:
            session["admin"] = admin[0]
            print(session["admin"])
            return redirect("/")
        else:
            return render_template("index.html", error="erorr")
        
    return render_template("index.html")

@app.route("/Logout")
def logout():
    session["admin"] = None
    return redirect("/")
#admin login





@app.route("/", methods=["POST", "GET"])
def dashboard():
    if not session.get("admin"):
        return redirect("/admin")
    return render_template("dashboard.html")
        
#gere etudiants
@app.route("/AjouterEtudiant", methods=["POST", "GET"])
def AjouterEtudiant():
    if not session.get("admin"):
        return redirect("/admin")
    conn = db_connection()
    cusrsor = conn.cursor()
    if request.method == "POST":
        etudiant = []
        for data in request.form:
            etudiant.append(request.form.get(data))
        query = "INSERT INTO Etudiant (cin, nom, prenom, login, password, age, niveau, filiere, groupe) VALUES(?,?,?,?,?,?,?,?,?)"
        cusrsor.execute(query, tuple(etudiant))
        conn.commit()
        return redirect("/ListEtudiants")
    return render_template("AjouterEtudiant.html")


@app.route("/ListEtudiants", methods=["POST", "GET"])
def listEtudiants():
    if not session.get("admin"):
        return redirect("/admin")
    conn = db_connection()
    cursor = conn.cursor()
    etudiants = cursor.execute("SELECT * from Etudiant")
    return render_template("ListEtudiants.html", etudiants=etudiants)
 


#gere matieres
@app.route("/AjouterMatiere", methods=["POST", "GET"])
def AjouterMatiere():
    if not session.get("admin"):
        return redirect("/admin")
    conn = db_connection()
    cursor = conn.cursor()
    if request.method == "POST":
        matiere = []
        for data in request.form:
            matiere.append(request.form.get(data))
        query = "INSERT INTO Matiere(codeMat, nom, heures, nom_enseignant, niveau, coeff) VALUES(?,?,?,?,?,?)"
        cursor.execute(query, tuple(matiere))
        conn.commit()
        return redirect("/ListMatiere")
    
    return render_template("AjouterMatiere.html")



@app.route("/ListMatiere", methods=["POST", "GET"])
def ListMatiere():
    if not session.get("admin"):
        return redirect("/admin")
    conn = db_connection()
    cursor = conn.cursor()
    matieres = cursor.execute("SELECT * from Matiere")
    
    return render_template("ListMatiere.html", matieres=matieres)


@app.route('/delete', methods=['POST'])
def delete():
    conn = db_connection()
    cursor = conn.cursor()
    if request.method == "POST":
        if 'deleteMatiere' in request.form:
            cursor.execute("DELETE FROM Matiere WHERE codeMat=?", (request.form.get("codeMat"),))
            conn.commit()
            return redirect("/ListMatiere")
        if 'desactivateEtudiant' in request.form:
            cursor.execute("DELETE FROM Etudiant WHERE cin=?", (request.form.get("cin"),))
            conn.commit()
            return redirect("/ListEtudiants")


@app.route("/note")
def note():
    if not session.get("admin"):
        return redirect("/admin")
    conn = db_connection()
    cursor1 = conn.cursor()
    cursor2 = conn.cursor()
    cursor1.execute("SELECT cin FROM Etudiant")
    cursor2.execute("SELECT codeMat from Matiere")
    cin = cursor1.fetchall()
    codeMat = cursor2.fetchall()
    print(cin)
    print(codeMat)
    return "note route"