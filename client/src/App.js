import './App.css';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import About from './pages/About';
import Help from './pages/Help';

import {BrowserRouter, Routes, Route} from 'react-router-dom'
function App() {
  return (
    <>
    <BrowserRouter>
      <Navbar/>
      <Routes>
        <Route path='/' exact element={<Home/>}/>
        <Route exact path='/about' element={<About/>}/>
        <Route exact path='/help' element={<Help/>}/>
      </Routes>
    </BrowserRouter>
    </>
  );
}

export default App;
