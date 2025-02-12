import pytest
from flask import Flask, jsonify
from flaskr.blueprints.notes import bp as notes_bp, create_note, get_notes, search_notes, get_page_notes, update_note, soft_delete_note, un_delete_note
from flaskr.models import db, Note, Page


def test_create_note(session):
    page = Page(page_number=1, content="Page content")
    session.add(page)
    session.commit()
    note = create_note(page.page_number, "Note text", "Note content", 0, 10)
    assert note['id'] is not None
    assert note['page_number'] == page.page_number
    assert note['note_text'] == "Note text"
    assert note['content'] == "Note content"
    assert note['text_start'] == 0
    assert note['text_end'] == 10

def test_get_notes(session):
    page = Page(page_number=1, content="Page content")
    session.add(page)
    session.commit()
    note = create_note(page.page_number, "Note text", "Note content", 0, 10)
    notes = get_notes([note['id']])
    assert len(notes) == 1
    assert notes[0].id == note['id']

def test_create_note_invalid_text_range(session):
    page = Page(page_number=1, content="Page content")
    session.add(page)
    session.commit()
    note = create_note(page.page_number, "Note text", "Note content", 10, 0)
    assert note['text_start'] is None
    assert note['text_end'] is None

def test_create_note_no_text_range(session):
    page = Page(page_number=1, content="Page content")
    session.add(page)
    session.commit()
    note = create_note(page.page_number, "Note text", "Note content")
    assert note['text_start'] is None
    assert note['text_end'] is None

def test_api_create_note_invalid_text_range(client):
    response = client.post('/note/create', json={
        'page_number': 1,
        'note_text': 'Note text',
        'content': 'Note content',
        'text_start': 10,
        'text_end': 0
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['text_start'] is None
    assert data['text_end'] is None

def test_api_create_note_no_text_range(client):
    response = client.post('/note/create', json={
        'page_number': 1,
        'note_text': 'Note text',
        'content': 'Note content'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['text_start'] is None
    assert data['text_end'] is None

def test_api_get_notes_invalid_id(client):
    response = client.get('/note/?id=9999')
    assert response.status_code == 404

def test_api_update_note_invalid_id(client):
    response = client.put('/note/update?id=9999', json={'content': 'Updated content'})
    assert response.status_code == 404

def test_api_soft_delete_note_invalid_id(client):
    response = client.put('/note/delete?id=9999')
    assert response.status_code == 404

def test_api_un_delete_note_invalid_id(client):
    response = client.put('/note/undelete?id=9999')
    assert response.status_code == 404

def test_get_page_notes(session):
    page = Page(page_number=1, content="Page content")
    session.add(page)
    session.commit()
    create_note(page.page_number, "Note text", "Note content", 0, 10)
    notes = get_page_notes(page)
    assert len(notes) == 1
    assert notes[0].page_number == page.page_number

def test_update_note(session):
    page = Page(page_number=1, content="Page content")
    session.add(page)
    session.commit()
    note = create_note(page.page_number, "Note text", "Note content", 0, 10)
    updated_note = update_note(Note.query.get(note['id']), "Updated content")
    assert updated_note.content == "Updated content"

def test_soft_delete_note(session):
    page = Page(page_number=1, content="Page content")
    session.add(page)
    session.commit()
    note = create_note(page.page_number, "Note text", "Note content", 0, 10)
    soft_deleted_note = soft_delete_note(Note.query.get(note['id']))
    assert soft_deleted_note.deleted == 1

def test_un_delete_note(session):
    page = Page(page_number=1, content="Page content")
    session.add(page)
    session.commit()
    note = create_note(page.page_number, "Note text", "Note content", 0, 10)
    soft_delete_note(Note.query.get(note['id']))
    un_deleted_note = un_delete_note(Note.query.get(note['id']))
    assert un_deleted_note.deleted == 0

def test_api_create_note(client):
    response = client.post('/note/create', json={
        'page_number': 1,
        'note_text': 'Note text',
        'content': 'Note content',
        'text_start': 0,
        'text_end': 10
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['id'] is not None
    assert data['page_number'] == 1
    assert data['note_text'] == 'Note text'
    assert data['content'] == 'Note content'
    assert data['text_start'] == 0
    assert data['text_end'] == 10

def test_api_get_notes(client, session):
    page = Page(page_number=1, content="Page content")
    session.add(page)
    session.commit()
    note = create_note(page.page_number, "Note text", "Note content", 0, 10)
    response = client.get(f'/note/?id={note["id"]}')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['id'] == note['id']

def test_api_search_notes(client, session):
    page = Page(page_number=1, content="Page content")
    session.add(page)
    session.commit()
    create_note(page.page_number, "Note text", "Note content", 0, 10)
    response = client.get('/note/search?term=Note content')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['content'] == "Note content"

def test_api_get_page_notes(client, session):
    page = Page(page_number=1, content="Page content")
    session.add(page)
    session.commit()
    create_note(page.page_number, "Note text", "Note content", 0, 10)
    response = client.get(f'/note/on-page?id={page.page_number}')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['page_number'] == page.page_number

def test_api_update_note(client, session):
    page = Page(page_number=1, content="Page content")
    session.add(page)
    session.commit()
    note = create_note(page.page_number, "Note text", "Note content", 0, 10)
    response = client.put(f'/note/update?id={note["id"]}', json={'content': 'Updated content'})
    assert response.status_code == 200
    data = response.get_json()
    assert data['content'] == 'Updated content'

def test_api_soft_delete_note(client, session):
    page = Page(page_number=1, content="Page content")
    session.add(page)
    session.commit()
    note = create_note(page.page_number, "Note text", "Note content", 0, 10)
    response = client.put(f'/note/delete?id={note["id"]}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['deleted'] == 1

def test_api_un_delete_note(client, session):
    page = Page(page_number=1, content="Page content")
    session.add(page)
    session.commit()
    note = create_note(page.page_number, "Note text", "Note content", 0, 10)
    client.put(f'/note/delete?id={note["id"]}')
    response = client.put(f'/note/undelete?id={note["id"]}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['deleted'] == 0