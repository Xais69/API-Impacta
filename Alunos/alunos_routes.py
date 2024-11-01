from flask import Blueprint, request, jsonify,render_template,redirect, url_for

from .alunos_model import AlunoNaoEncontrado,Aluno, listar_alunos, aluno_por_id, adicionar_aluno, atualizar_aluno, excluir_aluno
from config import db
from turmas.turmas_model import listar_turmas, Turma
from professor.professor_model import Professor	



alunos_blueprint = Blueprint('alunos', __name__)

@alunos_blueprint.route('/', methods=['GET'])
def getIndex():
    professores = Professor.query.all()
    turmas = Turma.query.all()
    alunos = Aluno.query.all()
    return render_template('alunos/index.html', professores=professores,
                           turmas=turmas, alunos=alunos)

## ROTA PARA TODOS OS ALUNOS
@alunos_blueprint.route('/alunos', methods=['GET'])
def get_alunos():
    alunos = Aluno.query.options(db.joinedload(Aluno.turma)).all()  # Carrega a turma junto
    return render_template('/alunos/alunos.html', alunos=alunos)

## ROTA PARA UM ALUNO
@alunos_blueprint.route('/aluno/<int:id_aluno>', methods=['GET'])
def get_aluno(id_aluno):
    try:
        aluno = aluno_por_id(id_aluno)
        return render_template('alunos/aluno_id.html', aluno=aluno)
    except AlunoNaoEncontrado:
        return jsonify({'message': 'Aluno não encontrado'}), 404

## ROTA ACESSAR O FORMULARIO DE CRIAÇÃO DE UM NOVO ALUNOS   
@alunos_blueprint.route('/alunos/adicionar', methods=['GET'])
def adicionar_aluno_page():
    turmas = listar_turmas()
    return render_template('alunos/criar_alunos.html', turmas = turmas)

## ROTA QUE CRIA UM NOVO ALUNO
@alunos_blueprint.route('/alunos/<int:id_aluno>/editar', methods=['GET', 'POST'])
def update_aluno(id_aluno):
    aluno = Aluno.query.get(id_aluno)  # Supondo que você esteja usando SQLAlchemy
    
    if request.method == 'POST':
        # Atualiza os dados do aluno
        aluno.nome = request.form['nome']
        aluno.idade = request.form['idade']
        aluno.nota_primeiro_semestre = request.form['nota_primeiro_semestre']
        aluno.nota_segundo_semestre = request.form['nota_segundo_semestre']
        aluno.professor = request.form['professor']

        db.session.commit()  # Salva as alterações no banco de dados
        return redirect(url_for('alunos.getIndex'))  # Redireciona para uma página após a atualização
    
    return render_template('alunos/aluno_update.html', aluno=aluno)
  # Renderiza um template para o formulário de atualização


   
## ROTA QUE DELETA UM ALUNO
@alunos_blueprint.route('/alunos/excluir/<int:id_aluno>', methods=['DELETE','POST'])
def delete_aluno(id_aluno):
        try:
            excluir_aluno(id_aluno)
            return redirect(url_for('alunos.get_alunos'))
        except AlunoNaoEncontrado:
            return jsonify({'message': 'Aluno não encontrado'}), 404
  