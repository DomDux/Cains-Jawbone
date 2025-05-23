"""
All the entities such as people, locations, and events behave in a similar way in relation to other objects.
I want a single file to look after all of them as they have very similar functions for creation, deletion etc.

    Entity:
     - Person
     - Location
     - Event
     - Tag

All entities are nodes.  To create an entity, we first create a Node and record it's ID.  We then create an entity
with THE SAME ID as the node to link the two together.  To create and manage links between entities, we must remember
that the IDs of entities and their corresponding Nodes are the same. 

"""

from flask import (
    Blueprint, request
)
from werkzeug.exceptions import abort, HTTPException
from sqlalchemy import inspect

from ..models import *
from .graph import create_node, create_relationship, merge_nodes, soft_delete_node, delete_node
from ..utils import get_json_body, get_params
from ..errors import *

people_bp = Blueprint('people', __name__, url_prefix='/people')
loc_bp = Blueprint('location', __name__, url_prefix='/location')
event_bp = Blueprint('event', __name__, url_prefix='/event')
tag_bp = Blueprint('tag', __name__, url_prefix='/tag')


# Helpers
def _return_entity(entity):
    inspector = inspect(type(entity))
    columns = inspector.columns
    return { str(c).split(".")[1] : getattr(entity, str(c).split(".")[1]) for c in columns}

# Could we use **kwargs to make this arbitrary???
def _create_person(node_id, name, content, gender=None):
    person = Person(
        node_id=node_id,
        name=name,
        content=content,
        gender=gender
    )
    db.session.add(person)
    db.session.commit()
    db.session.refresh(person)
    return person

def _create_location(node_id, name, content, country, district, town):
    location = Location(
        node_id=node_id,
        name=name,
        content=content,
        country=country,
        district=district,
        town=town
    )
    db.session.add(location)
    db.session.commit()
    db.session.refresh(location)
    return location

def _create_event(node_id, name, content, date):
    event = Event(
        node_id=node_id,
        name=name,
        content=content,
        date=date
    )
    db.session.add(event)
    db.session.commit()
    db.session.refresh(event)
    return event

def _create_tag(node_id, name):
    existing_tag = Tag.query.filter(Tag.name.ilike(name)).first()
    if existing_tag is not None:
        raise RecordAlreadyExists(name)
    tag = Tag(
        id=node_id,
        name=name
    )
    db.session.add(tag)
    db.session.commit()
    db.session.refresh(tag)
    return tag

def create_entity(model_class, **kwargs):
    """
    Create an entity of the specified type (e.g. person, location, event, tag) with the given attributes.
    Args:
        model_class (str): The type of entity to create (e.g. "person", "location", "event", "tag")
        **kwargs: Additional attributes for the entity
    Returns:
        The newly created entity object
    """
    # First create a corresponding node
    node_id = create_node(model_class)

    # Then create the entity
    CREATE_MAP = {
        'person': _create_person,
        'location': _create_location,
        'event': _create_event,
        'tag': _create_tag
    }
    create_function = CREATE_MAP[model_class]
    new_entity = create_function(node_id=node_id, **kwargs)
    return new_entity

def soft_delete_entity(entity):
    entity.deleted = 1
    db.session.commit()
    soft_delete_node(Node.query.get(entity.node_id))
    db.session.refresh(entity)
    return entity

def hard_delete_entity(entity):
    node = Node.query.get_or_404(entity.node_id)
    db.session.delete(entity)
    delete_node(node)
    db.session.commit()
    return None

######################
# PEOPLE
######################

def get_people(ids):
    people = [Person.query.get_or_404(id) for id in ids]
    return people

def get_people_from_nodes(node_ids: list[int]):
    people = db.session.query(Person).filter(Person.node_id.in_(node_ids)).all()
    return people

@people_bp.route('/', methods=["GET"])
def api_get_people():
    ids = get_params('id')
    people = get_people(ids)
    response = [_return_entity(person) for person in people]
    return response

@people_bp.route('/create', methods=["POST"])
def api_create_people():
    data = get_json_body('name', 'content', 'gender')
    person = create_entity('person', **data)
    return _return_entity(person)



######################
# LOCATIONS
######################

def get_locations(ids: list[int]):
    loc = [Location.query.get_or_404(id) for id in ids]
    return loc

def get_locations_from_nodes(node_ids: list[int]):
    loc = db.session.query(Location).filter(Location.node_id.in_(node_ids)).all()
    return loc

@loc_bp.route('/', methods=["GET"])
def api_get_loc():
    ids = get_params('id')
    locations = get_locations(ids)
    response = [_return_entity(loc) for loc in locations]
    return response

@loc_bp.route('/create', methods=["POST"])
def api_create_locations():
    data = get_json_body('name', 'content', 'country', 'district', 'town')
    location = create_entity('location', **data)
    return _return_entity(location)



######################
# EVENTS
######################

def get_events(ids):
    loc = [Event.query.get_or_404(id) for id in ids]
    return loc

