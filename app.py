from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from flask import flash

load_dotenv()

app = Flask(__name__)

app.secret_key = "una_clave_super"

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root@localhost:3306/encontrar_error"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
                                                                                                                        
from models import User

 
@app.route('/')
def index():
    return render_template('base.html')

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method=='POST':
        nombre = request.form.get('username')
        email = request.form.get('email')
    
        
        if User.query.filter_by(email=email).first():
            flash("Ese email ya está registrado", "warning")
            return redirect(url_for('users'))
        
        nuevo_usuario = User(username=nombre, email=email)
        db.session.add(nuevo_usuario)
        db.session.commit()    
    
        flash("Usuario creado con éxito", "success")
        return redirect(url_for('users'))
    
    usuarios= User.query.all()
    return render_template('users.html', users=usuarios)

if __name__ == '__main__':
    app.run(debug=True)
