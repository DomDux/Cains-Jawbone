from flask import (
    Blueprint, request
)
from werkzeug.exceptions import abort, HTTPException

from ..models import *
from .entities import get_entity_from_node

bp = Blueprint('vis', __name__, url_prefix='/vis')

def return_graph() -> dict:
    """Return the graph as a dictionary"""
    nodes = Node.query.filter(Node.deleted != True, Node.merged == None).all()
    node_entities = [
        get_entity_from_node(node.id) 
        for node in nodes
    ]
    relationships = Relationship.query.filter(Relationship.deleted != True).all()
    return {
        'nodes': [
            {
                'node_id': node.id,
                'created': node.created,
                'node_type': node.node_type,
                'entity': Serialiser.to_dict(entity.__class__, entity)
            }
            for node, entity in zip(nodes, node_entities)
        ],
        'relationships': Serialiser.to_dict_list(Relationship, relationships)
    }

@bp.route('/graph', methods=['GET'])
def graph():
    """Return the graph as a JSON object"""
    return return_graph(), 200