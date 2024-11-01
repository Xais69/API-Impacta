dados = {
    "alunos": [
        {"nome": "lucas", "id": 15},
        {"nome": "cicero", "id": 29},
    ],
    "professores": []
}

class AlunoNaoEncontrado(Exception):
    pass

class AlunoDuplicado(Exception):
    pass

def aluno_por_id(id_aluno):
    lista_alunos = dados['alunos']
    for dicionario in lista_alunos:
        if dicionario['id'] == id_aluno:
            return dicionario
    raise AlunoNaoEncontrado(f"Aluno com ID {id_aluno} não encontrado.")

def aluno_existe(id_aluno):
    try:
        aluno_por_id(id_aluno)
        return True
    except AlunoNaoEncontrado:
        return False

def adicionar_aluno(novo_aluno):
    """Adiciona um novo aluno à lista. Levanta um erro se o aluno já existir."""
    for aluno in dados['alunos']:  # Corrigido para iterar sobre a lista de alunos
        if aluno['id'] == novo_aluno['id']:
            raise AlunoDuplicado(f"Aluno com ID {novo_aluno['id']} já existe.")
    dados['alunos'].append(novo_aluno)  # Corrigido para adicionar o novo aluno à lista

def listar_alunos():
    return dados["alunos"]

def apaga_tudo():
    dados['alunos'] = []

def remover_aluno(aluno_id):
    """Remove um aluno da lista pelo ID."""
    for aluno in dados['alunos']:  # Corrigido para usar dados['alunos']
        if aluno['id'] == aluno_id:
            dados['alunos'].remove(aluno)  # Corrigido para remover o aluno da lista
            return
    raise AlunoNaoEncontrado(f"Aluno com ID {aluno_id} não encontrado.")

def editar_aluno(aluno_atualizado):
    """Atualiza as informações de um aluno."""
    for i, aluno in enumerate(dados['alunos']):  # Corrigido para usar dados['alunos']
        if aluno['id'] == aluno_atualizado['id']:
            dados['alunos'][i] = aluno_atualizado  # Substitui o aluno antigo pelo novo
            return
    raise AlunoNaoEncontrado(f"Aluno com ID {aluno_atualizado['id']} não encontrado.")
