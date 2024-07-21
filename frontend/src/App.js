import './App.css';
import React, { useState } from "react";
import { Container, Row, Col } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';

import PageComponent from './components/PageComponent';
import Navbar from './components/Navbar';
import ArrowButton from './components/ArrowButton';

function App() {
  const [pageNo, setPageNo] = useState(1);

  return (
    <div className="App">
      <Navbar />
      <Container>
        <Row className="justify-content-md-center">
          <Col xs={12} md={8} lg={6} xl={4}>
            <PageComponent pageNo={pageNo}/>
          </Col>
          <Col xs={12} md={8} lg={6} xl={4}>
            <ArrowButton direction={'left'} callback={()=>setPageNo(pageNo-1)}/>
            <ArrowButton direction={'right'} callback={()=>setPageNo(pageNo+1)}/>
          </Col>
        </Row>
      </Container>
    </div>
  );
}

export default App;
