import React from 'react'
import { Link } from 'react-router-dom'
import Mtn from './download.png'
import './Navbar.css'

function Navbar() {
    return (
        <>
            <div id='bar'>
                <Link to='/' id='homelink'><div id='logoside'><img src={Mtn} alt='logo' /><h2 id='heading'>Connections</h2></div></Link>

            </div>
        </>
    )
}

export default Navbar
