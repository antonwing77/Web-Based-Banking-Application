import React, { useState } from 'react';
import './styles.css'
import { useNavigate, Link } from 'react-router-dom';

// Login page, user will be redirected to client view or teller view depending on role
// Page will throw error if incorrect entry

function Login(){
    // Holds user entry, will be sent for authentication after user input
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate('');

    const handleSubmit = async(e) => {
        e.preventDefault();
        setError(''); // makes sure error is empty

        try {
            const response = await fetch('http://localhost:8000/api/login/', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                credentials: 'include',
                body: JSON.stringify({username, password})
            });
        if (response.ok) {
            const data = await response.json();
            if (data.role === 'Client') {
                navigate('/dashboard');
                }
            else if (data.role == 'Teller') {
                navigate('/tellerview');
                }
            else {
                setError("Unknown User Type")
                }
            } else {
                const data = await response.json();
                setError(data.detail || "Invalid Username/Password")
        }

        } catch(err) {
            setError("Server error.")
        }
     
    };

// Login page display and form 
    return (
        <div className="form-container">
            <h2>Login</h2>
            <form onSubmit={handleSubmit}>
                <input type="text" placeholder='Username' value={username} 
                onChange={(e) => setUsername(e.target.value)} required></input>
                <input type="password" placeholder='Password' value={password}
                onChange={(e) => setPassword(e.target.value)} required></input>
                {error && <p className='error'>{error}</p>}
                <div className='button-group'>
                    <button type="submit" className='btn blue'>Sign In</button>
                    <Link to='/' className='btn blue'>Back</Link>
                </div>
            </form>
        </div>
    );
}

export default Login;
