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
        // WALTER: file.name will give you all the file names
        const formData = new FormData();
        formData.set('file', file);
        formData.set('csvName', file.name);

        try {
            const response = await axios.post('http://127.0.0.1:5000/upload', formData);
            if (response.data.error) {
                const compiledError = response.data.error;
                window.alert(`Your csv has an error: ${compiledError}. You may reupload the csv after error has been addressed.`);
            }
            console.log('File sent successfully:', response.data);
        } catch (error) {
            console.error('Error uploading file:', error);
        }
        document.getElementById('csvreader').value = '';
    }

    /**/

    const handleInputChange = (e) => {
        setInput(e.target.value);
    };

    // Function to deep copy the state array
    const deepCopyStateArray = (array) => {
        return JSON.parse(JSON.stringify(array));
    };

    const handleInputSubmit = async (e) => {
        e.preventDefault();
        setCountArrowKey(0);
        setOutput([...output, `${input}`]);
        if (input) {
            setPrevInputs([...prevInputs, `${input}`])
        }
        const payload = {};
        // checks if previous code has generated an output and comments it out in the payload if so
        if (skipConditions) {
            const inputCopy = deepCopyStateArray(prevInputs)
            for (let i = 0; i < skipConditions.length; i++) {
                const skipMe = skipConditions[i]
                if (inputCopy.includes(skipMe)) {
                    inputCopy[inputCopy.indexOf(skipMe)] = `#${skipMe}`;
                }
            }
            payload['code'] = inputCopy.join('\n') + '\n' + input;
        } else {
            payload['code'] = prevInputs.join('\n') + '\n' + input;
        }
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
                } else {
                    setSkipConditions([...skipConditions, input]);
                    openPopup(respGET.data, varName);
                }
            } else {
                // if there is an error returned
                if (compiledError) {
                    setErr([...err, compiledError]);
                    setOutput([...output, input, compiledError]);
                    setSkipConditions([...skipConditions, input]);
                } else if (compiledResult) {
                    // if the output is multi-lined, split each line into its own element in an array to return it
                    if (compiledResult.includes('\n')) {
                        const strs = compiledResult.split('\n');
                        setOutput([...output, input, ...strs]);
                        setCompiledOutput([...compiledOutput, ...strs]);
                        setSkipConditions([...skipConditions, input]);
                    } else {
                        setOutput([...output, input, compiledResult]);
                        setCompiledOutput([...compiledOutput, compiledResult]);
                        setSkipConditions([...skipConditions, input]);
                    }
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
                        {output.map((line, index) => {
                            if (line.includes("https://")) {
                                // Extract the URL from the line
                                const urlRegex = /(https?:\/\/[^\s]+)/g;
                                const url = line.match(urlRegex)[0];

                                // Render the line as an <a> tag with the URL as href
                                return (
                                    <div key={index}>
                                        <a className='cursor' href={url.slice(0, url.length - 1)} target="_blank" rel="noopener noreferrer" style={{ textDecoration: 'underline' }}>{line}</a>
                                    </div>
                                );
                            } else if (compiledOutput.includes(line)) {
                                return (
                                    <div key={index}><p className='cursor'>{line}</p></div>
                                );
                            } else if (err.includes(line)) {
                                return (
                                    <div key={index}><p className='cursor' style={{ color: 'red' }}>{line}</p></div>
                                );
                            } else {
                                return (
                                    <div key={index}><p className='cursor'>&gt;&gt;&gt; {line}</p></div>
                                );
                            }
                        })}
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
            <input id='csvreader' type="file" accept=".csv" onChange={handleFileUpload} />
        </div>
    );
};

export default REPL;