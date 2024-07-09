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

from flaskr.db import get_db

bp = Blueprint('graph', __name__, url_prefix='/graph')


#######################
#  READ
#######################

# Get a node with a given id
@bp.route('/node/<int:id>', methods=["GET"])
def get_node(id):
    node = get_db().execute(
        'SELECT id, created, node_type, deleted, merged'
        ' FROM nodes n'
        ' WHERE n.id = ?',
        (id,)
    ).fetchone()
    if node  is None:
        abort(404, f"Node id {id} doesn't exist.")

    return node

# Get a relationship with a given id
@bp.route('/relationship/<int:id>', methods=["GET"])
def get_relationship(id):
    rel = get_db().execute(
        'SELECT id, created, name, start, end, rel, ler, deleted'
        ' FROM relationships r'
        ' WHERE r.id = ?',
        (id,)
    ).fetchone()
    if rel is None:
        abort(404, f"Relationship id {id} doesn't exist.")

    return rel


#######################
#  CREATE
#######################

# TODO:  Function to query nodes and find an appropriate primary key based on the next greated value of the 'id' field
# TODO:  Create a new node via ENDPOINT
@bp.route('/node/create', methods=["GET", "POST"])
def create():
    if request.method != "POST":
        return request.form
    node_type = request.json.get("node_type")
    error = None
    
    permitted_node_types = (
        'person', 'location', 'event', 'note', 'tag'
    )
    if node_type not in permitted_node_types:
        error = f'{node_type} is not a valid node type.'

    if error is not None:
        return error, 400
    else:
        db = get_db()
        db.execute(
            'INSERT INTO nodes (node_type)'
            ' VALUES (?);',
            (node_type)
        )
        db.commit()
        created_id = db.execute(
            'SELECT LAST_INSERTED_ID();'
        ).fetchone()
        return created_id

# TODO:  Create a new relationship via function
# TODO:  Create 2 new relationships via ENDPOINT (1 for forward relationship, 1 for backwards)



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
