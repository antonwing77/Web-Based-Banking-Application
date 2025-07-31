import React, { useState } from 'react';
import './styles.css'
import { useNavigate, Link } from 'react-router-dom';

function validatePassword(password) {
    // At least 8 chars, one uppercase, one digit
    return /^(?=.*[A-Z])(?=.*\d).{8,}$/.test(password);
}

function Login(){
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [attempts, setAttempts] = useState(0);
    const maxAttempts = 5;
    const [lockedOut, setLockedOut] = useState(false);
    const navigate = useNavigate();

    const handleSubmit = async(e) => {
        e.preventDefault();
        setError('');
        if (lockedOut || attempts >= maxAttempts) {
            setError('Too many failed attempts. Please try again later.');
            return;
        }
        if (!validatePassword(password)) {
            setError('Password must be at least 8 characters, include one uppercase letter and one number.');
            return;
        }
        try {
            const response = await fetch('http://localhost:8000/api/login/', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                credentials: 'include',
                body: JSON.stringify({username, password})
            });
            const data = await response.json();
            if (response.ok) {
                setAttempts(0);
                if (data.role === 'Client') navigate('/dashboard');
                else if (data.role === 'Teller') navigate('/tellerview');
                else setError('Unknown User Type');
            } else {
                setAttempts(prev => prev + 1);
                setError(data.detail || "Invalid Username/Password");
                if (data.detail && data.detail.includes('locked')) {
                    setLockedOut(true);
                }
            }
        } catch(err) {
            setError("Server error.")
        }
    };

    return (
        <div className="form-container">
            <h2>Login</h2>
            <form onSubmit={handleSubmit}>
                <input type="text" placeholder='Username' value={username}
                    onChange={(e) => setUsername(e.target.value)} required />
                <input type="password" placeholder='Password' value={password}
                    onChange={(e) => setPassword(e.target.value)} required />
                {error && <p className='error'>{error}</p>}
                <p>Attempts: {attempts} / {maxAttempts}</p>
                <div className='button-group'>
                    <button type="submit" className='btn blue' disabled={lockedOut || attempts >= maxAttempts}>Sign In</button>
                    <Link to='/' className='btn blue'>Back</Link>
                </div>
            </form>
            <div>
                <small>Password must be at least 8 characters, include one uppercase letter and one number.</small>
            </div>
        </div>
    );
}

export default Login;