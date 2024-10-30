from config import db

class Professor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150))
    idade = db.Column(db.Integer)
    materia = db.Column(db.String(40))


    def __init__(self,nome, idade, materia): 
        self.nome = nome
        self.idade = idade
        self.materia = materia

    def to_dict(self):
        return{'id': self.id, 'nome': self.nome, 'idade': self.idade, 'materia': self.materia} 

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
        materia=dados_professor['materia']
    )
    db.session.add(novo_professor)
    db.session.commit()


def atualizar_professor(id_professor, novos_dados):
    professor = Professor.query.get(id_professor)
    if not professor:
        raise ProfessorNaoEncontrado
    professor.nome = novos_dados['nome']
    professor.idade = novos_dados['idade']
    professor.materia = novos_dados['materia']

    db.session.commit()



def excluir_professor(id_professor):
    professor = Professor.query.get(id_professor)
    if not professor:
        raise ProfessorNaoEncontrado
    db.session.delete(professor)
    db.session.commit()