import React, { useState } from 'react';
import './styles.css';
import { Link } from 'react-router-dom';

function validatePassword(password) {
    // At least 8 chars, one uppercase, one digit
    return /^(?=.*[A-Z])(?=.*\d).{8,}$/.test(password);
}

function Register() {
    const [form, setForm] = useState({
        username: '',
        password: '',
        firstName: '',
        lastName: '',
        email: '',
        phone: '',
        address: '',
        city: '',
        state: '',
        zip: ''
    });
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');

    const handleChange = (e) => {
        setForm({ ...form, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setSuccess('');
        if (!validatePassword(form.password)) {
            setError('Password must be at least 8 characters, include one uppercase letter and one number.');
            return;
        }

        // Submit to backend (adjust URL as needed)
        try {
            const response = await fetch('http://localhost:8000/api/users/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    username: form.username,
                    password: form.password,
                    first_name: form.firstName,
                    last_name: form.lastName,
                    email: form.email,
                    phone: form.phone,
                    address: form.address,
                    city: form.city,
                    state: form.state,
                    zip_code: form.zip,
                }),
            });
            const data = await response.json();
            if (response.ok) {
                setSuccess('Registration successful! You may now log in.');
                setForm({
                    username: '',
                    password: '',
                    firstName: '',
                    lastName: '',
                    email: '',
                    phone: '',
                    address: '',
                    city: '',
                    state: '',
                    zip: ''
                });
            } else {
                setError(data.detail || 'Registration failed.');
            }
        } catch (err) {
            setError('Server error.');
        }
    };

    return (
        <div className='form-container'>
            <h2>Register</h2>
            <form onSubmit={handleSubmit} autoComplete="off">
                <input type="text" name="username" placeholder="Username" value={form.username} onChange={handleChange} required />
                <input type="password" name="password" placeholder="Password" value={form.password} onChange={handleChange} required />
                <input type="text" name="firstName" placeholder="First Name" value={form.firstName} onChange={handleChange} required />
                <input type="text" name="lastName" placeholder="Last Name" value={form.lastName} onChange={handleChange} required />
                <input type="email" name="email" placeholder="Email" value={form.email} onChange={handleChange} required />
                <input type="tel" name="phone" placeholder="Phone Number" value={form.phone} onChange={handleChange} required />
                <input type="text" name="address" placeholder="Address" value={form.address} onChange={handleChange} required />
                <input type="text" name="city" placeholder="City" value={form.city} onChange={handleChange} required />
                <input type="text" name="state" placeholder="State" value={form.state} onChange={handleChange} required />
                <input type="text" name="zip" placeholder="Zip Code" value={form.zip} onChange={handleChange} required />
                {error && <p className='error'>{error}</p>}
                {success && <p className='success'>{success}</p>}
                <div>
                    <small>Password must be at least 8 characters, include one uppercase letter and one number.</small>
                </div>
                <div className='button-group'>
                    <button type="submit" className='btn blue'>Register</button>
                    <Link to='/' className='btn blue'>Back</Link>
                </div>
            </form>
        </div>
    );
}

export default Register;