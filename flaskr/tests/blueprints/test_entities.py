import pytest
from flask import Flask, jsonify
from flaskr.blueprints.entities import (
    people_bp, loc_bp, event_bp, tag_bp,
    create_entity, soft_delete_entity, hard_delete_entity,
    link_entities, get_linked_nodes, get_linked_entities, merge_into_new
)
from flaskr.models import db, Person, Location, Event, Tag, Node, Relationship


def test_create_person(session):
    person = create_entity('person', name="John Doe", content="Person content", gender="Male")
    assert person.id is not None
    assert person.name == "John Doe"
    assert person.content == "Person content"
    assert person.gender == "Male"

def test_create_location(session):
    location = create_entity('location', name="Test Location", content="Location content", country="Country", district="District", town="Town")
    assert location.id is not None
    assert location.name == "Test Location"
    assert location.content == "Location content"
    assert location.country == "Country"
    assert location.district == "District"
    assert location.town == "Town"

def test_create_event(session):
    event = create_entity('event', name="Test Event", content="Event content", date="2025-02-11")
    assert event.id is not None
    assert event.name == "Test Event"
    assert event.content == "Event content"
    assert event.date == "2025-02-11"

def test_create_tag(session):
    tag = create_entity('tag', name="Test Tag")
    assert tag.id is not None
    assert tag.name == "Test Tag"

def test_soft_delete_entity(session):
    person = create_entity('person', name="John Doe", content="Person content", gender="Male")
    soft_deleted_person = soft_delete_entity(person)
    assert soft_deleted_person.deleted == 1

def test_hard_delete_entity(session):
    person = create_entity('person', name="John Doe", content="Person content", gender="Male")
    hard_delete_entity(person)
    assert Person.query.get(person.id) is None

def test_link_entities(session):
    person = create_entity('person', name="John Doe", content="Person content", gender="Male")
    location = create_entity('location', name="Test Location", content="Location content", country="Country", district="District", town="Town")
    rel_id, new_rel = link_entities(person, location, "visited", "was visited by")
    assert new_rel.id is not None
    assert new_rel.start == person.node_id
    assert new_rel.end == location.node_id
    assert new_rel.rel == "visited"
    assert new_rel.ler == "was visited by"

def test_get_linked_nodes(session):
    person = create_entity('person', name="John Doe", content="Person content", gender="Male")
    location = create_entity('location', name="Test Location", content="Location content", country="Country", district="District", town="Town")
    link_entities(person, location, "visited", "was visited by")
    linked_nodes = get_linked_nodes(person)
    assert len(linked_nodes) == 1
    assert linked_nodes[0].id == location.node_id

def test_get_linked_entities(session):
    person = create_entity('person', name="John Doe", content="Person content", gender="Male")
    location = create_entity('location', name="Test Location", content="Location content", country="Country", district="District", town="Town")
    link_entities(person, location, "visited", "was visited by")
    linked_entities = get_linked_entities(person, 'location')
    assert len(linked_entities) == 1
    assert linked_entities[0].id == location.id

def test_merge_into_new(session):
    person1 = create_entity('person', name="John Doe", content="Person content", gender="Male")
    person2 = create_entity('person', name="Jane Doe", content="Person content", gender="Female")
    merged_person = merge_into_new([person1, person2], 'person', name="Merged Person", content="Merged content", gender="Other")
    assert merged_person.id is not None
    assert merged_person.name == "Merged Person"
    assert merged_person.content == "Merged content"
    assert merged_person.gender == "Other"
    assert person1.node.merged == merged_person.node_id
    assert person2.node.merged == merged_person.node_id