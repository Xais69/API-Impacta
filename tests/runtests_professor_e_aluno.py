import requests
import unittest

'''
Cada aluno será representado por um dicionário JSON como o seguinte: 
{"id":1,"nome":"marcos"}

Testes 000 e 001:
Na URL /alunos, se o verbo for GET, 
retornaremos uma lista com um dicionário para cada aluno.

Na URL /alunos, com o verbo POST, ocorrerá a criação do aluno,
enviando um desses dicionários 

Teste 002
Na URL /alunos/<int:id>, se o verbo for GET, devolveremos o nome e id do aluno. 
(exemplo. /alunos/2 devolve o dicionário do aluno(a) de id 2)

Teste 003
Na URL /reseta, apagaremos a lista de alunos e professores (essa URL só atende o verbo POST e DELETE).

Teste 004
Na URL /alunos/<int:id>, se o verbo for DELETE, deletaremos o aluno.
(dica: procure lista.remove)

Teste 005
Na URL /alunos/<int:id>, se o verbo for PUT, 
editaremos o aluno, mudando seu nome. 
Para isso, o usuário vai enviar um dicionário 
com a chave nome, que deveremos processar

Se o usuário manda um dicionário {“nome”:”José”} para a url /alunos/40,
com o verbo PUT, trocamos o nome do usuário 40 para José

Tratamento de erros

Testes 006 a 008b: Erros de usuário darão um código de status 400, e retornarão um dicionário descrevendo o erro. 
No teste 006, tentamos fazer GET, PUT e DELETE na URL  /alunos/15, sendo que o aluno de id 15 não existe. Nesse caso, devemos retornar um código de status 400 e um dicionário {“erro”:'aluno nao encontrado'}
No teste 007, tentamos criar dois alunos com a mesma id. Nesse caso, devemos retornar um código de status 400 e um dicionário {‘erro’:'id ja utilizada'}
No teste 008a, tento enviar um aluno sem nome via post. Nesse caso, devemos retornar um código de status 400 e um dicionário {‘erro’:'aluno sem nome'}
No teste 008b, tento editar um aluno, usando o verbo put, mas mando um dicionário sem nome. Nesse caso, devemos retornar um código de status 400 e um dicionário {“erro”:'aluno sem nome'}
Testes 100 a 109: Teremos as URLs análogas para professores.


'''


