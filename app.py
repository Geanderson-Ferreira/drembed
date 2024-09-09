from flask import Flask, flash, render_template, request, redirect, url_for, session
from src.auth import auth
from src.SQLManager import get_session, get_valid_reports
from os import environ

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = 'supersecretkey'

#Tempo de sessão válida
app.config['PERMANENT_SESSION_LIFETIME'] = 900

#Tela de Login
@app.route('/')
def login():
    return render_template('login.html')

#Endpoint para Requisição de Login
@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    Auth = auth(username, password, get_session(environ['DATABASE_URL']))
    if Auth != False:
        session['logged_in'] = True
        return redirect(url_for('index'))
    else:
        flash('Incorreto ou não permitido.', 'danger')
        return redirect(url_for('login'))

#Endpoint para Requisição de Logout
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

#Tela dos botões, escolha o relatório
@app.route('/index', methods=['GET', 'POST'])
def index():
    
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        reports = get_valid_reports(get_session(environ['DATABASE_URL']))
        return render_template('index.html', reps=reports[0].keys()) 

#Função base para renderizar o report escolhido
@app.route('/<report>', methods=['GET', 'POST'])
def report(report):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:

        reports = get_valid_reports(get_session(environ['DATABASE_URL']))
        iframe_dict = reports[0]
        indicator_dict = reports[1]
        
        try:
            return render_template('base.html', rep=iframe_dict[report], rep_type=indicator_dict[report]) 
        except:
            report_keys = iframe_dict.keys()
            return redirect(url_for('index', reps=list(report_keys)))

@app.route('/rep-content')
def render_rep_content():
    rep = request.args.get('rep')  # Obtém o parâmetro 'rep' da URL
    return render_template('rep_content.html', rep=rep)


#Roda o serverpy
if __name__ == '__main__':
    app.run(debug=True)