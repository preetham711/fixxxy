/**
 * Orders Page - View order history
 * Shows list of all orders with details
 */
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ordersAPI } from '../services/api';
import { formatCurrency, formatDate } from '../utils/format';
import { getUser, isAdmin } from '../utils/auth';
import Sidebar from '../components/Sidebar';

function Orders() {
  const navigate = useNavigate();
  const user = getUser();
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedOrder, setSelectedOrder] = useState(null);
  const [statusFilter, setStatusFilter] = useState('all');

  useEffect(() => {
    loadOrders();
  }, []);

  const loadOrders = async () => {
    try {
      setLoading(true);
      const ordersData = await ordersAPI.getAll();
      // Sort by most recent first
      setOrders(ordersData.sort((a, b) => new Date(b.order_date) - new Date(a.order_date)));
    } catch (error) {
      console.error('Failed to load orders:', error);
    } finally {
      setLoading(false);
    }
  };

  const getStatusBadgeClass = (status) => {
    const statusMap = {
      'pending': 'badge-warning',
      'confirmed': 'badge-info',
      'processing': 'badge-info',
      'completed': 'badge-success',
      'cancelled': 'badge-error'
    };
    return statusMap[status] || 'badge-secondary';
  };

  const filteredOrders = statusFilter === 'all'
    ? orders
    : orders.filter(order => order.status === statusFilter);

  if (loading) {
    return (
      <div className="loading-container">
        <div className="spinner"></div>
        <p className="loading-text">Loading orders...</p>
      </div>
    );
  }

  return (
    <div className="dashboard-container">
      <Sidebar />

      <main className="main-content">
        <div className="page-header">
          <div>
            <h1 className="page-title">My Orders</h1>
            <p className="page-subtitle">{filteredOrders.length} order{filteredOrders.length !== 1 ? 's' : ''} found</p>
          </div>
        </div>

        {/* Status Filter */}
        <div className="card" style={{ marginBottom: 'var(--spacing-lg)' }}>
          <div className="card-body">
            <div style={{ display: 'flex', gap: 'var(--spacing-sm)', flexWrap: 'wrap' }}>
              {['all', 'pending', 'confirmed', 'processing', 'completed', 'cancelled'].map(status => (
                <button
                  key={status}
                  className={`btn ${statusFilter === status ? 'btn-primary' : 'btn-secondary'}`}
                  onClick={() => setStatusFilter(status)}
                >
                  {status === 'all' ? 'All Orders' : status.charAt(0).toUpperCase() + status.slice(1)}
                  {status === 'all' && ` (${orders.length})`}
                  {status !== 'all' && ` (${orders.filter(o => o.status === status).length})`}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Orders List */}
        {filteredOrders.length === 0 ? (
          <div className="card">
            <div className="card-body" style={{ textAlign: 'center', padding: 'var(--spacing-xxl)' }}>
              <div style={{ fontSize: '4rem', marginBottom: 'var(--spacing-md)' }}>📦</div>
              <h3 style={{ color: 'var(--text)', marginBottom: 'var(--spacing-sm)' }}>No orders found</h3>
              <p className="text-muted" style={{ marginBottom: 'var(--spacing-lg)' }}>
                {statusFilter === 'all'
                  ? "You haven't placed any orders yet."
                  : `No ${statusFilter} orders found.`}
              </p>
              {statusFilter === 'all' && (
                <button className="btn btn-primary" onClick={() => navigate('/products')}>
                  Start Shopping
                </button>
              )}
            </div>
          </div>
        ) : (
          <div style={{ display: 'grid', gap: 'var(--spacing-lg)' }}>
            {filteredOrders.map(order => (
              <div key={order.id} className="card">
                <div className="card-body">
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: 'var(--spacing-md)' }}>
                    <div>
                      <h3 style={{ color: 'var(--text)', marginBottom: '0.25rem' }}>
                        Order #{order.id}
                      </h3>
                      <p className="text-muted" style={{ fontSize: '0.875rem' }}>
                        Placed on {formatDate(order.order_date)}
                      </p>
                    </div>
                    <div style={{ textAlign: 'right' }}>
                      <span className={`badge ${getStatusBadgeClass(order.status)}`}>
                        {order.status}
                      </span>
                      <div style={{ fontSize: '1.25rem', fontWeight: '600', color: 'var(--orange)', marginTop: '0.5rem' }}>
                        {formatCurrency(order.final_amount)}
                      </div>
                    </div>
                  </div>

                  {/* Order Items Preview */}
                  <div style={{ 
                    background: 'var(--panel2)', 
                    padding: 'var(--spacing-md)', 
                    borderRadius: 'var(--radius)',
                    marginBottom: 'var(--spacing-md)'
                  }}>
                    <div style={{ fontSize: '0.875rem', fontWeight: '500', marginBottom: 'var(--spacing-sm)' }}>
                      Items ({order.items.length})
                    </div>
                    {order.items.map(item => (
                      <div
                        key={item.id}
                        style={{
                          display: 'flex',
                          justifyContent: 'space-between',
                          marginBottom: '0.5rem',
                          fontSize: '0.875rem'
                        }}
                      >
                        <span>
                          {item.product_name} × {item.quantity}
                        </span>
                        <span className="text-muted">
                          {formatCurrency(item.subtotal)}
                        </span>
                      </div>
                    ))}
                    
                    {order.discount_amount > 0 && (
                      <div style={{
                        display: 'flex',
                        justifyContent: 'space-between',
                        marginTop: 'var(--spacing-sm)',
                        paddingTop: 'var(--spacing-sm)',
                        borderTop: '1px solid var(--border)',
                        fontSize: '0.875rem',
                        color: 'var(--success)'
                      }}>
                        <span>Discount Applied</span>
                        <span>-{formatCurrency(order.discount_amount)}</span>
                      </div>
                    )}
                  </div>

                  {/* Order Details */}
                  <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 'var(--spacing-md)', fontSize: '0.875rem' }}>
                    <div>
                      <div className="text-muted">Payment Method</div>
                      <div style={{ fontWeight: '500', textTransform: 'capitalize' }}>
                        {order.payment_method.replace('_', ' ')}
                      </div>
                    </div>
                    
                    {order.vehicle && (
                      <div>
                        <div className="text-muted">Vehicle</div>
                        <div style={{ fontWeight: '500' }}>
                          {order.vehicle.make} {order.vehicle.model} {order.vehicle.year}
                        </div>
                      </div>
                    )}
                    
                    {order.notes && (
                      <div style={{ gridColumn: '1 / -1' }}>
                        <div className="text-muted">Order Notes</div>
                        <div style={{ fontWeight: '500' }}>
                          {order.notes}
                        </div>
                      </div>
                    )}
                  </div>

                  {/* Action Buttons */}
                  <div style={{ display: 'flex', gap: 'var(--spacing-sm)', marginTop: 'var(--spacing-md)', paddingTop: 'var(--spacing-md)', borderTop: '1px solid var(--border)' }}>
                    <button
                      className="btn btn-secondary btn-sm"
                      onClick={() => setSelectedOrder(selectedOrder?.id === order.id ? null : order)}
                    >
                      {selectedOrder?.id === order.id ? 'Hide Details' : 'View Details'}
                    </button>
                    
                    {order.status === 'pending' && isAdmin() && (
                      <button
                        className="btn btn-primary btn-sm"
                        onClick={async () => {
                          try {
                            await ordersAPI.updateStatus(order.id, 'confirmed');
                            loadOrders();
                          } catch (error) {
                            console.error('Failed to update status:', error);
                          }
                        }}
                      >
                        Confirm Order
                      </button>
                    )}
                  </div>

                  {/* Expanded Details */}
                  {selectedOrder?.id === order.id && (
                    <div style={{
                      marginTop: 'var(--spacing-md)',
                      padding: 'var(--spacing-md)',
                      background: 'var(--panel2)',
                      borderRadius: 'var(--radius)'
                    }}>
                      <h4 style={{ marginBottom: 'var(--spacing-md)' }}>Complete Order Details</h4>
                      <div style={{ fontSize: '0.875rem' }}>
                        <div style={{ marginBottom: 'var(--spacing-sm)' }}>
                          <span className="text-muted">Order ID:</span> #{order.id}
                        </div>
                        <div style={{ marginBottom: 'var(--spacing-sm)' }}>
                          <span className="text-muted">Customer:</span> {order.customer_name} ({order.customer_email})
                        </div>
                        <div style={{ marginBottom: 'var(--spacing-sm)' }}>
                          <span className="text-muted">Subtotal:</span> {formatCurrency(order.subtotal)}
                        </div>
                        {order.discount_amount > 0 && (
                          <div style={{ marginBottom: 'var(--spacing-sm)', color: 'var(--success)' }}>
                            <span className="text-muted">Discount:</span> -{formatCurrency(order.discount_amount)}
                          </div>
                        )}
                        <div style={{ marginBottom: 'var(--spacing-sm)', fontSize: '1rem', fontWeight: '600' }}>
                          <span className="text-muted">Total:</span> {formatCurrency(order.final_amount)}
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}

export default Orders;
