from flask import Blueprint, request, jsonify,render_template,redirect, url_for

from .alunos_model import AlunoNaoEncontrado, listar_alunos, aluno_por_id, adicionar_aluno, atualizar_aluno, excluir_aluno
from config import db



alunos_blueprint = Blueprint('alunos', __name__)

@alunos_blueprint.route('/', methods=['GET'])
def getIndex():
    return "Meu index"

## ROTA PARA TODOS OS ALUNOS
@alunos_blueprint.route('/alunos', methods=['GET'])
def get_alunos():
    alunos = listar_alunos()
    return render_template("alunos/alunos.html", alunos=alunos)

## ROTA PARA UM ALUNO
@alunos_blueprint.route('/alunos/<int:id_aluno>', methods=['GET'])
def get_aluno(id_aluno):
    try:
        aluno = aluno_por_id(id_aluno)
        return render_template('alunos/aluno_id.html', aluno=aluno)
    except AlunoNaoEncontrado:
        return jsonify({'message': 'Aluno não encontrado'}), 404

## ROTA ACESSAR O FORMULARIO DE CRIAÇÃO DE UM NOVO ALUNOS   
@alunos_blueprint.route('/alunos/adicionar', methods=['GET'])
def adicionar_aluno_page():
    return render_template('alunos/criar_alunos.html')

## ROTA QUE CRIA UM NOVO ALUNO
@alunos_blueprint.route('/alunos', methods=['POST'])
def create_aluno():
    nome = request.form['nome']
    idade = request.form['idade']
    email = request.form['email']
    telefone = request.form['telefone']
    novo_aluno = {'nome': nome, 'idade': idade, 'email': email, 'telefone': telefone}
    adicionar_aluno(novo_aluno)
    return redirect(url_for('alunos.get_alunos'))

## ROTA PARA O FORMULARIO PARA EDITAR UM NOVO ALUNO
@alunos_blueprint.route('/alunos/<int:id_aluno>/editar', methods=['GET'])
def editar_aluno_page(id_aluno):
    try:
        aluno = aluno_por_id(id_aluno)
        return render_template('alunos/aluno_update.html', aluno=aluno)
    except AlunoNaoEncontrado:
        return jsonify({'message': 'Aluno não encontrado'}), 404

## ROTA QUE EDITA UM ALUNO
@alunos_blueprint.route('/alunos/<int:id_aluno>', methods=['PUT', 'POST'])
def update_aluno(id_aluno):
    print("Dados recebidos no formulário:", request.form)
    try:
        aluno = aluno_por_id(id_aluno)
        aluno['nome'] = request.form['nome']
        aluno['idade'] = int(request.form['idade'])
        aluno['email'] = request.form['email']
        aluno['telefone'] = request.form['telefone']
        
        atualizar_aluno(id_aluno, aluno)
        
        return redirect(url_for('alunos.get_aluno', id_aluno=id_aluno))
    except AlunoNaoEncontrado:
        return jsonify({'message': 'Aluno não encontrado'}), 404

   
## ROTA QUE DELETA UM ALUNO
@alunos_blueprint.route('/alunos/delete/<int:id_aluno>', methods=['DELETE','POST'])
def delete_aluno(id_aluno):
        try:
            excluir_aluno(id_aluno)
            return redirect(url_for('alunos.get_alunos'))
        except AlunoNaoEncontrado:
            return jsonify({'message': 'Aluno não encontrado'}), 404
  