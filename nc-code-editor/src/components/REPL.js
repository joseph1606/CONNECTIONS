import React, { useState } from 'react';
import './REPL.css'

const REPL = () => {
    const [input, setInput] = useState('');
    const [output, setOutput] = useState([]);

    const handleInputChange = (e) => {
        setInput(e.target.value);
    };

    const handleInputSubmit = (e) => {
        e.preventDefault();
        setOutput([...output, `>>> ${input}`]);
        setInput('');
    };

    return (
        <div>
            <div>
                {output.map((line, index) => (
                    <div key={index}>{line}</div>
                ))}
            </div>
            <div id='repl'>
                <p>&gt;&gt;&gt;</p>
                <form onSubmit={handleInputSubmit}>
                    <input
                        type="text"
                        value={input}
                        onChange={handleInputChange}
                        placeholder="Enter Python code here..."
                    />
                </form>
            </div>
        </div>
    );
};

export default REPL;