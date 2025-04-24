import * as d3 from "d3"; // we will need d3.js
import React, { useEffect, useRef } from "react"; // we will need react


export const NetworkDiagram = () => {

    // read the data
    // compute the nodes position using a d3-force
    // build the links
    // build the nodes

    const svgRef = useRef(null);
    const [data, setData] = React.useState(null);

    // Fetch data from the server
    useEffect(() => {
        const fetchData = async () => {
            // const res = await fetch('/api/data');  // Adjust if needed (e.g., proxy or full URL)
            const res = await fetch('/vis/graph');  // Adjust if needed (e.g., proxy or full URL)   
            const json = await res.json();
            sessionStorage.setItem("chartData", JSON.stringify(json)); // Optional
            setData(json);
            console.log("Data fetched: ", json);
        };
        fetchData();
    }, []);    
   

    // set the dimensions and margins of the graph
    var margin = {top: 10, right: 30, bottom: 30, left: 40},
    width = 800 - margin.left - margin.right,
    height = 600 - margin.top - margin.bottom;

    // Update the graph when data changes
    useEffect(() => {
        if (!data) return; // Wait for data to be loaded

        // Clear the previous SVG content
        d3.select(svgRef.current).selectAll("*").remove();
        // Append the svg object to the body of the page
        console.log("Data: ", data);
        
        var svg = d3.select(svgRef.current)
            // .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform",
                "translate(" + margin.left + "," + margin.top + ")");
    
        
        // Initialize the links
        var link = svg
            .selectAll("line")
            .data(data.relationships)
            .enter()
            .append("line")
                .style("stroke", "#aaa")
    
        // Initialize the nodes
        var node = svg
            .selectAll("circle")
            .data(data.nodes)
            .enter()
            .append("circle")
                .attr("r", 4)
                .attr("node_id", (d) => d.node_id)
                .style("fill", "#69b3a2")

        // Add labels to the nodes
        var labels = node
        .append("title")
            .text(function(d) { return d.entity.name ? d.entity.name : ""; }) // Use entity.name if it exists
    
        // Let's list the force we wanna apply on the network
        var simulation = d3.forceSimulation(data.nodes)                 // Force algorithm is applied to data.nodes
            .force("link", d3.forceLink()                               // This force provides links between nodes
                .id(function(d) { return d.node_id; })                     // This provide  the id of a node
                .links(data.relationships.map(d => {
                    var obj = {
                        "source": d.start,
                        "target": d.end
                    };
                    return obj;
                } ))                                    // and this the list of links
            )
            .force("charge", d3.forceManyBody().strength(-400))         // This adds repulsion between nodes. Play with the -400 for the repulsion strength
            .force("center", d3.forceCenter(width / 2, height / 2))     // This force attracts nodes to the center of the svg area
            .on("end", ticked);
    
        // This function is run at each iteration of the force algorithm, updating the nodes position.
        function ticked() {
            link
            .attr("x1", function(d) { return d.start.x; })
            .attr("y1", function(d) { return d.start.y; })
            .attr("x2", function(d) { return d.end.x; })
            .attr("y2", function(d) { return d.end.y; });
    
            node
            .attr("cx", function (d) { return d.x+6; })
            .attr("cy", function(d) { return d.y-6; });
        }
    

    }, [data]); // Only re-run the effect if data changes


    return (
        <div>
            <svg ref={svgRef}>
            </svg>
        </div>
    );
};