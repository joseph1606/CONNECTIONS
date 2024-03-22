import React, { useState } from 'react';

function read() {
    var fr = new FileReader();
    fr.onload = function () {
        let lines = fr.result.split('\r\n')
        lines.forEach(myFunction);

        function myFunction(value, index, array) {
            lines[index] = lines[index].split(',')
        }
        console.log(lines)
        document.getElementById('header').textContent = lines[0];
        document.getElementById('output').textContent = lines[1];
    }
    /*
    payload['code'] = "graphwithcsv1(csv)"
    payload['code'] = "graphwithcsv2(csv)"
    */
    fr.readAsText(document.getElementById('csvreader').files[0]);
}


const CSV = () => {
    return (
        <div>
            <input id='csvreader' type="file" accept=".csv" onChange={read} />
            <h2 id='header'>Header</h2>
            <p id='output'>Output</p>
        </div>
    )
}

export default CSV  