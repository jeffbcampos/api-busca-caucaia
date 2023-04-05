from flask import Flask, request, jsonify, redirect
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
        endereco = request.form['endereco']
        bairro = request.form['bairro']
        descricao = request.form['descricao']
        horariofechamento = request.form['fimHorario']
        horarioabertura = request.form['inicioHorario']
        finalsemana = request.form['fimSemana']
        iniciosemana = request.form['inicioSemana']
        produtos = request.form['produtos']
        filename = imagem.filename
        mimetype = imagem.mimetype
        # imagem.save(filename)
        url = fazer_upload_para_drive(filename, imagem, mimetype, os.getenv("FOLDER"))
        sql = "INSERT INTO estabelecimento (id_categoria, nome, imagem, telefone, cep, numero, descricao, produtos, endereco, bairro, horariofechamento, horarioabertura, finalsemana, iniciosemana) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (categoria, nome, url, telefone, cep, numero, descricao, produtos, endereco, bairro, horariofechamento, horarioabertura, finalsemana, iniciosemana)
        con.queryExecute(sql, values)
        # os.remove(filename)
        return jsonify({'status': 'success'})   

    @app.route('/categorias', methods=['GET'])
    def categorias():
        sql = "SELECT * FROM categoria"
        results = con.querySelect(sql, values=None)           
        return jsonify(results)
    
    @app.route('/lanchonetes', methods=['GET'])
    def lanchonetes():
        sql = f"SELECT * FROM estabelecimento WHERE id_categoria = '1' "
        results = con.querySelect(sql, values=None)    
        return jsonify(results)
    
    @app.route('/academias', methods=['GET'])
    def academias():
        sql = f"SELECT * FROM estabelecimento WHERE id_categoria = '2' "
        results = con.querySelect(sql, values=None)    
        return jsonify(results)
    
    @app.route('/mercados', methods=['GET'])
    def mercados():
        sql = f"SELECT * FROM estabelecimento WHERE id_categoria = '3' "
        results = con.querySelect(sql, values=None)    
        return jsonify(results)
    
    @app.route('/petshop', methods=['GET'])
    def petshop():
        sql = f"SELECT * FROM estabelecimento WHERE id_categoria = '4' "
        results = con.querySelect(sql, values=None)    
        return jsonify(results)
    
    @app.route('/farmacia', methods=['GET'])
    def farmacia():
        sql = f"SELECT * FROM estabelecimento WHERE id_categoria = '5' "
        results = con.querySelect(sql, values=None)    
        return jsonify(results)

    @app.route('/otica', methods=['GET'])
    def otica():
        sql = f"SELECT * FROM estabelecimento WHERE id_categoria = '6' "
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
        con.queryExecute(sql, values)
        return jsonify({'status': 'success'})        
            
    @app.route('/categoria/<int:id>', methods=['GET'])
    def get_categoria(id):
        sql = f"SELECT * FROM estabelecimento WHERE id_categoria = '{id}'"
        results = con.querySelect(sql, values=None)        
        return jsonify(results) 
        

    if __name__ == '__main__':
        app.run(debug=True)
except Exception as e:
    print(e)