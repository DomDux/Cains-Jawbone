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
    Blueprint, flash, g, redirect, request, session, url_for
)
from werkzeug.exceptions import abort

from .models import *

bp = Blueprint('graph', __name__, url_prefix='/graph')


#######################
#  READ
#######################

# Get a node with a given id
@bp.route('/node/<int:id>', methods=["GET"])
def get_node(id):
    node = Node.query.get(id)
    if node is None:
        abort(404, f"Node id {id} doesn't exist.")

    return {
        'id': node.id,
        'created': node.created,
        'deleted': node.deleted,
        'node_type': node.node_type
    }

# Get a relationship with a given id
@bp.route('/relationship/<int:id>', methods=["GET"])
def get_relationship(id):
    rel = Relationship.query.get(id)
    if rel is None:
        abort(404, f"Relationship id {id} doesn't exist.")

    return {
        'id':rel.id,
        'created': rel.created,
        'name' : rel.name,
        'start' : rel.start,
        'end' : rel.end,
        'rel': rel.rel,
        'ler' : rel.ler,
        'deleted' : rel.deleted
    }


#######################
#  CREATE
#######################

@bp.route('/node/create', methods=["GET", "POST"])
def create_node():
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
        new_node = Node(node_type=node_type)
        db.session.add(new_node)
        db.session.commit()
        db.session.refresh(new_node)
        created_id = new_node.id
        return str(created_id)

# Create a new relationship via function
def _create_relationship(start, end, rel, ler):
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

# TODO:  Create 2 new relationships via ENDPOINT (1 for forward relationship, 1 for backwards)
@bp.route('/relationship/create', methods=["POST"])
def create_relationship():
    data = request.get_json()

    start = data.get('start')
    end = data.get('end')
    forward_relationship = data.get('forward_relationship')
    reverse_relationship = data.get('reverse_relationship')

    id1, first_rel = _create_relationship(start, end, forward_relationship, reverse_relationship)
    id2, second_rel = _create_relationship(end, start, reverse_relationship, forward_relationship)
    return {
        id1: {
            'id':first_rel.id,
            'created':first_rel.created,
            'start':first_rel.start,
            'end':first_rel.end,
            'forward_relationship': first_rel.rel,
            'reverse_relationship': first_rel.ler
        },
        id2: {
            'id':second_rel.id,
            'created':second_rel.created,
            'start':second_rel.start,
            'end':second_rel.end,
            'forward_relationship': second_rel.rel,
            'reverse_relationship': second_rel.ler
        }
    }



#######################
#  UPDATE
#######################

# TODO:  Update relationship text
# TODO:  "Soft" delete node by updating value of deleted field
# TODO:  "Soft" delete relationship by updating value of deleted field
# TODO:  Mark node as merged by updating value of merged field.  This is called in conjunction with merge functions in other blueprints

#######################
#  DELETE
#######################

# TODO:  Delete node of given id
# TODO:  Delete relationship of given id
