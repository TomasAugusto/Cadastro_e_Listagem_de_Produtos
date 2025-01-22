from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    with sqlite3.connect('produtos.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                descricao TEXT NOT NULL,
                valor REAL NOT NULL,
                disponivel INTEGER NOT NULL
            )
        ''')
        conn.commit()


init_db()

@app.route('/')
def listagem_produtos():
    with sqlite3.connect('produtos.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, nome, valor FROM produtos WHERE disponivel = 1 ORDER BY valor ASC')
        disponiveis = [(row[0], row[1], f"R$ {row[2]:,.2f}") for row in cursor.fetchall()]
        cursor.execute('SELECT id, nome, valor FROM produtos WHERE disponivel = 0 ORDER BY valor ASC')
        nao_disponiveis = [(row[0], row[1], f"R$ {row[2]:,.2f}") for row in cursor.fetchall()]
    return render_template('listagem.html', disponiveis=disponiveis, nao_disponiveis=nao_disponiveis)

@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar_produto():
    if request.method == 'POST':
        # Obter dados do formulário
        nome = request.form['nome']
        descricao = request.form['descricao']
        valor = float(request.form['valor'])
        disponivel = 1 if request.form['disponivel'] == 'sim' else 0

        # Inserir produto no banco de dados
        with sqlite3.connect('produtos.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO produtos (nome, descricao, valor, disponivel)
                VALUES (?, ?, ?, ?)
            ''', (nome, descricao, valor, disponivel))
            conn.commit()

        return redirect(url_for('listagem_produtos'))

    return render_template('cadastrar.html')

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_produto(id):
    if request.method == 'POST':
        # Obter dados do formulário
        nome = request.form['nome']
        descricao = request.form['descricao']
        valor = float(request.form['valor'])
        disponivel = 1 if request.form['disponivel'] == 'sim' else 0

        # Atualizar produto no banco de dados
        with sqlite3.connect('produtos.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE produtos
                SET nome = ?, descricao = ?, valor = ?, disponivel = ?
                WHERE id = ?
            ''', (nome, descricao, valor, disponivel, id))
            conn.commit()

        return redirect(url_for('listagem_produtos'))

    # Obter dados do produto para edição
    with sqlite3.connect('produtos.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT nome, descricao, valor, disponivel FROM produtos WHERE id = ?', (id,))
        produto = cursor.fetchone()

    return render_template('editar.html', produto=produto, id=id)

if __name__ == '__main__':
    app.run(debug=True)