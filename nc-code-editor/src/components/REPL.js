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

    const openPopup = (htmlData, graphName) => {
        // opens a new window
        const newWindow = window.open('', '_blank', 'width=600,height=520');
        // adds a title of the graph name on the window
        const i = htmlData.indexOf("<head>");
        htmlData = htmlData.slice(0, i + 6) + `\n\t\t<title>Graph ${graphName}</title>` + htmlData.slice(i + 6);

        // writes html content to window
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

    /* functionality for file send to API */

    const handleFileUpload = async (event) => {
        const file = event.target.files[0];
        const formData = new FormData();
        formData.append('file', file);
        console.log(formData);

        try {
            const response = await axios.post('http://127.0.0.1:5000/upload', formData);
            if (response.data.error) {
                const compiledError = response.data.error;
                window.alert(`Your csv has an error: ${compiledError}. You may reupload the csv after error has been addressed.`);
            }
            console.log('File sent successfully:', response.data);
            //document.getElementById('functions').textContent = document.getElementById('functions').textContent + '\n' + formData.
        } catch (error) {
            console.error('Error uploading file:', error);
        }
    }

    /**/

    const handleInputChange = (e) => {
        setInput(e.target.value);
    };

    const handleInputSubmit = async (e) => {
        e.preventDefault();
        setCountArrowKey(0);
        setOutput([...output, `${input}`]);
        if (input) {
            setPrevInputs([...prevInputs, `${input}`])
        }
        const payload = {};
        // change to prev
        if (skipConditions) {
            const updatedInputs = prevInputs.map((line) => {
                if (skipConditions.includes(line)) {
                    return "#" + line;
                }
                return line;
            });
            payload['code'] = updatedInputs.join('\n') + '\n' + input;
        } else {
            payload['code'] = prevInputs.join('\n') + '\n' + input;
        }
        console.log(payload);
        /* contacting API for code compilation */
        try {
            const resp = await axios.post('http://127.0.0.1:5000/compile', payload);
            const compiledError = resp.data.error;
            const compiledResult = resp.data.output;
            const functionNameStart = input.indexOf("(");
            const functionName = input.substring(0, functionNameStart);
            if (functionName === "Vis") {
                const varName = input.substring(functionNameStart + 1, input.length - 1);
                const respGET = await axios.get('http://127.0.0.1:5000/get_graph?varName=' + varName);
                if (respGET.data.error) {
                    setErr([...err, compiledError]);
                    setOutput([...output, input, compiledError]);
                    setSkipConditions([...skipConditions, input]);
                    // setSkipConditions([...skipConditions, input, compiledError]);
                } else {
                    setSkipConditions([...skipConditions, input]);
                    openPopup(respGET.data, varName);
                }
            } else {
                if (compiledError) {
                    setErr([...err, compiledError]);
                    setOutput([...output, input, compiledError]);
                    setSkipConditions([...skipConditions, input]);
                    // setSkipConditions([...skipConditions, input, compiledError]);
                } else if (compiledResult) {
                    if (compiledResult.includes('\n')) {
                        const strs = compiledResult.split('\n');

                        setOutput([...output, input, ...strs]);
                        setCompiledOutput([...compiledOutput, ...strs]);
                        setSkipConditions([...skipConditions, input]);
                        // setSkipConditions([...skipConditions, input, ...strs]);
                    } else {
                        setOutput([...output, input, compiledResult]);
                        setCompiledOutput([...compiledOutput, compiledResult]);
                        setSkipConditions([...skipConditions, input]);
                        // setSkipConditions([...skipConditions, input, compiledResult]);
                    }
                }
            }
        } catch (error) {
            console.error('Error: ', error);
        }
        console.log(output);
        setInput('');
    };

    return (
        <div style={{ height: '92.5vh', display: 'flex', backgroundColor: 'gainsboro' }} >
            <div id='inputbox' style={{ width: '20vw', height: '92.5vh', padding: '10px' }}>
                <div id='fileinputbox' style={{ width: '100%', height: '100%', padding: '10px', backgroundColor: 'white', borderRadius: '15px', padding: '5%', border: '2px solid grey' }}>
                    <h2>File Input:</h2>
                    <input id='csvreader' type="file" accept=".csv" onChange={handleFileUpload} />
                    <br />
                    <br />
                    <h4>Files:</h4>
                    <p id='files'></p>
                </div>
            </div>
            <div id='codearea' style={{ width: '80vw', height: '92.5vh', zIndex: 0, padding: '10px' }}>
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
        </div>
    );
};

export default REPL;