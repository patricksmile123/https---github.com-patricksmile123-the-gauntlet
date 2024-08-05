import React from 'react';
import './Navbar.css';

const Navbar = ({user, setUser}) => {
    return (
        <nav className='navbar'>
            <ul>
                <li><a href="/wordle">Play</a></li>
                <li><a href="/leaderboard">Leaderboard</a></li>
                <li><a href="/login">Login</a></li>
                <li><a href="/signup">Signup</a></li>
                <li><a href="/logout">Logout</a></li>
            </ul>
        </nav>
    );
};

export default Navbar;