from flask import Flask, render_template, request, jsonify
import pandas as pd
from flask import send_file, Response
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('estoque.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS produtos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    quantidade INTEGER NOT NULL,
                    preco REAL NOT NULL)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/produtos', methods=['GET'])
def listar_produtos():
    conn = sqlite3.connect('estoque.db')
    c = conn.cursor()
    c.execute("SELECT * FROM produtos")
    produtos = c.fetchall()
    conn.close()
    return jsonify(produtos)

@app.route('/api/adicionar', methods=['POST'])
def adicionar_produto():
    dados = request.get_json()
    nome = dados['nome']
    quantidade = dados['quantidade']
    preco = dados['preco']
    
    conn = sqlite3.connect('estoque.db')
    c = conn.cursor()
    c.execute("INSERT INTO produtos (nome, quantidade, preco) VALUES (?, ?, ?)", (nome, quantidade, preco))
    conn.commit()
    conn.close()

@app.route('/remover/<int:id>', methods=['DELETE'])
def remover_produto(id):
    conn = sqlite3.connect('estoque.db')
    c = conn.cursor()
    c.execute("DELETE FROM produtos WHERE id = ?", (id,))
    conn.commit()
    conn.close()    

@app.route('/atualizar_produto/<int:id>', methods=['PUT'])
def atualizar_produto(id):
    dados = request.get_json() 
    quantidade = dados['quantidade']
    preco = dados['preco']

    conn = sqlite3.connect('estoque.db')
    c = conn.cursor()
    c.execute('UPDATE produtos SET quantidade = ?, preco = ? WHERE id = ?', (quantidade, preco, id)) 
    conn.commit()
    conn.close()

    return jsonify({"mensagem": "Produto atualizado com sucesso"})

@app.route('/exportar_excel', methods=['GET'])
def exportar_excel():
    conn = sqlite3.connect('estoque.db')
    df = pd.read_sql_query("SELECT * FROM produtos",conn)
    conn.close()

    from io import BytesIO
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    output.seek(0)

    return Response(
        output,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=relatorio_estoque.xlsx"}
    )