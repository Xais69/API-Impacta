from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from professor.professor_model import ProfessorNaoEncontrado, listar_professores, professor_por_id, adicionar_professor, atualizar_professor, excluir_professor
from config import db
from turmas.turmas_model import Turma

professores_blueprint = Blueprint('professores', __name__)

# Rota para listar todos os professores
@professores_blueprint.route('/professores', methods=['GET'])
def get_professores():
    professores = listar_professores()
    return render_template("professores/professores.html", professores=professores)

# Rota para exibir detalhes de um professor por ID
@professores_blueprint.route('/professores/<int:id_professor>', methods=['GET'])
def get_professor(id_professor):
    try:
        professor = professor_por_id(id_professor)
        return render_template('professores/professor_id.html', professor=professor)
    except ProfessorNaoEncontrado:
        return jsonify({'message': 'Professor não encontrado'}), 404

# Rota para exibir o formulário de criação de professor
@professores_blueprint.route('/professores/adicionar', methods=['GET'])
def adicionar_professor_page():
    return render_template('professores/criar_professor.html')

# Rota para criar um novo professor
@professores_blueprint.route('/professores', methods=['POST','GET'])
def create_professor():
    if request.method == 'POST':
        dados_professor = {
            'nome': request.form['nome'],
            'idade': request.form['idade'],
            'materia': request.form['materia'],
            'observacoes': request.form['observacoes'],
            'turmas_ids': request.form.getlist('turmas_ids')  # Captura a lista de turmas selecionadas
        }
        adicionar_professor(dados_professor)
        return redirect(url_for('professores.get_professores'))

    # GET: Renderiza o formulário e passa as turmas
    turmas = Turma.query.all()  # Obtém todas as turmas
    print(turmas)
    return render_template('criar_professor.html', turmas=turmas)


# Rota para exibir o formulário de edição de professor
@professores_blueprint.route('/professores/<int:id_professor>/editar', methods=['GET'])
def editar_professor_page(id_professor):
    try:
        professor = professor_por_id(id_professor)
        return render_template('professores/professor_update.html', professor=professor)
    except ProfessorNaoEncontrado:
        return jsonify({'message': 'Professor não encontrado'}), 404

# Rota para editar um professor existente
@professores_blueprint.route('/professores/<int:id_professor>', methods=['PUT', 'POST'])
def update_professor(id_professor):
    try:
        professor = professor_por_id(id_professor)
        
        professor['nome'] = request.form['nome']
        professor['idade'] = int(request.form['idade'])
        professor['materia'] = request.form['materia']
        professor['observacoes'] = request.form['observacoes']
        
        atualizar_professor(id_professor,{
            'nome': professor['nome'],
            'idade': professor['idade'],
            'materia': professor['materia'],
            'observacoes': professor['observacoes'], 
        })
        
        return redirect(url_for('professores.get_professor', id_professor=id_professor))
    
    except ProfessorNaoEncontrado:
        return jsonify({'message': 'Professor não encontrado'}), 404



# Rota para deletar um professor
@professores_blueprint.route('/professores/delete/<int:id_professor>', methods=['DELETE', 'POST'])
def delete_professor(id_professor):
    try:
        excluir_professor(id_professor)
        return redirect(url_for('professores.get_professores'))
    except ProfessorNaoEncontrado:
        return jsonify({'message': 'Professor não encontrado'}), 404
