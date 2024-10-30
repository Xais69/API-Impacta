from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from turmas.turmas_model import TurmaNaoEncontrada, turma_por_id, listar_turmas, adicionar_turma, atualizar_turma, excluir_turma
from config import db

turmas_blueprint = Blueprint('turmas',__name__)

# Rota para listar todos os professores
@turmas_blueprint.route('/turmas', methods=['GET'])
def get_turmas():
    turmas = listar_turmas()
    return render_template("turmas/turmas.html", turmas = turmas)

# Rota para exibir detalhes de um professor por ID
@turmas_blueprint.route('/turmas/<int:id_turma>', methods=['GET'])
def get_turma(id_turma):
    try:
        turmas = turma_por_id(id_turma)
        return render_template('turmas/turmas_id.html', turmas=turmas)
    except TurmaNaoEncontrada:
        return jsonify({'message': 'Turma não encontrada'}), 404


# Rota para exibir o formulário de criação de professor
@turmas_blueprint.route('/turmas/adicionar', methods=['GET'])
def adicionar_turma_page():
    return render_template('turmas/criar_turmas.html')



# Rota para criar um novo professor
@turmas_blueprint.route('/turmas', methods=['POST'])
def create_turma():
    nome_turma = request.form['nome_turma']
    qtd_alunos = request.form['qtd_alunos']
    nova_turma = {'nome_turma': nome_turma, 'qtd_alunos': qtd_alunos}
    adicionar_turma(nova_turma)
    return redirect(url_for('turmas.get_turmas'))
 

    
# Rota para exibir o formulário de edição de turma
@turmas_blueprint.route('/turmas/<int:id_turma>/editar', methods=['GET'])
def editar_turma_page(id_turma):
    try:
        turmas = turma_por_id(id_turma)
        return render_template('turmas/turmas_update.html', turmas = turmas)
    except TurmaNaoEncontrada:
        return jsonify({'message': 'Turma não encontrado'}), 404
    
# Rota para editar uma turma existente
@turmas_blueprint.route('/turmas/<int:id_turma>', methods=['PUT', 'POST'])
def update_turma(id_turma):
    try:
        turmas= turma_por_id(id_turma)
        nome_turma = request.form['turma_ano']
        turmas['nome_turma'] = nome_turma
        atualizar_turma(id_turma, turmas)
        return redirect(url_for('turma.get_turma', id_turma=id_turma))
    except TurmaNaoEncontrada:
        return jsonify({'message': 'Turma não encontrado'}), 404
    
# Rota para deletar um professor
@turmas_blueprint.route('/turmas/delete/<int:id_turma>', methods=['DELETE', 'POST'])
def delete_turma(id_turma):
    try:
        excluir_turma(id_turma)
        return redirect(url_for('turmas.get_turmas'))
    except TurmaNaoEncontrada:
        return jsonify({'message': 'Turma não encontrada'}), 404
