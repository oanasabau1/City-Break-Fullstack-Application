import React from 'react';
import 'react-datepicker/dist/react-datepicker.css';
import './Home.css';

const Home = () => {


  return (
    <div className='homepage'>
      <div className='homepage-content'>
        <h1>Welcome to CityVenture, your gateway to the most exciting city breaks around the globe. Discover vibrant cultures, unforgettable events, and info about local forecast. Start exploring your options now!</h1>
        <div className='button-container'>
          <a href='/events'><button className='button'>Events</button></a>
          <a href='/weather'><button className='button'>Weather</button></a>
        </div>
      </div>

    </div>
  );
}

export default Home;
