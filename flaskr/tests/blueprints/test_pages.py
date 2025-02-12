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
    assert fetched_page.id == page.id
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