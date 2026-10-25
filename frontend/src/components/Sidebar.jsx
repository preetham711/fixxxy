/**
 * Sidebar Component - Navigation menu for all pages
 * Shows different options based on user role
 */
import { useNavigate, useLocation } from 'react-router-dom';
import { getUser, clearAuth, isAdmin } from '../utils/auth';

function Sidebar() {
  const navigate = useNavigate();
  const location = useLocation();
  const user = getUser();

  const handleLogout = () => {
    clearAuth();
    navigate('/');
  };

  const isActive = (path) => location.pathname === path;

  return (
    <aside className="sidebar">
      <div className="sidebar-brand">
        <div className="sidebar-brand-icon">F</div>
        <div className="sidebar-brand-text">FIXXY</div>
      </div>

      <p className="text-muted" style={{ fontSize: '0.75rem', marginBottom: 'var(--spacing-xl)', paddingLeft: 'var(--spacing-sm)' }}>
        CAR CARE • PARTS • SERVICE
      </p>

      <nav className="sidebar-nav">
        <button
          onClick={() => navigate(isAdmin() ? '/admin' : '/dashboard')}
          className={`sidebar-link ${isActive('/dashboard') || isActive('/admin') ? 'active' : ''}`}
        >
          <span>⌂</span>
          <span>Dashboard</span>
        </button>
        
        <button
          onClick={() => navigate('/products')}
          className={`sidebar-link ${isActive('/products') ? 'active' : ''}`}
        >
          <span>⌕</span>
          <span>Find Parts</span>
        </button>
        
        <button
          onClick={() => navigate('/cart')}
          className={`sidebar-link ${isActive('/cart') ? 'active' : ''}`}
        >
          <span>▣</span>
          <span>Cart & Billing</span>
        </button>
        
        <button
          onClick={() => navigate('/waterwash')}
          className={`sidebar-link ${isActive('/waterwash') ? 'active' : ''}`}
        >
          <span>✦</span>
          <span>Water Wash</span>
        </button>
        
        <button
          onClick={() => navigate('/orders')}
          className={`sidebar-link ${isActive('/orders') ? 'active' : ''}`}
        >
          <span>▤</span>
          <span>Orders</span>
        </button>

        {isAdmin() && (
          <>
            <div className="sidebar-section-title">ADMIN TOOLS</div>
            <button
              onClick={() => navigate('/admin/products')}
              className={`sidebar-link ${isActive('/admin/products') ? 'active' : ''}`}
            >
              <span>⚙</span>
              <span>Manage Products</span>
            </button>
            <button
              onClick={() => navigate('/admin/coupons')}
              className={`sidebar-link ${isActive('/admin/coupons') ? 'active' : ''}`}
            >
              <span>✂</span>
              <span>Coupons</span>
            </button>
            <button
              onClick={() => navigate('/admin/reports')}
              className={`sidebar-link ${isActive('/admin/reports') ? 'active' : ''}`}
            >
              <span>📊</span>
              <span>Reports</span>
            </button>
          </>
        )}
      </nav>

      <div style={{ marginTop: 'auto', padding: 'var(--spacing-md)', borderTop: '1px solid var(--border)' }}>
        <div style={{ marginBottom: 'var(--spacing-md)', fontSize: '0.875rem' }}>
          <div style={{ color: 'var(--text)', fontWeight: '500' }}>{user?.full_name || 'User'}</div>
          <div className="text-muted" style={{ fontSize: '0.75rem' }}>
            {user?.role === 'admin' ? '● Administrator' : '● Customer'}
          </div>
        </div>
        <button onClick={handleLogout} className="btn btn-secondary" style={{ width: '100%' }}>
          ↪ Logout
        </button>
      </div>
    </aside>
  );
}

export default Sidebar;
