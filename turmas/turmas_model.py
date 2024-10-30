from config import db

class Turma(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_turma = db.Column(db.String(100))
    qtd_alunos = db.Column(db.Integer)



    def __init__(self, nome_turma, qtd_alunos):
        self.nome_turma = nome_turma
        self.qtd_alunos = qtd_alunos

    def to_dict(self):
        return {'id': self.id, 'nome_turma': self.nome_turma, 'qtd_alunos': self.qtd_alunos}

class TurmaNaoEncontrada(Exception):
    pass

def turma_por_id(id_turma):
    turma = Turma.query.get(id_turma)
    if not turma:
        raise TurmaNaoEncontrada
    return turma.to_dict()

def listar_turmas():
    turmas = Turma.query.all()
    return [turma.to_dict() for turma in turmas] 

def adicionar_turma(turma_data):
    nova_turma = Turma(
    nome_turma=turma_data['nome_turma'],
    qtd_alunos=turma_data['qtd_alunos'])
    db.session.add(nova_turma)
    db.session.commit()

def atualizar_turma(id_turma, novos_dados):
    turma = Turma.query.get(id_turma)
    if not turma:
        raise TurmaNaoEncontrada
    turma.nome_turma = novos_dados['nome_turma'],
    turma.qtd_alunos = novos_dados['qtd_alunos']
    db.session.commit()

def excluir_turma(id_turma):
    turma = Turma.query.get(id_turma)
    if not turma:
        raise TurmaNaoEncontrada
    db.session.delete(turma)
    db.session.commit()
