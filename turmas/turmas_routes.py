from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from turmas.turmas_model import TurmaNaoEncontrada,Turma, turma_por_id, listar_turmas, adicionar_turma, atualizar_turma, excluir_turma
from config import db

turmas_blueprint = Blueprint('turmas',__name__)

# Rota para listar todos as turmas
@turmas_blueprint.route('/turmas', methods=['GET'])
def get_turmas():
    turma = Turma.query.options(db.joinedload(Turma.professor)).all()
    turmas = listar_turmas()
    return render_template("turmas/turmas.html", turmas = turmas)

# Rota para exibir detalhes de uma turma
@turmas_blueprint.route('/turmas/<int:id_turma>', methods=['GET'])
def get_turma(id_turma):
    try:
        turmas = turma_por_id(id_turma)
        return render_template('turmas/turmas_id.html', turmas=turmas)
    except TurmaNaoEncontrada:
        return jsonify({'message': 'Turma não encontrada'}), 404


# Rota para exibir o formulário de criação de turma
@turmas_blueprint.route('/turmas/adicionar', methods=['GET'])
def adicionar_turma_page():
    return render_template('turmas/criar_turmas.html')



# Rota para criar uma nova turma
@turmas_blueprint.route('/turmas', methods=['POST'])
def create_turma():
    descricao = request.form['descricao']
    status = request.form['status']
    professor_id = request.form['professor_id']
    nova_turma = {'descricao': descricao, 'status': status,}
    adicionar_turma(nova_turma,professor_id)
    return redirect(url_for('turmas.get_turmas'))
 

    
# Rota para exibir o formulário de edição de turma
@turmas_blueprint.route('/turmas/<int:id_turma>/editar', methods=['GET'])
def editar_turma_page(id_turma):
    try:
        turma = turma_por_id(id_turma)
        return render_template('turmas/turmas_update.html', turma = turma)
    except TurmaNaoEncontrada:
        return jsonify({'message': 'Turma não encontrado'}), 404
    
# Rota para editar uma turma existente
@turmas_blueprint.route('/turmas/<int:id_turma>', methods=['PUT', 'POST'])
def update_turma(id_turma):
    try:
        turma = turma_por_id(id_turma)
        turma['descricao'] = request.form['descricao']
        turma['status'] = request.form['status'] == 'True'  
        
        atualizar_turma(id_turma, {
            'descricao': turma['descricao'],
            'status': turma['status'],
        })
        
        return redirect(url_for('turmas.get_turma', id_turma=id_turma))
    except TurmaNaoEncontrada:
        return jsonify({'message': 'Turma não encontrada'}), 404
    
# Rota para deletar uma turma
@turmas_blueprint.route('/turmas/delete/<int:id_turma>', methods=['DELETE', 'POST'])
def delete_turma(id_turma):
    try:
        excluir_turma(id_turma)
        return redirect(url_for('turmas.get_turmas'))
    except TurmaNaoEncontrada:
        return jsonify({'message': 'Turma não encontrada'}), 404
