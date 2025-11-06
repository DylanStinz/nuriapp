from flask import Flask, render_template, request , redirect ,url_for ,flash,session
app=Flask(__name__)
USUARIOS_REGISTRADOS = {
    "hola@gmail.com":{
        "password":"holamundo",
        "nombre":"Juan Perez"        
    }    
}
app.config["SECRET_KEY"]="una_clave_muy_larga_y_dificil_de_adivinar"
@app.route('/')
def index():
    return render_template('base.html')

@app.route('/encuest1')
def encues():
    return render_template('encuesta.html')

@app.route('/calcula')
def calc():
    return render_template('calculadora.html')


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
        else:
            return redirect(url_for("encues"))
        
        
    return render_template("crear.html")


@app.route("/login")
def inicio():
    if session.get("logueado")==True:
        session.clear()
        return render_template('base.html')
    return render_template('login.html')


@app.route("/validalogin", methods=["POST", "GET"])
def validalogin():
    if request.method=="POST":
        email=request.form.get("email", "").strip()
        passwor=request.form.get("password")
    
    if not email or not passwor:
        flash("Debe ingresar un email y una contraseña", "error")
    elif email in USUARIOS_REGISTRADOS:
        usuario= USUARIOS_REGISTRADOS[email]
        if usuario["password"]==passwor:
            session["usuario_email"]=email
            session["usuario_nombre"]=usuario["nombre"]
            session["logueado"]=True
            
            return redirect(url_for("index"))
        else:
            flash("Contraseña incorrecta", "error")
    else:
        flash("El usuario no está registrado", "error")
    return redirect(url_for("inicio"))

if __name__ == "__main__":
    app.run(debug=True)