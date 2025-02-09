import React, { useEffect, useState } from "react";
import NoteTab from "./NoteTab"; // Assuming NoteTab component is imported

export default function NoteListComponent({ pageNumber, newNote }) {
    const [notes, setNotes] = useState([]);

    useEffect(() => {
        fetchNotes();
    }, [pageNumber]);

    useEffect(() => {
        if (newNote) {
            setNotes(prevNotes => [...prevNotes, newNote]);
        }
    }, [newNote]);

    // Set the notes on the page to be rendered
    // Rerun this every time something changes on the page
    const fetchNotes = async () => {
        try {
            const response = await fetch(`/note/on-page?id=${pageNumber}`);
            const data = await response.json();
            setNotes(data);
        } catch (error) {
            console.error("Error fetching notes:", error);
        }
    };

    return (
        <div className="note-list">
            {notes.map(note => (
                <NoteTab key={note.id} data={note} />
            ))}
        </div>
    );
}
