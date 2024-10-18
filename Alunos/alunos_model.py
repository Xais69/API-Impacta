from config import db

class Aluno (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120))

    def __init__(self, nome):
        self.nome = nome
    def to_dict(self):
        return{'id': self.id, 'nome':self.nome}

class AlunoNaoEncontrado(Exception):
    pass

def aluno_por_id(id_aluno):
    aluno = Aluno.query.get(id_aluno)
    if not aluno:
        raise AlunoNaoEncontrado
    return aluno.to_dict()

def listar_alunos():
    alunos = Aluno.query.all()
    return [aluno.to_dict() for aluno in alunos]

#def adicionar_aluno(aluno):
    dados['alunos'].append(aluno)

#def atualizar_aluno(id_aluno, novos_dados):
    aluno = aluno_por_id(id_aluno)
    aluno.update(novos_dados)

#def excluir_aluno(id_aluno):
    aluno = aluno_por_id(id_aluno)
    dados['alunos'].remove(aluno)