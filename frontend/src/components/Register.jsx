import React from 'react';
import './styles.css';
import { Link } from 'react-router-dom';

// Register page, shows form for user to fill out. Info will be exported to SQL database.
function Register() {
    return(
        <div className='form-container'>
            <h2>Register</h2>
            <form action="/addToClients" method="post">
                <input type="text" placeholder="Username" required />
                <input type="password" placeholder="Password" required />
                <input type="text" placeholder="First Name" required />
                <input type="text" placeholder="Last Name" required />
                <input type="email" placeholder="Email" required />
                <input type="tel" placeholder="Phone Number" required />
                <input type="text" placeholder="Address" required />
                <input type="text" placeholder="City" required />
                <input type="text" placeholder="State" required />
                <input type="text" placeholder="Zip Code" required />
                <div className='button-group'>
                    <button type="submit" className='btn blue'>Register</button>
                    <Link to='/' className='btn blue'>Back</Link>
                </div>
            </form>
        </div>
    );
}

export default Register;
