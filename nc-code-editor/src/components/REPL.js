import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './REPL.css'

const REPL = () => {
    const [err, setErr] = useState([]);
    const [input, setInput] = useState('');
    const [output, setOutput] = useState([]);
    const [prevInputs, setPrevInputs] = useState([]);
    const [countArrowKey, setCountArrowKey] = useState(0);
    const [compiledOutput, setCompiledOutput] = useState([]);
    const [skipConditions, setSkipConditions] = useState([]);
    

    /* for popup graph display window */

    const openPopup = (htmlData) => {
        const newWindow = window.open('', '_blank', 'width=600,height=520');
        console.log(htmlData);
        if (newWindow) {
            const htmlContent = `
            <!DOCTYPE html>
            ${htmlData}
        `;
        newWindow.document.open();
        newWindow.document.write(htmlContent);
        newWindow.document.close();
        } else {
            alert('Popup blocked by the browser. Please enable popups for this site.');
        }
    };

    /**/

    /* for up arrow key functionality */

    useEffect(() => {
        function handleKeyDown(event) {
            if ((event.key === 'ArrowUp') && (countArrowKey < prevInputs.length - 1)) {
                setInput(prevInputs[prevInputs.length - countArrowKey - 1]);
                setCountArrowKey(countArrowKey + 1);
            } else if ((event.key === 'ArrowUp') && (countArrowKey === prevInputs.length - 1)) {
                setInput(prevInputs[0]);
            } else if ((event.key === 'ArrowDown') && (countArrowKey === 0)) {
                setInput('');
            } else if (event.key === 'ArrowDown') {
                setInput(prevInputs[prevInputs.length - countArrowKey]);
                setCountArrowKey(countArrowKey - 1);
            }
        }

        document.addEventListener('keydown', handleKeyDown);

        return () => {
            document.removeEventListener('keydown', handleKeyDown);
        };
    }, [prevInputs, countArrowKey]);

    /**/

    const handleInputChange = (e) => {
        setInput(e.target.value);
    };

    const handleInputSubmit = async (e) => {
        e.preventDefault();
        setOutput([...output, `${input}`]);
        if (input) {
            setPrevInputs([...prevInputs, `${input}`])
        }
        const payload = {};
        if (skipConditions) {
            const updatedOutput = output.map((line) => {
                if (!skipConditions.includes(line)) {
                    return line;
                }
            });
            payload['code'] = updatedOutput.join('\n') + '\n' + input;
        } else {
            payload['code'] = output.join('\n') + '\n' + input;
        }
        /* contacting API for code compilation */
        try {
            const resp = await axios.post('http://127.0.0.1:5000/compile', payload);
            const compiledError = resp.data.error;
            const compiledResult = resp.data.output;
            const functionNameStart = input.indexOf("(");
            const functionName = input.substring(0, functionNameStart);
            if (functionName === "displayGraph") {
                const varName = input.substring(functionNameStart + 1, input.length - 1);
                const respGET = await axios.get('http://127.0.0.1:5000/get_graph?varName=' + varName);
                if (respGET.data.error) {
                    setErr([...err, compiledError]);
                    setOutput([...output, input, compiledError]);
                    setSkipConditions([...skipConditions, input, compiledError]);
                } else {
                    setSkipConditions([...skipConditions, input]);
                    openPopup(respGET.data);
                }
            } else {
                if (compiledError) {
                    setErr([...err, compiledError]);
                    setOutput([...output, input, compiledError]);
                    setSkipConditions([...skipConditions, input, compiledError]);
                } else if (compiledResult) {
                    setOutput([...output, input, compiledResult]);
                    setCompiledOutput([...compiledOutput, compiledResult]);
                    setSkipConditions([...skipConditions, input, compiledResult]);
                }
            }
        } catch (error) {
            console.error('Error: ', error);
        }
        setInput('');
    };

    return (
        <div>
            <div id="flexbox">
                <div className="terminal-loader">
                    <div className="terminal-header">
                        <div className="terminal-title">Connections REPL</div>
                    </div>
                    <div>
                        {output.map((line, index) => (
                            compiledOutput.includes(line) ? (
                                <div key={index}><p className='cursor'>{line}</p></div>
                            ) : (
                                err.includes(line) ? (
                                    <div key={index}><p className='cursor' style={{ color: 'red' }}>{line}</p></div>
                                ) : (
                                    <div key={index}><p className='cursor'>&gt;&gt;&gt; {line}</p></div>
                                )
                            )
                        ))}
                    </div>
                    <div>
                        <p className='cursor'>&gt;&gt;&gt;</p>
                        <form onSubmit={handleInputSubmit}>
                            &nbsp;<input
                                type="text"
                                value={input}
                                onChange={handleInputChange}
                                width="80"
                                placeholder="Enter Python code here..."
                            />
                        </form>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default REPL;