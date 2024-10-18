from config import db, app
from Alunos.alunos_routes import alunos_blueprint
from professor.professor_routes import prossores_blueprint

# Registrando os blueprints
app.register_blueprint(alunos_blueprint)
# app.register_blueprint(prossores_blueprint)

# Criando as tabelas no banco de dados
with app.app_context():
    db.create_all()

# Iniciando o servidor
if __name__ == '__main__':
    app.run(host=app.config['HOST'], port=app.config['PORT'], debug=app.config['DEBUG'])
