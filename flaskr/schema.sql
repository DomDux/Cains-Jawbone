DROP TABLE IF EXISTS pages;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS tags;
DROP TABLE IF EXISTS nodes;
DROP TABLE IF EXISTS relationships;
DROP TABLE IF EXISTS notes;
DROP TABLE IF EXISTS people;
DROP TABLE IF EXISTS locations;
DROP TABLE IF EXISTS events;


-- REFERENCE DATA
-- Data for the page content.
CREATE TABLE pages (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  page_number INTEGER NOT NULL,
  content TEXT NOT NULL
);
----------------------------

-- MASTER DATA
-- Users of the app
CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);


-- Tags for filtering nodes
CREATE TABLE tags (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  deleted INTEGER DEFAULT 0,
  name TEXT NOT NULL
);
-------------------------------

-- TRANSACTION DATA
-- GRAPH DATABASE:  Describe all entities like people, places etc as nodes on a graph
CREATE TABLE nodes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  node_type TEXT NOT NULL,
  deleted INTEGER DEFAULT 0

  CONSTRAINT CHK_Type CHECK node_type IN (
    'person', 'location', 'event', 'note', 'tag'
  )
);
/* 
CREATE TABLE relationships (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  name TEXT NOT NULL,
  start INTEGER NOT NULL,
  end INTEGER NOT NULL,
  relationship TEXT NON NULL, -- Description of the relationship e.g. Mother
  pihsnoitaler TEXT NON NULL,  -- Reverse relationship description e.g. Son
  deleted INTEGER DEFAULT 0,

  CONSTRAINT FK_Start FOREIGN KEY (start) REFERENCES nodes (id),
  CONSTRAINT FK_End FOREIGN KEY (end) REFERENCES nodes (id)
);

-- User generated notes.  These link to potential entities
CREATE TABLE notes (
  id INTEGER PRIMARY KEY,
  note_text TEXT NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  page_number INTEGER NOT NULL,
  content TEXT,
  deleted INTEGER DEFAULT 0,
  resolved INTEGER DEFAULT 0,  -- If e.g. 2 nodes are resolved into 1 entity, we create 1 linked node to act for both and set this to 1 to avoid reuse.

  CONSTRAINT FK_Page FOREIGN KEY (page_number) REFERENCES pages (id),
  CONSTRAINT FK_Node FOREIGN KEY (id) REFERENCES nodes (id)
);

-- People
CREATE TABLE people (
  id INTEGER PRIMARY KEY,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  deleted INTEGER DEFAULT 0,
  name TEXT NOT NULL,
  content TEXT NOT NULL,

  gender TEXT,
  
  CONSTRAINT FK_Node FOREIGN KEY (id) REFERENCES nodes (id)
);

-- Locations
CREATE TABLE locations (
  id INTEGER PRIMARY KEY,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  deleted INTEGER DEFAULT 0,
  name TEXT NOT NULL,
  content TEXT NOT NULL,

  country TEXT,
  district TEXT,
  town TEXT,

  CONSTRAINT FK_Node FOREIGN KEY (id) REFERENCES nodes (id)
);

-- Events/ Things that happen on a date
CREATE TABLE events (
  id INTEGER PRIMARY KEY,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  deleted INTEGER DEFAULT 0,
  name TEXT NOT NULL,
  content TEXT NOT NULL,

  date DATETIME,

  CONSTRAINT FK_Node FOREIGN KEY (id) REFERENCES nodes (id)
);

 */