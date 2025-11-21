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
def calculadora():
    
    return render_template('calculadora.html')

@app.route("/imc", methods=["GET", "POST"])
def imc():
    if request.method == "POST":
        peso = float(request.form["peso"])
        altura_cm = float(request.form["altura"])
        altura_m = altura_cm / 100
        imc_value  = round((peso / (altura_m ** 2)),2)
        if imc_value < 18.5:
            estado = "Bajo peso"
        elif imc_value < 25:
            estado = "Normal"
        elif imc_value < 30:
            estado = "Sobrepeso"
        else:
            estado = "Obesidad"
        return render_template("imc.html", imc=imc_value, estado=estado)
    
    return render_template("imc.html")



@app.route("/tmb", methods=["GET", "POST"])
def tmb():
    if request.method == "POST":
        peso = float(request.form["peso"])
        altura = float(request.form["altura"])
        edad = int(request.form["edad"])
        sexo = request.form["sexo"]
        if sexo == "hombre":
            tmb_value = round((10*peso + 6.25*altura - 5*edad + 5),2)
        else:
            tmb_value = round((10*peso + 6.25*altura - 5*edad - 161),2)
        return render_template("TMB.html", tmb=tmb_value)
    return render_template("TMB.html")

@app.route("/gct", methods=["GET", "POST"])
def gct():
    if request.method == "POST":
        tmb = float(request.form["tmb"])
        actividad = request.form["actividad"]
        factores = {
            "sedentario": 1.2,
            "ligero": 1.375,
            "moderado": 1.55,
            "activo": 1.725,
            "muy_activo": 1.9
        }
        gct_value = round((tmb * factores[actividad]),2)
        return render_template("gct.html", gct=gct_value)
    return render_template("gct.html")


@app.route("/peso_ideal", methods=["GET", "POST"])
def peso_ideal():
    if request.method == "POST":
        altura_cm = float(request.form["altura"])
        sexo = request.form["sexo"]
        altura_in = altura_cm / 2.54
        if sexo == "hombre":
            ideal = 50 + 2.3 * (altura_in - 60)
        else:
            ideal = 45.5 + 2.3 * (altura_in - 60)
        return render_template("peso_ideal.html", ideal=ideal)
    return render_template("peso_ideal.html")




@app.route("/macros", methods=["GET", "POST"])
def macros():
    if request.method == "POST":
        calorias = float(request.form["calorias"])
        objetivo = request.form["objetivo"]
        perfiles = {
            "perder_grasa": {"p": 0.30, "c": 0.40, "g": 0.30},
            "mantenimiento": {"p": 0.25, "c": 0.50, "g": 0.25},
            "ganar_musculo": {"p": 0.30, "c": 0.50, "g": 0.20}
        }
        p = (calorias * perfiles[objetivo]["p"]) / 4
        c = (calorias * perfiles[objetivo]["c"]) / 4
        g = (calorias * perfiles[objetivo]["g"]) / 9
        return render_template("macros.html", p=p, c=c, g=g)
    return render_template("macros.html")

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