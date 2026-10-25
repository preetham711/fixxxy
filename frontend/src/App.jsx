import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import { isAuthenticated, getUser, isAdmin } from './utils/auth';
import './App.css';

// Pages
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import AdminDashboard from './pages/AdminDashboard';
import Products from './pages/Products';
import Cart from './pages/Cart';
import Checkout from './pages/Checkout';
import OrderSuccess from './pages/OrderSuccess';
import Orders from './pages/Orders';
import WaterWash from './pages/WaterWash';

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const currentUser = getUser();
    setUser(currentUser);
    setLoading(false);
  }, []);

  // Update user state when authentication changes
  const updateUser = () => {
    const currentUser = getUser();
    setUser(currentUser);
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="spinner"></div>
        <p className="loading-text">Loading FIXXY...</p>
      </div>
    );
  }

  return (
    <BrowserRouter>
      <Routes>
        {/* Landing page with role selection */}
        <Route 
          path="/" 
          element={!isAuthenticated() ? <Login onLogin={updateUser} /> : (
            isAdmin() ? <Navigate to="/admin" /> : <Navigate to="/dashboard" />
          )} 
        />
        
        {/* Customer Dashboard */}
        <Route 
          path="/dashboard" 
          element={isAuthenticated() ? <Dashboard /> : <Navigate to="/" />} 
        />
        
        {/* Admin Dashboard */}
        <Route 
          path="/admin" 
          element={
            isAuthenticated() ? (
              isAdmin() ? <AdminDashboard /> : <Navigate to="/dashboard" />
            ) : (
              <Navigate to="/" />
            )
          } 
        />
        
        {/* Products & Shopping */}
        <Route 
          path="/products" 
          element={isAuthenticated() ? <Products /> : <Navigate to="/" />} 
        />
        <Route 
          path="/cart" 
          element={isAuthenticated() ? <Cart /> : <Navigate to="/" />} 
        />
        <Route 
          path="/checkout" 
          element={isAuthenticated() ? <Checkout /> : <Navigate to="/" />} 
        />
        <Route 
          path="/order-success/:orderId" 
          element={isAuthenticated() ? <OrderSuccess /> : <Navigate to="/" />} 
        />
        <Route 
          path="/orders" 
          element={isAuthenticated() ? <Orders /> : <Navigate to="/" />} 
        />
        <Route 
          path="/waterwash" 
          element={isAuthenticated() ? <WaterWash /> : <Navigate to="/" />} 
        />
        
        {/* Catch all */}
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
