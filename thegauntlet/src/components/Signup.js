import React, { useState, useEffect } from 'react';
import './Signup.css';

function Signup() {
    const [username, setUsername] = useState('');
    const [firstname, setFirstname] = useState('');
    const [lastname, setLastname] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [errors, setErrors] = useState({});
    const [csrfToken, setCsrfToken] = useState('');

    useEffect(() => {
        async function fetchCsrfToken() {
            try {
                const response = await fetch('http://127.0.0.1:5000/get_csrf_token');
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const data = await response.json();
                console.log(data.csrf_token)
                setCsrfToken(data.csrf_token);
            } catch (error) {
                console.error('Error fetching CSRF token:', error);
            }
        }

        fetchCsrfToken();
    }, []);
    const handleSubmit = async (e) => {
        e.preventDefault();  // Prevent the default form submission
        console.log("Using the handleSubmit function");
        try {
            const response = await fetch('http://127.0.0.1:5000/signup', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken  // Add the CSRF token here
                },
                body: JSON.stringify({
                    username: username,
                    password: password,
                    confirmPassword: confirmPassword,
                    firstname: firstname,
                    lastname: lastname,
                    csrf_token: csrfToken
                })
            });
            console.log(JSON.stringify({
                username: username,
                password: password,
                confirmPassword: confirmPassword,
                firstname: firstname,
                lastname: lastname
            }))
    
            // Check if the response status is not OK
            if (!response.ok) {
                const errorData = await response.json();
                console.log('Error data:', errorData);
                if (errorData.errors) {
                    setErrors(errorData.errors);
                } else {
                    alert('An error occurred');
                }
            } else {
                const data = await response.json();
                console.log('Success:', data);
                // Handle success (e.g., redirect to another page or update the UI)
            }
        } catch (error) {
            console.error('An error occurred:', error);
            alert('An error occurred');
        }
    };

    return (
        <div className="signup-container">
          <h2>Sign Up</h2>
          <form onSubmit={handleSubmit} className="signup-form">
            <div className="form-group">
              <label>Username</label>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="form-control"
              />
              {errors.username && <p className="error">{errors.username[0]}</p>}
            </div>
            <div className="form-group">
              <label>First Name</label>
              <input
                type="text"
                value={firstname}
                onChange={(e) => setFirstname(e.target.value)}
                className="form-control"
              />
              {errors.firstname && <p className="error">{errors.firstname[0]}</p>}
            </div>
            <div className="form-group">
              <label>Last Name</label>
              <input
                type="text"
                value={lastname}
                onChange={(e) => setLastname(e.target.value)}
                className="form-control"
              />
              {errors.lastname && <p className="error">{errors.lastname[0]}</p>}
            </div>
            <div className="form-group">
              <label>Password</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="form-control"
              />
              {errors.password && <p className="error">{errors.password[0]}</p>}
            </div>
            <div className="form-group">
              <label>Confirm Password</label>
              <input
                type="password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                className="form-control"
              />
              {errors.confirm_password && <p className="error">{errors.confirm_password[0]}</p>}
            </div>
            <button type="submit" className="btn btn-primary">Sign Up</button>
          </form>
        </div>
    );
}
export default Signup;
