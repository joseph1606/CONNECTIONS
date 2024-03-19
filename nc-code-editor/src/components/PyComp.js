import React, { useState, useEffect } from 'react';
import DOMPurify from 'dompurify'; // Import DOMPurify library


const MyComponent = () => {
    const [htmlContent, setHtmlContent] = useState('');
    useEffect(() => {
        // Fetch HTML content from API
        fetch('http://127.0.0.1:5000/compile')
            .then(response = response.json())
            .then(data => {
                // Sanitize HTML content
                const sanitizedHtml = DOMPurify.sanitize(data.html);
                // Set sanitized HTML content to state
                setHtmlContent(sanitizedHtml);
            })
            .catch(error => console.error('Error fetching HTML content:', error));
    }, []);
}