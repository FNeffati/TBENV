import React from 'react';
import "./styling/Header.css"


function Header() {
    return (
        <div className="header_container">
            <header>
                <div className="logo">Tampa Bay Environmentalist</div>
            </header>
            <div className="links">
                <a href="http://localhost:3000/">Contact Us</a>
                <a href="http://localhost:3000/">News</a>
            </div>
        </div>
    );
}

export default Header;
