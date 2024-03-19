import React, { useState } from 'react';
import axios from 'axios';
import './REPL.css'

const REPL = () => {
    const [input, setInput] = useState('');
    const [output, setOutput] = useState([]);
    const [compiledOutput, setCompiledOutput] = useState([]);
    const [skipConditions, setSkipConditions] = useState([]);

    const handleInputChange = (e) => {
        setInput(e.target.value);
    };

    const handleInputSubmit = async (e) => {
        e.preventDefault();
        setOutput([...output, `${input}`]);
        const payload = {};
        if (skipConditions) {
            const updatedOutput = output.map((line) => {
                if (!skipConditions.includes(line)) {
                    return line
                }
            });
            payload['code'] = updatedOutput.join('\n') + '\n' + input;
        } else {
            payload['code'] = output.join('\n') + '\n' + input;
        }
        /* contacting API for code compilation */
        try {
            const resp = await axios.post('http://127.0.0.1:5000/compile', payload);
            /* factor in returning errors in the output instead of just output */
            const compiledResult = resp.data.output;
            console.log(compiledResult);
            if (compiledResult) {
                setCompiledOutput([compiledResult]);
                setSkipConditions([...skipConditions, input]);
            } else {
                setCompiledOutput([]);
            }
        } catch (error) {
            console.error('Error: ', error);
        }
        setInput('');
    };

    return (
        <div>
            <div>
                {output.map((line, index) => (
                    <div key={index}><p className='cursor'>&gt;&gt;&gt;</p>{line}</div>
                ))}
            </div>
            <div id='repl'>
                {compiledOutput}
                {console.log(compiledOutput[0])}
                {typeof compiledOutput[0] === 'string' && (
                    <br/>
                )}
                <p className='cursor'>&gt;&gt;&gt;</p>
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