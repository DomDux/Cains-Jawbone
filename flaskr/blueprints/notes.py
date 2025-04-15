"""
Here is where we'll add all the views relating to the notes table.   
Notes are the basis for all of our work going forward so they need to be flexible and able to link to other entities.
"""

from flask import (
    Blueprint, request
)
from werkzeug.exceptions import abort

from ..models import *
from .graph import create_node, create_relationship
from ..utils import get_params

bp = Blueprint('notes', __name__, url_prefix='/note')

def _return_note(note):
    return {
        'id': note.id,
        'node_id': note.node_id,
        'page_number': note.page_number,
        'note_text': note.note_text,
        'content': note.content,
        'deleted': note.deleted,
        'text_start': note.text_start,
        'text_end': note.text_end
    }

#####################
# CREATE 
#####################
def create_note(page, note_text, content="", text_start=None, text_end=None):
    # First we create a node for this object
    node_id = create_node('note')

    text_range_valid = text_start is not None and text_end is not None and text_start < text_end
    if not text_range_valid:
        text_start = None
        text_end = None

    # Second we create an entry in the notes table and link it to the node
    note = Note(
        note_text=note_text,
        page_number=page,
        content=content,
        node_id=node_id,
        text_start=text_start,
        text_end=text_end
    )
    db.session.add(note)
    db.session.commit()
    db.session.refresh(note)
    
    return _return_note(note)

@bp.route('/create', methods=["POST"])
def api_create_note():
    data = request.get_json()
    page = data.get('page_number')
    note_text = data.get('note_text')
    content = data.get('content')
    text_start = data.get('text_start')
    text_end = data.get('text_end')
    return create_note(page, note_text, content, text_start, text_end)


##################
# READ
##################
def get_notes(ids):
    return [Note.query.get_or_404(id) for id in ids]

@bp.route('/', methods=["GET"])
def api_get_notes():
    ids = request.args.getlist('id')
    notes = get_notes(ids)
    return [_return_note(note) for note in notes]


# Query for notes containing words
def search_notes(search_term):
    notes = Note.query.filter(Note.content.ilike(f"%{search_term}%")).all()
    return notes

@bp.route('/search', methods=["GET"])
def api_search_notes():
    search_terms = request.args.getlist('term')
    if not search_terms:
        return []
    
    notes = set()
    for term in search_terms:
        results = set(search_notes(term))
        notes.update(results)
    
    return [_return_note(n) for n in list(notes)]

# Return all the notes linked to a page
def get_page_notes(page) -> list[Note]:
    notes = Note.query.filter(Note.page_number == page.page_number).all()
    return notes

@bp.route('/on-page', methods=["GET"])
def api_get_page_notes():
    page_numbers = get_params('id')
    notes = []
    for p in page_numbers:
        page = Page.query.get_or_404(p)
        note_objects = get_page_notes(page)
        notes += [_return_note(n) for n in note_objects]
    return notes

##################
# UPDATE
##################
def update_note(note, new_content):
    note.content = new_content
    db.session.commit()
    db.session.refresh(note)
    return note

@bp.route('/update', methods=["PUT"])
def api_update_note():
    data = request.get_json()
    id = request.args.get('id')
    note = get_notes([id])[0]

    new_content = data.get('content')
    if new_content is not None:
        note = update_note(note, new_content)
    return _return_note(note)


##################
# DELETE
##################
def soft_delete_note(note):
    note.deleted = 1
    db.session.commit()
    db.session.refresh(note)
    return note

@bp.route('/delete', methods=["PUT"])
def api_soft_delete_note():
    id = request.args.get('id')
    note = get_notes([id])[0]
    note = soft_delete_note(note)
    return _return_note(note)

def un_delete_note(note):
    note.deleted = 0
    db.session.commit()
    db.session.refresh(note)
    return note

@bp.route('/undelete', methods=["PUT"])
def api_un_delete_note():
    id = request.args.get('id')
    note = get_notes([id])[0]
    note = un_delete_note(note)
    return _return_note(note)

