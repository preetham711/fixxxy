/**
 * Water Wash Page - Book car wash services
 * Shows water wash packages and allows adding to cart
 */
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { productsAPI } from '../services/api';
import { formatCurrency } from '../utils/format';
import Sidebar from '../components/Sidebar';

function WaterWash() {
  const navigate = useNavigate();
  const [services, setServices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [cart, setCart] = useState([]);

  useEffect(() => {
    loadServices();
    loadCartFromStorage();
  }, []);

  const loadServices = async () => {
    try {
      setLoading(true);
      const products = await productsAPI.getAll();
      // Filter only Water Wash services
      const waterWashServices = products.filter(p => p.category === 'Water Wash');
      setServices(waterWashServices);
    } catch (error) {
      console.error('Failed to load services:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadCartFromStorage = () => {
    const savedCart = localStorage.getItem('cart');
    if (savedCart) {
      setCart(JSON.parse(savedCart));
    }
  };

  const saveCartToStorage = (newCart) => {
    localStorage.setItem('cart', JSON.stringify(newCart));
  };

  const addToCart = (service) => {
    const existingItem = cart.find(item => item.id === service.id);
    let newCart;

    if (existingItem) {
      newCart = cart.map(item =>
        item.id === service.id
          ? { ...item, quantity: item.quantity + 1 }
          : item
      );
    } else {
      newCart = [...cart, { ...service, quantity: 1 }];
    }

    setCart(newCart);
    saveCartToStorage(newCart);
  };

  const getCartQuantity = (serviceId) => {
    const item = cart.find(i => i.id === serviceId);
    return item ? item.quantity : 0;
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="spinner"></div>
        <p className="loading-text">Loading services...</p>
      </div>
    );
  }

  return (
    <div className="dashboard-container">
      <Sidebar />

      <main className="main-content">
        <div className="page-header">
          <div>
            <h1 className="page-title">✦ Water Wash Services</h1>
            <p className="page-subtitle">Professional car care and cleaning packages</p>
          </div>
          <button 
            className="btn btn-primary"
            onClick={() => navigate('/cart')}
          >
            🛒 Cart ({cart.reduce((sum, item) => sum + item.quantity, 0)})
          </button>
        </div>

        {/* Info Banner */}
        <div style={{
          background: 'linear-gradient(135deg, var(--primary) 0%, var(--orange) 100%)',
          padding: 'var(--spacing-xl)',
          borderRadius: 'var(--radius)',
          color: 'white',
          marginBottom: 'var(--spacing-lg)'
        }}>
          <h2 style={{ fontSize: '1.5rem', marginBottom: 'var(--spacing-sm)' }}>
            Premium Car Wash Services
          </h2>
          <p style={{ opacity: 0.9, fontSize: '1rem' }}>
            Choose from our range of professional car cleaning packages. All services include eco-friendly products and expert care.
          </p>
        </div>

        {/* Services Grid */}
        {services.length === 0 ? (
          <div className="card">
            <div className="card-body" style={{ textAlign: 'center', padding: 'var(--spacing-xxl)' }}>
              <p className="text-muted">No water wash services available at the moment.</p>
            </div>
          </div>
        ) : (
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))', gap: 'var(--spacing-lg)' }}>
            {services.map(service => (
              <div 
                key={service.id} 
                className="card" 
                style={{ 
                  display: 'flex', 
                  flexDirection: 'column',
                  border: '2px solid transparent',
                  transition: 'all 0.3s',
                  cursor: 'pointer'
                }}
                onMouseEnter={(e) => e.currentTarget.style.borderColor = 'var(--primary)'}
                onMouseLeave={(e) => e.currentTarget.style.borderColor = 'transparent'}
              >
                <div className="card-body" style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
                  {/* Service Icon/Badge */}
                  <div style={{
                    width: '60px',
                    height: '60px',
                    borderRadius: '50%',
                    background: 'var(--primary)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontSize: '1.5rem',
                    marginBottom: 'var(--spacing-md)'
                  }}>
                    🚗
                  </div>

                  {/* Service Title */}
                  <h3 style={{ 
                    color: 'var(--text)', 
                    fontSize: '1.5rem', 
                    marginBottom: 'var(--spacing-sm)',
                    fontWeight: '600'
                  }}>
                    {service.name}
                  </h3>

                  {/* SKU */}
                  <p className="text-muted" style={{ fontSize: '0.75rem', marginBottom: 'var(--spacing-md)' }}>
                    SKU: {service.sku}
                  </p>

                  {/* Description */}
                  {service.description && (
                    <p className="text-muted" style={{ 
                      fontSize: '0.95rem', 
                      lineHeight: '1.6',
                      marginBottom: 'var(--spacing-lg)',
                      flex: 1
                    }}>
                      {service.description}
                    </p>
                  )}

                  {/* Price and CTA */}
                  <div style={{ 
                    marginTop: 'auto',
                    paddingTop: 'var(--spacing-md)',
                    borderTop: '1px solid var(--border)'
                  }}>
                    <div style={{ 
                      display: 'flex', 
                      justifyContent: 'space-between', 
                      alignItems: 'center'
                    }}>
                      <div>
                        <div className="text-muted" style={{ fontSize: '0.75rem', marginBottom: '0.25rem' }}>
                          Package Price
                        </div>
                        <div style={{ 
                          fontSize: '2rem', 
                          fontWeight: '700', 
                          color: 'var(--orange)',
                          lineHeight: '1'
                        }}>
                          {formatCurrency(service.price)}
                        </div>
                      </div>
                      
                      <button
                        className="btn btn-primary"
                        onClick={() => addToCart(service)}
                        style={{ 
                          minWidth: '120px',
                          padding: 'var(--spacing-md) var(--spacing-lg)'
                        }}
                      >
                        {getCartQuantity(service.id) > 0 
                          ? `Add More (${getCartQuantity(service.id)})` 
                          : '+ Book Now'}
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Features Section */}
        <div className="card" style={{ marginTop: 'var(--spacing-xxl)' }}>
          <div className="card-header">
            <h3 className="card-title">Why Choose FIXXY Water Wash?</h3>
          </div>
          <div className="card-body">
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: 'var(--spacing-lg)' }}>
              <div>
                <div style={{ fontSize: '2rem', marginBottom: 'var(--spacing-sm)' }}>✨</div>
                <h4 style={{ marginBottom: 'var(--spacing-sm)' }}>Premium Quality</h4>
                <p className="text-muted" style={{ fontSize: '0.875rem' }}>
                  Professional cleaning with eco-friendly products
                </p>
              </div>
              <div>
                <div style={{ fontSize: '2rem', marginBottom: 'var(--spacing-sm)' }}>⚡</div>
                <h4 style={{ marginBottom: 'var(--spacing-sm)' }}>Quick Service</h4>
                <p className="text-muted" style={{ fontSize: '0.875rem' }}>
                  Fast and efficient service without compromising quality
                </p>
              </div>
              <div>
                <div style={{ fontSize: '2rem', marginBottom: 'var(--spacing-sm)' }}>💰</div>
                <h4 style={{ marginBottom: 'var(--spacing-sm)' }}>Best Value</h4>
                <p className="text-muted" style={{ fontSize: '0.875rem' }}>
                  Competitive pricing with package deals and discounts
                </p>
              </div>
              <div>
                <div style={{ fontSize: '2rem', marginBottom: 'var(--spacing-sm)' }}>🛡️</div>
                <h4 style={{ marginBottom: 'var(--spacing-sm)' }}>Safe & Secure</h4>
                <p className="text-muted" style={{ fontSize: '0.875rem' }}>
                  Gentle on your car's paint and finish
                </p>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default WaterWash;
