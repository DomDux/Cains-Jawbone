/*********************************************************************************************************************
  Page Component
  This component renders the text information for a given page.  This includes:
  - The text from the database retrieved with the `/page?page=${pageNo}` API call
  - 

  Page View Component
  This contains the full view for the page i.e. the PageComponent AND any associated notes
   - 

*********************************************************************************************************************/


import React, { useState, useEffect } from 'react';
import { Button, Modal, Form, Container, Row, Col } from "react-bootstrap";

import NoteListComponent from "./NoteListComponent"; 
import ArrowButton from './ArrowButton';

import '../styles/PageComponent.css';

export default function PageComponent({ pageNo, onCreateNote }) {
  // Hooks for loading page content
  const [content, setContent] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Notes
  const [notes, setNotes] = useState([]);

  useEffect(() => {
    fetchNotes();
  }, []);

  const fetchNotes = async () => {
    try {
      const response = await fetch(`/note/on-page?id=${pageNo}`);
      const data = await response.json();
      setNotes(data);
      applyPersistentHighlights(data);
    } catch (error) {
      console.error("Error fetching notes:", error);
    }
  };

  // Hooks for creating new notes
  const [selectedText, setSelectedText] = useState("");
  const [textRange, setTextRange] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [noteContent, setNoteContent] = useState("");


  /**
   * Function to take the selected text and store it in the state
   */
  const handleTextSelection = () => {
    const selection = window.getSelection();
    if (selection && selection.toString()) {
      const range = selection.getRangeAt(0);
      setSelectedText(selection.toString());
      setTextRange(range);
    }
  };

  /**
   * Function to open the modal to create a new note. 
   * Called when the user clicks the "Create New Note" button.
   */
  const openCreateNoteModal = () => {
    if (selectedText) {
      setShowModal(true);
    } else {
      alert("Please highlight some text to create a note.");
    }
  };

  const handleModalClose = () => {
    setShowModal(false);
    setNoteContent("");
    setSelectedText("");
    setTextRange(null);
  };

  /**
   * Function to save the note to the database
   */
  const handleSaveNote = async () => {
    const noteData = {
      page_number: pageNo,
      note_text: selectedText,
      content: noteContent,
    };

    try {
      const response = await fetch("/note/create", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(noteData),
      });

      if (response.ok) {
        // Handle success (e.g., apply highlight to text)
        const createdNote = await response.json();
        onCreateNote(createdNote);
        handleModalClose();
      } else {
        console.error("Failed to create note.");
      }
    } catch (error) {
      console.error("Error:", error);
    }
  };

  /**
   * Given a note ID, apply a highlight to the text it corresponds to.
   * @param {string} note_text - The text we wish to highlight
   * @param {number} note_id - The ID of the note
   */
  const applyHighlightToText = (note_text, note_id) => {
    const contentElement = document.querySelector(".page-content p");
    if (contentElement === null) {
      return;
    }
    console.log(contentElement);
    const contentText = contentElement.textContent;

    // Find the start and end positions of the note text
    const startIndex = contentText.indexOf(note_text);
    const endIndex = startIndex + note_text.length;

    if (startIndex !== -1 && endIndex !== -1) {
      const range = document.createRange();
      const startNode = contentElement.firstChild;

      // Set the range to the start and end positions
      range.setStart(startNode, startIndex);
      range.setEnd(startNode, endIndex);

      // Create a span element to apply the highlight
      const span = document.createElement("span");
      span.className = "highlighted-text";
      span.dataset.noteId = note_id;
      range.surroundContents(span); // Apply the highlight
    }
  };

  /**
   * Iterate through the notes provided and apply highlights to the text.
   * @param {Array} notes
   */
  const applyPersistentHighlights = (notes) => {
    notes.forEach(note => {
        applyHighlightToText(note.text, note.id);
      }
    );
  };

  
  useEffect(() => {
    // Function to fetch the page content
    const fetchPageContent = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await fetch(`/page?page=${pageNo}`);
        const content = await response.text();
        setContent(content);
        // applyPersistentHighlights(notes);
      } catch (err) {
        setError(err.message);
      }
      setLoading(false);
    };

    fetchPageContent();
  }, [pageNo]);

  if (loading) {
    return <div className='page-content'>Loading...</div>;
  }

  if (error) {
    return <div className='page-content'>Error: {error}</div>;
  }

  const modalForNewNode = (
    <Modal show={showModal} onHide={handleModalClose}>
      <Modal.Header closeButton>
        <Modal.Title>Create New Note</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <Form>
          <Form.Group>
            <Form.Label>Highlighted Text</Form.Label>
            <Form.Control as="textarea" rows={2} value={selectedText} readOnly />
          </Form.Group>
          <Form.Group className="mt-3">
            <Form.Label>Page Number</Form.Label>
            <Form.Control type="text" value={pageNo} readOnly />
          </Form.Group>
          <Form.Group className="mt-3">
            <Form.Label>Note Content</Form.Label>
            <Form.Control as="textarea" rows={5} value={noteContent} onChange={(e) => setNoteContent(e.target.value)} />
          </Form.Group>
        </Form>
      </Modal.Body>
      <Modal.Footer>
          <Button variant="secondary" onClick={handleModalClose}>Cancel</Button>
          <Button variant="primary" onClick={handleSaveNote}>Save Note</Button>
      </Modal.Footer>
    </Modal>
  );


  return (
    <div className='page-content'>
      <h1>Page {pageNo}</h1>
      <div onMouseUp={handleTextSelection}>
        <p>{content}</p>
        {selectedText && <Button variant="primary" onClick={openCreateNoteModal}>Create New Note</Button>}
        {/* Note Tabs */}
        {/* {notes.map(note => (
          <NoteTab key={note.id} data={note.content} />
        ))} */}
        {modalForNewNode}
      </div>
    </div>
  );
}
  
export function PageViewComponent() {
  const [newNote, setNewNote] = useState(null);
  const [updateNote, setUpdateNote] = useState(null);

  const [pageNo, setPageNo] = useState(1);

  const handleCreateNote = (note) => {
    setNewNote(note);
  };

  const handleUpdateNote = (note) => {
    setUpdateNote(note);
  };

  return (
    <div className="page-view-component">
      <Container>
        <Row className="justify-content-md-center">
          <Col xs={12} md={8} lg={6} xl={4}>
            <PageComponent pageNo={pageNo} onCreateNote={handleCreateNote} />
          </Col>
        </Row>
        <Row className='justify-content-md-center'>
          <Col xs={12} md={8} lg={6} xl={4}>
            <ArrowButton direction={'left'} callback={()=> pageNo > 1 && setPageNo(pageNo-1)}/>
            <ArrowButton direction={'right'} callback={()=> pageNo < 100 && setPageNo(pageNo+1)}/>
          </Col>
        </Row>
      </Container>
      <NoteListComponent pageNumber={pageNo} newNote={newNote} />
    </div>
  );
}
