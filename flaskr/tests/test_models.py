import pytest
from flaskr.models import Page, User, Tag, Node, Relationship, Note, Person, Location, Event

def test_create_page(session):
    page = Page(page_number=1, content="Page content")
    session.add(page)
    session.commit()
    assert page.id is not None
    assert page.page_number == 1
    assert page.content == "Page content"

def test_create_user(session):
    session.query(User).delete() # Clear the User table
    user = User(username="testuser", password="password")
    session.add(user)
    session.commit()
    assert user.id is not None
    assert user.username == "testuser"
    assert user.password == "password"

def test_create_tag(session):
    tag = Tag(name="testtag")
    session.add(tag)
    session.commit()
    assert tag.id is not None
    assert tag.name == "testtag"

def test_create_node(session):
    node = Node(node_type="testtype")
    session.add(node)
    session.commit()
    assert node.id is not None
    assert node.node_type == "testtype"

def test_create_relationship(session):
    node1 = Node(node_type="testtype1")
    node2 = Node(node_type="testtype2")
    session.add(node1)
    session.add(node2)
    session.commit()
    relationship = Relationship(start=node1.id, end=node2.id, rel="related", ler="testler")
    session.add(relationship)
    session.commit()
    assert relationship.id is not None
    assert relationship.start == node1.id
    assert relationship.end == node2.id
    assert relationship.rel == "related"
    assert relationship.ler == "testler"

def test_create_note(session):
    page = Page(page_number=1, content="Page content")
    session.add(page)
    session.commit()
    note = Note(note_text="Note text", page_number=page.id, content="Note content")
    session.add(note)
    session.commit()
    assert note.id is not None
    assert note.note_text == "Note text"
    assert note.page_number == page.id
    assert note.content == "Note content"

def test_create_person(session):
    person = Person(name="John Doe", content="Person content")
    session.add(person)
    session.commit()
    assert person.id is not None
    assert person.name == "John Doe"
    assert person.content == "Person content"

def test_create_location(session):
    location = Location(name="Test Location", content="Location content")
    session.add(location)
    session.commit()
    assert location.id is not None
    assert location.name == "Test Location"
    assert location.content == "Location content"

def test_create_event(session):
    event = Event(name="Test Event", content="Event content")
    session.add(event)
    session.commit()
    assert event.id is not None
    assert event.name == "Test Event"
    assert event.content == "Event content"


def test_serialiser(session):
    # Create a sample node and relationship
    node = Node(node_type="testtype")
    session.add(node)
    session.commit()

    relationship = Relationship(start=node.id, end=node.id, rel="related", ler="testler")
    session.add(relationship)
    session.commit()

    # Serialize the node and relationship
    serialized_node = {
        'id': node.id,
        'created': node.created,
        'deleted': node.deleted,
        'merged': node.merged,
        'node_type': node.node_type
    }

    serialized_relationship = {
        'id': relationship.id,
        'created': relationship.created,
        'start': relationship.start,
        'end': relationship.end,
        'rel': relationship.rel,
        'ler': relationship.ler,
        'deleted': relationship.deleted
    }

    assert serialized_node['id'] == node.id
    assert serialized_node['node_type'] == "testtype"

    assert serialized_relationship['id'] == relationship.id
    assert serialized_relationship['rel'] == "related"
    assert serialized_relationship['start'] == node.id
    assert serialized_relationship['end'] == node.id
    assert serialized_relationship['ler'] == "testler"