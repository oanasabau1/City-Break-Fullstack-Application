import './App.css';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import Footer from './components/Footer';
import Home from './pages/home/Home'
import Events from './pages/events/Events';
import Weather from './pages/weather/Weather';

function App() {
  return (
    <BrowserRouter>
    <div>
    <Header />
      <Routes>
        <Route path='/' element={<Home />}/>
        <Route path='/events' element={<Events />}/>
        <Route path='/weather' element={<Weather />}/>
      </Routes>
      <Footer />
    </div>
    </BrowserRouter>
  );
}

export default App;
