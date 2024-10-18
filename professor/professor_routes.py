
from flask import Blueprint, request, jsonify
from .professor_model import ProfessorNaoEncontrado, listar_professores, professor_por_id, adicionar_professor, autalizar_professor, excluir_professor

prossores_blueprint = Blueprint('professores', __name__)


@prossores_blueprint.route('/professores', methods=['GET'])
def get_professor():
    return jsonify(listar_professores())

@prossores_blueprint.route('/professores/<int:id_professor>', methods=['GET'])
def get_professor(id_professor):
    try:
        professor = professor_por_id(id_professor)
        return jsonify(professor)
    except ProfessorNaoEncontrado:
        return jsonify({'message': 'Aluno não encontrado'}), 404

@prossores_blueprint.route('/professores', methods=['POST'])
def create_aluno():
    data = request.json
    adicionar_professor(data)
    return jsonify(data), 201

@prossores_blueprint.route('/professores/<int:id_professor>', methods=['PUT'])
def update_professor(id_professor):
    data = request.json
    try:
        autalizar_professor,(id_professor, data)
        return jsonify(professor_por_id(id_professor))
    except ProfessorNaoEncontrado:
        return jsonify({'message': 'Aluno não encontrado'}), 404

@prossores_blueprint.route('/professores/<int:id_professor>', methods=['DELETE'])
def delete_professor(id_professor):
    try:
        excluir_professor(id_professor)
        return '', 204
    except ProfessorNaoEncontrado:
        return jsonify({'message': 'Aluno não encontrado'}), 404