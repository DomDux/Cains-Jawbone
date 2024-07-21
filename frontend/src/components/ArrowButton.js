import React from "react";

export default function ArrowButton({ direction, callback }) {
    const DIRECTIONS = {
        "left": "<",
        "right": ">",
        "up": "^",
        "down": "D"
    };
    const val = DIRECTIONS[direction];
    return (
        <button onClick={callback}>
            {val}
        </button>
    )
}