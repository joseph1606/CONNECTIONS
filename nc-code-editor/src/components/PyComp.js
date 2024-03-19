import React, { useState, useEffect } from 'react';
import DOMPurify from 'dompurify'; // Import DOMPurify library


const MyComponent = () => {
    const [htmlContent, setHtmlContent] = useState('');
    useEffect(() => {
        // Fetch HTML content from API
        fetch('/api/your_endpoint')
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