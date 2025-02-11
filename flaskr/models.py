from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()

class Page(db.Model):
    __tablename__ = 'pages'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    page_number = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self) -> str:
        return f"<Page {self.id}>"

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __repr__(self) -> str:
        return f"<User {self.username}>"

class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created = db.Column(db.DateTime, default=datetime.now, nullable=False)
    deleted = db.Column(db.Integer, default=0)
    name = db.Column(db.String, nullable=False)

    def __repr__(self) -> str:
        return f"<Tag {self.name}>"

class Node(db.Model):
    __tablename__ = 'nodes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created = db.Column(db.DateTime, default=datetime.now, nullable=False)
    node_type = db.Column(db.String, nullable=False)
    deleted = db.Column(db.Integer, default=0)
    merged = db.Column(db.Integer, nullable=True)

    def __repr__(self) -> str:
        return f"<Node {id}>"

class Relationship(db.Model):
    __tablename__ = 'relationships'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created = db.Column(db.DateTime, default=datetime.now, nullable=False)
    start = db.Column(db.Integer, db.ForeignKey('nodes.id'), nullable=False)
    end = db.Column(db.Integer, db.ForeignKey('nodes.id'), nullable=False)
    rel = db.Column(db.String, nullable=False)
    ler = db.Column(db.String, nullable=False)
    deleted = db.Column(db.Integer, default=0)

    start_node = db.relationship('Node', foreign_keys=[start])
    end_node = db.relationship('Node', foreign_keys=[end])

    def __repr__(self) -> str:
        return f"<Relationship {id}>"

class Note(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    note_text = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, default=datetime.now, nullable=False)
    page_number = db.Column(db.Integer, db.ForeignKey('pages.id'), nullable=False)
    content = db.Column(db.Text, nullable=True)
    deleted = db.Column(db.Integer, default=0)
    resolved = db.Column(db.Integer, default=0)
    node_id = db.Column(db.Integer, db.ForeignKey('nodes.id'), nullable=True)

    page = db.relationship('Page')
    node = db.relationship('Node', foreign_keys=[node_id])
    def __repr__(self) -> str:
        return f"<Note {id}>"

class Person(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created = db.Column(db.DateTime, default=datetime.now, nullable=False)
    deleted = db.Column(db.Integer, default=0)
    name = db.Column(db.String, nullable=False)
    content = db.Column(db.Text, nullable=False)
    gender = db.Column(db.String, nullable=True)
    node_id = db.Column(db.Integer, db.ForeignKey('nodes.id'), nullable=True)

    node = db.relationship('Node', foreign_keys=[node_id])

    def __repr__(self) -> str:
        return f"<Person {id}>"

class Location(db.Model):
    __tablename__ = 'locations'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created = db.Column(db.DateTime, default=datetime.now, nullable=False)
    deleted = db.Column(db.Integer, default=0)
    name = db.Column(db.String, nullable=False)
    content = db.Column(db.Text, nullable=False)
    country = db.Column(db.String, nullable=True)
    district = db.Column(db.String, nullable=True)
    town = db.Column(db.String, nullable=True)
    node_id = db.Column(db.Integer, db.ForeignKey('nodes.id'), nullable=True)

    node = db.relationship('Node', foreign_keys=[node_id])

    def __repr__(self) -> str:
        return f"<Location {id}>"

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created = db.Column(db.DateTime, default=datetime.now, nullable=False)
    deleted = db.Column(db.Integer, default=0)
    name = db.Column(db.String, nullable=False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=True)
    node_id = db.Column(db.Integer, db.ForeignKey('nodes.id'), nullable=True)

    node = db.relationship('Node', foreign_keys=[node_id])
    
    def __repr__(self) -> str:
        return f"<Event {id}>"

if __name__ == '__main__':
    db.create_all()
