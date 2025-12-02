from flask import Flask, render_template, request, redirect, url_for, flash, session
import pymysql
pymysql.install_as_MySQLdb()
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import re
import requests

app = Flask(__name__) 

API_KEY = "aac9bd7f35444ba5ba14e9de0a3a5aeb"
API_URL = "https://api.spoonacular.com/recipes/complexSearch"

USUARIOS_REGISTRADOS = {
    "hola@gmail.com": {
        "password": "holamundo",
        "nombre": "Juan Perez",
        "altura_cm": "178cm",
        "peso_actual_kg": "70kg",
        "peso_objetivo_kg": "80kg",
        "nivel_actividad": 'muy_activo',
        "objetivo_salud": 'ganar_musculo',
        "meta_semanal": 'ganar_1kg' 
    }
}

app.config["SECRET_KEY"] = "una_clave_muy_larga_y_dificil_de_adivinar"


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'              
app.config['MYSQL_PASSWORD'] = ''  
app.config['MYSQL_DB'] = 'fitbite'         
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)


@app.route('/')
def index():
    return render_template('base.html')

@app.route('/calcula')
def calculadora():
    return render_template('calculadora.html')

@app.route("/imc", methods=["GET", "POST"])
def imc():
    imagen_estado = None
    reproducir_audio = False
    estado = None
    imc_value = None

    if request.method == "POST":
        peso = float(request.form["peso"])
        altura_cm = float(request.form["altura"])
        altura_m = altura_cm / 100
        imc_value = round(peso / (altura_m ** 2), 2)

        if imc_value < 18.5:
            estado = "Bajo peso"
            imagen_estado = "image/21.png"
        elif imc_value < 25:
            estado = "Normal"
            imagen_estado = "image/22.png"
        elif imc_value < 30:
            estado = "Sobrepeso"
            imagen_estado = "image/23.png"
        else:
            estado = "Obesidad"
            imagen_estado = "image/24.png"
            reproducir_audio = True   

        return render_template(
            "imc.html",
            imc=imc_value,
            estado=estado,
            imagen_estado=imagen_estado,
            reproducir_audio=reproducir_audio
        )

    return render_template("imc.html")



@app.route("/tmb", methods=["GET", "POST"])
def tmb():
    tmb_value = None
    gct_value = None

    if request.method == "POST":
        peso = float(request.form["peso"])
        altura = float(request.form["altura"])
        edad = int(request.form["edad"])
        sexo = request.form["sexo"]
        actividad = request.form["actividad"]

        if sexo.lower() == "hombre":
            tmb_value = round(10*peso + 6.25*altura - 5*edad + 5, 2)
        else:
            tmb_value = round(10*peso + 6.25*altura - 5*edad - 161, 2)

        factores = {
            "sedentario": 1.2,
            "ligero": 1.375,
            "moderado": 1.55,
            "activo": 1.725,
            "muy_activo": 1.9
        }

        gct_value = round(tmb_value * factores[actividad], 2)

        return render_template("TMB.html", tmb=tmb_value, gct=gct_value)

    return render_template("TMB.html")

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
        
        ideal = round(ideal, 2) 
        
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
    if 'usuario_id' not in session:
        flash('Debes iniciar sesión.', 'warning')
        return redirect(url_for('inicio'))

    usuario_id = session['usuario_id']

    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT p1, p2, p3, p4, p5
        FROM preguntas
        WHERE usuario_id = %s
        ORDER BY id DESC
        LIMIT 1
    """, (usuario_id,))
    respuestas = cur.fetchone()
    cur.close()

    return render_template('usuario.html', respuestas=respuestas)


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
        altura_cm        = request.form.get("altura_cm")
        peso_actual_kg   = request.form.get("peso_actual_kg")
        peso_objetivo_kg = request.form.get("peso_objetivo_kg")

        if password != confirmPassword:
            error = "Las contraseñas no coinciden"
        elif not nombreCompleto or not email or not password:
            error = "Todos los campos obligatorios deben completarse."

        if error:
            flash(error, "error")
            return render_template("crear.html")

        password_hash = generate_password_hash(password)

        cursor = mysql.connection.cursor()
        cursor.execute("""
            INSERT INTO usuarios (
                nombre, apellido, correo, password_hash, nacimiento,
                genero, altura, actual, objetivo
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            nombreCompleto,
            apellido,
            email,
            password_hash,
            fechaNacimiento,
            genero if genero != "personalizado" else "personalizado",
            altura_cm,
            peso_actual_kg,
            peso_objetivo_kg
        ))
        mysql.connection.commit()

        flash("Cuenta creada con éxito. Ahora responde unas preguntas.", "success")
        return redirect(url_for("pregunta1"))

    return render_template("crear.html")


