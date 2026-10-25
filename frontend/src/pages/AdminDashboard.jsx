import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getUser, clearAuth } from '../utils/auth';
import { productsAPI, ordersAPI } from '../services/api';
import { formatCurrency } from '../utils/format';

function AdminDashboard() {
  const navigate = useNavigate();
  const user = getUser();
  const [stats, setStats] = useState({
    totalProducts: 0,
    totalStock: 0,
    lowStockCount: 0,
    totalOrders: 0,
    totalRevenue: 0,
  });
  const [recentOrders, setRecentOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    setLoading(true);
    setError('');
    
    try {
      // Load products
      const products = await productsAPI.getAll();
      const spareParts = products.filter(p => p.category !== 'Water Wash' && p.active);
      const totalStock = spareParts.reduce((sum, p) => sum + p.stock, 0);
      const lowStock = spareParts.filter(p => p.stock < 10).length;

      // Load order statistics
      const orderStats = await ordersAPI.getStatistics();

      setStats({
        totalProducts: spareParts.length,
        totalStock,
        lowStockCount: lowStock,
        totalOrders: orderStats.total_orders || 0,
        totalRevenue: orderStats.total_revenue || 0,
      });

      // Set recent orders
      if (orderStats.recent_orders) {
        setRecentOrders(orderStats.recent_orders.slice(0, 5));
      }
    } catch (error) {
      console.error('Failed to load dashboard data:', error);
      setError('Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    clearAuth();
    navigate('/login');
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="spinner"></div>
        <p className="loading-text">Loading admin dashboard...</p>
      </div>
    );
  }

  return (
    <div className="dashboard-container">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="sidebar-brand">
          <div className="sidebar-brand-icon">F</div>
          <div className="sidebar-brand-text">FIXXY</div>
        </div>

        <p className="text-muted" style={{ fontSize: '0.75rem', marginBottom: 'var(--spacing-xl)', paddingLeft: 'var(--spacing-sm)' }}>
          ADMIN PANEL
        </p>

        <nav className="sidebar-nav">
          <div className="sidebar-section-title">ADMIN</div>
          
          <a href="/admin" className="sidebar-link active">
            <span>📊</span>
            <span>Dashboard</span>
          </a>
          <a href="/admin/products" className="sidebar-link">
            <span>📦</span>
            <span>Products</span>
          </a>
          <a href="/admin/inventory" className="sidebar-link">
            <span>📋</span>
            <span>Inventory</span>
          </a>
          <a href="/admin/orders" className="sidebar-link">
            <span>🛒</span>
            <span>Orders</span>
          </a>
          <a href="/admin/coupons" className="sidebar-link">
            <span>🎫</span>
            <span>Coupons</span>
          </a>
          <a href="/admin/settings" className="sidebar-link">
            <span>⚙</span>
            <span>Settings</span>
          </a>

          <div className="sidebar-section-title" style={{ marginTop: 'var(--spacing-xl)' }}>CUSTOMER VIEW</div>
          
          <a href="/dashboard" className="sidebar-link">
            <span>👤</span>
            <span>Customer Dashboard</span>
          </a>
        </nav>

        <button onClick={handleLogout} className="btn btn-secondary" style={{ width: '100%', marginTop: 'auto' }}>
          ↪ Logout
        </button>
      </aside>

      {/* Main Content */}
      <main className="main-content">
        <div className="page-header">
          <div>
            <h1 className="page-title">Admin Dashboard</h1>
            <p className="page-subtitle">Welcome back, {user?.full_name}! Manage your FIXXY store.</p>
          </div>
          <div className="badge badge-danger" style={{ fontSize: '0.875rem', padding: '0.5rem 1rem' }}>
            🔐 ADMIN
          </div>
        </div>

        {error && (
          <div className="alert alert-error">
            {error}
          </div>
        )}

        {/* Statistics Grid */}
        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-label">Total Products</div>
            <div className="stat-value">{stats.totalProducts}</div>
            <div className="stat-description">Active spare parts</div>
          </div>

          <div className="stat-card green">
            <div className="stat-label">Total Stock</div>
            <div className="stat-value">{stats.totalStock}</div>
            <div className="stat-description">Units in inventory</div>
          </div>

          <div className="stat-card red">
            <div className="stat-label">Low Stock Items</div>
            <div className="stat-value">{stats.lowStockCount}</div>
            <div className="stat-description">Products below 10 units</div>
          </div>

          <div className="stat-card blue">
            <div className="stat-label">Total Orders</div>
            <div className="stat-value">{stats.totalOrders}</div>
            <div className="stat-description">All time orders</div>
          </div>

          <div className="stat-card">
            <div className="stat-label">Total Revenue</div>
            <div className="stat-value" style={{ fontSize: '1.75rem' }}>
              {formatCurrency(stats.totalRevenue)}
            </div>
            <div className="stat-description">Lifetime sales</div>
          </div>
        </div>

        {/* Recent Orders */}
        <div className="card" style={{ marginTop: 'var(--spacing-xl)' }}>
          <div className="card-header">
            <h3 className="card-title">Recent Orders</h3>
          </div>
          <div className="table-container">
            {recentOrders.length > 0 ? (
              <table>
                <thead>
                  <tr>
                    <th>Bill No</th>
                    <th>Customer</th>
                    <th>Total</th>
                    <th>Status</th>
                    <th>Date</th>
                  </tr>
                </thead>
                <tbody>
                  {recentOrders.map((order) => (
                    <tr key={order.id}>
                      <td><strong>{order.bill_no}</strong></td>
                      <td>{order.customer_name}</td>
                      <td><span className="text-orange">{formatCurrency(order.grand_total)}</span></td>
                      <td>
                        <span className="badge badge-success">{order.status}</span>
                      </td>
                      <td className="text-muted">{new Date(order.created_at).toLocaleDateString()}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : (
              <p className="text-muted" style={{ padding: 'var(--spacing-xl)', textAlign: 'center' }}>
                No orders yet
              </p>
            )}
          </div>
        </div>

        {/* Quick Actions */}
        <div className="card" style={{ marginTop: 'var(--spacing-xl)' }}>
          <div className="card-header">
            <h3 className="card-title">Quick Actions</h3>
          </div>
          <div className="grid grid-3">
            <div style={{ background: 'var(--panel2)', padding: 'var(--spacing-lg)', borderRadius: 'var(--radius)' }}>
              <h4 style={{ color: 'var(--orange)', marginBottom: 'var(--spacing-sm)' }}>📦 Add Product</h4>
              <p className="text-muted" style={{ fontSize: '0.875rem', marginBottom: 'var(--spacing-md)' }}>
                Add new spare parts to inventory
              </p>
              <button className="btn btn-primary" onClick={() => navigate('/admin/products')}>
                Open Products →
              </button>
            </div>

            <div style={{ background: 'var(--panel2)', padding: 'var(--spacing-lg)', borderRadius: 'var(--radius)' }}>
              <h4 style={{ color: 'var(--green)', marginBottom: 'var(--spacing-sm)' }}>📋 Update Stock</h4>
              <p className="text-muted" style={{ fontSize: '0.875rem', marginBottom: 'var(--spacing-md)' }}>
                Manage inventory levels
              </p>
              <button className="btn btn-success" onClick={() => navigate('/admin/inventory')}>
                Open Inventory →
              </button>
            </div>

            <div style={{ background: 'var(--panel2)', padding: 'var(--spacing-lg)', borderRadius: 'var(--radius)' }}>
              <h4 style={{ color: 'var(--blue)', marginBottom: 'var(--spacing-sm)' }}>🎫 Manage Coupons</h4>
              <p className="text-muted" style={{ fontSize: '0.875rem', marginBottom: 'var(--spacing-md)' }}>
                Create discount coupons
              </p>
              <button className="btn btn-primary" onClick={() => navigate('/admin/coupons')}>
                Open Coupons →
              </button>
            </div>
          </div>
        </div>

        {/* Admin Guide */}
        <div className="card" style={{ marginTop: 'var(--spacing-xl)' }}>
          <div className="card-header">
            <h3 className="card-title">Admin Features</h3>
          </div>
          <div className="card-body">
            <p className="text-muted">
              As an administrator, you have full access to manage the FIXXY store:
            </p>
            <ul style={{ color: 'var(--muted)', marginLeft: 'var(--spacing-lg)', lineHeight: '1.8', marginTop: 'var(--spacing-md)' }}>
              <li><strong>Products:</strong> Add, edit, and delete spare parts and services</li>
              <li><strong>Inventory:</strong> Track stock levels and identify low-stock items</li>
              <li><strong>Orders:</strong> View all customer orders and manage order status</li>
              <li><strong>Coupons:</strong> Create and manage discount coupons</li>
              <li><strong>Settings:</strong> Configure shop details, GST rates, and business information</li>
              <li><strong>Reports:</strong> Export sales and inventory data</li>
            </ul>
            <p className="text-muted" style={{ marginTop: 'var(--spacing-lg)' }}>
              <strong>Note:</strong> Admin pages are currently under development. Use the API documentation at 
              <a href="http://localhost:8000/docs" target="_blank" rel="noopener noreferrer" style={{ marginLeft: '0.25rem' }}>
                http://localhost:8000/docs
              </a> to test backend functionality.
            </p>
          </div>
        </div>
      </main>
    </div>
  );
}

export default AdminDashboard;
