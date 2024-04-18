import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './REPL.css'

const REPL = () => {
    const [err, setErr] = useState([]);
    const [input, setInput] = useState('');
    const [output, setOutput] = useState([]);
    const [inFunc, setInFunc] = useState(0);
    const [blockCode, setBlockCode] = useState([]);
    const [prevInputs, setPrevInputs] = useState([]);
    const [multiLine, setMultiLine] = useState(false);
    const [countArrowKey, setCountArrowKey] = useState(0);
    const [uploadedFiles, setUploadedFiles] = useState([]);
    const [compiledOutput, setCompiledOutput] = useState([]);
    const [skipConditions, setSkipConditions] = useState([]);
    const [tableData, setTableData] = useState([]);
    const [format, setFormat] = useState(0);

    const editor = () => {
        document.getElementById('terminal-loader').style.visibility = 'visible';
        document.getElementById('terminal-loader').style.display = '';
        document.getElementById('terminal-loader').style.visibility = 'visible';
        document.getElementById('terminal-loader').style.display = '';
    }
    const viewData = () => {
        console.log(document.getElementById('terminal-loader').style.display)
        document.getElementById('terminal-loader').style.visibility = 'collpase';
        document.getElementById('terminal-loader').style.display = 'none';

    }

    const read = () => {
        var fr = new FileReader();
        fr.onload = function () {
            let lines = fr.result.split('\r\n')
            lines.forEach(myFunction);

            function myFunction(value, index, array) {
                lines[index] = lines[index].split(',')
            }
            // console.log(lines)
            if (lines[0].length == 3) {
                const table = []

                for (let i = 1; i < lines.length; i++) {
                    table.push({
                        persona: lines[i][0],
                        relat: lines[i][1],
                        relatv: lines[i][2],
                    });
                }

                setTableData([[], ...table])
                setFormat(2)

            } else if (lines[0].length == 4) {

                const table = []

                for (let i = 1; i < lines.length; i++) {
                    table.push({
                        persona: lines[i][0],
                        personb: lines[i][1],
                        relat: lines[i][2],
                        relatv: lines[i][3],
                    });
                }

                setTableData([[], ...table])
                setFormat(1)
            } else {
                document.getElementById('format').textContent = 'Incorrect Format';
                setTableData([[], []])
                setFormat(0)
            }
        }
        fr.readAsText(document.getElementById('csvreader').files[0]);

        document.getElementById('dataviewer').style.border = '1px solid black';
    }


    /* for popup graph display window */

    const openPopup = (htmlData, graphName) => {
        // opens a new window
        const newWindow = window.open('', '_blank', 'width=1000,height=1000');
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
        read();

        try {
            const response = await axios.post('http://127.0.0.1:5000/upload', formData);
            if (response.data.error) {
                const compiledError = response.data.error;
                window.alert(`Your csv has an error: ${compiledError}. You may reupload the csv after error has been addressed.`);
            } else {
                console.log('File sent successfully:', response.data);
                setUploadedFiles([...uploadedFiles, file.name]);
            }
        } catch (error) {
            console.error('Error uploading file:', error);
        }
        document.getElementById('csvreader').value = '';
    }

    /**/

    /* functionality for tabbing behavior in input tag */

    const handleKeyDown = (e) => {
        if (e.key === 'Tab') {
            e.preventDefault(); // prevent default tab behavior

            // Get cursor position
            const start = e.target.selectionStart;
            const end = e.target.selectionEnd;

            // Insert tab character at cursor position
            const newValue = input.substring(0, start) + '\t' + input.substring(end);

            // Update input value and cursor position
            setInput(newValue);
            e.target.selectionStart = e.target.selectionEnd = start + 1;
        }
        if (inFunc > 0 && /^\s*$/.test(input) && e.key === 'Backspace') {
            setInFunc(inFunc - 1);
        }
    };

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
        // if the input is a string and is not the block code toggler, add it to prevInputs
        if ((input)) {
            if ((input.trim() !== ":{") && (input.trim() !== ":}")) {
                setPrevInputs([...prevInputs, `${input.trim()}`]);
            }
        }
        // if multiLine is enabled
        if (multiLine) {
            // if the input is closing the block code, run the code that was just entered
            if (input.trim() === ":}") {
                setMultiLine(false);
                setSkipConditions([...skipConditions, input]);
                setInFunc(0);

                const payload = {};
                // checks if previous code has generated an output and comments it out in the payload if so
                if (skipConditions) {
                    const inputCopy = deepCopyStateArray(prevInputs);
                    for (let i = 0; i < skipConditions.length; i++) {
                        const skipMe = skipConditions[i];
                        if (inputCopy.includes(skipMe)) {
                            inputCopy[inputCopy.indexOf(skipMe)] = `#${skipMe}`;
                        }
                    }
                    payload['code'] = inputCopy.join('\n') + '\n';
                } else {
                    payload['code'] = prevInputs.join('\n') + '\n';
                }
                /* contacting API for code compilation */
                try {
                    const resp = await axios.post('http://127.0.0.1:5000/compile', payload);
                    const compiledError = resp.data.error;
                    const compiledResult = resp.data.output;
                    const functionNameStart = input.indexOf("(");

                    for (const prev of prevInputs) {
                        if (prev.includes("print")) {
                            setSkipConditions([...skipConditions, prev]);
                        }
                    }
                    // if there is an error returned
                    if (compiledError) {
                        setErr([...err, compiledError]);
                        setOutput([...output, input, compiledError]);
                        setSkipConditions([...skipConditions, ...blockCode, input]);
                    } else if (compiledResult) {
                        // if the output is multi-lined, split each line into its own element in an array to return it
                        if (compiledResult.includes('\n')) {
                            const keepThese = []
                            const strs = compiledResult.split('\n');
                            // checks if any outputs end in .html or .csv to determine if the Vis or Save functionality needs to run
                            for (const str of strs) {
                                if (/.html$/.test(str)) {
                                    const varName = str.replace(/\.html$/, '');
                                    const respGET = await axios.get('http://127.0.0.1:5000/get_graph?varName=' + varName);
                                    // if there is an error
                                    if (respGET.data.error) {
                                        setErr([...err, compiledError]);
                                        setOutput([...output, input, compiledError]);
                                        setSkipConditions([...skipConditions, input]);
                                        // if not, open graph popup window
                                    } else {
                                        setSkipConditions([...skipConditions, input]);
                                        openPopup(respGET.data, varName);
                                    }
                                } else if (/.csv$/.test(str)) {
                                    // if there is an error
                                    if (compiledError) {
                                        setErr([...err, compiledError]);
                                        setOutput([...output, input, compiledError]);
                                        setSkipConditions([...skipConditions, input]);
                                        // if not, download csv file
                                    } else {
                                        const varName = input.substring(functionNameStart + 1, input.length - 1);
                                        const respGET = await axios.get('http://127.0.0.1:5000/save_graph?varName=' + varName, {
                                            responseType: 'blob', // Set the response type to blob
                                        });
                                        // Create a URL for the Blob object
                                        const url = window.URL.createObjectURL(new Blob([respGET.data]));

                                        // Create a temporary <a> element and set its attributes
                                        const a = document.createElement('a');
                                        a.href = url;
                                        a.download = varName + '.csv'; // Specify the filename to download
                                        a.style.display = 'none';

                                        // Append the <a> element to the document body
                                        document.body.appendChild(a);

                                        // Trigger the click event to start the download
                                        a.click();

                                        // Clean up by removing the <a> element and revoking the URL
                                        document.body.removeChild(a);
                                        window.URL.revokeObjectURL(url);

                                        setSkipConditions([...skipConditions, input]);
                                    }
                                } else {
                                    // removes the .html or .csv from being added to compiledOutput
                                    keepThese.push(str)
                                }
                            }
                            setOutput([...output, input, ...keepThese]);
                            setCompiledOutput([...compiledOutput, ...keepThese]);
                        } else {
                            setOutput([...output, input, compiledResult]);
                            setCompiledOutput([...compiledOutput, compiledResult]);
                        }
                    }
                } catch (error) {
                    console.error('Error: ', error);
                }
            } else {
                setBlockCode([...blockCode, input]);
            }
        } else {
            if (input === ":{") {
                setMultiLine(true);
                setSkipConditions([...skipConditions, input]);
                setBlockCode([]);
            } else if (input === 'clear') {
                setSkipConditions([...skipConditions, input]);
                setOutput([]);
            } else {
                const payload = {};
                // checks if previous code has generated an output and comments it out in the payload if so
                if (skipConditions) {
                    const inputCopy = deepCopyStateArray(prevInputs);
                    for (let i = 0; i < skipConditions.length; i++) {
                        const skipMe = skipConditions[i];
                        if (inputCopy.includes(skipMe)) {
                            inputCopy[inputCopy.indexOf(skipMe)] = `#${skipMe}`;
                        }
                    }
                    payload['code'] = inputCopy.join('\n') + '\n' + input;
                } else {
                    payload['code'] = prevInputs.join('\n') + '\n' + input;
                }
                /* contacting API for code compilation */
                console.log(payload);
                try {
                    const resp = await axios.post('http://127.0.0.1:5000/compile', payload);
                    const compiledError = resp.data.error;
                    const compiledResult = resp.data.output;
                    const functionNameStart = input.indexOf("(");

                    // if there is an error returned
                    if (compiledError) {
                        setErr([...err, compiledError]);
                        setOutput([...output, input, compiledError]);
                        setSkipConditions([...skipConditions, input]);
                        // if a output is returned
                    } else if (compiledResult) {
                        // if the output is multi-lined, split each line into its own element in an array to return it
                        if (compiledResult.includes('\n')) {
                            const strs = compiledResult.split('\n');
                            const keepThese = []
                            // checks if any outputs end in .html or .csv to determine if the Vis or Save functionality needs to run
                            for (const str of strs) {
                                if (/.html$/.test(str)) {
                                    const varName = str.replace(/\.html$/, '');
                                    const respGET = await axios.get('http://127.0.0.1:5000/get_graph?varName=' + varName);
                                    // if there is an error
                                    if (respGET.data.error) {
                                        setErr([...err, compiledError]);
                                        setOutput([...output, input, compiledError]);
                                        setSkipConditions([...skipConditions, input]);
                                        // if not, open graph popup window
                                    } else {
                                        setSkipConditions([...skipConditions, input]);
                                        openPopup(respGET.data, varName);
                                    }
                                } else if (/.csv$/.test(str)) {
                                    // if there is an error
                                    if (compiledError) {
                                        setErr([...err, compiledError]);
                                        setOutput([...output, input, compiledError]);
                                        setSkipConditions([...skipConditions, input]);
                                        // if not, download csv file
                                    } else {
                                        const varName = input.substring(functionNameStart + 1, input.length - 1);
                                        const respGET = await axios.get('http://127.0.0.1:5000/save_graph?varName=' + varName, {
                                            responseType: 'blob', // Set the response type to blob
                                        });
                                        // Create a URL for the Blob object
                                        const url = window.URL.createObjectURL(new Blob([respGET.data]));

                                        // Create a temporary <a> element and set its attributes
                                        const a = document.createElement('a');
                                        a.href = url;
                                        a.download = varName + '.csv'; // Specify the filename to download
                                        a.style.display = 'none';

                                        // Append the <a> element to the document body
                                        document.body.appendChild(a);

                                        // Trigger the click event to start the download
                                        a.click();

                                        // Clean up by removing the <a> element and revoking the URL
                                        document.body.removeChild(a);
                                        window.URL.revokeObjectURL(url);

                                        setSkipConditions([...skipConditions, input]);
                                    }
                                } else {
                                    // removes the .html or .csv from being added to compiledOutput
                                    keepThese.push(str)
                                }
                            }
                            setOutput([...output, input, ...keepThese]);
                            setCompiledOutput([...compiledOutput, ...keepThese]);
                            setSkipConditions([...skipConditions, input]);
                        } else {
                            setOutput([...output, input, compiledResult]);
                            setCompiledOutput([...compiledOutput, compiledResult]);
                            setSkipConditions([...skipConditions, input]);
                        }
                    }

                } catch (error) {
                    console.error('Error: ', error);
                }
            }
        }
        if (multiLine) {
            if (input[input.length - 1] === ":") {
                setInFunc(inFunc + 1);
                setInput('\t'.repeat(inFunc + 1) + '');
            } else if ((inFunc > 0) && (input.trim() !== ":}")) {
                setInput('\t'.repeat(inFunc) + '');
            } else {
                setInput('');
            }
        } else {
            setInput('');
        }
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
                    {uploadedFiles.map((line, index) => (
                        <div id={index} key={index}><p>{line}</p></div>
                    ))}
                </div>
            </div>
            <div id='codearea' style={{ width: '80vw', height: '92.5vh', zIndex: 0, padding: '10px' }}>
                <div id="flexbox">
                    <div id='tabselect' style={{
                        marginLeft: '35px'
                    }}>
                        <button onClick={editor}>Editor</button>
                        <button onClick={viewData}>View File Data</button>
                    </div>
                    <div id="terminal-loader">
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
                                            <a className='cursor' href={url.slice(0, url.length - 1)} target="_blank" rel="noopener noreferrer" style={{ textDecoration: 'underline', color: 'green' }}>{line}</a>
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
                                } else if (line.includes('\t')) {
                                    return (
                                        <div key={index}><p className='cursor'>&gt;&gt;&gt; {line.replace(/\t/g, '\u00a0\u00a0\u00a0\u00a0')}</p></div>
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
                                    onKeyDown={handleKeyDown}
                                    width="80"
                                    placeholder="Enter Python code here..."
                                />
                            </form>
                        </div>
                    </div>
                    <table id='dataviewer' style={{ width: '80%', textAlign: 'center', marginLeft: '10%', overflowY: 'scroll', marginTop: '1vh', maxHeight: '80vh' }}>
                        <thead>
                            {(() => {
                                if (format == 1) {
                                    return (
                                        <tr>
                                            <th>Person 1</th>
                                            <th>Person 2</th>
                                            <th>Relationship</th>
                                            <th>Relationship Value</th>
                                        </tr>
                                    );
                                } else if (format == 2) {
                                    return (
                                        <tr>
                                            <th>Person</th>
                                            <th>Relationship</th>
                                            <th>Relationship Value</th>
                                        </tr>
                                    );
                                } else {
                                    return null; // or return an appropriate default header
                                }
                            })()}
                        </thead>
                        <tbody>
                            {
                                tableData.map((obj) => {
                                    if (Object.keys(obj).length == 4) {
                                        return (
                                            <tr >
                                                <td style={{ border: ' 1px solid black' }}>{obj.persona}</td>
                                                <td style={{ border: ' 1px solid black' }}>{obj.personb}</td>
                                                <td style={{ border: ' 1px solid black' }}>{obj.relat}</td>
                                                <td style={{ border: ' 1px solid black' }}>{obj.relatv}</td>
                                            </tr>
                                        );
                                    } else if (Object.keys(obj).length == 3) {
                                        return (
                                            <tr>
                                                <td style={{ border: ' 1px solid black' }}>{obj.persona}</td>
                                                <td style={{ border: ' 1px solid black' }}>{obj.relat}</td>
                                                <td style={{ border: ' 1px solid black' }}>{obj.relatv}</td>
                                            </tr>
                                        );
                                    }
                                })
                            }
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
};

export default REPL;