import unittest
from model_alunos_professores import (
    apaga_tudo,
    listar_alunos,
    adicionar_aluno,
    aluno_por_id,
    AlunoNaoEncontrado,
    AlunoDuplicado,
    remover_aluno,  # Supondo que você tenha essa função
    editar_aluno    # Supondo que você tenha essa função
)

class TestAlunos(unittest.TestCase):

    def setUp(self):
        # Limpa a lista de alunos antes de cada teste
        apaga_tudo()
        # Adiciona um aluno para os testes
        self.aluno = {"nome": "lucas", "id": 15}
        adicionar_aluno(self.aluno)

    def test_adiciona_aluno(self):
        """Testa se o aluno é adicionado corretamente."""
        self.assertIn(self.aluno, listar_alunos())

    def test_aluno_por_id(self):
        """Testa a recuperação do aluno por ID."""
        aluno = aluno_por_id(15)
        self.assertEqual(aluno['nome'], "lucas")

    def test_aluno_nao_encontrado(self):
        """Testa a exceção quando o aluno não é encontrado."""
        with self.assertRaises(AlunoNaoEncontrado):
            aluno_por_id(999)  # ID que não existe

    def test_lista_alunos_vazia(self):
        """Testa se a lista de alunos está vazia após a limpeza."""
        apaga_tudo()
        self.assertEqual(listar_alunos(), [])

    def test_adiciona_aluno_duplicado(self):
        aluno_duplicado = {"nome": "Lucas", "id": 15}  # ID duplicado
        with self.assertRaises(AlunoDuplicado):  # Espera que a exceção seja levantada
            adicionar_aluno(aluno_duplicado)  # Tenta adicionar o aluno duplicado


    def test_edita_aluno(self):
        """Testa a edição de um aluno."""
        # Adiciona um aluno e depois edita
        aluno_atualizado = {"nome": "lucas atualizado", "id": 15}
        editar_aluno(aluno_atualizado)  # Supondo que você tenha uma função de edição
        aluno = aluno_por_id(15)
        self.assertEqual(aluno['nome'], "lucas atualizado")

    def test_remove_aluno(self):
        """Testa a remoção de um aluno."""
        remover_aluno(15)  # Supondo que você tenha uma função para remover
        with self.assertRaises(AlunoNaoEncontrado):
            aluno_por_id(15)  # Verifica se o aluno foi realmente removido

if __name__ == "__main__":
    unittest.main()
