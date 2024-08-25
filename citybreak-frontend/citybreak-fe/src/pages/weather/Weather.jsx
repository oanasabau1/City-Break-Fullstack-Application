import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './Weather.css';
import ConfirmationDialog from '../../components/confirmationDialog/ConfirmationDialog';

const Weather = () => {
  const [weathers, setWeathers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isEditing, setIsEditing] = useState(false);
  const [isAdding, setIsAdding] = useState(false);
  const [selectedWeather, setSelectedWeather] = useState(null);
  const [newWeather, setNewWeather] = useState({
    city: '',
    date: '',
    temperature: '',
    humidity: '',
    description: ''
  });
  const [showConfirmDelete, setShowConfirmDelete] = useState(false);
  const [weatherToDelete, setWeatherToDelete] = useState(null);
  const [searchParams, setSearchParams] = useState({
    city: '',
    date: ''
  });

  useEffect(() => {
    fetchWeathers();
  }, [searchParams]);

  const fetchWeathers = async () => {
    try {
      const response = await axios.get('http://localhost:5000/weather', {
        params: searchParams
      });
      setWeathers(response.data);
      setLoading(false);
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };

  const handleEditClick = (weather) => {
    setSelectedWeather(weather);
    setIsEditing(true);
  };

  const handleAddClick = () => {
    setNewWeather({
      city: '',
      date: '',
      temperature: '',
      humidity: '',
      description: ''
    });
    setIsAdding(true);
  };

  const handleCloseForm = () => {
    setIsEditing(false);
    setIsAdding(false);
    setSelectedWeather(null);
  };

  const handleDeleteClick = (weather) => {
    setWeatherToDelete(weather);
    setShowConfirmDelete(true);
  };

  const handleConfirmDelete = async () => {
    try {
      await axios.delete(`http://localhost:5000/weather/delete`, {
        params: { id: weatherToDelete.id }
      });
      setWeathers(weathers.filter(weather => weather.id !== weatherToDelete.id));
      setShowConfirmDelete(false);
      setWeatherToDelete(null);
    } catch (err) {
      setError(err.message);
      setShowConfirmDelete(false);
      setWeatherToDelete(null);
    }
  };

  const handleAddWeather = async (e) => {
    e.preventDefault();
    try {
      await axios.post('http://localhost:5000/weather/add', newWeather, {
        headers: { 'Content-Type': 'application/json' }
      });
      fetchWeathers();
      handleCloseForm();
    } catch (err) {
      setError(err.message);
    }
  };

  const handleUpdateWeather = async (updatedWeather) => {
    try {
      await axios.put('http://localhost:5000/weather/update', {
        city: updatedWeather.city,
        date: updatedWeather.date,
        temperature: updatedWeather.temperature,
        humidity: updatedWeather.humidity,
        description: updatedWeather.description
      }, {
        headers: { 'Content-Type': 'application/json' },
        params: { id: updatedWeather.id } 
      });
      fetchWeathers(); 
      handleCloseForm();
    } catch (err) {
      setError(err.message);
    }
  };

  const handleSearchChange = (e) => {
    const { name, value } = e.target;
    setSearchParams((prevParams) => ({
      ...prevParams,
      [name]: value
    }));
  };

  return (
    <div className='weather-container'>
      <h1>Weather</h1>
      <button className="add-button" onClick={handleAddClick}>Add Weather</button>
      
      <div className='search-form'>
        <h2>Search Weather</h2>
        <form>
          <label>
            City:
            <input
              type="text"
              name="city"
              value={searchParams.city}
              onChange={handleSearchChange}
            />
          </label>
          <label>
            Date:
            <input
              type="date"
              name="date"
              value={searchParams.date}
              onChange={handleSearchChange}
            />
          </label>
        </form>
      </div>

      {loading && <div>Loading...</div>}
      {error && <div>Error: {error}</div>}
      {weathers.length > 0 ? (
        <ul>
          {weathers.map((weather) => (
            <li key={weather.id}>
              <h2>{weather.city}</h2>
              <p><strong>Date:</strong> {weather.date}</p>
              <p><strong>Temperature:</strong> {weather.temperature} °C</p>
              <p><strong>Humidity:</strong> {weather.humidity}%</p>
              <p><strong>Description:</strong> {weather.description}</p>
              <button className='edit-button' onClick={() => handleEditClick(weather)}>Edit</button>
              <button className='delete-button' onClick={() => handleDeleteClick(weather)}>Delete</button>
            </li>
          ))}
        </ul>
      ) : (
        <div>No weather data found.</div>
      )}

      {isEditing && selectedWeather && (
        <div className='modal'>
          <EditWeatherForm 
            weather={selectedWeather} 
            onClose={handleCloseForm} 
            onUpdate={handleUpdateWeather}
          />
        </div>
      )}

      {isAdding && (
        <div className='modal'>
          <AddWeatherForm 
            weather={newWeather}
            onChange={(e) => setNewWeather({ ...newWeather, [e.target.name]: e.target.value })}
            onClose={handleCloseForm}
            onSubmit={handleAddWeather}
          />
        </div>
      )}

      {showConfirmDelete && (
        <ConfirmationDialog
          message={`Are you sure you want to delete the weather data for "${weatherToDelete.city}" on "${weatherToDelete.date}"?`}
          onConfirm={handleConfirmDelete}
          onCancel={() => setShowConfirmDelete(false)}
        />
      )}
    </div>
  );
};

const EditWeatherForm = ({ weather, onClose, onUpdate }) => {
  const [formData, setFormData] = useState({ ...weather });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await onUpdate(formData);
    } catch (err) {
      console.error('Update failed:', err);
    }
  };

  return (
    <div className='edit-weather-form'>
      <h2>Edit Weather Data</h2>
      <form onSubmit={handleSubmit}>
        <label>
          City:
          <input
            type="text"
            name="city"
            value={formData.city}
            onChange={handleChange}
          />
        </label>
        <label>
          Date:
          <input
            type="date"
            name="date"
            value={formData.date}
            onChange={handleChange}
          />
        </label>
        <label>
          Temperature (°C):
          <input
            type="number"
            name="temperature"
            value={formData.temperature}
            onChange={handleChange}
            step="0.1"
          />
        </label>
        <label>
          Humidity (%):
          <input
            type="number"
            name="humidity"
            value={formData.humidity}
            onChange={handleChange}
            step="1"
          />
        </label>
        <label>
          Description:
          <input
            type="text"
            name="description"
            value={formData.description}
            onChange={handleChange}
          />
        </label>
        <button type="submit">Save Changes</button>
        <button type="button" onClick={onClose}>Cancel</button>
      </form>
    </div>
  );
};

const AddWeatherForm = ({ weather, onChange, onClose, onSubmit }) => {
  return (
    <div className='edit-weather-form'>
      <h2>Add Weather Data</h2>
      <form onSubmit={onSubmit}>
        <label>
          City:
          <input
            type="text"
            name="city"
            value={weather.city}
            onChange={onChange}
          />
        </label>
        <label>
          Date:
          <input
            type="date"
            name="date"
            value={weather.date}
            onChange={onChange}
          />
        </label>
        <label>
          Temperature (°C):
          <input
            type="number"
            name="temperature"
            value={weather.temperature}
            onChange={onChange}
            step="0.1"
          />
        </label>
        <label>
          Humidity (%):
          <input
            type="number"
            name="humidity"
            value={weather.humidity}
            onChange={onChange}
            step="1"
          />
        </label>
        <label>
          Description:
          <input
            type="text"
            name="description"
            value={weather.description}
            onChange={onChange}
          />
        </label>
        <button type="submit">Add Weather</button>
        <button type="button" onClick={onClose}>Cancel</button>
      </form>
    </div>
  );
};

export default Weather;
