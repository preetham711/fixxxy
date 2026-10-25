/**
 * Checkout Page - Complete order with vehicle and payment details
 * Creates order and clears cart on success
 */
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ordersAPI, vehiclesAPI } from '../services/api';
import { formatCurrency } from '../utils/format';
import { getUser } from '../utils/auth';
import Sidebar from '../components/Sidebar';

function Checkout() {
  const navigate = useNavigate();
  const user = getUser();
  const [cart, setCart] = useState([]);
  const [appliedCoupon, setAppliedCoupon] = useState(null);
  const [vehicles, setVehicles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  const [formData, setFormData] = useState({
    vehicle_id: '',
    payment_method: 'cash',
    notes: ''
  });

  useEffect(() => {
    loadCheckoutData();
  }, []);

  const loadCheckoutData = async () => {
    // Load cart
    const savedCart = localStorage.getItem('cart');
    if (!savedCart || JSON.parse(savedCart).length === 0) {
      navigate('/cart');
      return;
    }
    setCart(JSON.parse(savedCart));

    // Load coupon if applied
    const savedCoupon = localStorage.getItem('appliedCoupon');
    if (savedCoupon) {
      setAppliedCoupon(JSON.parse(savedCoupon));
    }

    // Load vehicles
    try {
      const vehiclesData = await vehiclesAPI.getAll();
      setVehicles(vehiclesData);
      
      // Auto-select primary vehicle if exists
      const primaryVehicle = vehiclesData.find(v => v.is_primary);
      if (primaryVehicle) {
        setFormData(prev => ({ ...prev, vehicle_id: primaryVehicle.id }));
      }
    } catch (error) {
      console.error('Failed to load vehicles:', error);
    }
  };

  // Calculate totals
  const subtotal = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
  
  let discount = 0;
  if (appliedCoupon) {
    if (appliedCoupon.discount_type === 'percentage') {
      discount = (subtotal * appliedCoupon.discount_value) / 100;
      if (appliedCoupon.max_discount && discount > appliedCoupon.max_discount) {
        discount = appliedCoupon.max_discount;
      }
    } else {
      discount = appliedCoupon.discount_value;
    }
  }
  
  const total = subtotal - discount;

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      // Prepare order data
      const orderData = {
        items: cart.map(item => ({
          product_id: item.id,
          quantity: item.quantity,
          unit_price: item.price
        })),
        vehicle_id: formData.vehicle_id ? parseInt(formData.vehicle_id) : null,
        coupon_code: appliedCoupon?.code || null,
        payment_method: formData.payment_method,
        notes: formData.notes || null
      };

      // Create order
      const order = await ordersAPI.create(orderData);

      // Clear cart and coupon
      localStorage.removeItem('cart');
      localStorage.removeItem('appliedCoupon');

      // Redirect to success page with order ID
      navigate(`/order-success/${order.id}`);
    } catch (error) {
      console.error('Order creation failed:', error);
      setError(error.response?.data?.detail || 'Failed to create order. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  if (cart.length === 0) {
    return null; // Will redirect in useEffect
  }

  return (
    <div className="dashboard-container">
      <Sidebar />

      <main className="main-content">
        <div className="page-header">
          <div>
            <h1 className="page-title">Checkout</h1>
            <p className="page-subtitle">Complete your order</p>
          </div>
          <button 
            className="btn btn-secondary"
            onClick={() => navigate('/cart')}
          >
            ← Back to Cart
          </button>
        </div>

        <form onSubmit={handleSubmit}>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 400px', gap: 'var(--spacing-lg)' }}>
            {/* Checkout Form */}
            <div>
              {/* Vehicle Selection */}
              <div className="card" style={{ marginBottom: 'var(--spacing-lg)' }}>
                <div className="card-header">
                  <h3 className="card-title">Vehicle Information</h3>
                </div>
                <div className="card-body">
                  <label className="label">Select Vehicle (Optional)</label>
                  <select
                    name="vehicle_id"
                    className="input"
                    value={formData.vehicle_id}
                    onChange={handleInputChange}
                  >
                    <option value="">No vehicle selected</option>
                    {vehicles.map(vehicle => (
                      <option key={vehicle.id} value={vehicle.id}>
                        {vehicle.make} {vehicle.model} {vehicle.year} 
                        {vehicle.registration_number && ` - ${vehicle.registration_number}`}
                        {vehicle.is_primary && ' ⭐'}
                      </option>
                    ))}
                  </select>
                  <p className="text-muted" style={{ fontSize: '0.875rem', marginTop: '0.5rem' }}>
                    Linking a vehicle helps us provide better service recommendations
                  </p>
                </div>
              </div>

              {/* Payment Method */}
              <div className="card" style={{ marginBottom: 'var(--spacing-lg)' }}>
                <div className="card-header">
                  <h3 className="card-title">Payment Method</h3>
                </div>
                <div className="card-body">
                  <div style={{ display: 'flex', gap: 'var(--spacing-md)', flexWrap: 'wrap' }}>
                    {['cash', 'card', 'upi', 'bank_transfer'].map(method => (
                      <label key={method} style={{
                        flex: '1',
                        minWidth: '140px',
                        padding: 'var(--spacing-md)',
                        border: `2px solid ${formData.payment_method === method ? 'var(--primary)' : 'var(--border)'}`,
                        borderRadius: 'var(--radius)',
                        cursor: 'pointer',
                        background: formData.payment_method === method ? 'var(--primary-light)' : 'transparent',
                        transition: 'all 0.2s'
                      }}>
                        <input
                          type="radio"
                          name="payment_method"
                          value={method}
                          checked={formData.payment_method === method}
                          onChange={handleInputChange}
                          style={{ marginRight: '0.5rem' }}
                        />
                        <span style={{ textTransform: 'capitalize' }}>
                          {method.replace('_', ' ')}
                        </span>
                      </label>
                    ))}
                  </div>
                </div>
              </div>

              {/* Order Notes */}
              <div className="card">
                <div className="card-header">
                  <h3 className="card-title">Order Notes (Optional)</h3>
                </div>
                <div className="card-body">
                  <textarea
                    name="notes"
                    className="input"
                    rows="4"
                    placeholder="Any special instructions or notes for this order..."
                    value={formData.notes}
                    onChange={handleInputChange}
                  />
                </div>
              </div>
            </div>

            {/* Order Summary */}
            <div>
              <div className="card">
                <div className="card-header">
                  <h3 className="card-title">Order Summary</h3>
                </div>
                <div className="card-body">
                  {/* Items List */}
                  <div style={{ marginBottom: 'var(--spacing-lg)', maxHeight: '300px', overflowY: 'auto' }}>
                    {cart.map(item => (
                      <div 
                        key={item.id}
                        style={{
                          display: 'flex',
                          justifyContent: 'space-between',
                          marginBottom: 'var(--spacing-sm)',
                          padding: 'var(--spacing-sm)',
                          background: 'var(--panel2)',
                          borderRadius: 'var(--radius)',
                          fontSize: '0.875rem'
                        }}
                      >
                        <div style={{ flex: 1 }}>
                          <div>{item.name}</div>
                          <div className="text-muted" style={{ fontSize: '0.75rem' }}>
                            {formatCurrency(item.price)} × {item.quantity}
                          </div>
                        </div>
                        <div style={{ fontWeight: '600' }}>
                          {formatCurrency(item.price * item.quantity)}
                        </div>
                      </div>
                    ))}
                  </div>

                  {/* Price Breakdown */}
                  <div style={{ borderTop: '1px solid var(--border)', paddingTop: 'var(--spacing-md)' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 'var(--spacing-sm)' }}>
                      <span className="text-muted">Subtotal</span>
                      <span>{formatCurrency(subtotal)}</span>
                    </div>
                    
                    {appliedCoupon && discount > 0 && (
                      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 'var(--spacing-sm)', color: 'var(--success)' }}>
                        <span>Discount ({appliedCoupon.code})</span>
                        <span>-{formatCurrency(discount)}</span>
                      </div>
                    )}
                    
                    <div style={{
                      display: 'flex',
                      justifyContent: 'space-between',
                      fontSize: '1.5rem',
                      fontWeight: '600',
                      paddingTop: 'var(--spacing-md)',
                      borderTop: '1px solid var(--border)',
                      color: 'var(--orange)'
                    }}>
                      <span>Total</span>
                      <span>{formatCurrency(total)}</span>
                    </div>
                  </div>

                  {error && (
                    <div style={{
                      marginTop: 'var(--spacing-md)',
                      padding: 'var(--spacing-sm)',
                      background: 'var(--error-light)',
                      color: 'var(--error)',
                      borderRadius: 'var(--radius)',
                      fontSize: '0.875rem'
                    }}>
                      {error}
                    </div>
                  )}

                  <button
                    type="submit"
                    className="btn btn-primary"
                    style={{ width: '100%', marginTop: 'var(--spacing-lg)' }}
                    disabled={loading}
                  >
                    {loading ? 'Processing...' : `Place Order - ${formatCurrency(total)}`}
                  </button>

                  <p className="text-muted" style={{ fontSize: '0.75rem', textAlign: 'center', marginTop: 'var(--spacing-md)' }}>
                    By placing this order, you agree to our terms and conditions
                  </p>
                </div>
              </div>
            </div>
          </div>
        </form>
      </main>
    </div>
  );
}

export default Checkout;
