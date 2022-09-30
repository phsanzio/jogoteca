from flask import Flask, render_template, request, redirect, session, flash, url_for, abort, g
import usuarios

class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console


jogo1 = Jogo('CSGO', 'Tiro', 'PC')
jogo2 = Jogo('God of War', 'Hack n Slash', 'Playstation')
lista = [jogo1, jogo2]


app = Flask(__name__)
app.secret_key = 'ifmg'

@app.route('/')
def index():
    return render_template('lista.html', titulo='Jogos', jogos=lista)


@app.route('/novo')
def novo():
    if not usuario_logado():
      abort(403)
      
    return render_template('novo.html', titulo='Novo Jogo')


@app.route('/criar', methods=['POST',])
def criar():
    if not usuario_logado():
      abort(403)
    
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)

    lista.append(jogo)
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    email = request.form['email']
    senha = request.form['senha']
    usuario = usuarios.buscar(email, senha)
    if usuario is None:
      flash('Usuário/senha inválidos.')
    else:
      session['usuario_email'] = usuario.email
      session['usuario_nome'] = usuario.nome
      return redirect(url_for('index'))
      
  return render_template('login.html')

@app.route('/logout', methods=['POST'])
def logout():
  session.pop('usuario_email', None)
  session.pop('usuario_nome', None)
  return redirect(url_for('index'))

def usuario_logado():
  return 'usuario_email' in session

@app.errorhandler(403)
def acesso_negado(erro):
  return render_template('acesso_negado.html', titulo='Ops!'), 403

@app.before_request
def carregar_usuario():
  if 'usuario_email' in session:
    g.usuario = usuarios.buscar_por_email(session['usuario_email'])

app.run(host='0.0.0.0', port=81, debug=True)