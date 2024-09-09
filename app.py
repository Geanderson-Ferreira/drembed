from flask import Flask, flash, render_template, request, redirect, url_for, session
from src.auth import auth
from src.SQLManager import get_valid_reports

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['PERMANENT_SESSION_LIFETIME'] = 900

# Tela de Login
@app.route('/')
def login():
    return render_template('login.html')

# Endpoint para Requisição de Login
@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']

    try:
        if auth(username, password):
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            flash('Credenciais incorretas ou não permitidas.', 'danger')
            return redirect(url_for('login'))
    except Exception as e:
        print(e)
        flash(f'Credenciais incorretas ou não permitidas.', 'danger')
        return redirect(url_for('login'))

# Endpoint para Requisição de Logout
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

# Tela dos botões, escolha o relatório
@app.route('/index', methods=['GET', 'POST'])
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        reports = get_valid_reports()
        return render_template('index.html', reps=reports[0].keys()) 

# Função base para renderizar o report escolhido
@app.route('/<report>', methods=['GET', 'POST'])
def report(report):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        reports = get_valid_reports()
        iframe_dict = reports[0]
        indicator_dict = reports[1]
        
        try:
            return render_template('base.html', rep=iframe_dict[report], rep_type=indicator_dict[report]) 
        except KeyError:
            report_keys = iframe_dict.keys()
            return redirect(url_for('index', reps=list(report_keys)))

@app.errorhandler(500)
def handle_500_error(e):
    
    # Renderiza uma página personalizada ou redireciona para outra rota
    return redirect(url_for('index', reps=[]))


# Roda o server
if __name__ == '__main__':
    app.run(debug=True)
