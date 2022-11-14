import './App.css';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Reports from './pages/Reports';
import Products from './pages/Products';
import {BrowserRouter, Routes, Route} from 'react-router-dom'
function App() {
  return (
    <>
    <BrowserRouter>
      <Navbar/>
      <Routes>
        <Route path='/' exact element={<Home/>}/>
        <Route exact path='/reports' element={<Reports/>}/>
        <Route exact path='/products' element={<Products/>}/>
      </Routes>
    </BrowserRouter>
    </>
  );
}

export default App;
