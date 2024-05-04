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
    const [sessionId, setSessionId] = useState(null);
    const [countArrowKey, setCountArrowKey] = useState(0);
    const [uploadedFiles, setUploadedFiles] = useState([]);
    const [compiledOutput, setCompiledOutput] = useState([]);
    const [skipConditions, setSkipConditions] = useState([]);
    const [tableData, setTableData] = useState([]);
    const [format, setFormat] = useState(0);
    const [outputhtml, setOutputhtml] = useState("<p>Your output will appear here</p>");
    const [outputs, setOutputs] = useState({});
    const [files, setfiles] = useState({});
    const [windowSize, setWindowSize] = useState({
        width: window.innerWidth,
        height: window.innerHeight
    });
    var filecollapsed = false;
    var fileinput = false;


    const viewFile = (file) => {
        if (files[file['name']]) {
            setTableData([[], ...files[file['line']]['data']])
            setFormat(files[file['line']]['format'])
        }
        viewData()
    }

    const viewoldOutput = (name) => {
        console.log(outputs[name['item']].content)
        console.log(outputhtml == outputs[name['item']].content)
        if (outputs[name['item']]) {
            renderolddata(outputs[name['item']].content, '')
        }

        document.getElementById('outholder').scrollTop = '322';
        document.getElementById('outholder').scrollLeft = '100';
    }

    const filecollapse = () => {
        if (filecollapsed) {
            document.getElementById('codearea').style.width = '85vw'
            document.getElementById('inputbox').style.width = '15vw'
            document.getElementById('fileinputbox').style.visibility = 'visible';
            document.getElementById('fileinputbox').style.display = '';
            document.getElementById('filetoggle').textContent = '>';
            document.getElementById('filetogglebtn').style.marginLeft = '-18px';
            filecollapsed = false;
        } else {
            document.getElementById('codearea').style.width = '100vw'
            document.getElementById('inputbox').style.width = '0vw'
            document.getElementById('fileinputbox').style.visibility = 'collapse';
            document.getElementById('fileinputbox').style.display = 'none';
            document.getElementById('filetoggle').textContent = '<';
            document.getElementById('filetogglebtn').style.marginLeft = '-10px';
            filecollapsed = true;
        }
        console.log(filecollapsed)
    }
    const editor = () => {
        document.getElementById('terminal-loader').style.visibility = 'visible';
        document.getElementById('terminal-loader').style.display = '';
        document.getElementById('alloutput').style.visibility = 'collpase';
        document.getElementById('alloutput').style.display = 'none';
        document.getElementById('dataviewer').style.visibility = 'collpase';
        document.getElementById('dataviewer').style.display = 'none';
        document.getElementById('outputbtn').style.backgroundColor = '';
        document.getElementById('databtn').style.backgroundColor = '';
        document.getElementById('editorbtn').style.backgroundColor = 'darkgrey';
        document.getElementById('outputbtn').style.borderRadius = '';
        document.getElementById('databtn').style.borderRadius = '';
        document.getElementById('editorbtn').style.borderRadius = '5%';
    }
    const viewData = () => {
        document.getElementById('terminal-loader').style.visibility = 'collpase';
        document.getElementById('terminal-loader').style.display = 'none';
        document.getElementById('alloutput').style.visibility = 'collpase';
        document.getElementById('alloutput').style.display = 'none';
        document.getElementById('dataviewer').style.visibility = 'visible';
        document.getElementById('dataviewer').style.display = '';
        document.getElementById('outputbtn').style.backgroundColor = '';
        document.getElementById('editorbtn').style.backgroundColor = '';
        document.getElementById('databtn').style.backgroundColor = 'darkgrey';
        document.getElementById('outputbtn').style.borderRadius = '';
        document.getElementById('editorbtn').style.borderRadius = '';
        document.getElementById('databtn').style.borderRadius = '5%';
    }
    const viewOutput = () => {
        document.getElementById('terminal-loader').style.visibility = 'collpase';
        document.getElementById('terminal-loader').style.display = 'none';
        document.getElementById('dataviewer').style.visibility = 'collpase';
        document.getElementById('dataviewer').style.display = 'none';
        document.getElementById('alloutput').style.visibility = 'visible';
        document.getElementById('alloutput').style.display = '';
        document.getElementById('databtn').style.backgroundColor = '';
        document.getElementById('editorbtn').style.backgroundColor = '';
        document.getElementById('outputbtn').style.backgroundColor = 'darkgrey';
        document.getElementById('databtn').style.borderRadius = '';
        document.getElementById('editorbtn').style.borderRadius = '';
        document.getElementById('outputbtn').style.borderRadius = '5%';
    }

    const read = (fileName) => {
        var fr = new FileReader();
        fr.onload = function () {
            let lines = fr.result.split('\n')
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
                setfiles({ ...files, [fileName]: { format: 2, data: table } })
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
                setfiles({ ...files, [fileName]: { format: 1, data: table } })
                setTableData([[], ...table])
                setFormat(1)
            } else {
                //               document.getElementById('format').textContent = 'Incorrect Format';
                console.log(lines[0])
                console.log(lines[0].length)
                setTableData([[], []])
                setFormat(0)
            }
        }
        fr.readAsText(document.getElementById('csvreader').files[0]);

        document.getElementById('dataviewer').style.border = '1px solid black';
    }


    /* for creating a session id */

    useEffect(() => {
        // Make a request to the server to initiate a session
        axios.get('http://127.0.0.1:5000/initiate')
            .then(response => {
                // Retrieve the session ID from the response
                const sessionId = response.data.session_id;
                // Set the session ID in the state
                setSessionId(sessionId);
            })
            .catch(error => {
                console.error('Error initiating session:', error);
            });
    }, []); // Only run once on component mount

    // adds eventListener for resizing
    useEffect(() => {
        const handleResize = () => {
            setWindowSize({
                width: window.innerWidth,
                height: window.innerHeight
            });
        };

        window.addEventListener('resize', handleResize);
    }, []);

    /**/

    // Axios interceptor to add session ID to request headers

    axios.interceptors.request.use(config => {
        if (sessionId) {
            config.headers['session'] = sessionId;
        }
        return config;
    });

    /* for popup graph display window */

    const openPopup = async (htmlData, graphName) => {
        // adds a title of the graph name on the window

        const i = htmlData.indexOf("<head>");
        htmlData = htmlData.slice(0, i + 6) + `\n\t\t<title>Graph ${graphName}</title>` + htmlData.slice(i + 6);

        // Fetch script content using Axios
        const utilsScript = await axios.get('http://127.0.0.1:5000/scripts/bindings/utils.js');
        const tomSelectCSS = await axios.get('http://127.0.0.1:5000/scripts/tom-select/tom-select.css');
        const tomSelectScript = `<script 
                                    src="https://cdnjs.cloudflare.com/ajax/libs/tom-select/2.0.0-rc.4/js/tom-select.complete.min.js" 
                                    integrity="sha512-/ThRxlSqzRzFRVNByE+IzvT7iZTAtrAr5Xkk9As+xsDRYvsnPBQbYjG5z4vaJFNaWjBEnSRxICQw5t/mUmJ6Kw==" 
                                    crossorigin="anonymous" 
                                    referrerpolicy="no-referrer"></script>`;

        htmlData = htmlData.replace('<script src="lib/bindings/utils.js"></script>', `<script>${utilsScript.data}</script>`);
        htmlData = htmlData.replace('<link href="lib/tom-select/tom-select.css" rel="stylesheet">', `<style>${tomSelectCSS.data}</style>`);
        htmlData = htmlData.replace('<script src="lib/tom-select/tom-select.complete.min.js"></script>', `${tomSelectScript}`);

        viewOutput();

        const htmlContent = `
        <!DOCTYPE html>
        ${htmlData}`;
        setOutputhtml(htmlContent);
        setOutputs({ ...outputs, [graphName]: { content: htmlContent } });
        document.getElementById('outholder').scrollTop = '322';
        document.getElementById('outholder').scrollLeft = '100';

    };

    const renderolddata = async (htmlData, graphName) => {
        // adds a title of the graph name on the window

        const i = htmlData.indexOf("<head>");
        htmlData = htmlData.slice(0, i + 6) + `\n\t\t<title>Graph ${graphName}</title>` + htmlData.slice(i + 6);

        // Fetch script content using Axios
        const utilsScript = await axios.get('http://127.0.0.1:5000/scripts/bindings/utils.js');
        const tomSelectCSS = await axios.get('http://127.0.0.1:5000/scripts/tom-select/tom-select.css');
        const tomSelectScript = `<script 
                                    src="https://cdnjs.cloudflare.com/ajax/libs/tom-select/2.0.0-rc.4/js/tom-select.complete.min.js" 
                                    integrity="sha512-/ThRxlSqzRzFRVNByE+IzvT7iZTAtrAr5Xkk9As+xsDRYvsnPBQbYjG5z4vaJFNaWjBEnSRxICQw5t/mUmJ6Kw==" 
                                    crossorigin="anonymous" 
                                    referrerpolicy="no-referrer"></script>`;

        htmlData = htmlData.replace('<script src="lib/bindings/utils.js"></script>', `<script>${utilsScript.data}</script>`);
        htmlData = htmlData.replace('<link href="lib/tom-select/tom-select.css" rel="stylesheet">', `<style>${tomSelectCSS.data}</style>`);
        htmlData = htmlData.replace('<script src="lib/tom-select/tom-select.complete.min.js"></script>', `${tomSelectScript}`);

        viewOutput();

        const htmlContent = `
        <!DOCTYPE html>
        ${htmlData}`;
        setOutputhtml(htmlContent);
        document.getElementById('outholder').scrollTop = '322';
        document.getElementById('outholder').scrollLeft = '100';

    };

    /**/

    /* for up arrow key functionality */

    useEffect(() => {
        function handleKeyDown(event) {
            if ((event.key === 'ArrowUp') && (countArrowKey < prevInputs.length - 1)) {
                setInput(prevInputs[prevInputs.length - countArrowKey - 1].trim());
                setCountArrowKey(countArrowKey + 1);
            } else if ((event.key === 'ArrowUp') && (countArrowKey === prevInputs.length - 1)) {
                setInput(prevInputs[0].trim());
            } else if ((event.key === 'ArrowDown') && (countArrowKey === 0)) {
                setInput('');
            } else if (event.key === 'ArrowDown') {
                setInput(prevInputs[prevInputs.length - countArrowKey].trim());
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
        formData.set('file', file);
        formData.set('csvName', file.name);
        try {
            const response = await axios.post('http://127.0.0.1:5000/upload', formData);
            if (response.data.error) {
                const compiledError = response.data.error;
                window.alert(`Your csv has an error: ${compiledError}. You may reupload the csv after error has been addressed.`);
            } else {
                console.log('File sent successfully:', response.data);
                const lastIndex = file.name.lastIndexOf('.');
                const base = file.name.substring(0, lastIndex);
                const ext = file.name.substring(lastIndex + 1);
                let fileName = file.name.toLowerCase();
                let counter = 1;
                while (uploadedFiles.includes(fileName)) {
                    fileName = `${base} (${counter}).${ext}`;
                    counter += 1
                }
                setUploadedFiles([...uploadedFiles, fileName]);
                read(fileName);
                if (!fileinput) {
                    document.getElementById('blankinput').style.visibility = 'collpase';
                    document.getElementById('blankinput').style.display = 'none';
                    fileinput = true;
                }
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
                // replaces weird curvy quotations with normal
                if (/[“”]/.test(input)) {
                    // Replace curved double quotes with straight double quotes
                    let str = input.replace(/[\u201C\u201D]/g, '"');
                    setPrevInputs([...prevInputs, `${str}`]);
                } else if (/[‘’]/.test(input)) {
                    // Replace curved single quotes with straight single quotes
                    let str = input.replace(/[\u2018\u2019]/g, "'");
                    setPrevInputs([...prevInputs, `${str}`]);
                } else {
                    setPrevInputs([...prevInputs, `${input}`]);
                }
            }
        }
        // if multiLine is enabled
        if (multiLine) {
            // if the input is closing the block code, run the code that was just entered
            if (input.trim() === ":}") {
                setMultiLine(false);
                setSkipConditions([...skipConditions, input]);
                setInFunc(0);

                const payload = { "height": windowSize.height, "width": windowSize.width };
                // checks if previous code has generated an output and comments it out in the payload if so
                if (skipConditions) {
                    const inputCopy = deepCopyStateArray(prevInputs);
                    for (let i = 0; i < skipConditions.length; i++) {
                        const skipMe = skipConditions[i];
                        if (inputCopy.includes(skipMe)) {
                            // Count the number of tabs at the beginning of the string
                            let tabCount = (skipMe.match(/^\t*/)[0] || "").length;
                            inputCopy[inputCopy.indexOf(skipMe)] = "\t".repeat(tabCount) + `pass`;
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
                                    for (const line of blockCode) {
                                        if (line.includes("print")) {
                                            setSkipConditions([...skipConditions, line]);
                                        }
                                    }
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
            if (input.trim() === ":{") {
                setMultiLine(true);
                setSkipConditions([...skipConditions, input]);
                setBlockCode([]);
            } else if (input === 'clear') {
                setSkipConditions([...skipConditions, input]);
                setOutput([]);
            } else {

                // replaces weird curvy quotations with normal
                let str = "";
                if (/[“”]/.test(input)) {
                    // Replace curved double quotes with straight double quotes
                    str = input.replace(/[\u201C\u201D]/g, '"');
                } else if (/[‘’]/.test(input)) {
                    // Replace curved single quotes with straight single quotes
                    str = input.replace(/[\u2018\u2019]/g, "'");
                } else {
                    str = input;
                }

                const payload = { "height": windowSize.height, "width": windowSize.width };

                // checks if previous code has generated an output and comments it out in the payload if so
                if (skipConditions) {
                    const inputCopy = deepCopyStateArray(prevInputs);
                    for (let i = 0; i < skipConditions.length; i++) {
                        const skipMe = skipConditions[i];
                        if (inputCopy.includes(skipMe)) {
                            // Count the number of tabs at the beginning of the string
                            let tabCount = (skipMe.match(/^\t*/)[0] || "").length;
                            inputCopy[inputCopy.indexOf(skipMe)] = "\t".repeat(tabCount) + `pass`;
                        }
                    }

                    payload['code'] = inputCopy.join('\n') + '\n' + str;
                } else {
                    payload['code'] = prevInputs.join('\n') + '\n' + str;
                }
                /* contacting API for code compilation */
                //console.log(payload);
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
            <div id='codearea' style={{ width: '85vw', height: '92.5vh', zIndex: 0, padding: '10px' }}>
                <div id="flexbox">
                    <div id='tabselect' style={{
                        marginLeft: '35px'
                    }}>
                        <button id='editorbtn' onClick={editor} style={{ backgroundColor: 'darkgray', borderRadius: '5%' }}>Editor</button>
                        <button id='databtn' onClick={viewData}>View File Data</button>
                        <button id='outputbtn' onClick={viewOutput} >Output</button>
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
                    <div>
                        <table id='dataviewer' style={{ width: '80%', textAlign: 'center', marginLeft: '10%', overflowY: 'scroll', marginTop: '1vh', maxHeight: '80vh', display: 'none', visibility: 'collapse' }}>
                            <p id='blankinput' style={{ margin: 'auto', fontSize: '30px' }}>Files you input will appear here</p>
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
                    <div id='alloutput'>
                        <div id='outputlist' style={{ height: '60px', borderTop: '2px solid black', borderLeft: '2px solid black', borderRight: '2px solid black', width: '90%', paddingLeft: '5px' }}>
                            <h2>View Outputs: </h2>
                            {Object.keys(outputs).map((item, index) => (
                                <button style={{ height: '25px', marginLeft: '5px' }} onClick={() => { viewoldOutput({ item }) }}>{item}</button>
                            ))}</div>
                        <div id='outholder' style={{ position: 'relative', width: '90%', height: '87%', overflow: 'hidden', overflowX: 'hidden', border: '2px solid black' }}>
                            <iframe id='outputviewer' style={{ position: 'relative', width: `${windowSize.width - 460}px`, height: `${windowSize.height - 220}px`, overflowX: 'hidden' }} srcDoc={outputhtml} title="my-iframe">
                            </iframe>
                        </div>
                    </div>
                </div>
            </div>
            <div id='inputbox' style={{ width: '15vw', height: '92.5vh', padding: '10px' }}>
                <div id='filetogglebtn' onClick={filecollapse} style={{ position: 'absolute', zIndex: 2, marginLeft: '-18px', width: '20px', height: '50px', marginTop: '5vh', backgroundColor: 'white', border: '2px solid grey' }}>
                    <p id='filetoggle' style={{ position: 'relative', margin: 'auto', height: '25px', marginTop: '12.5px', width: '50%', marginLeft: '5px' }}>&gt;</p>
                </div>
                <div id='fileinputbox' style={{ position: 'relative', width: '100%', zIndex: 2, height: '100%', padding: '10px', backgroundColor: 'white', borderRadius: '15px', padding: '5%', border: '2px solid grey' }}>
                    <h2>File Input:</h2>
                    <input id='csvreader' type="file" accept=".csv" onChange={handleFileUpload} />
                    <br />
                    <br />
                    <h4>Files (click to view):</h4>
                    {uploadedFiles.map((line, index) => (
                        <div id={index} key={index}><p className='file' onClick={() => viewFile({ line })}>{line}</p></div>
                    ))}
                </div>
            </div>
        </div >
    );
};

export default REPL;