import React from 'react';
import { GiEarthAmerica } from "react-icons/gi";
import './Header.css';

const Header = () => {
  return (
    <header className="header">
      <div className="container">
        <a href="/" className="icon-link">
          <GiEarthAmerica className="icon" />
        </a>
        <h1 className="logo">CityVenture - your City Break Application</h1>
      </div>
    </header>
  );
}

export default Header;
