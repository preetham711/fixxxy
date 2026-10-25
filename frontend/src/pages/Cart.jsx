/**
 * Cart Page - Review items and proceed to checkout
 * Shows cart items with quantity controls and price calculation
 */
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { couponsAPI } from '../services/api';
import { formatCurrency } from '../utils/format';
import Sidebar from '../components/Sidebar';

function Cart() {
  const navigate = useNavigate();
  const [cart, setCart] = useState([]);
  const [couponCode, setCouponCode] = useState('');
  const [appliedCoupon, setAppliedCoupon] = useState(null);
  const [couponError, setCouponError] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadCartFromStorage();
  }, []);

  const loadCartFromStorage = () => {
    const savedCart = localStorage.getItem('cart');
    if (savedCart) {
      setCart(JSON.parse(savedCart));
    }
  };

  const saveCartToStorage = (newCart) => {
    localStorage.setItem('cart', JSON.stringify(newCart));
    setCart(newCart);
  };

  const updateQuantity = (productId, newQuantity) => {
    if (newQuantity < 1) return;
    
    const newCart = cart.map(item =>
      item.id === productId ? { ...item, quantity: newQuantity } : item
    );
    saveCartToStorage(newCart);
  };

  const removeItem = (productId) => {
    const newCart = cart.filter(item => item.id !== productId);
    saveCartToStorage(newCart);
  };

  const clearCart = () => {
    saveCartToStorage([]);
    setAppliedCoupon(null);
  };

  const applyCoupon = async () => {
    if (!couponCode.trim()) return;
    
    setLoading(true);
    setCouponError('');
    
    try {
      const coupon = await couponsAPI.validate(couponCode.trim());
      setAppliedCoupon(coupon);
      setCouponCode('');
    } catch (error) {
      setCouponError(error.response?.data?.detail || 'Invalid coupon code');
      setAppliedCoupon(null);
    } finally {
      setLoading(false);
    }
  };

  const removeCoupon = () => {
    setAppliedCoupon(null);
    setCouponCode('');
    setCouponError('');
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

  const handleCheckout = () => {
    if (cart.length === 0) return;
    
    // Store coupon in localStorage for checkout page
    if (appliedCoupon) {
      localStorage.setItem('appliedCoupon', JSON.stringify(appliedCoupon));
    } else {
      localStorage.removeItem('appliedCoupon');
    }
    
    navigate('/checkout');
  };

  return (
    <div className="dashboard-container">
      <Sidebar />

      <main className="main-content">
        <div className="page-header">
          <div>
            <h1 className="page-title">Shopping Cart</h1>
            <p className="page-subtitle">{cart.length} item{cart.length !== 1 ? 's' : ''} in your cart</p>
          </div>
          <button 
            className="btn btn-secondary"
            onClick={() => navigate('/products')}
          >
            ← Continue Shopping
          </button>
        </div>

        {cart.length === 0 ? (
          <div className="card">
            <div className="card-body" style={{ textAlign: 'center', padding: 'var(--spacing-xxl)' }}>
              <div style={{ fontSize: '4rem', marginBottom: 'var(--spacing-md)' }}>🛒</div>
              <h3 style={{ color: 'var(--text)', marginBottom: 'var(--spacing-sm)' }}>Your cart is empty</h3>
              <p className="text-muted" style={{ marginBottom: 'var(--spacing-lg)' }}>
                Add some products to get started!
              </p>
              <button className="btn btn-primary" onClick={() => navigate('/products')}>
                Browse Products
              </button>
            </div>
          </div>
        ) : (
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 400px', gap: 'var(--spacing-lg)' }}>
            {/* Cart Items */}
            <div>
              <div className="card">
                <div className="card-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <h3 className="card-title">Cart Items</h3>
                  <button className="btn btn-secondary btn-sm" onClick={clearCart}>
                    Clear All
                  </button>
                </div>
                <div className="card-body">
                  {cart.map(item => (
                    <div 
                      key={item.id}
                      style={{
                        display: 'flex',
                        gap: 'var(--spacing-md)',
                        padding: 'var(--spacing-md)',
                        borderBottom: '1px solid var(--border)',
                        alignItems: 'center'
                      }}
                    >
                      <div style={{ flex: 1 }}>
                        <h4 style={{ color: 'var(--text)', marginBottom: '0.25rem' }}>
                          {item.name}
                        </h4>
                        <p className="text-muted" style={{ fontSize: '0.75rem', marginBottom: '0.5rem' }}>
                          SKU: {item.sku} • {item.category}
                        </p>
                        <div style={{ fontSize: '1.125rem', fontWeight: '600', color: 'var(--orange)' }}>
                          {formatCurrency(item.price)} × {item.quantity} = {formatCurrency(item.price * item.quantity)}
                        </div>
                      </div>
                      
                      <div style={{ display: 'flex', gap: 'var(--spacing-sm)', alignItems: 'center' }}>
                        <button
                          className="btn btn-secondary btn-sm"
                          onClick={() => updateQuantity(item.id, item.quantity - 1)}
                          disabled={item.quantity <= 1}
                        >
                          −
                        </button>
                        <span style={{ minWidth: '2rem', textAlign: 'center', fontWeight: '600' }}>
                          {item.quantity}
                        </span>
                        <button
                          className="btn btn-secondary btn-sm"
                          onClick={() => updateQuantity(item.id, item.quantity + 1)}
                          disabled={item.quantity >= item.stock}
                        >
                          +
                        </button>
                        <button
                          className="btn btn-secondary btn-sm"
                          onClick={() => removeItem(item.id)}
                          style={{ marginLeft: 'var(--spacing-sm)' }}
                        >
                          🗑️
                        </button>
                      </div>
                    </div>
                  ))}
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
                  {/* Coupon Code */}
                  <div style={{ marginBottom: 'var(--spacing-lg)' }}>
                    <label className="label">Coupon Code</label>
                    {!appliedCoupon ? (
                      <div style={{ display: 'flex', gap: 'var(--spacing-sm)' }}>
                        <input
                          type="text"
                          className="input"
                          placeholder="Enter coupon code"
                          value={couponCode}
                          onChange={(e) => setCouponCode(e.target.value.toUpperCase())}
                          onKeyPress={(e) => e.key === 'Enter' && applyCoupon()}
                          disabled={loading}
                        />
                        <button
                          className="btn btn-primary"
                          onClick={applyCoupon}
                          disabled={loading || !couponCode.trim()}
                        >
                          {loading ? '...' : 'Apply'}
                        </button>
                      </div>
                    ) : (
                      <div style={{
                        display: 'flex',
                        justifyContent: 'space-between',
                        alignItems: 'center',
                        padding: 'var(--spacing-sm)',
                        background: 'var(--success)',
                        borderRadius: 'var(--radius)',
                        color: 'white'
                      }}>
                        <span>✓ {appliedCoupon.code} applied</span>
                        <button
                          onClick={removeCoupon}
                          style={{
                            background: 'transparent',
                            border: 'none',
                            color: 'white',
                            cursor: 'pointer',
                            padding: '0.25rem 0.5rem'
                          }}
                        >
                          ✕
                        </button>
                      </div>
                    )}
                    {couponError && (
                      <p style={{ color: 'var(--error)', fontSize: '0.875rem', marginTop: '0.5rem' }}>
                        {couponError}
                      </p>
                    )}
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

                  <button
                    className="btn btn-primary"
                    style={{ width: '100%', marginTop: 'var(--spacing-lg)' }}
                    onClick={handleCheckout}
                  >
                    Proceed to Checkout →
                  </button>
                </div>
              </div>

              {/* Cart Summary */}
              <div className="card" style={{ marginTop: 'var(--spacing-lg)' }}>
                <div className="card-body">
                  <h4 style={{ fontSize: '0.875rem', color: 'var(--muted)', marginBottom: 'var(--spacing-sm)' }}>
                    CART SUMMARY
                  </h4>
                  <div style={{ fontSize: '0.875rem' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                      <span className="text-muted">Items</span>
                      <span>{cart.reduce((sum, item) => sum + item.quantity, 0)} units</span>
                    </div>
                    <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                      <span className="text-muted">Products</span>
                      <span>{cart.length} different</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default Cart;
