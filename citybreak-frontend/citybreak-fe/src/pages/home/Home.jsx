import React, { useState } from 'react';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import './Home.css';

const Home = () => {
  const [showForms, setShowForms] = useState(false);
  const [selectedDate, setSelectedDate] = useState(null);

  const handleButtonClick = () => {
    setShowForms(true);
  };

  return (
    <div className='homepage'>
      <div className='homepage-content'>
        <h1>Welcome to CityVenture, your gateway to the most exciting city breaks around the globe. Discover vibrant cultures, unforgettable events, and info about local forecast. Start exploring your options now!</h1>
        <div className='button-container'>
          <button className='button' onClick={handleButtonClick}>Events</button>
          <button className='button' onClick={handleButtonClick}>Weather</button>
        </div>
      </div>
      {showForms && (
        <div className='form-container'>
          <form className='combined-form'>
            <div className='form-group'>
              <label htmlFor="city">Enter the City Name:</label>
              <input type="text" id="city" name="city" />
            </div>
            <div className='form-group'>
              <label htmlFor="date">Select Date:</label>
              <DatePicker
                selected={selectedDate}
                onChange={(date) => setSelectedDate(date)}
                dateFormat="yyyy-MM-dd"
                placeholderText="Click to select a date"
              />
            </div>
            <button className='button' type="submit">Search</button>
          </form>
        </div>
      )}
    </div>
  );
}

export default Home;
