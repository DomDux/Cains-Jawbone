"""
This will be the blueprint for all endpoints relating to the creation and maintenance of 
node and relationship entities in the database.  The data model is as follows:

    -------------               -----------------
    |           |   id    start |               |
    |   nodes   |   |------<    |   relations   |
    |           |   id    end   |               |
    -------------               -----------------
          - id
          |
          - id
    -------------
    |           |
    |   misc    |
    |           |
    -------------
A 1-to-1 relationship with nodes and all other misc entities such as people is required to 
ensure that complex relationships between entities of different types are able to be managed.
This means that for any subsequent entity like a Person table, every record in that table has
to match with a node in the nodes table.  So, for a CREATE action on the person table, a record
must first be created in the nodes table and the generated primary key from that action is used 
as the primary key in the subsequent table.   Similarly, for DELETE actions, these should be 
performed in sync with actions on nodes.
"""

import functools
import time

from flask import (
    Blueprint, request
)
from werkzeug.exceptions import abort, HTTPException

from ..models import *

bp = Blueprint('graph', __name__, url_prefix='/graph')

# Helper return functions.  Return a dictionary for the corresponding objects
def _return_node(node: Node) -> dict:
    """Return a dictionary of the node object"""
    return {
        'id': node.id,
        'created': node.created,
        'deleted': node.deleted,
        'merged': node.merged,
        'node_type': node.node_type
    }

def _return_relationship(rel: Relationship) -> dict:
    """Return a dictionary of the relationship object"""
    return {
        'id':rel.id,
        'created': rel.created,
        'start' : rel.start,
        'end' : rel.end,
        'rel': rel.rel,
        'ler' : rel.ler,
        'deleted' : rel.deleted
    }

def _relationship_partner(rel: Relationship) -> Relationship:
    """Return the reverse relationship of a given relationship"""
    return Relationship.query.filter_by(start=rel.end, end=rel.start).first()

#### ERROR HANDLING ####

class NodeNotFoundError(HTTPException):
    code = 404
    description = "Node not found."

class InvalidNodeIDError(HTTPException):
    code = 400
    description = "Invalid node ID provided."

def handle_node_not_found_error(e):
    response = {
        "error": "NodeNotFoundError",
        "message": e.description
    }
    response.status_code = e.code
    return response

def handle_invalid_node_id_error(e):
    response = {
        "error": "InvalidNodeIDError",
        "message": e.description
    }
    response.status_code = e.code
    return response


#######################
#  READ
#######################

# Get a node with a given ids
def get_nodes(ids):
    response = []
    for id in ids:
        node = Node.query.get(id)
        if node is None:
            raise NodeNotFoundError()
            # abort(404, f"Node id {id} doesn't exist.")
        response.append(_return_node(node))
    return response

@bp.route('/node', methods=["GET"])
def api_get_nodes():
    args = request.args
    ids = args.getlist('id')
    if ids is None:
        abort(400, f"An ID must be provided")
    elif not isinstance(ids, list):
        ids = [ids]
    return get_nodes(ids)

# Get a relationship with a given ids
def get_relationships(ids):
    response = []
    for id in ids:
        rel = Relationship.query.get(id)
        if rel is None:
            abort(404, f"Relationship id {id} doesn't exist.")
        response.append(_return_relationship(rel))
    return response

@bp.route('/relationship', methods=["GET"])
def api_get_relationships():
    args = request.args
    ids = args.getlist('id')
    if ids is None:
        abort(400, f"An ID must be provided")
    return get_relationships(ids)
    


#######################
#  CREATE
#######################

def create_node(node_type):
    new_node = Node(node_type=node_type)
    db.session.add(new_node)
    db.session.commit()
    db.session.refresh(new_node)
    created_id = new_node.id
    return str(created_id)


@bp.route('/node/create', methods=["POST"])
def api_create_node():
    if request.method != "POST":
        return request.form
    data = request.get_json()
    node_type = data.get('node_type')

    error = None
    if not node_type:
        error = "Node type is required"
    permitted_node_types = (
        'person', 'location', 'event', 'note', 'tag'
    )
    if node_type not in permitted_node_types:
        error = f'{node_type} is not a valid node type.'

    if error is not None:
        return error, 400
    else:
        return create_node(node_type)

# Create a new relationship via function
def _create_relationship(start, end, rel, ler) -> tuple[str, Relationship]:
    """
    Create a new relationship between two nodes.  This function is called by the create_relationship function
    
    Args:
        start (int): the id of the start node
        end (int): the id of the end node
        rel (int): the relationship text
        ler (int): the reverse relationship text

    Returns:
        str - the id of the created relationship
        Relationship - the created relationship object
    """
    start_node = Node.query.get(start)
    if not start_node:
        abort(400, f"There doesn't exist a start node with id {start}")
        
    end_node = Node.query.get(end)
    if not end_node:
        abort(400, f"There doesn't exist a end node with id {end}")

    existing_rels = Relationship.query.filter_by(start=start, end=end).all()

    if len(existing_rels) > 0:
        abort(400, f"There already exists a relationship between nodes {start} and {end}")

    new_rel = Relationship(
        start=start,
        end=end,
        rel=rel,
        ler=ler
    )
    db.session.add(new_rel)
    db.session.commit()
    db.session.refresh(new_rel)
    created_id = new_rel.id
    return str(created_id), new_rel

