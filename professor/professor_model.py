dados = {
    "alunos": [
        {"nome": "Lucas", "id": 15},
        {"nome": "Cicero", "id": 29},
        {"nome": "Amanda", "id": 34},
        {"nome": "Gabriel", "id": 42},
        {"nome": "Beatriz", "id": 53},
        {"nome": "João", "id": 67},
        {"nome": "Larissa", "id": 73},
        {"nome": "Carlos", "id": 88}
    ], "professores":[
        {"nome": "Renata", "id": 101},
        {"nome": "Ricardo", "id": 102},
        {"nome": "Fernanda", "id": 103},
        {"nome": "Paulo", "id": 104},
        {"nome": "Márcia", "id": 105},
        {"nome": "Gustavo", "id": 106},
        {"nome": "Sabrina", "id": 107},
        {"nome": "André", "id": 108}
    ]
}

class ProfessorNaoEncontrado(Exception):
    pass

def professor_por_id(id_professor):
    listar_professores = dados['professores']
    for dicionario in listar_professores:
        if dicionario['id'] == id_professor:
            return dicionario
    raise ProfessorNaoEncontrado

def listar_professores():
    return dados['professores']

def adicionar_professor(professor):
    dados['professores'].append(professor)

def autalizar_professor(id_professor, novos_dados):
    professor = professor_por_id(id_professor)
    professor.update(novos_dados)

def excluir_professor(id_professor):
    professor = professor_por_id(id_professor)
    dados['professor'].remove(professor)