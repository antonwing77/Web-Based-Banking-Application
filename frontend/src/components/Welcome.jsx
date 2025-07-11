import React from 'react';
import { Link } from 'react-router-dom';
import './styles.css';
import logo from '../assets/logo.png';

// Welcome Page, first thing user is greeted with, contains links to login or register pages
function Welcome() {
    return (
        <div className="center-container">
            <img src={logo} alt="logo"></img>
            <h1>Welcome to Serpent Savings</h1>
            <div className="button-group">
                <Link to="/login" className="btn blue">Login</Link>
                <Link to="/register" className="btn blue">Register</Link>
            </div>
        </div>
    );
}

export default Welcome;
