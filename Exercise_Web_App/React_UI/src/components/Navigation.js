import React from 'react';
import { Link } from 'react-router-dom';

function Navigation() {
    return (
        <nav>
            <ul>
                <li id="home-button"><Link to="/">Home</Link></li>
                <li><Link to="/create-exercise">Create Entry</Link></li>
            </ul>
        </nav>
    );
}

export default Navigation;