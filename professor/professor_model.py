from config import db
from turmas.turmas_model import Turma

class Professor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150))
    idade = db.Column(db.Integer)
    materia = db.Column(db.String(40))
    observacoes = db.Column(db.String(250))
    turmas = db.relationship('Turma', backref='professor', lazy="select")

    def __init__(self,nome, idade, materia,observacoes): 
        self.nome = nome
        self.idade = idade
        self.materia = materia
        self.observacoes = observacoes


    def to_dict(self):
        return{'id': self.id, 'nome': self.nome, 'idade': self.idade, 'materia': self.materia,
                'observacoes': self.observacoes,
                'turmas': [turma.descricao for turma in self.turmas]} 

class ProfessorNaoEncontrado(Exception):
    pass

def professor_por_id(id_professor):
    professor = Professor.query.get(id_professor)
    if not professor:
        raise ProfessorNaoEncontrado
    return professor.to_dict()

def listar_professores():
    professores = Professor.query.all()
    return [professor.to_dict() for professor in professores]


def adicionar_professor(dados_professor):
    novo_professor = Professor(
        nome=dados_professor['nome'],
        idade=dados_professor['idade'],
        materia=dados_professor['materia'],
        observacoes=dados_professor['observacoes']
    )

    # Se o professor está associado a alguma turma, vincule as turmas ao professor
    for turma_id in dados_professor.get('turmas_ids', []):
        turma = Turma.query.get(turma_id)
        if turma:
            turma.professor = novo_professor  # Estabelece a relação professor-turma

    db.session.add(novo_professor)  # Adiciona o novo professor à sessão
    db.session.commit()  # Salva as alterações no banco de dados




def atualizar_professor(id_professor, novos_dados):
    professor = Professor.query.get(id_professor)
    if not professor:
        raise ProfessorNaoEncontrado
    professor.nome = novos_dados['nome']
    professor.idade = novos_dados['idade']
    professor.materia = novos_dados['materia']
    professor.observacoes = novos_dados['observacoes']
    db.session.commit()  # Não esqueça de salvar as mudanças!


    db.session.commit()



def excluir_professor(id_professor):
    professor = Professor.query.get(id_professor)
    if not professor:
        raise ProfessorNaoEncontrado
    db.session.delete(professor)
    db.session.commit()
