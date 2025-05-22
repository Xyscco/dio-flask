from flask import Flask, request
from flask_restful import Resource, Api
from models import Pessoas, Atividades


app = Flask(__name__)
api = Api(app)


class Pessoa(Resource):
    def get(self, nome):
        try:
            pessoa = Pessoas.query.filter_by(nome=nome).first()
            if pessoa:
                response = {
                    'nome': pessoa.nome, 
                    'idade': pessoa.idade,
                    'id': pessoa.id
                }, 200
            
            return response if pessoa else {'message': 'Pessoa não encontrada'}, 404
        except AttributeError:
            return {'message': 'Atributo não encontrado'}, 400

        except Exception as e:
            return {'message': str(e)}, 500
        
    def put(self, nome):
        try:
            pessoa = Pessoas.query.filter_by(nome=nome).first()
            if pessoa:
                dados = request.json
                if 'nome' in dados:
                    pessoa.nome = dados['nome']
                if 'idade' in dados:
                    pessoa.idade = dados['idade']
                pessoa.save()
                
                response = {
                    'id': pessoa.id,
                    'nome': pessoa.nome,
                    'idade': pessoa.idade
                }, 200

                return response
            else:
                return {'message': 'Pessoa não encontrada'}, 404
        except Exception as e:
            return {'message': str(e)}, 500
        
    def delete(self, nome):
        try:
            pessoa = Pessoas.query.filter_by(nome=nome).first()
            if pessoa:
                pessoa.delete()
                return {'message': 'Pessoa excluída com sucesso'}, 200
            else:
                return {'message': 'Pessoa não encontrada'}, 404
        except Exception as e:
            return {'message': str(e)}, 500
        
class ListarInserirPessoas(Resource):
    def get(self):
        try:
            pessoas = Pessoas.query.all()
            response = [{'id': i.id, 'nome': i.nome, 'idade': i.idade} for i in pessoas]
            # for pessoa in pessoas:
            #     response.append({
            #         'id': pessoa.id,
            #         'nome': pessoa.nome,
            #         'idade': pessoa.idade
            #     })
            return response, 200
        except Exception as e:
            return {'message': str(e)}, 500
        
    def post(self):
        try:
            dados = request.json
            pessoa = Pessoas(nome=dados['nome'], idade=dados['idade'])
            pessoa.save()
            response = {
                'id': pessoa.id,
                'nome': pessoa.nome,
                'idade': pessoa.idade
            }, 201
        except Exception as e:
            return {'message': str(e)}, 500
        

        return response
    
class Atividades(Resource):
    def get(self):
        try:
            atividades = Atividades.query.all()
            response = [{'id': i.id, 'nome': i.nome, 'pessoa': i.pessoa.nome} for i in atividades]
            return response, 200
        except Exception as e:
            return {'message': str(e)}, 500

    def post(self):
        try:
            dados = request.json

            atividade = Atividades(nome=dados['nome'], pessoa_id=dados['pessoa_id'])
            atividade.save()
            response = {
                'id': atividade.id,
                'nome': atividade.nome,
                'pessoa_id': atividade.pessoa_id
            }, 201
        except Exception as e:
            return {'message': str(e)}, 500

        return response
    
api.add_resource(Pessoa, '/pessoa/<string:nome>')
api.add_resource(ListarInserirPessoas, '/pessoas')
api.add_resource(Atividades, '/atividades')

if __name__ == '__main__':
    app.run(debug=True)