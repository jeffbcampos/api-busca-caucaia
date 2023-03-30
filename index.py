from flask import Flask, request, jsonify
from flask_cors import CORS
from Controle.funcs import *
from Controle.classConexao import Conexao
from dotenv import load_dotenv
load_dotenv()
import os

try:
    
    con = Conexao(host=os.getenv("HOST"), user=os.getenv("USER"), password=os.getenv("PASSWORD"), port=os.getenv("PORT"), database=os.getenv("DATABASE"))
    print("conectado")    
    
    app = Flask(__name__)

    CORS(app)   

    @app.route('/')
    def home():
        return 'API em construção'

    @app.route('/inserirEstabelecimento', methods=['POST'])
    def inserir_estabelecimento():
        categoria = request.form['categoria']
        nome = request.form['nome']
        imagem = request.files['imagem']
        telefone = request.form['telefone']
        cep = request.form['cep']
        numero = request.form['numero']
        observacao = request.form['observacao']
        produtos = request.form['produtos']
        url = uploadImg(imagem)
        sql = "INSERT INTO estabelecimento (categoria_id, nome, imagem, telefone, cep, numero, observacao, produtos) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        values = (categoria, nome, url, telefone, cep, numero, observacao, produtos)
        con.queryExecute(sql, values)
        return jsonify({'status': 'success'})   

    @app.route('/categorias', methods=['GET'])
    def categorias():
        sql = "SELECT * FROM categoria"
        results = con.querySelect(sql, values=None)    
        return jsonify(results)

    @app.route('/mercados', methods=['GET'])
    def mercados():
        sql = f"SELECT * FROM estabelecimento WHERE categoria_id = '3' "
        results = con.querySelect(sql, values=None)    
        return jsonify(results)

    @app.route('/inserirUsuario', methods=['POST'])
    def inserir_usuario():
        nome = request.json['nome']
        email = request.json['email']
        telefone = request.json['telefone']
        cep = request.json['cep']
        endereco = request.json['endereco']
        bairro = request.json['bairro']
        senha = request.json['senha']
        sql = "INSERT INTO usuario (nome, email, telefone, cep, endereco, bairro, senha) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (nome, email, telefone, cep, endereco, bairro, senha)
        print(values)
        con.queryExecute(sql, values)
        return jsonify({'status': 'success'})
        
            
    @app.route('/categoria/<int:id>', methods=['GET'])
    def get_categoria(id):
        sql = f"SELECT * FROM estabelecimento WHERE categoria_id = '{id}'"
        results = con.querySelect(sql, values=None)
        return jsonify(results) 
        

    if __name__ == '__main__':
        app.run(debug=True)
except Exception as e:
    print(e)