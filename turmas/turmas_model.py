from config import db


class Turma(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(150))
    status = db.Column(db.Boolean, default=True)   


    professor_id = db.Column(db.Integer, db.ForeignKey('professor.id'), nullable=True)

    alunos = db.relationship('Aluno', backref='turma', lazy="select")


    def __init__(self, descricao, status, professor_id=None):  # Adiciona professor_id
        self.descricao = descricao
        self.status = status
        self.professor_id = professor_id
        

    def to_dict(self):
        return {'id': self.id, 
                'descricao': self.descricao, 
                'status': self.status,
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
    try:
        print(f"Dados Recebidos: {turma_data}")
        professor_id = turma_data.get("professor_id")
        print(f"ID do Professor: {professor_id}")

        if professor_id is None:
            raise ValueError("professor_id não pode ser None")

        professor = Professor.query.get(professor_id)
        if professor is None:
            raise ValueError(f"Professor com id `{professor_id}` não existe")

        nova_turma = Turma(
            descricao=turma_data.get("descricao"),
            professor_id=professor_id,
            status=turma_data.get("status")
        )

        db.session.add(nova_turma)
        db.session.commit()
        print(f"Turma '{nova_turma.descricao}' criada com sucesso!")

    except Exception as e:
        db.session.rollback()  # Reverte a sessão em caso de erro
        print(f"Erro ao adicionar a turma: {str(e)}")
        raise  # Relevanta a exceção para ser tratada em outro lugar


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