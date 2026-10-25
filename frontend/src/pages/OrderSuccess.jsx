/**
 * Order Success Page - Confirmation after successful order
 * Shows order details and next steps
 */
import { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { ordersAPI } from '../services/api';
import { formatCurrency, formatDate } from '../utils/format';
import Sidebar from '../components/Sidebar';

function OrderSuccess() {
  const navigate = useNavigate();
  const { orderId } = useParams();
  const [order, setOrder] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (orderId) {
      loadOrder();
    }
  }, [orderId]);

  const loadOrder = async () => {
    try {
      const orderData = await ordersAPI.getById(orderId);
      setOrder(orderData);
    } catch (error) {
      console.error('Failed to load order:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="spinner"></div>
        <p className="loading-text">Loading order details...</p>
      </div>
    );
  }

  if (!order) {
    return (
      <div className="dashboard-container">
        <Sidebar />
        <main className="main-content">
          <div className="card">
            <div className="card-body" style={{ textAlign: 'center', padding: 'var(--spacing-xxl)' }}>
              <h3>Order not found</h3>
              <button className="btn btn-primary" onClick={() => navigate('/orders')}>
                View All Orders
              </button>
            </div>
          </div>
        </main>
      </div>
    );
  }

  return (
    <div className="dashboard-container">
      <Sidebar />

      <main className="main-content">
        <div className="card" style={{ maxWidth: '800px', margin: '0 auto' }}>
          <div className="card-body" style={{ textAlign: 'center', padding: 'var(--spacing-xxl)' }}>
            <div style={{ fontSize: '4rem', marginBottom: 'var(--spacing-md)' }}>✓</div>
            <h1 style={{ color: 'var(--success)', fontSize: '2rem', marginBottom: 'var(--spacing-sm)' }}>
              Order Placed Successfully!
            </h1>
            <p className="text-muted" style={{ fontSize: '1.125rem', marginBottom: 'var(--spacing-xl)' }}>
              Thank you for your order. Your order ID is #{order.id}
            </p>

            {/* Order Details */}
            <div style={{
              background: 'var(--panel2)',
              padding: 'var(--spacing-lg)',
              borderRadius: 'var(--radius)',
              textAlign: 'left',
              marginBottom: 'var(--spacing-xl)'
            }}>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 'var(--spacing-md)', marginBottom: 'var(--spacing-lg)' }}>
                <div>
                  <div className="text-muted" style={{ fontSize: '0.875rem', marginBottom: '0.25rem' }}>
                    Order Date
                  </div>
                  <div style={{ fontWeight: '500' }}>
                    {formatDate(order.order_date)}
                  </div>
                </div>
                <div>
                  <div className="text-muted" style={{ fontSize: '0.875rem', marginBottom: '0.25rem' }}>
                    Status
                  </div>
                  <span className="badge badge-warning">
                    {order.status}
                  </span>
                </div>
                <div>
                  <div className="text-muted" style={{ fontSize: '0.875rem', marginBottom: '0.25rem' }}>
                    Payment Method
                  </div>
                  <div style={{ fontWeight: '500', textTransform: 'capitalize' }}>
                    {order.payment_method.replace('_', ' ')}
                  </div>
                </div>
                <div>
                  <div className="text-muted" style={{ fontSize: '0.875rem', marginBottom: '0.25rem' }}>
                    Total Amount
                  </div>
                  <div style={{ fontSize: '1.5rem', fontWeight: '600', color: 'var(--orange)' }}>
                    {formatCurrency(order.final_amount)}
                  </div>
                </div>
              </div>

              {/* Items */}
              <div style={{ borderTop: '1px solid var(--border)', paddingTop: 'var(--spacing-md)' }}>
                <h4 style={{ marginBottom: 'var(--spacing-md)', fontSize: '1rem' }}>Order Items</h4>
                {order.items.map(item => (
                  <div
                    key={item.id}
                    style={{
                      display: 'flex',
                      justifyContent: 'space-between',
                      marginBottom: 'var(--spacing-sm)',
                      padding: 'var(--spacing-sm)',
                      background: 'var(--bg)',
                      borderRadius: 'var(--radius)'
                    }}
                  >
                    <div>
                      <div>{item.product_name}</div>
                      <div className="text-muted" style={{ fontSize: '0.875rem' }}>
                        {formatCurrency(item.unit_price)} × {item.quantity}
                      </div>
                    </div>
                    <div style={{ fontWeight: '600' }}>
                      {formatCurrency(item.subtotal)}
                    </div>
                  </div>
                ))}
              </div>

              {order.discount_amount > 0 && (
                <div style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  marginTop: 'var(--spacing-md)',
                  paddingTop: 'var(--spacing-md)',
                  borderTop: '1px solid var(--border)',
                  color: 'var(--success)'
                }}>
                  <span>Discount Applied</span>
                  <span>-{formatCurrency(order.discount_amount)}</span>
                </div>
              )}
            </div>

            {/* Action Buttons */}
            <div style={{ display: 'flex', gap: 'var(--spacing-md)', justifyContent: 'center' }}>
              <button
                className="btn btn-primary"
                onClick={() => navigate('/orders')}
              >
                View All Orders
              </button>
              <button
                className="btn btn-secondary"
                onClick={() => navigate('/products')}
              >
                Continue Shopping
              </button>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default OrderSuccess;
