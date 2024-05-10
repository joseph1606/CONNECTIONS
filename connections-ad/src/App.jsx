import React from 'react'
import './App.css'
import Home from './Home.jsx'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'

function App() {
  return (
    <Router>
      <Routes>
        <Route path='/' exact element={<Home />} />
      </Routes>
    </Router>
  )
}


export default App
