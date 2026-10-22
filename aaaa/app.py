import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash

# Configuração que define 'front_end' como a pasta principal de HTML e CSS
app = Flask(__name__, template_folder='front_end', static_folder='front_end',  static_url_path='')

app.secret_key = 'chave_secreta_infratec'

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Tabela de Usuários
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL
        )
    ''')
    
    # Tabela de Funcionários
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS funcionarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            matricula TEXT NOT NULL,
            nome TEXT NOT NULL,
            setor TEXT NOT NULL,
            cargo TEXT NOT NULL
        )
    ''')

    # Tabela de Ocorrências
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ocorrencias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            matricula TEXT NOT NULL,
            tipo TEXT NOT NULL,
            gravidade TEXT NOT NULL,
            data TEXT NOT NULL
        )
    ''')

    # Tabela de EPIs
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS epis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            matricula TEXT NOT NULL,
            epi TEXT NOT NULL,
            entrega TEXT NOT NULL,
            validade TEXT NOT NULL,
            status TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

init_db()

@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')

# Cadastro
@app.route('/cadastro.html', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form.get('nome_sistema')
        email = request.form.get('email')
        senha = request.form.get('senha')

        if not nome or not email or not senha:
            flash('Preencha todos os campos.')
            return redirect(url_for('cadastro'))

        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)', (nome, email, senha))
            conn.commit()
            conn.close()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('E-mail já cadastrado.')
            return redirect(url_for('cadastro'))

    return render_template('cadastro.html')

# Login
@app.route('/login.html', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE email = ? AND senha = ?', (email, senha))
        user = cursor.fetchone()
        conn.close()

        if user:
            return redirect(url_for('dashboard'))
        else:
            flash('Credenciais inválidas.')
            return redirect(url_for('login'))

    return render_template('login.html')

# Dashboard
@app.route('/dashboard.html')
def dashboard():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM funcionarios')
    total_funcionarios = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM ocorrencias')
    total_ocorrencias = cursor.fetchone()[0]
    
    conn.close()
    
    return render_template('dashboard.html', 
                           total_funcionarios=total_funcionarios, 
                           total_ocorrencias=total_ocorrencias)

# Funcionários
@app.route('/funcionarios.html', methods=['GET', 'POST'])
def funcionarios():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        nome = request.form.get('nome')
        setor = request.form.get('setor')
        cargo = request.form.get('cargo')

        # Gera a matrícula automática iniciando em 1001 (1001, 1002, 1003...)
        cursor.execute('SELECT COUNT(*) FROM funcionarios')
        total = cursor.fetchone()[0]
        matricula_auto = str(1001 + total)

        if nome and setor and cargo:
            cursor.execute('INSERT INTO funcionarios (matricula, nome, setor, cargo) VALUES (?, ?, ?, ?)',
                           (matricula_auto, nome, setor, cargo))
            conn.commit()

    cursor.execute('SELECT matricula, nome, setor, cargo FROM funcionarios')
    lista_funcionarios = cursor.fetchall()
    conn.close()

    return render_template('funcionarios.html', funcionarios=lista_funcionarios)

# EPIs
@app.route('/epis.html')
def epis():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM epis')
    lista_epis = cursor.fetchall()
    conn.close()

    return render_template('epis.html', epis=lista_epis)

# Ocorrências
@app.route('/ocorrencias.html', methods=['GET', 'POST'])
def ocorrencias():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        tipo = request.form.get('tipo')
        gravidade = request.form.get('gravidade')
        data = request.form.get('data')

        # Gera a matrícula automática no formato '01', '02', '03'...
        cursor.execute('SELECT COUNT(*) FROM ocorrencias')
        total = cursor.fetchone()[0]
        matricula_auto = f"{total + 1:02d}"

        if tipo and gravidade and data:
            cursor.execute('INSERT INTO ocorrencias (matricula, tipo, gravidade, data) VALUES (?, ?, ?, ?)',
                           (matricula_auto, tipo, gravidade, data))
            conn.commit()

    cursor.execute('SELECT id, matricula, tipo, gravidade, data FROM ocorrencias')
    lista_ocorrencias = cursor.fetchall()
    conn.close()

    return render_template('ocorrencias.html', ocorrencias=lista_ocorrencias)

# Outras páginas
@app.route('/treinamentos.html')
def treinamentos():
    return render_template('treinamentos.html')

@app.route('/inspecoes.html')
def inspecoes():
    return render_template('inspecoes.html')

@app.route('/profissionais.html')
def profissionais():
    return render_template('profissionais.html')

@app.route('/relatorios.html')
def relatorios():
    return render_template('relatorios.html')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False) 