class TestStringMethods(unittest.TestCase):

    def test_000_professor_retorna_lista(self):
        r = requests.get('http://192.168.15.18:8000/professores')
        if r.status_code == 404:
            self.fail("Você não definiu a página /professores no seu server")

        self.assertEqual(r.status_code, 200,
                         "Falha ao buscar lista de Professores")

        self.assertIn('text/html', r.headers['Content-Type'],
                      "Esperava resposta HTML para a lista de professores")
        self.assertIn('<h1>Lista de Professores</h1>', r.text,
                      "Conteúdo HTML esperado não encontrado na resposta")

    def test_001_adiciona_alunos(self):
        r = requests.post('http://192.168.15.18:8000/alunos',
                          data={'nome': 'fernando', 'id': 1})
        r = requests.post('http://192.168.15.18:8000/alunos',
                          data={'nome': 'roberto', 'id': 2})

        r_lista = requests.get('http://192.168.15.18:8000/alunos')
        self.assertIn('text/html', r_lista.headers['Content-Type'],
                      "Esperava resposta HTML para a lista de alunos")

        self.assertIn('<h1>Lista de Alunos</h1>', r_lista.text,
                      "Conteúdo HTML esperado não encontrado na resposta")

        # Verifica se os alunos foram adicionados
        self.assertIn('fernando', r_lista.text,
                      "aluno fernando não apareceu na lista de alunos")
        self.assertIn('roberto', r_lista.text,
                      "aluno roberto não apareceu na lista de alunos")

    def test_002_aluno_por_id(self):
        r = requests.post('http://192.168.15.18:8000/alunos',
                          data={'nome': 'mario', 'id': 20})

        resposta = requests.get('http://192.168.15.18:8000/alunos/20')
        self.assertIn('text/html', resposta.headers['Content-Type'],
                      "Esperava resposta HTML para o aluno")

        self.assertIn('<h1>Aluno: mario</h1>', resposta.text,
                      "Conteúdo HTML esperado não encontrado na resposta")

    def test_003_reseta(self):
        r = requests.post('http://192.168.15.18:8000/alunos',
                          data={'nome': 'cicero', 'id': 29})
        r_lista = requests.get('http://192.168.15.18:8000/alunos')
        self.assertTrue(len(r_lista.text) > 0)

        r_reset = requests.post('http://192.168.15.18:8000/reseta')
        self.assertEqual(r_reset.status_code, 200)

        r_lista_depois = requests.get('http://192.168.15.18:8000/alunos')
        self.assertEqual(len(r_lista_depois.text), 0)

    def test_004_deleta(self):
        r_reset = requests.post('http://192.168.15.18:8000/reseta')
        self.assertEqual(r_reset.status_code, 200)

        requests.post('http://192.168.15.18:8000/alunos',
                      data={'nome': 'cicero', 'id': 29})
        requests.post('http://192.168.15.18:8000/alunos',
                      data={'nome': 'lucas', 'id': 28})
        requests.post('http://192.168.15.18:8000/alunos',
                      data={'nome': 'marta', 'id': 27})

        r_lista = requests.get('http://192.168.15.18:8000/alunos')
        self.assertIn('text/html', r_lista.headers['Content-Type'],
                      "Esperava resposta HTML para a lista de alunos")

        requests.delete('http://192.168.15.18:8000/alunos/28')
        r_lista2 = requests.get('http://192.168.15.18:8000/alunos')
        self.assertIn('text/html', r_lista2.headers['Content-Type'],
                      "Esperava resposta HTML para a lista de alunos após "
                      "deleção")

        self.assertIn('marta', r_lista2.text,
                      "aluno marta não encontrado na lista após deleção")
        self.assertIn('cicero', r_lista2.text,
                      "aluno cicero não encontrado na lista após deleção")

    def test_005_edita(self):
        r_reset = requests.post('http://192.168.15.18:8000/reseta')
        self.assertEqual(r_reset.status_code, 200)

        requests.post('http://192.168.15.18:8000/alunos',
                      data={'nome': 'lucas', 'id': 28})
        r_antes = requests.get('http://192.168.15.18:8000/alunos/28')
        self.assertIn('text/html', r_antes.headers['Content-Type'],
                      "Esperava resposta HTML para o aluno antes da edição")

        requests.put('http://192.168.15.18:8000/alunos/28',
                     data={'nome': 'lucas mendes'})
        r_depois = requests.get('http://192.168.15.18:8000/alunos/28')
        self.assertIn('text/html', r_depois.headers['Content-Type'],
                      "Esperava resposta HTML para o aluno após a edição")

    def test_006a_id_inexistente_no_put(self):
        r_reset = requests.post('http://192.168.15.18:8000/reseta')
        self.assertEqual(r_reset.status_code, 200)

        r = requests.put('http://192.168.15.18:8000/alunos/15',
                         data={'nome': 'bowser', 'id': 15})
        self.assertIn(r.status_code, [400, 404])
        self.assertIn('text/html', r.headers['Content-Type'],
                      "Esperava resposta HTML para erro de aluno não encontrado")
        self.assertIn('aluno nao encontrado', r.text,
                      "Mensagem de erro não encontrada na resposta")

    def test_006b_id_inexistente_no_get(self):
        r_reset = requests.post('http://192.168.15.18:8000/reseta')
        self.assertEqual(r_reset.status_code, 200)

        r = requests.get('http://192.168.15.18:8000/alunos/15')
        self.assertIn(r.status_code, [400, 404])
        self.assertIn('text/html', r.headers['Content-Type'],
                      "Esperava resposta HTML para erro de aluno não encontrado")
        self.assertIn('aluno nao encontrado', r.text,
                      "Mensagem de erro não encontrada na resposta")

    def test_006c_id_inexistente_no_delete(self):
        r_reset = requests.post('http://192.168.15.18:8000/reseta')
        self.assertEqual(r_reset.status_code, 200)

        r = requests.delete('http://192.168.15.18:8000/alunos/15')
        self.assertIn(r.status_code, [400, 404])
        self.assertIn('text/html', r.headers['Content-Type'],
                      "Esperava resposta HTML para erro de aluno não encontrado")
        self.assertIn('aluno nao encontrado', r.text,
                      "Mensagem de erro não encontrada na resposta")

    # tento criar 2 caras com a  mesma id
    def test_007_criar_com_id_ja_existente(self):
        # dou reseta e confiro que deu certo
        r_reset = requests.post('http://192.168.15.18:8000/reseta')
        self.assertEqual(r_reset.status_code, 200)

        # crio o usuario bond e confiro
        r = requests.post('http://192.168.15.18:8000/alunos',
                          data={'nome': 'bond', 'id': 7})
        self.assertEqual(r.status_code, 200)

        # tento usar o mesmo id para outro usuário
        r = requests.post('http://192.168.15.18:8000/alunos',
                          data={'nome': 'james', 'id': 7})
        self.assertEqual(r.status_code, 400)
        # Altere para r.text se a resposta for em HTML
        self.assertEqual(r.text, 'id ja utilizada')

