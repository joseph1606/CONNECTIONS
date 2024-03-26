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
        if (lines[0].length == 3) {
            document.getElementById('format').textContent = 'Format 2 Selected: Person1(string),Relationship(s),(comma delimited strings),Relationship Value(s) (comma separated strings)';
            document.getElementById('header').textContent = lines[0];
            document.getElementById('output').textContent = lines[1];
        } else if (lines[0].length == 4) {
            document.getElementById('format').textContent = 'Format 1 Selected: Person1(string),Person2(string),Relationship(s),(comma delimited strings),Relationship Value(s) (comma separated strings) ';
            document.getElementById('header').textContent = lines[0];
            document.getElementById('output').textContent = lines[1];
        } else {
            document.getElementById('format').textContent = 'Incorrect Format';
            document.getElementById('header').textContent = '';
            document.getElementById('output').textContent = '';
        }

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
            <h4 id='format'></h4>
            <h6 id='header'>Header</h6>
            <p id='output'>Output</p>
        </div>
    )
}

export default CSV

