from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__) 

USUARIOS_REGISTRADOS = {
    "hola@gmail.com": {
        "password": "holamundo",
        "nombre": "Juan Perez",
         "altura_cm":"178cm",
        "peso_actual_kg":"70kg",
         "peso_objetivo_kg":"80kg",
        "nivel_actividad": 'muy_activo',
        "objetivo_salud":'ganar_musculo',
        "meta_semanal":'ganar_1kg' 
    }
}

app.config["SECRET_KEY"] = "una_clave_muy_larga_y_dificil_de_adivinar"

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/calcula')
def calc():
    return render_template('calculadora.html')

@app.route('/usuario')
def usuario():
    return render_template('usuario.html')

@app.route("/crear", methods=["GET", "POST"])
def crear():
    error = None
    if request.method == "POST":
        nombreCompleto = request.form.get("nombre")
        apellido = request.form.get("apellido")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmPassword = request.form.get("confirmPassword")
        fechaNacimiento = request.form.get("fechaNacimiento")
        genero = request.form.get("genero")
        genero_personalizado = request.form.get("genero_personalizado")

        if password != confirmPassword:
            error = "Las contraseñas no coinciden"
        elif not nombreCompleto or not email or not password:
            error = "Todos los campos obligatorios deben completarse."
        if error:
            flash(error, "error")
            return render_template("crear.html")
        return redirect(url_for("pregunta1"))

    return render_template("crear.html")


@app.route("/pregunta1", methods=["GET", "POST"])
def pregunta1():
    if request.method == "POST":
        respuesta = request.form.get("pregunta1")
        if not respuesta:
            flash("Debe seleccionar una opción antes de continuar.", "error")
            return redirect(url_for("pregunta1"))
        return redirect(url_for("pregunta2"))
    return render_template("pregunta1.html")


@app.route("/pregunta2", methods=["GET", "POST"])
def pregunta2():
    if request.method == "POST":
        respuesta2 = request.form.get("pregunta2")
        if not respuesta2:
            flash("Debe seleccionar una opción antes de continuar.", "error")
            return redirect(url_for("pregunta2"))
        return redirect(url_for("pregunta3"))
    return render_template("pregunta2.html")

@app.route("/pregunta3", methods=["GET", "POST"])
def pregunta3():
    if request.method == "POST":
        respuesta3 = request.form.get("pregunta3")
        if not respuesta3:
            flash("Debe seleccionar una opción antes de continuar.", "error")
            return redirect(url_for("pregunta3"))
        return redirect(url_for("pregunta4"))
    return render_template("pregunta3.html")

@app.route("/pregunta4", methods=["GET", "POST"])
def pregunta4():
    if request.method == "POST":
        respuesta4 = request.form.get("pregunta4")
        if not respuesta4:
            flash("Debe seleccionar una opción antes de continuar.", "error")
            return redirect(url_for("pregunta4"))
        session["respuesta_pregunta4"] = respuesta4
        return redirect(url_for("pregunta5"))  
    return render_template("pregunta4.html")

@app.route("/pregunta5", methods=["GET", "POST"])
def pregunta5():
    if request.method == "POST":
        respuesta5 = request.form.get("pregunta5")
        if not respuesta5:
            flash("Debe seleccionar una opción antes de continuar.", "error")
            return redirect(url_for("pregunta5"))
        return redirect(url_for("index")) 
    return render_template("pregunta5.html")

@app.route("/login")
def inicio():
    if session.get("logueado") == True:
        session.clear()
        return render_template('base.html')
    return render_template('login.html')


@app.route("/validalogin", methods=["POST", "GET"])
def validalogin():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        passwor = request.form.get("password")

        if not email or not passwor:
            flash("Debe ingresar un email y una contraseña", "error")
        elif email in USUARIOS_REGISTRADOS:
            usuario = USUARIOS_REGISTRADOS[email]
            if usuario["password"] == passwor:
                session["usuario_email"] = email
                session["usuario_nombre"] = usuario["nombre"]
                session["peso"] = usuario["peso_actual_kg"]
                session["altura"] = usuario["altura_cm"]
                session["pesoO"] =usuario["peso_objetivo_kg"]
                session["act"] = usuario["nivel_actividad"]
                session["obj"] = usuario[ "objetivo_salud"]
                session["logueado"] = True
                return redirect(url_for("index"))
            else:
                flash("Contraseña incorrecta", "error")
        else:
            flash("El usuario no está registrado", "error")

    return redirect(url_for("inicio"))

if __name__ == "__main__":
    app.run(debug=True)