def get_events_from_nodes(node_ids: list[int]):
    event = db.session.query(Event).filter(Event.node_id.in_(node_ids)).all()
    return event

@event_bp.route('/', methods=["GET"])
def api_get_events():
    ids = get_params('id')
    events = get_events(ids)
    response = [_return_entity(e) for e in events]
    return response

@event_bp.route('/create', methods=["POST"])
def api_create_events():
    data = get_json_body('name', 'content', 'date')
    event = create_entity('event', **data)
    return _return_entity(event)

######################
# TAGS
######################

def get_tags(ids):
    tag = [Tag.query.get_or_404(id) for id in ids]
    return tag

def get_tags_from_nodes(node_ids: list[int]):
    tags = db.session.query(Tag).filter(Tag.node_id.in_(node_ids)).all()
    return tags

@tag_bp.route('/', methods=["GET"])
def api_get_tags():
    ids = get_params('id')
    tags = get_tags(ids)
    response = [_return_entity(tag) for tag in tags]
    return response

@tag_bp.route('/create', methods=["POST"])
def api_create_tags():
    data = get_json_body('name')
    tag = create_entity('tag', **data)
    return _return_entity(tag)

######################
# QUERY ENTITIES
######################

# Call this function to create a relationship between two entites e.g. a note and a tag, a person and a note, a location and a tag etc
def link_entities(e1, e2, rel, ler):
    """
    Link two entities by creating a relationship between their corresponding nodes.  The relationship is bi-directional.
    e.g. a person visited a location, the location was visited by a person.
    
    Args:
        e1: The first entity (e.g. person, location, event, tag)
        e2: The second entity (e.g. person, location, event, tag)
        rel: The relationship type (e.g. "visited", "attended", "tagged")
        ler: The reverse relationship type (e.g. "was visited by", "was attended by", "was tagged by")

    Returns:
        forward_rel: The forward relationship object
        backward_rel: The backward relationship object
    """
    node_1, node_2 = e1.node_id, e2.node_id
    forward_rel, backward_rel = create_relationship(node_1, node_2, rel, ler)
    return forward_rel, backward_rel

# Get all the linked nodes from an e.g. tag
def get_linked_nodes(entity) -> list:
    """
    Get all the linked nodes from an entity.
    Args:
        entity: The entity record to get linked nodes from (e.g. person, location, event, tag)
    Returns:
        A list of linked nodes
    """
    # rels = Relationship.query.filter(Relationship.start == entity.node_id).all()
    rels = db.session.query(Relationship).filter(Relationship.start == entity.node_id).all()
    linked_node_ids = [r.end for r in rels]
    nodes = [Node.query.get_or_404(id) for id in linked_node_ids]
    return nodes

# Call this function to get the linked e.g. tags from an entity
def get_linked_entities(entity, expected_type: str):
    """
    Get the linked entities of a specific type from an entity.
    Args:
        entity: The entity record to get linked entities from (e.g. person, location, event, tag)
        expected_type (str): The type of linked entities to retrieve (e.g. "person", "location", "event", "tag")
    Returns:
        A list of linked entities of the specified type
    """
    all_nodes = get_linked_nodes(entity)
    nodes = [n for n in all_nodes if n.node_type == expected_type]
    if not nodes:
        return None
    
    ids = [node.id for node in nodes]
    RETRIEVE_MAP= {
        'person': get_people_from_nodes,
        'location': get_locations_from_nodes,
        'event': get_events_from_nodes,
        'tag': get_tags_from_nodes
    }
    get_fn = RETRIEVE_MAP[expected_type]
    return get_fn(ids)

# Merge into a new entity
def merge_into_new(entities: list, entity_type: str, **kwargs):
    """
    Merge multiple entities into a new entity of the specified type.
    Args:
        entities: A list of entity records to merge (e.g. people, locations, events, tags)
        entity_type (str): The type of the new entity to create (e.g. "person", "location", "event", "tag")
        **kwargs: Additional attributes for the new entity
    Returns:
        The new entity created by merging the specified entities
    """
    nodes = [Node.query.get_or_404(e.node_id) for e in entities]
    
    new_entity = create_entity(entity_type, **kwargs)
    return merge_nodes(new_entity, nodes)

def get_entity_from_node(node_id: int):
    """
    Get the entity corresponding to a node ID.
    Args:
        node_id (int): The ID of the node to retrieve the entity from
    Returns:
        The entity object of the specified type
    """
    RETRIEVE_MAP = {
        'person': Person,
        'location': Location,
        'event': Event,
        'tag': Tag
    }
    node = Node.query.get_or_404(node_id)
    entity_type = node.node_type.lower()
    if entity_type not in RETRIEVE_MAP:
        raise HTTPException(f"Entity type '{entity_type}' not found.")
    entity_class = RETRIEVE_MAP[entity_type]
    return entity_class.query.filter(entity_class.node_id == node_id).first()