def create_relationship(start, end, rel, ler):
    """
    Create a new relationship between two nodes
    
    Returns:
        dict - a dictionary of the created relationships
    """
    id1, first_rel = _create_relationship(start, end, rel, ler)
    id2, second_rel = _create_relationship(end, start, rel, ler)
    return {
        id1: _return_relationship(first_rel),
        id2: _return_relationship(second_rel)
    }

# Create 2 new relationships via ENDPOINT (1 for forward relationship, 1 for backwards)
@bp.route('/relationship/create', methods=["POST"])
def api_create_relationship():
    data = request.get_json()

    start = data.get('start')
    end = data.get('end')
    forward_relationship = data.get('forward_relationship')
    reverse_relationship = data.get('reverse_relationship')

    return create_relationship(start, end, forward_relationship, reverse_relationship)



#######################
#  UPDATE
#######################

# TODO:  Update relationship text
# "Soft" delete node by updating value of deleted field
def soft_delete_node(node: Node) -> Node:
    """Soft delete a node by setting its deleted field to 1"""
    node.deleted = 1
    # TODO: Soft delete all relationships associated with this node
    # relationships = Relationship.query.filter((Relationship.start == node.id) | (Relationship.end == node.id)).all()
    db.session.commit()
    db.session.refresh(node)
    return node

@bp.route('/node/delete', methods=["PUT"])
def api_soft_delete_node():
    args = request.args
    id = args.get('id')
    if id is None:
        abort(400, "An ID must be provided")
    node = Node.query.get(id)
    if node is None:
        abort(404, f"Could not find node with id {id}")
    soft_delete_node(node)
    return _return_node(node)

# "Soft" delete relationship by updating value of deleted field
def soft_delete_rel(rel: Relationship) -> Relationship:
    rel.deleted = 1
    reverse_rel = _relationship_partner(rel)
    if reverse_rel is not None:
        reverse_rel.deleted = 1
    db.session.commit()
    db.session.refresh(rel)
    return rel

@bp.route('/relationship/delete', methods=["PUT"])
def api_soft_delete_rel():
    args = request.args
    id = args.get('id')
    if id is None:
        abort(400, "An ID must be provided")
    rel = Relationship.query.get(id)
    if rel is None:
        abort(404, f"Could not find relationship with id {id}")
    reverse_rel = _relationship_partner(rel)
    if reverse_rel is None:
        abort(404, "Could not find the partner relationship")
    
    soft_delete_rel(rel)
    # Return the relationship and its reverse relationship
    return {
        str(id): _return_relationship(rel),
        str(reverse_rel.id): _return_relationship(reverse_rel)
    }

# Mark node as merged by updating value of merged field.  
# This is called in conjunction with merge functions in other blueprints
# In the other functions, we create the merged node first and then call this function
def merge_nodes(merged_node, nodes):
    for node in nodes:
        node.merged = merged_node.id
    db.session.commit()
    return [merged_node]+nodes

@bp.route('/node/merge',  methods=["PUT", "POST"])
def merge():
    data = request.get_json()
    node_ids = data.get('id')
    if not node_ids or not isinstance(node_ids, list):
        abort(400, "A list of node IDs must be provided")
    nodes_to_merge = [Node.query.get_or_404(node_id, f"Could not find node {node_id} to merge") for node_id in node_ids]
        
    node_types = [n.node_type for n in nodes_to_merge]
    distinct_node_types = list(set(node_types))
    if len(distinct_node_types) != 1:
        abort(400, "Cannot merge nodes of different types")
    
    new_node = Node(node_type=distinct_node_types[0])
    db.session.add(new_node)
    db.session.commit()
    db.session.refresh(new_node)
    merge_nodes(new_node, nodes_to_merge)
    return [_return_node(n) for n in [new_node]+nodes_to_merge]

#######################
#  DELETE
#######################

# Delete node of given id
def delete_node(node: Node):
    """Delete a node from the database"""
    db.session.delete(node)
    db.session.commit()
    return node

@bp.route('/node/harddelete', methods=["DELETE"])
def api_delete_node():
    args = request.args
    id = args.get('id')
    if id is None:
        abort(400, "ID of the resource should be provided")
    node_to_delete = Node.query.get_or_404(id, description=f"There does not exist a node with id {id}")
    delete_node(node_to_delete)
    return f"Deleted node {id}"

# TODO:  Delete relationship of given id
@bp.route('/relationship/harddelete', methods=["DELETE"])
def delete_relationship():
    args = request.args
    id = args.get('id')
    if id is None:
        abort(400, "ID of the resource should be provided")
    rel_to_delete = Relationship.query.get_or_404(id, description=f"There does not exist a node with id {id}")
    start, end = rel_to_delete.start, rel_to_delete.end
    reverse_rel_to_delete = Relationship.query.filter_by(start=end, end=start).first()
    reverse_rel_id = reverse_rel_to_delete.id

    db.session.delete(rel_to_delete)
    db.session.delete(reverse_rel_to_delete)
    db.session.commit()
    return f"Deleted relationships {id} and {reverse_rel_id}"
