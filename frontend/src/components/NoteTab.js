import React, { useState, useCallback }from "react";
import ArrowButton from "./ArrowButton";

export default function NoteTab({ data, active = false }) {
    
    // Will have a state for the collapsed tag and the open tab.  
    const [isActive, setIsActive] = useState(active);

    // Memoize the callback to prevent re-creating it on every render
    const toggleIsActive = useCallback(() => {
        setIsActive(prevIsActive => !prevIsActive);
    }, []);

    const header = (
        <div>
            <h3 className="note-header">Note #{data.id}</h3>Is Active: {isActive ? "Yes" : "No"}
            <ArrowButton direction={isActive ? "up" : "down"} callback={toggleIsActive} />
        </div>
    );
        
    const body = (
        <div>
            <p>{data.content}</p>
        </div>
    );

    return (
        <div id={`note-${data.id}`}>
            {header}
            {isActive && body}
        </div>
    )

}

async function getNoteData(id) {
    const data = fetch(`/note?id=${id}`)
        .then((r) => r.json())
        .catch(err => err);
    return await data
}