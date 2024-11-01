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
        turma = turma_por_id(id_turma)
        return render_template('turmas/turmas_id.html', turma=turma)
    except TurmaNaoEncontrada:
        return jsonify({'message': 'Turma não encontrada'}), 404


# Rota para exibir o formulário de criação de turma
@turmas_blueprint.route('/turmas/adicionar', methods=['GET'])
def adicionar_turma_page():
    return render_template('turmas/criar_turmas.html')



# Rota para criar uma nova turma
@turmas_blueprint.route('/turmas', methods=['POST'])
def create_turma():
    if request.method == "POST":
        data = request.form
        status = data.get('status') == '1'
        descricao = data.get('descricao')
        
        # Aqui estamos assumindo que os IDs dos professores são passados como uma lista separada por vírgulas
        professor_ids = data.get('professor_ids', '').split(',')
        
        try:
            adicionar_turma({
                'descricao': descricao,
                'status': status,
                'professor_ids': [int(id) for id in professor_ids if id]  # Converte para int e ignora IDs vazios
            })
            # Redireciona para a lista de turmas
            return redirect(url_for('turmas.get_turmas'))
        except Exception as e:
            return jsonify({"error": str(e)}), 400
    try:
        turma = turma_por_id(id_turma)
        return render_template('turmas/turmas_update.html', turma = turma)
    except TurmaNaoEncontrada:
        return jsonify({'message': 'Turma não encontrado'}), 404
    
# Rota para editar uma turma existente
@turmas_blueprint.route('/turmas/<int:id_turma>/editar', methods=['GET', 'POST','PUT'])
def update_turma(id_turma):
    try:
        turma = turma_por_id(id_turma)

        if request.method == 'POST':
            turma.descricao = request.form['descricao']
            turma.status = request.form['status'] == 'True'
            
            atualizar_turma(id_turma, {
                'descricao': turma.descricao,
                'status': turma.status,
            })
            
            return redirect(url_for('turmas.get_turma', id_turma=id_turma))

        return render_template('turmas/turmas_update.html', turma=turma)

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