# cria alunos sem nome, o que tem que dar erro


def test_008a_post_sem_nome(self):
    r_reset = requests.post('http://192.168.15.18:8000/reseta')
    self.assertEqual(r_reset.status_code, 200)

    # tentei criar um aluno, sem enviar um nome
    r = requests.post('http://192.168.15.18:8000/alunos', data={'id': 8})
    self.assertEqual(r.status_code, 400)
    self.assertEqual(r.text, 'aluno sem nome')  # Altere para r.text

# tenta editar alunos sem passar nome, o que também tem que dar erro


def test_008b_put_sem_nome(self):
    r_reset = requests.post('http://192.168.15.18:8000/reseta')
    self.assertEqual(r_reset.status_code, 200)

    # criei um aluno sem problemas
    r = requests.post('http://192.168.15.18:8000/alunos',
                      data={'nome': 'maximus', 'id': 7})
    self.assertEqual(r.status_code, 200)

    # mas tentei editar ele sem mandar o nome
    r = requests.put('http://192.168.15.18:8000/alunos/7', data={'id': 7})
    self.assertEqual(r.status_code, 400)
    self.assertEqual(r.text, 'aluno sem nome')  # Altere para r.text


def test_100_professores_retorna_lista(self):
    r = requests.get('http://192.168.15.18:8000/professores')
    # Se a resposta for HTML, você pode verificar se é do tipo str
    self.assertEqual(type(r.text), str)


def test_100b_nao_confundir_professor_e_aluno(self):
    r_reset = requests.post('http://192.168.15.18:8000/reseta')
    r = requests.post('http://192.168.15.18:8000/alunos',
                      data={'nome': 'fernando', 'id': 1})
    self.assertEqual(r.status_code, 200)
    r = requests.post('http://192.168.15.18:8000/alunos',
                      data={'nome': 'roberto', 'id': 2})
    self.assertEqual(r.status_code, 200)
    r_lista = requests.get('http://192.168.15.18:8000/professores')
    # Se a lista de professores for retornada em HTML
    self.assertEqual(len(r_lista.text.splitlines()), 0)
    r_lista_alunos = requests.get('http://192.168.15.18:8000/alunos')
    self.assertEqual(len(r_lista_alunos.text.splitlines()), 2)


def test_101_adiciona_professores(self):
    r = requests.post('http://192.168.15.18:8000/professores',
                      data={'nome': 'fernando', 'id': 1})
    r = requests.post('http://192.168.15.18:8000/professores',
                      data={'nome': 'roberto', 'id': 2})
    r_lista = requests.get('http://192.168.15.18:8000/professores')
    achei_fernando = 'fernando' in r_lista.text
    achei_roberto = 'roberto' in r_lista.text
    if not achei_fernando:
        self.fail('professor fernando nao apareceu na lista de professores')
    if not achei_roberto:
        self.fail('professor roberto nao apareceu na lista de professores')


def test_102_professores_por_id(self):
    r = requests.post('http://192.168.15.18:8000/professores',
                      data={'nome': 'mario', 'id': 20})
    r_lista = requests.get('http://192.168.15.18:8000/professores/20')
    self.assertIn('mario', r_lista.text)


def test_103_adiciona_e_reseta(self):
    r = requests.post('http://192.168.15.18:8000/professores',
                      data={'nome': 'cicero', 'id': 29})
    r_lista = requests.get('http://192.168.15.18:8000/professores')
    self.assertTrue(len(r_lista.text.splitlines()) > 0)
    r_reset = requests.post('http://localhost:5002/reseta')
    self.assertEqual(r_reset.status_code, 200)
    r_lista_depois = requests.get('http://localhost:5002/professores')
    self.assertEqual(len(r_lista_depois.text.splitlines()), 0)