@app.route('/pregunta1', methods=['GET', 'POST'])
def pregunta1():
    if 'usuario_id' not in session:
        flash('Primero inicia sesión.', 'warning')
        return redirect(url_for('inicio'))
    if request.method == 'POST':
        respuesta = request.form.get('pregunta1')
        if not respuesta:
            flash('Selecciona una opción para continuar.', 'danger')
            return redirect(url_for('pregunta1'))
        session['p1'] = respuesta
        return redirect(url_for('pregunta2'))

    return render_template('pregunta1.html')



@app.route('/pregunta2', methods=['GET', 'POST'])
def pregunta2():
    if 'usuario_id' not in session:
        flash('Primero inicia sesión.', 'warning')
        return redirect(url_for('inicio'))
    if request.method == 'POST':
        respuesta = request.form.get('pregunta2')
        if not respuesta:
            flash('Selecciona una opción para continuar.', 'danger')
            return redirect(url_for('pregunta2'))
        session['p2'] = respuesta
        return redirect(url_for('pregunta3'))

    return render_template('pregunta2.html')



@app.route('/pregunta3', methods=['GET', 'POST'])
def pregunta3():
    if 'usuario_id' not in session:
        flash('Primero inicia sesión.', 'warning')
        return redirect(url_for('inicio'))
    if request.method == 'POST':
        respuesta = request.form.get('pregunta3')
        if not respuesta:
            flash('Selecciona una opción para continuar.', 'danger')
            return redirect(url_for('pregunta3'))
        session['p3'] = respuesta
        return redirect(url_for('pregunta4'))

    return render_template('pregunta3.html')



@app.route('/pregunta4', methods=['GET', 'POST'])
def pregunta4():
    if 'usuario_id' not in session:
        flash('Primero inicia sesión.', 'warning')
        return redirect(url_for('inicio'))
    if request.method == 'POST':
        respuesta = request.form.get('pregunta4')
        if not respuesta:
            flash('Selecciona una opción para continuar.', 'danger')
            return redirect(url_for('pregunta4'))
        session['p4'] = respuesta
        return redirect(url_for('pregunta5'))

    return render_template('pregunta4.html')


@app.route('/pregunta5', methods=['GET', 'POST'])
def pregunta5():
    if 'usuario_id' not in session:
        flash('Primero inicia sesión.', 'warning')
        return redirect(url_for('inicio'))
    if request.method == 'POST':
        respuesta = request.form.get('pregunta5')
        if not respuesta:
            flash('Selecciona una opción para continuar.', 'danger')
            return redirect(url_for('pregunta5'))
        session['p5'] = respuesta
        p1 = session.get('p1')
        p2 = session.get('p2')
        p3 = session.get('p3')
        p4 = session.get('p4')
        p5 = session.get('p5')
        usuario_id = session['usuario_id']
        if not all([p1, p2, p3, p4, p5]):
            flash('Faltan respuestas, vuelve a comenzar la encuesta.', 'danger')
            return redirect(url_for('pregunta1'))
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO preguntas (usuario_id, p1, p2, p3, p4, p5)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (usuario_id, p1, p2, p3, p4, p5))
        mysql.connection.commit()
        cur.close()
        for clave in ['p1', 'p2', 'p3', 'p4', 'p5']:
            session.pop(clave, None)
        flash('Respuestas guardadas correctamente.', 'success')
        return redirect(url_for('usuario'))

    return render_template('pregunta5.html')


@app.route("/descarg")
def pdf():
    return render_template('descarg.html')


@app.route("/recetas")
def recetasParamancos():
    return render_template('recetas.html')

@app.route("/hidra")
def Hydra():
    return render_template('hidra.html')

@app.route("/vm")
def mitYvrd():
    return render_template('vm.html')

@app.route("/consejos")
def consejos():
    return render_template('consejos.html')

@app.route("/login")
def inicio():
    if session.get("logueado") == True:
        return redirect(url_for('usuario'))
    return render_template('login.html')


