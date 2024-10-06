from flask import Flask, session, redirect, url_for, request, g, render_template
import sqlite3


# Le problème courant dans la gestion des sessions est l'absence de régénération d'ID de session après l'authentification.
# Cela peut exposer l'application à des attaques comme le Session Fixation.
# Code Flask vulnérable à la gestion des sessions
# Ici, après l'authentification, l'ID de session n'est pas régénéré, ce qui permet à un attaquant qui connaît ou fixe 
# l'ID de session avant l'authentification d'accéder à la session de l'utilisateur après connexion.


app = Flask(__name__)
app.secret_key = 'mysecretkey'

DATABASE = 'users.db'

# Connexion à la base de données
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

# Fermeture de la connexion à la base de données après chaque requête
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Fonction pour démarrer la session (sans régénération d'ID)
def start_session(user_id):
    session['user_id'] = user_id

# Création de la table des utilisateurs (à exécuter une seule fois)
def create_user_table():
    with app.app_context():
        db = get_db()
        db.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL UNIQUE,
                        password TEXT NOT NULL)''')
        db.commit()

# Ajout d'un utilisateur dans la base de données
def add_user(username, password):
    db = get_db()
    try:
        db.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        db.commit()
        return True
    except sqlite3.IntegrityError:
        return False

# Vérification de l'utilisateur dans la base de données
def verify_user(username, password):
    db = get_db()
    cur = db.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    return cur.fetchone()

# Route de création de compte
@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if add_user(username, password):
            return redirect(url_for('login'))
        else:
            return "Nom d'utilisateur déjà pris"
    return render_template('register.html')

# Route de connexion
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = verify_user(username, password)
        if user:
            start_session(user[0])  # Démarre la session avec l'ID utilisateur
            return redirect(url_for('profile'))
        else:
            return 'Échec de la connexion, vérifiez vos identifiants.'
    return render_template('login.html')

# Route du profil utilisateur
@app.route('/profile')
def profile():
    if 'user_id' in session:
        user_id = session['user_id']
        db = get_db()
        cur = db.execute("SELECT username FROM users WHERE id = ?", (user_id,))
        user = cur.fetchone()
        if user:
            return f"Profil de l'utilisateur : {user[0]}"
    return 'Non authentifié. Veuillez vous connecter.'

if __name__ == '__main__':
    create_user_table()  # Crée la table des utilisateurs si elle n'existe pas
    app.run(debug=True)
