import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './REPL.css'

const REPL = () => {
    const [iframeUrl, setIframeUrl] = useState('');
    const [err, setErr] = useState([]);
    const [input, setInput] = useState('');
    const [output, setOutput] = useState([]);
    const [countArrowKey, setCountArrowKey] = useState(0);
    const [compiledOutput, setCompiledOutput] = useState([]);
    const [skipConditions, setSkipConditions] = useState([]);

    /* for up arrow key functionality */

    useEffect(() => {
        function handleKeyDown(event) {
            if ((event.key === 'ArrowUp') && (countArrowKey <= output.length - 1)) {
                setInput(String(output[output.length - 1 - countArrowKey]));
                setCountArrowKey(countArrowKey + 1);
            } else if ((event.key === 'ArrowDown') && (countArrowKey === 0)) {
                setInput('');
            } else if (event.key === 'ArrowDown') {
                setInput(output[output.length - countArrowKey]);
                setCountArrowKey(countArrowKey - 1);
            }
        }

        document.addEventListener('keydown', handleKeyDown);

        return () => {
            document.removeEventListener('keydown', handleKeyDown);
        };
    }, [output, countArrowKey]);

    /**/

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
                    return line;
                }
            });
            payload['code'] = updatedOutput.join('\n') + '\n' + input;
        } else {
            payload['code'] = output.join('\n') + '\n' + input;
        }
        console.log(payload);
        /* contacting API for code compilation */
        try {
            const resp = await axios.post('http://127.0.0.1:5000/compile', payload);
            const compiledError = resp.data.error;
            const compiledResult = resp.data.output;
            if (input === "displayGraph(g)") {
                setIframeUrl('http://127.0.0.1:5000/get_graph');
                setSkipConditions([...skipConditions, input]);
                /*const graphResp = await axios.get('http://127.0.0.1:5000/get_graph');
                const graphHtmlContent = graphResp.data.htmlContent;
                setHtmlContent(graphHtmlContent);
                const sanitizedHtml = DOMPurify.sanitize(compiledResult);
                setHtmlContent(sanitizedHtml);*/
            }/* else if (error) {
                setOutput([...output, input, err]);
                setSkipConditions([...skipConditions, input]);
                setErr([...err, error]);
            }*/ else {
                /* factor in returning errors in the output instead of just output */
                /*
                if (compiledResult && !error) {
                    setOutput([...output, input, compiledResult]);
                    setCompiledOutput([...compiledOutput, compiledResult]);
                    setSkipConditions([...skipConditions, input]);
                } else {
                    setOutput([...output, input, error]);
                    setErr([...err, error]);
                    setSkipConditions([...skipConditions, input, error]);
                }
                */
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
            <div id='repl'>
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
            {iframeUrl && (<iframe src={iframeUrl} title="HTML Content" width="100%" height="500px" />)}
        </div>
    );
};

export default REPL;