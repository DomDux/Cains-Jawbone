import React from "react";

// Import the SVG files
import { ReactComponent as LeftArrow } from '../assets/left-arrow.svg';
import { ReactComponent as RightArrow } from '../assets/right-arrow.svg';
// import UpArrow from '../assets/up-arrow.svg';
// import DownArrow from '../assets/down-arrow.svg';


export default function ArrowButton({ direction, callback }) {
    const DIRECTIONS = {
        "left": <LeftArrow/>,
        "right": <RightArrow />,
        "up": "^",//<UpArrow />,
        "down": "D"//<DownArrow />
    };
    const val = DIRECTIONS[direction];
    return (
        <button onClick={callback}>
            {val}
        </button>
    )
}