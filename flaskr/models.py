from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()

class Page(db.Model):
    """
    Represents a page in the application.

    Attributes:
        id (int): The primary key of the page.
        page_number (int): The number of the page.
        content (str): The content of the page.
    """
    __tablename__ = 'pages'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    page_number = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self) -> str:
        return f"<Page {self.id}>"

class User(db.Model):
    """
    Represents a user in the application.

    Attributes:
        id (int): The primary key of the user.
        username (str): The username of the user.
        password (str): The password of the user.
    """
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __repr__(self) -> str:
        return f"<User {self.username}>"

class Tag(db.Model):
    """
    Represents a tag in the application.

    Attributes:
        id (int): The primary key of the tag.
        created (datetime): The creation date of the tag.
        deleted (int): Indicates if the tag is deleted (0 or 1).
        name (str): The name of the tag.
    """
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created = db.Column(db.DateTime, default=datetime.now, nullable=False)
    deleted = db.Column(db.Integer, default=0)
    name = db.Column(db.String, nullable=False)

    def __repr__(self) -> str:
        return f"<Tag {self.name}>"

class Node(db.Model):
    """
    Represents a node in the application.

    Attributes:
        id (int): The primary key of the node.
        created (datetime): The creation date of the node.
        node_type (str): The type of the node.
        deleted (int): Indicates if the node is deleted (0 or 1).
        merged (int): Indicates if the node is merged (nullable).
    """
    __tablename__ = 'nodes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created = db.Column(db.DateTime, default=datetime.now, nullable=False)
    node_type = db.Column(db.String, nullable=False)
    deleted = db.Column(db.Integer, default=0)
    merged = db.Column(db.Integer, nullable=True)

    def __repr__(self) -> str:
        return f"<Node {self.id}>"

class Relationship(db.Model):
    """
    Represents a relationship between two nodes in the application.

    Attributes:
        id (int): The primary key of the relationship.
        created (datetime): The creation date of the relationship.
        start (int): The starting node ID of the relationship.
        end (int): The ending node ID of the relationship.
        rel (str): The type of the relationship.
        ler (str): The reverse type of the relationship.
        deleted (int): Indicates if the relationship is deleted (0 or 1).
    """
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
        return f"<Relationship {self.id}>"

class Note(db.Model):
    """
    Represents a note in the application.

    Attributes:
        id (int): The primary key of the note.
        note_text (str): The text of the note.
        created (datetime): The creation date of the note.
        page_number (int): The page number the note is associated with.
        content (str): The content of the note.
        deleted (int): Indicates if the note is deleted (0 or 1).
        resolved (int): Indicates if the note is resolved (0 or 1).
        node_id (int): The node ID the note is associated with.
        text_start (int): The start index for text highlighting.
        text_end (int): The end index for text highlighting.
    """
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    note_text = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, default=datetime.now, nullable=False)
    page_number = db.Column(db.Integer, db.ForeignKey('pages.id'), nullable=False)
    content = db.Column(db.Text, nullable=True)
    deleted = db.Column(db.Integer, default=0)
    resolved = db.Column(db.Integer, default=0)
    node_id = db.Column(db.Integer, db.ForeignKey('nodes.id'), nullable=True)

    # Indexes for text highlighting
    text_start = db.Column(db.Integer, nullable=True)
    text_end = db.Column(db.Integer, nullable=True)

    page = db.relationship('Page')
    node = db.relationship('Node', foreign_keys=[node_id])
    
    def __repr__(self) -> str:
        return f"<Note {self.id}>"

class Person(db.Model):
    """
    Represents a person in the application.

    Attributes:
        id (int): The primary key of the person.
        created (datetime): The creation date of the person.
        deleted (int): Indicates if the person is deleted (0 or 1).
        name (str): The name of the person.
        content (str): The content of the person.
        gender (str): The gender of the person.
        node_id (int): The node ID the person is associated with.
    """
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
        return f"<Person {self.id}>"

class Location(db.Model):
    """
    Represents a location in the application.

    Attributes:
        id (int): The primary key of the location.
        created (datetime): The creation date of the location.
        deleted (int): Indicates if the location is deleted (0 or 1).
        name (str): The name of the location.
        content (str): The content of the location.
        country (str): The country of the location.
        district (str): The district of the location.
        town (str): The town of the location.
        node_id (int): The node ID the location is associated with.
    """
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
        return f"<Location {self.id}>"

class Event(db.Model):
    """
    Represents an event in the application.

    Attributes:
        id (int): The primary key of the event.
        created (datetime): The creation date of the event.
        deleted (int): Indicates if the event is deleted (0 or 1).
        name (str): The name of the event.
        content (str): The content of the event.
        date (datetime): The date of the event.
        node_id (int): The node ID the event is associated with.
    """
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
        return f"<Event {self.id}>"

if __name__ == '__main__':
    db.create_all()
