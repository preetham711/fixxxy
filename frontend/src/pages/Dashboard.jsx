import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getUser } from '../utils/auth';
import { productsAPI } from '../services/api';
import Sidebar from '../components/Sidebar';

function Dashboard() {
  const navigate = useNavigate();
  const user = getUser();
  const [stats, setStats] = useState({
    totalProducts: 0,
    totalStock: 0,
    waterWashServices: 0,
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      const products = await productsAPI.getAll();
      const spareParts = products.filter(p => p.category !== 'Water Wash');
      const waterWash = products.filter(p => p.category === 'Water Wash');
      const totalStock = spareParts.reduce((sum, p) => sum + p.stock, 0);

      setStats({
        totalProducts: spareParts.length,
        totalStock,
        waterWashServices: waterWash.length,
      });
    } catch (error) {
      console.error('Failed to load stats:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="spinner"></div>
        <p className="loading-text">Loading dashboard...</p>
      </div>
    );
  }

  return (
    <div className="dashboard-container">
      <Sidebar />

      {/* Main Content */}
      <main className="main-content">
        <div className="page-header">
          <div>
            <h1 className="page-title">Dashboard</h1>
            <p className="page-subtitle">Welcome back, {user?.full_name || 'User'}!</p>
          </div>
          <div className="text-muted">● {user?.role || 'customer'}</div>
        </div>

        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-label">Spare Parts</div>
            <div className="stat-value">{stats.totalProducts}</div>
            <div className="stat-description">Browse the catalogue</div>
          </div>

          <div className="stat-card green">
            <div className="stat-label">Units Available</div>
            <div className="stat-value">{stats.totalStock}</div>
            <div className="stat-description">Current parts stock</div>
          </div>

          <div className="stat-card blue">
            <div className="stat-label">Wash Packages</div>
            <div className="stat-value">{stats.waterWashServices}</div>
            <div className="stat-description">Care for your car</div>
          </div>
        </div>

        <div className="card">
          <div className="card-header">
            <h3 className="card-title">Quick Actions</h3>
          </div>
          <div className="grid grid-2">
            <div style={{ background: 'var(--panel2)', padding: 'var(--spacing-lg)', borderRadius: 'var(--radius)' }}>
              <h4 style={{ color: 'var(--orange)', marginBottom: 'var(--spacing-sm)' }}>Find Parts</h4>
              <p className="text-muted" style={{ fontSize: '0.875rem', marginBottom: 'var(--spacing-md)' }}>
                Visual spare-parts catalogue
              </p>
              <button className="btn btn-primary" onClick={() => navigate('/products')}>Open →</button>
            </div>

            <div style={{ background: 'var(--panel2)', padding: 'var(--spacing-lg)', borderRadius: 'var(--radius)' }}>
              <h4 style={{ color: 'var(--orange)', marginBottom: 'var(--spacing-sm)' }}>Water Wash</h4>
              <p className="text-muted" style={{ fontSize: '0.875rem', marginBottom: 'var(--spacing-md)' }}>
                Foam wash, full clean and more
              </p>
              <button className="btn btn-primary" onClick={() => navigate('/waterwash')}>Open →</button>
            </div>
          </div>
        </div>

        <div className="card" style={{ marginTop: 'var(--spacing-xl)' }}>
          <div className="card-header">
            <h3 className="card-title">Getting Started</h3>
          </div>
          <div className="card-body">
            <p className="text-muted">
              This is your FIXXY dashboard. Use the sidebar to navigate between different sections.
            </p>
            <ul style={{ color: 'var(--muted)', marginLeft: 'var(--spacing-lg)', lineHeight: '1.8' }}>
              <li><strong>Find Parts:</strong> Browse and search for car spare parts</li>
              <li><strong>Water Wash:</strong> Book professional car wash services</li>
              <li><strong>Cart & Billing:</strong> Review your cart and place orders</li>
              <li><strong>Orders:</strong> View your order history and invoices</li>
              {user?.role === 'admin' && <li><strong>Admin Tools:</strong> Manage products, inventory, and coupons</li>}
            </ul>
          </div>
        </div>
      </main>
    </div>
  );
}

export default Dashboard;
