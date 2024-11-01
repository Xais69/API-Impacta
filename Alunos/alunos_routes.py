from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from datetime import datetime
from Alunos.alunos_model import AlunoNaoEncontrado, Aluno,listar_alunos, aluno_por_id, adicionar_aluno, atualizar_aluno, excluir_aluno
from config import db
from turmas.turmas_model import listar_turmas, Turma
from professor.professor_model import Professor

alunos_blueprint = Blueprint('alunos', __name__)

@alunos_blueprint.route('/', methods=['GET'])
def getIndex():
    professores = Professor.query.all()
    turmas = Turma.query.all()
    alunos = listar_alunos()  # Presumindo que esta função retorne todos os alunos
    return render_template('alunos/index.html', professores=professores, turmas=turmas, alunos=alunos)

## ROTA PARA TODOS OS ALUNOS
@alunos_blueprint.route('/alunos', methods=['GET'])
def get_alunos():
    alunos = listar_alunos()  # Presumindo que esta função retorne todos os alunos
    return render_template('alunos/alunos.html', alunos=alunos)

## ROTA PARA UM ALUNO
@alunos_blueprint.route('/aluno/<int:id_aluno>', methods=['GET'])
def get_aluno(id_aluno):
    try:
        aluno = aluno_por_id(id_aluno)
        return render_template('alunos/aluno_id.html', aluno=aluno)
    except AlunoNaoEncontrado:
        return jsonify({'message': 'Aluno não encontrado'}), 404

## ROTA PARA EXIBIR O FORMULÁRIO DE ADICIONAR ALUNO
@alunos_blueprint.route('/alunos/adicionar', methods=['GET'])
def adicionar_aluno_page():
    return render_template('alunos/criar_alunos.html')

## ROTA PARA CRIAR UM NOVO ALUNO   
@alunos_blueprint.route('/alunos/adicionar', methods=['POST'])
def create_aluno():
    if request.method == "POST":
        data = request.form
        nome = data.get('nome')
        idade = data.get('idade')
        data_nascimento = data.get('data_nascimento')
        nota_primeiro_semestre = data.get('nota_primeiro_semestre')
        nota_segundo_semestre = data.get('nota_segundo_semestre')
        turma_id = data.get('turma_id')  # Obter o ID da turma do formulário
        professor = data.get('professor')
        try:
            # Criação do novo aluno com os dados recebidos
            novo_aluno = Aluno(
                nome=nome,
                idade=int(idade),  # Converter idade para int
                data_nascimento=datetime.strptime(data_nascimento, '%Y-%m-%d').date(),  # Converter data
                nota_primeiro_semestre=float(nota_primeiro_semestre),  # Converter para float
                nota_segundo_semestre=float(nota_segundo_semestre),     # Converter para float
                turma_id=turma_id,
                professor=professor  # Relacionando o aluno com a turma
            )

            # Adiciona o novo aluno ao banco de dados
            db.session.add(novo_aluno)
            db.session.commit()

            # Redireciona para a página de lista de alunos
            return redirect(url_for('alunos.get_alunos'))

        except Exception as e:
            # Se ocorrer um erro, exibe uma mensagem de erro
            return jsonify({"error": str(e)}), 400

    return redirect(url_for('alunos.adicionar_aluno_page'))

## ROTA PARA EDITAR UM ALUNO
@alunos_blueprint.route('/alunos/<int:id_aluno>/editar', methods=['GET', 'POST'])
def update_aluno(id_aluno):
    aluno = aluno_por_id(id_aluno)  # Supondo que você esteja usando SQLAlchemy
    
    if request.method == 'POST':
        # Atualiza os dados do aluno
        aluno.nome = request.form['nome']
        aluno.idade = request.form['idade']
        aluno.nota_primeiro_semestre = request.form['nota_primeiro_semestre']
        aluno.nota_segundo_semestre = request.form['nota_segundo_semestre']
        aluno.turma_id = request.form['turma_id']  # Atualiza o ID da turma se necessário

        db.session.commit()  # Salva as alterações no banco de dados
        return redirect(url_for('alunos.getIndex'))  # Redireciona para uma página após a atualização
    
    return render_template('alunos/aluno_update.html', aluno=aluno)  # Renderiza um template para o formulário de atualização

## ROTA PARA DELETAR UM ALUNO
@alunos_blueprint.route('/alunos/excluir/<int:id_aluno>', methods=['DELETE','POST'])
def delete_aluno(id_aluno):
    try:
        excluir_aluno(id_aluno)
        return redirect(url_for('alunos.get_alunos'))
    except AlunoNaoEncontrado:
        return jsonify({'message': 'Aluno não encontrado'}), 404
