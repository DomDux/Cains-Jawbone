import './App.css';
import React, { useState, useEffect } from "react";
import { Container, Row, Col } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';

import PageComponent, { PageViewComponent } from './components/PageComponent';
import Navbar from './components/Navbar';
import ArrowButton from './components/ArrowButton';
import NoteTab from './components/NoteTab';
import { NetworkDiagram } from './components/NetworkDiagram';

function App() {
  const [pageNo, setPageNo] = useState(1);

  async function getPageNotes(pageNo) {
    try {
      const response = await fetch(`/note/on-page?id=${pageNo}`);
      const data = await response.json(); // This will be your array of notes
      return data
    } catch (err) {
      console.error(err);
      return []; // Return an empty array or handle the error as needed
    }
  };

  const [pageNotes, setPageNotes] = useState([]);

  // Call this every time we change the pageNo
  useEffect(() => {
    async function fetchNotes() {
      const data = await getPageNotes(pageNo);
      setPageNotes(data);
    }
    fetchNotes();
  }, [pageNo]);


  //console.log("Page Notes: ",   pageNotes);
  /* return (
    <div className="App">
      <Navbar />
      <Container>
        <Row className="justify-content-md-center">
          <Col xs={12} md={8} lg={6} xl={4}>
            <PageComponent pageNo={pageNo}/>
          </Col>
        </Row>
        <Row className='justify-content-md-center'>
          <Col xs={12} md={8} lg={6} xl={4}>
            <ArrowButton direction={'left'} callback={()=> pageNo>1 && setPageNo(pageNo-1)}/>
            <ArrowButton direction={'right'} callback={()=> pageNo <100 && setPageNo(pageNo+1)}/>
          </Col>
        </Row>
      </Container>
      <div id='notes'>
        {pageNotes.map(d => (
          <NoteTab key={d.id} data={d}/>
        ))}
      </div>

    </div>
  ); */




  return (
    <div className='App'>
      <Navbar />
      <PageViewComponent pageNumber={pageNo} />
      <NetworkDiagram width={400} height={320} />
    </div>
  )
}

export default App;
