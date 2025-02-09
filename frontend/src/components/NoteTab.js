/********************************************************************************************************************* 
                                                    NOTE TABS
 These are the components in which the content of a note is displayed.  Each note relates to a single NOTE object
 represented by the `note_id` field and corresponds to a single record in the "notes" table of the database.  It is 
 possible for a note to be linked to 0 to many entities via relationships from the "relationships" table and these 
 should be visible as links on the note itself.  As a component, this should be a collapseable tab visible near the 
 rendering of the page text.  It must display information about the note, it's linked entities, the text it relates to,
 and provide links to edit or create  new notes.

 Requirements for the Note Tab:
  - Collapseable:  When inactive, show Title, names of linked tags, and appear small with a drop-down arrow indicating it
    can be expanced.  When active, show
        - Note content 
        - Links to linked entities
  - Needs a button to EDIT the content of the note which should make the note text display an editable textbox area 
    with the existing text populated by default, and a SAVE button should appear.  When we hit save, it executes a PUT
    request on the database to update the note.
  - Needs an "Add Tags" button for people to add tags to the UI.

**********************************************************************************************************************/


import React, { useState, useCallback }from "react";
import { Button, Card, Collapse, Form } from "react-bootstrap";
import ArrowButton from "./ArrowButton";

export default function NoteTab({ data, active = false }) {
    
    // Will have a state for the collapsed tag and the open tab.  
    const [isActive, setIsActive] = useState(active);
    // When this is true, the note is unlocked for user edits
    const [isEditing, setIsEditing] = useState(false);
    // When this is true, the note is unlocked for adding tags
    const [isTagging, setIsTagging] = useState(false);
    // Use this to highlight page text when hovered over
    const [isHovered, setIsHovered] = useState(false);
    // Use this to update the content of the tab
    const [content, setContent] = useState(data.content);

    // Memoize the callback to prevent re-creating it on every render
    const toggleIsActive = useCallback(() => {
        setIsActive(prevIsActive => !prevIsActive);
        console.log("Toggle Active");
    }, []);

    // Toggles the edit mode
    const toggleEditMode = () => {
        setIsEditing(prevIsEditing => !prevIsEditing);
    };

    // Handles content changes in the edit mode
    const handleContentChange = (e) => {
        setContent(e.target.value);
    };

    // Handles saving the edited content
    const handleSave = async () => {
        try {
            const response = await fetch(`/note/update?id=${data.id}`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ content })
            });
            if (response.ok) {
                setIsEditing(false);
            } else {
                console.error("Failed to save the note.");
            }
        } catch (err) {
            console.error("Error:", err);
        }
    };

    // Handles adding tags
    const toggleAddTag = () => {
        setIsTagging(prevIsTagging => !prevIsTagging)
    } 

    // Mouseover Actions
    const handleMouseEnter = () => {
        setIsHovered(true);
        highlightText(true);
    };

    const handleMouseLeave = () => {
        setIsHovered(false);
        highlightText(false);
    };

    const highlightText = (isActive) => {
        const spans = document.querySelectorAll(`.highlighted-text[data-note-id="${data.id}"]`);
        spans.forEach(span => {
            if (isActive) {
                span.classList.add("active");
            } else {
                span.classList.remove("active");
            }
        });
    };


    const header = (
        <div
            className="note-tab"
            onMouseEnter={handleMouseEnter}
            onMouseLeave={handleMouseLeave}
        >
            <h3 className="note-header">Note #{data.id}</h3>Is Active: {isActive ? "Yes" : "No"}
            <ArrowButton direction={isActive ? "up" : "down"} callback={toggleIsActive} />
        </div>
    );
        
    const body = (
        <div>
            <p>{data.content}</p>
        </div>
    );
    /*
    return (
        <div id={`note-${data.id}`}>
            {header}
            {isActive && body}
        </div>
    )*/

    return (
        <div 
            className="d-flex justify-content-center my-3"
            onMouseEnter={handleMouseEnter}
            onMouseLeave={handleMouseLeave}
        >
            <Card style={{ width: "100%", maxWidth: "600px", borderRadius: "8px", boxShadow: "0 2px 4px rgba(0, 0, 0, 0.1)" }}>
                <Card.Header className="d-flex justify-content-between align-items-center" onClick={toggleIsActive} style={{ cursor: "pointer" }}>
                    <h5 className="mb-0">Note #{data.id}</h5>
                    <ArrowButton direction={isActive ? "up" : "down"} callback={() => ''} />
                </Card.Header>
                <Collapse in={isActive}>
                    <Card.Body>
                        {isEditing ? (
                            <>
                                <Form.Control as="textarea" rows={5} value={content} onChange={handleContentChange} />
                                <div className="d-flex justify-content-end mt-2">
                                    <Button variant="secondary" onClick={toggleEditMode} className="me-2">Cancel</Button>
                                    <Button variant="primary" onClick={handleSave}>Save</Button>
                                </div>
                            </>
                        ) : (
                            <>
                                <p>{content}</p>
                                <Button variant="outline-primary" size="sm" onClick={toggleEditMode}>Edit</Button>
                            </>
                        )}
                        <div className="mt-3">
                            <Button variant="outline-success" size="sm">Add Tags</Button>
                        </div>
                    </Card.Body>
                </Collapse>
            </Card>
        </div>
    )
}





async function getNoteData(id) {
    const data = fetch(`/note?id=${id}`)
        .then((r) => r.json())
        .catch(err => err);
    return await data
}