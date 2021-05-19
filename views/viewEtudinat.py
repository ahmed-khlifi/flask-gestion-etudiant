def AjouterEtudiant():
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



def listEtudiants():
    conn = db_connection()
    cursor = conn.cursor()
    etudiants = cursor.execute("SELECT * from Etudiant")
    return render_template("ListEtudiants.html", etudiants=etudiants)