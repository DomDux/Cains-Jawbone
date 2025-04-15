import pytest
from flask import Flask, jsonify
from flaskr.blueprints.pages import bp as pages_bp, populate_pages, get_page, edit_page_content, search_pages
from flaskr.models import db, Page


def test_populate_pages(session):
    # Assuming you have some test data files in the specified directory
    populate_pages()
    pages = Page.query.all()
    assert len(pages) > 0  # Ensure that pages were populated

def test_get_page(session):
    page = Page(page_number=1, content="Page content")
    session.add(page)
    session.commit()
    fetched_page = get_page(page.page_number)
    assert fetched_page.page_number == page.page_number
    assert fetched_page.content == page.content

def test_edit_page_content(session):
    page = Page(page_number=1, content="Page content")
    session.add(page)
    session.commit()
    updated_page = edit_page_content(page, "Updated content")
    assert updated_page.content == "Updated content"

def test_search_pages(session):
    page = Page(page_number=1, content="Page content")
    session.add(page)
    session.commit()
    pages = search_pages("Page content")
    assert len(pages) == 1
    assert pages[0].content == "Page content"

def test_api_get_page(client, session):
    page = Page(page_number=1, content="Page content")
    session.add(page)
    session.commit()
    response = client.get(f'/page/?page={page.page_number}')
    assert response.status_code == 200
    assert response.get_data(as_text=True) == page.content

def test_api_edit_page_content(client, session):
    page = Page(page_number=1, content="Page content")
    session.add(page)
    session.commit()
    response = client.put(f'/page/update?page={page.page_number}', json={'content': 'Updated content'})
    assert response.status_code == 200
    assert response.get_data(as_text=True) == 'Updated content'

def test_api_search_pages(client, session):
    page = Page(page_number=1, content="Page content")
    session.add(page)
    session.commit()
    response = client.get('/page/search?term=Page content')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0] == page.page_number

def test_api_get_page_not_found(client):
    response = client.get('/page/?page=999')
    assert response.status_code == 404
    assert response.get_data(as_text=True) == "Page not found"

def test_api_edit_page_content_no_page(client):
    response = client.put('/page/update?page=999', json={'content': 'Updated content'})
    assert response.status_code == 404
    assert response.get_data(as_text=True) == "Page not found"

def test_api_edit_page_content_no_content(client, session):
    page = Page(page_number=1, content="Page content")
    session.add(page)
    session.commit()
    response = client.put(f'/page/update?page={page.page_number}', json={})
    assert response.status_code == 401
    assert response.get_data(as_text=True) == "Must provide updated content"

def test_api_search_pages_no_term(client):
    response = client.get('/page/search')
    assert response.status_code == 200
    data = response.get_json()
    assert data == []