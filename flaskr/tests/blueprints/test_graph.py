import pytest
from flask import Flask, jsonify
from flaskr.blueprints.graph import bp as graph_bp, _return_node, _return_relationship, create_node, create_relationship
from flaskr.models import db, Node, Relationship


def test_return_node(session):
    node = Node(node_type="testtype")
    session.add(node)
    session.commit()
    result = _return_node(node)
    assert result == {
        'id': node.id,
        'created': node.created,
        'deleted': node.deleted,
        'merged': node.merged,
        'node_type': node.node_type
    }

def test_return_relationship(session):
    start_node = Node(node_type="testtype1")
    end_node = Node(node_type="testtype2")
    session.add(start_node)
    session.add(end_node)
    session.commit()
    relationship = Relationship(start=start_node.id, end=end_node.id, rel="related", ler="testler")
    session.add(relationship)
    session.commit()
    result = _return_relationship(relationship)
    assert result == {
        'id': relationship.id,
        'created': relationship.created,
        'start': relationship.start,
        'end': relationship.end,
        'rel': relationship.rel,
        'ler': relationship.ler,
        'deleted': relationship.deleted
    }

def test_create_node(client):
    response = client.post('/graph/node/create', json={'node_type': 'person'})
    assert response.status_code == 200
    node_id = response.get_data(as_text=True)
    node = Node.query.get(node_id)
    assert node is not None
    assert node.node_type == 'person'

def test_create_relationship(client, session):
    start_node = Node(node_type="testtype1")
    end_node = Node(node_type="testtype2")
    session.add(start_node)
    session.add(end_node)
    session.commit()
    response = client.post('/graph/relationship/create', json={
        'start': start_node.id,
        'end': end_node.id,
        'forward_relationship': 'related',
        'reverse_relationship': 'related'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2
    for rel_id, rel_data in data.items():
        assert 'id' in rel_data
        assert 'created' in rel_data
        assert 'start' in rel_data
        assert 'end' in rel_data
        assert 'rel' in rel_data
        assert 'ler' in rel_data
        assert 'deleted' in rel_data

def test_get_nodes(client, session):
    node = Node(node_type="testtype")
    session.add(node)
    session.commit()
    response = client.get(f'/graph/node?id={node.id}')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['id'] == node.id
    assert data[0]['node_type'] == node.node_type

def test_get_relationships(client, session):
    start_node = Node(node_type="testtype1")
    end_node = Node(node_type="testtype2")
    session.add(start_node)
    session.add(end_node)
    session.commit()
    relationship = Relationship(start=start_node.id, end=end_node.id, rel="related", ler="testler")
    session.add(relationship)
    session.commit()
    response = client.get(f'/graph/relationship?id={relationship.id}')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['id'] == relationship.id
    assert data[0]['start'] == relationship.start
    assert data[0]['end'] == relationship.end
    assert data[0]['rel'] == relationship.rel
    assert data[0]['ler'] == relationship.ler

def test_soft_delete_node(client, session):
    node = Node(node_type="testtype")
    session.add(node)
    session.commit()
    response = client.put(f'/graph/node/delete?id={node.id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['deleted'] == 1

def test_soft_delete_relationship(client, session):
    start_node = Node(node_type="testtype1")
    end_node = Node(node_type="testtype2")
    session.add(start_node)
    session.add(end_node)
    session.commit()
    relationship = Relationship(start=start_node.id, end=end_node.id, rel="related", ler="testler")
    reverse_relationship = Relationship(start=end_node.id, end=start_node.id, rel="related", ler="testler")
    session.add(relationship)
    session.add(reverse_relationship)
    session.commit()
    response = client.put(f'/graph/relationship/delete?id={relationship.id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data[str(relationship.id)]['deleted'] == 1
    assert data[str(reverse_relationship.id)]['deleted'] == 1

def test_merge_nodes(client, session):
    node1 = Node(node_type="testtype")
    node2 = Node(node_type="testtype")
    session.add(node1)
    session.add(node2)
    session.commit()
    response = client.put('/graph/node/merge', json={'id': [node1.id, node2.id]})
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 3  # new node + 2 merged nodes
    assert data[0]['node_type'] == 'testtype'
    assert data[1]['merged'] == data[0]['id']
    assert data[2]['merged'] == data[0]['id']

def test_delete_node(client, session):
    node = Node(node_type="testtype")
    session.add(node)
    session.commit()
    response = client.delete(f'/graph/node/harddelete?id={node.id}')
    assert response.status_code == 200
    assert Node.query.get(node.id) is None

def test_delete_relationship(client, session):
    start_node = Node(node_type="testtype1")
    end_node = Node(node_type="testtype2")
    session.add(start_node)
    session.add(end_node)
    session.commit()
    relationship = Relationship(start=start_node.id, end=end_node.id, rel="related", ler="testler")
    reverse_relationship = Relationship(start=end_node.id, end=start_node.id, rel="related", ler="testler")
    session.add(relationship)
    session.add(reverse_relationship)
    session.commit()
    response = client.delete(f'/graph/relationship/harddelete?id={relationship.id}')
    assert response.status_code == 200
    assert Relationship.query.get(relationship.id) is None
    assert Relationship.query.get(reverse_relationship.id) is None