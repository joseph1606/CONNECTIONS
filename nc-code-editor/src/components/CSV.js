import React, { useState } from 'react';

const CSV = () => {

    const [tableData, setTableData] = useState([]);

    const [format, setFormat] = useState(0);

    const read = () => {
        var fr = new FileReader();
        fr.onload = function () {
            let lines = fr.result.split('\r\n')
            lines.forEach(myFunction);

            function myFunction(value, index, array) {
                lines[index] = lines[index].split(',')
            }
            // console.log(lines)
            // checks if csv has 3 or 4 columns. if not, throw error
            // find out how to figure out length of formData

            /* relationship and relationship values are of different length */
            /* empty cell */
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
    }

    return (
        <div>
            <input id='csvreader' type="file" accept=".csv" onChange={read} />
            <h4 id='format' style={{ width: '20%', textAlign: 'center', marginLeft: '40%', fontSize: '20px' }}></h4>
            <table style={{ width: '80%', textAlign: 'center', marginLeft: '10%' }}>
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
                            } else {
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
    )
}

export default CSV

