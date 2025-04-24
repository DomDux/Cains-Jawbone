import pytest
from flaskr.models import Page, User, Tag, Node, Relationship, Note, Person, Location, Event
from flaskr import db
from flaskr.models import Serialiser
from flaskr.blueprints.entities import create_entity
from flaskr.blueprints.vis import return_graph

from datetime import datetime


def test_return_graph(client, session):
    # Create a sample graph with nodes and relationships
    person = create_entity("person", name="John Doe", content="Person content")
    location = create_entity(
        "location",
        name="Test Location",
        content="Location content",
        country="UK",
        district="Lake District",
        town="Kendal"
    )
    event = create_entity("event", name="Test Event", content="Event content", date=datetime.now())
    session.add(person)
    session.add(location)
    session.add(event)
    session.commit()

    relationship1 = Relationship(start=person.node_id, end=location.node_id, rel="lives_in", ler="testler")
    relationship2 = Relationship(start=person.node_id, end=event.node_id, rel="attended", ler="testler")
    session.add(relationship1)
    session.add(relationship2)
    session.commit()

    # Call the return_graph function
    graph_data = return_graph()

    # Check if the graph data is returned correctly
    assert len(graph_data['nodes']) == 3
    assert len(graph_data['relationships']) == 2