import React, { useState, useEffect } from 'react';

import '../styles/PageComponent.css';

export default function PageComponent({ pageNo }) {
    const [content, setContent] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
  
    useEffect(() => {
      // Function to fetch the page content
      const fetchPageContent = async () => {
        setLoading(true);
        setError(null);
        try {
          const response = await fetch(`/page?page=${pageNo}`);
          const content = await response.text();
          setContent(content);
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
  
    return (
      <div className='page-content'>
        <h1>Page {pageNo}</h1>
        <p>{content}</p>
      </div>
    );
  }
  