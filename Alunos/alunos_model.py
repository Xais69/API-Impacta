from config import db

class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    idade = db.Column(db.Integer)
    email = db.Column(db.String(100))
    telefone = db.Column(db.String(15))
    

    def __init__(self, nome, idade, email, telefone):  
        self.nome = nome
        self.idade = idade  
        self.email = email
        self.telefone = telefone

    def to_dict(self):
        return {'id': self.id, 
                'nome': self.nome, 
                'idade': self.idade,
                'email': self.email,
                'telefone': self.telefone}

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

def adicionar_aluno(aluno_data):
    novo_aluno = Aluno(nome=aluno_data['nome'], idade=aluno_data['idade'], email=aluno_data['email'],
                       telefone=aluno_data['telefone'])
    db.session.add(novo_aluno)
    db.session.commit()

def atualizar_aluno(id_aluno, novos_dados):
    aluno = Aluno.query.get(id_aluno)
    if not aluno:
        raise AlunoNaoEncontrado
    aluno.nome = novos_dados.get('nome', aluno.nome)
    aluno.idade = novos_dados.get('idade', aluno.idade)       
    aluno.email = novos_dados.get('email', aluno.email)
    aluno.telefone = novos_dados.get('telefone', aluno.telefone)  
    db.session.commit()

def excluir_aluno(id_aluno):
    aluno = Aluno.query.get(id_aluno)
    if not aluno:
        raise AlunoNaoEncontrado
    db.session.delete(aluno)
    db.session.commit()