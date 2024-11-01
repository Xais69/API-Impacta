from config import db

class Turma(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(150))
    status = db.Column(db.Boolean, default=True)
    professor_id = db.Column(db.Integer, db.ForeignKey('professor.id'), nullable=True)
    professor = db.relationship('Professor', back_populates='turmas')

    alunos = db.relationship('Aluno', backref='turma', lazy="select")


    def __init__(self, descricao,status):
        self.descricao = descricao 
        self.status = status

    def to_dict(self):
        return {'id': self.id, 'descricao': self.descricao, 'status': self.status,
                'professor_id': self.professor_id,
                'professor_nome': self.professor.nome if self.professor else None
        }

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
    descricao=turma_data['descricao'],
    status=turma_data['status'] == 'True',
    professor_id =professor_id )   
    db.session.add(nova_turma)
    db.session.commit()

def atualizar_turma(id_turma, novos_dados):
    turma = Turma.query.get(id_turma)
    if not turma:
        raise TurmaNaoEncontrada
    turma.descricao = novos_dados.get('descricao', turma.descricao)  # Mantém a descrição antiga se não for fornecida
    turma.status = novos_dados.get('status', turma.status)  # Mantém o status antigo se não for fornecido
    db.session.commit()



def excluir_turma(id_turma):
    turma = Turma.query.get(id_turma)
    if not turma:
        raise TurmaNaoEncontrada
    db.session.delete(turma)
    db.session.commit()