def test_104_deleta(self):
    r_reset = requests.post('http://localhost:5002/reseta')
    self.assertEqual(r_reset.status_code, 200)
    requests.post('http://localhost:5002/professores',
                  data={'nome': 'cicero', 'id': 29})
    requests.post('http://localhost:5002/professores',
                  data={'nome': 'lucas', 'id': 28})
    r_lista = requests.get('http://localhost:5002/professores')
    self.assertEqual(len(r_lista.text.splitlines()), 2)
    requests.delete('http://localhost:5002/professores/28')
    r_lista = requests.get('http://localhost:5002/professores')
    self.assertEqual(len(r_lista.text.splitlines()), 1)


def test_105_edita(self):
    r_reset = requests.post('http://localhost:5002/reseta')
    self.assertEqual(r_reset.status_code, 200)
    requests.post('http://localhost:5002/professores',
                  data={'nome': 'lucas', 'id': 28})
    r_antes = requests.get('http://localhost:5002/professores/28')
    self.assertIn('lucas', r_antes.text)
    requests.put('http://localhost:5002/professores/28',
                 data={'nome': 'lucas mendes'})
    r_depois = requests.get('http://localhost:5002/professores/28')
    self.assertIn('lucas mendes', r_depois.text)


def test_106_id_inexistente(self):
    r_reset = requests.post('http://localhost:5002/reseta')
    self.assertEqual(r_reset.status_code, 200)
    r = requests.put('http://localhost:5002/professores/15',
                     data={'nome': 'bowser', 'id': 15})
    self.assertEqual(r.status_code, 400)
    self.assertEqual(r.text, 'professor nao encontrado')
    r = requests.get('http://localhost:5002/professores/15')
    self.assertEqual(r.status_code, 400)
    self.assertEqual(r.text, 'professor nao encontrado')
    r = requests.delete('http://localhost:5002/professores/15')
    self.assertEqual(r.status_code, 400)
    self.assertEqual(r.text, 'professor nao encontrado')


def test_107_criar_com_id_ja_existente(self):
    r_reset = requests.post('http://localhost:5002/reseta')
    self.assertEqual(r_reset.status_code, 200)
    r = requests.post('http://localhost:5002/professores',
                      data={'nome': 'bond', 'id': 7})
    self.assertEqual(r.status_code, 200)
    r = requests.post('http://localhost:5002/professores',
                      data={'nome': 'james', 'id': 7})
    self.assertEqual(r.status_code, 400)
    self.assertEqual(r.text, 'id ja utilizada')


def test_108_post_ou_put_sem_nome(self):
    r_reset = requests.post('http://localhost:5002/reseta')
    self.assertEqual(r_reset.status_code, 200)
    r = requests.post('http://localhost:5002/professores', data={'id': 8})
    self.assertEqual(r.status_code, 400)
    self.assertEqual(r.text, 'professor sem nome')
    r = requests.post('http://localhost:5002/professores',
                      data={'nome': 'maximus', 'id': 7})
    self.assertEqual(r.status_code, 200)
    r = requests.put('http://localhost:5002/professores/7', data={'id': 7})
    self.assertEqual(r.status_code, 400)
    self.assertEqual(r.text, 'professor sem nome')


def test_109_nao_confundir_professor_e_aluno(self):
    r_reset = requests.post('http://localhost:5002/reseta')
    self.assertEqual(r_reset.status_code, 200)
    requests.post('http://localhost:5002/alunos',
                  data={'nome': 'fernando', 'id': 1})
    requests.post('http://localhost:5002/alunos',
                  data={'nome': 'roberto', 'id': 2})
    r_lista = requests.get('http://localhost:5002/professores')
    self.assertEqual(len(r_lista.text.splitlines()), 0)
    r_lista_alunos = requests.get('http://localhost:5002/alunos')
    self.assertEqual(len(r_lista_alunos.text.splitlines()), 2)


def runTests():
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestStringMethods)
    unittest.TextTestRunner(verbosity=2, failfast=True).run(suite)


if __name__ == '__main__':
    runTests()