import os

from flask import Blueprint, request
from flaskr import db
from ..models import Page

bp = Blueprint('page', __name__, url_prefix='/page')

def populate_pages():
    data_folder = r'C:\Users\domjd\OneDrive\Documents\Projects\Cains Jawbone\data\processed'
    for filename in os.listdir(data_folder):
        if filename.endswith('.txt') and filename.startswith('page_'):
            page_id = int(filename.split('_')[1].split('.')[0])
            with open(os.path.join(data_folder, filename), 'r', encoding='utf-8', errors='ignore') as file:
                content = file.read()
                # Check if the page already exists to avoid duplicate entries
                page = Page.query.get(page_id)
                if not page:
                    page = Page(id=page_id, page_number=page_id, content=content)
                    db.session.add(page)
                else:
                    page.content = content  # Update content if it already exists
    db.session.commit()


def get_page(page_number: int) -> Page:
    page = db.session.query(Page).filter(Page.page_number == page_number).first()
    return page

@bp.route('/', methods=["GET"])
def api_get_page():
    page_number = request.args.get('page')
    if not page_number:
        return "Page not found", 404
    page = get_page(page_number)
    if not page:
        return "Page not found", 404
    return page.content


def edit_page_content(page, new_content):
    page.content = new_content
    db.session.commit()
    db.session.refresh(page)
    return page

@bp.route('/update', methods=["PUT"])
def api_edit_page_content():
    page_number = request.args.get('page')
    if not page_number:
        return "Page not found", 404
    page = get_page(page_number)
    if not page:
        return "Page not found", 404

    data = request.get_json()
    new_content = data.get('content')
    if new_content is None:
        return "Must provide updated content", 401
    page = edit_page_content(page, new_content)
    return page.content


# Search accross all pages
def search_pages(search_term):
    pages = Page.query.filter(Page.content.ilike(f"%{search_term}%")).all()
    return pages

@bp.route('/search', methods=["GET"])
def api_search_pages():
    search_terms = request.args.getlist('term')
    if not search_terms:
        return []
    
    pages = set()
    for term in search_terms:
        results = set(search_pages(term))
        pages.update(results)
    
    return [n.page_number for n in list(pages)]