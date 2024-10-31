from config import db
from datetime import datetime

class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    idade = db.Column(db.Integer)
    data_nascimento = db.Column(db.Date)
    nota_primeiro_semestre = db.Column(db.Float)
    nota_segundo_semestre = db.Column(db.Float)
    media_final = db.Column(db.Float)

    def __init__(self, nome, idade, data_nascimento, nota_primeiro_semestre, nota_segundo_semestre):  
        self.nome = nome
        self.idade = idade  
        self.data_nascimento = data_nascimento
        self.nota_primeiro_semestre = float(nota_primeiro_semestre)  # Converter para float
        self.nota_segundo_semestre = float(nota_segundo_semestre)    # Converter para float
        self.media_final = self.calcular_media()  # Calcular média no momento da criação

    def calcular_media(self):
        # Verifica se as notas são válidas
        if self.nota_primeiro_semestre is not None and self.nota_segundo_semestre is not None:
            return (self.nota_primeiro_semestre + self.nota_segundo_semestre) / 2
        return None  # Retorna None se não houver notas para calcular

    def to_dict(self):
        return {
            'id': self.id, 
            'nome': self.nome, 
            'idade': self.idade,
            'data_nascimento': self.data_nascimento,
            'nota_primeiro_semestre': self.nota_primeiro_semestre,
            'nota_segundo_semestre': self.nota_segundo_semestre,
            'media_final': self.media_final
        }

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
    novo_aluno = Aluno(
        nome=aluno_data['nome'], 
        idade=aluno_data['idade'], 
        data_nascimento=datetime.strptime(aluno_data['data_nascimento'], '%Y-%m-%d').date(),  # Certifique-se de que a data está sendo convertida
        nota_primeiro_semestre=float(aluno_data['nota_primeiro_semestre']),  # Converter para float
        nota_segundo_semestre=float(aluno_data['nota_segundo_semestre'])     # Converter para float
    )
    db.session.add(novo_aluno)
    db.session.commit()

def atualizar_aluno(id_aluno, novos_dados):
    aluno = Aluno.query.get(id_aluno)
    if not aluno:
        raise AlunoNaoEncontrado
    
    aluno.nome = novos_dados.get('nome', aluno.nome)
    aluno.idade = novos_dados.get('idade', aluno.idade)

    # Converte a data de nascimento para um objeto date
    if 'data_nascimento' in novos_dados:
        aluno.data_nascimento = datetime.strptime(novos_dados['data_nascimento'], '%Y-%m-%d').date()
    
    # Atualiza as notas e recalcula a média
    aluno.nota_primeiro_semestre = float(novos_dados.get('nota_primeiro_semestre', aluno.nota_primeiro_semestre))
    aluno.nota_segundo_semestre = float(novos_dados.get('nota_segundo_semestre', aluno.nota_segundo_semestre))
    
    # Recalcula a média
    aluno.media_final = aluno.calcular_media()

    db.session.commit()

def excluir_aluno(id_aluno):
    aluno = Aluno.query.get(id_aluno)
    if not aluno:
        raise AlunoNaoEncontrado
    db.session.delete(aluno)
    db.session.commit()