@app.route("/validalogin", methods=["POST", "GET"])
def validalogin():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        passwor = request.form.get("password")

        if not email or not passwor:
            flash("Debe ingresar un email y una contraseña", "error")
            return redirect(url_for("inicio"))

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE correo = %s", (email,))
        usuario = cursor.fetchone()

        if usuario:
            if check_password_hash(usuario["password_hash"], passwor):

                session["usuario_id"] = usuario["id"]      
                session["usuario_email"] = usuario["correo"]
                session["usuario_nombre"] = usuario["nombre"] + " " + usuario["apellido"]
                session["peso"] = usuario["actual"]
                session["altura"] = usuario["altura"]
                session["pesoO"] = usuario["objetivo"]
                session["act"] = usuario.get("nivel_actividad") if isinstance(usuario, dict) else None
                session["obj"] = usuario.get("objetivo_salud") if isinstance(usuario, dict) else None
                session["logueado"] = True

                return redirect(url_for("usuario"))
            else:
                flash("Contraseña incorrecta", "error")
                return redirect(url_for("inicio"))

        elif email in USUARIOS_REGISTRADOS:
            usuario = USUARIOS_REGISTRADOS[email]
            if usuario["password"] == passwor:
                session["usuario_email"] = email
                session["usuario_nombre"] = usuario["nombre"]
                session["peso"] = usuario["peso_actual_kg"]
                session["altura"] = usuario["altura_cm"]
                session["pesoO"] = usuario["peso_objetivo_kg"]
                session["act"] = usuario["nivel_actividad"]
                session["obj"] = usuario["objetivo_salud"]
                session["logueado"] = True
                return redirect(url_for("usuario"))
            else:
                flash("Contraseña incorrecta", "error")
        else:
            flash("El usuario no está registrado", "error")

    return redirect(url_for("inicio"))


@app.route("/logout")
def logout():
    session.clear()  
    flash("Sesión cerrada correctamente.", "success")
    return redirect(url_for("index")) 

@app.route("/analiza", methods=["GET", "POST"])
def anal():
    foods = []   # Lista para almacenar resultados
    query = None

    if request.method == "POST":
        query = request.form.get("query", "").strip()  # Obtener búsqueda

        if not query:
            flash("Por favor, escribe un alimento para buscar.", "warning")
        else:
            params = {
                "apiKey": API_KEY,          # API key
                "query": query,             # Alimento a buscar
                "number": 9,                # Número máximo de resultados
                "addRecipeNutrition": True  # Incluir información nutricional
            }

            try:
                response = requests.get(API_URL, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()

                results = data.get("results", [])

                for item in results:
                    try:
                        nutrients = item.get("nutrition", {}).get("nutrients", [])

                        calories = nutrients[0]["amount"]
                        fat = nutrients[1]["amount"]
                        saturated = nutrients[2]["amount"]
                        carbs = nutrients[3]["amount"]

                        # Evaluación rápida de salud
                        healthy = (
                            calories < 650 and
                            fat < 25 and
                            saturated < 8 and
                            carbs < 70
                        )
                    except:
                        healthy = None

                    foods.append({
                        "id": item.get("id"),
                        "title": item.get("title"),
                        "image": item.get("image"),
                        "nutrition": item.get("nutrition"),
                        "healthy": healthy
                    })

                if not foods:
                    flash(f"No se encontraron resultados para '{query}'.", "info")

            except requests.exceptions.RequestException:
                flash("Error al conectar con la API.", "danger")

    return render_template("analiza.html", foods=foods, query=query)


@app.route("/api", methods=["GET", "POST"])
def api():
    foods = []   
    query = None

    if request.method == "POST":
        query = request.form.get("query", "").strip()

        if not query:
            flash("Por favor, escribe un alimento para buscar.", "warning")
        else:
            params = {
                "apiKey": API_KEY,
                "query": query,
                "number": 9
            }

            try:
                response = requests.get(API_URL, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()

                results = data.get("results", [])
                foods = []
                for item in results:
                    name = item.get("title") or item.get("name") or "Nombre no disponible"
                    image = item.get("image", "")
                    foods.append({"name": name, "image": image})

                if not foods:
                    flash(f"No se encontraron resultados para '{query}'.", "info")

            except requests.exceptions.RequestException:
                flash("Error al conectar con la API.", "danger")

    return render_template("apiresultado.html", foods=foods, query=query)


@app.route("/apiresultado", methods=["GET", "POST"])
def apiresultado():
    return render_template('apiresultado.html')

if __name__ == "__main__":
    app.run(debug=True)