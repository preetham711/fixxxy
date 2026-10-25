import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { authAPI } from '../services/api';
import { saveAuth } from '../utils/auth';

function Login({ onLogin }) {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleRoleSelection = async (role) => {
    setLoading(true);
    setError('');

    try {
      // Auto-login based on role selection
      const credentials = role === 'admin' 
        ? { username: 'admin', password: 'admin123' }
        : { username: 'customer', password: 'customer123' };
      
      const response = await authAPI.login(credentials.username, credentials.password);
      
      // Save authentication data
      saveAuth(response.access_token, response.user);
      
      // Update parent component
      if (onLogin) {
        onLogin();
      }
      
      // Redirect based on role
      if (role === 'admin') {
        navigate('/admin');
      } else {
        navigate('/dashboard');
      }
    } catch (err) {
      console.error('Login error:', err);
      setError(`Failed to login as ${role}. Please ensure backend is running.`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container" style={{ flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
      <div style={{ maxWidth: '800px', width: '100%', textAlign: 'center', padding: '3rem' }}>
        {/* FIXXY Logo */}
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '1rem', marginBottom: '1rem' }}>
          <div style={{ 
            width: '80px', 
            height: '80px', 
            background: 'var(--orange)', 
            borderRadius: '20px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: '48px',
            fontWeight: 'bold',
            color: 'white'
          }}>
            F
          </div>
          <div style={{ fontSize: '4rem', fontWeight: '700', color: 'var(--orange)' }}>
            FIXXY
          </div>
        </div>
        
        <p style={{ fontSize: '1.5rem', color: 'var(--muted)', marginBottom: '1rem' }}>
          Drive Better • Fix Smarter
        </p>

        <h1 style={{ fontSize: '2.5rem', marginBottom: '1rem', marginTop: '3rem' }}>
          CAR SPARE PARTS &<br />BILLING SYSTEM
        </h1>
        
        <p className="text-muted" style={{ fontSize: '1.2rem', marginBottom: '4rem' }}>
          Select your access level to continue
        </p>

        {error && (
          <div className="alert alert-error" style={{ marginBottom: '2rem', maxWidth: '600px', margin: '0 auto 2rem' }}>
            {error}
          </div>
        )}

        {/* Role Selection Buttons */}
        <div style={{ 
          display: 'grid', 
          gridTemplateColumns: 'repeat(2, 1fr)', 
          gap: '2rem',
          maxWidth: '700px',
          margin: '0 auto'
        }}>
          {/* Customer Button */}
          <div 
            onClick={() => !loading && handleRoleSelection('customer')}
            style={{
              background: 'var(--panel)',
              padding: '3rem 2rem',
              borderRadius: '15px',
              cursor: loading ? 'not-allowed' : 'pointer',
              transition: 'all 0.3s ease',
              border: '3px solid transparent',
              opacity: loading ? 0.6 : 1
            }}
            onMouseEnter={(e) => {
              if (!loading) {
                e.currentTarget.style.transform = 'translateY(-8px)';
                e.currentTarget.style.borderColor = 'var(--green)';
                e.currentTarget.style.boxShadow = '0 8px 24px rgba(67, 197, 138, 0.3)';
              }
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = 'translateY(0)';
              e.currentTarget.style.borderColor = 'transparent';
              e.currentTarget.style.boxShadow = 'none';
            }}
          >
            <div style={{ fontSize: '4rem', marginBottom: '1rem' }}>👤</div>
            <h2 style={{ fontSize: '2rem', marginBottom: '1rem', color: 'var(--green)' }}>
              CUSTOMER
            </h2>
            <p className="text-muted" style={{ fontSize: '1rem', lineHeight: '1.6' }}>
              Browse spare parts<br />
              Place orders<br />
              Track purchases<br />
              Water wash services
            </p>
          </div>

          {/* Admin Button */}
          <div 
            onClick={() => !loading && handleRoleSelection('admin')}
            style={{
              background: 'var(--panel)',
              padding: '3rem 2rem',
              borderRadius: '15px',
              cursor: loading ? 'not-allowed' : 'pointer',
              transition: 'all 0.3s ease',
              border: '3px solid transparent',
              opacity: loading ? 0.6 : 1
            }}
            onMouseEnter={(e) => {
              if (!loading) {
                e.currentTarget.style.transform = 'translateY(-8px)';
                e.currentTarget.style.borderColor = 'var(--orange)';
                e.currentTarget.style.boxShadow = '0 8px 24px rgba(255, 121, 24, 0.3)';
              }
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = 'translateY(0)';
              e.currentTarget.style.borderColor = 'transparent';
              e.currentTarget.style.boxShadow = 'none';
            }}
          >
            <div style={{ fontSize: '4rem', marginBottom: '1rem' }}>🔐</div>
            <h2 style={{ fontSize: '2rem', marginBottom: '1rem', color: 'var(--orange)' }}>
              ADMIN
            </h2>
            <p className="text-muted" style={{ fontSize: '1rem', lineHeight: '1.6' }}>
              Manage products<br />
              Control inventory<br />
              View all orders<br />
              Business analytics
            </p>
          </div>
        </div>

        {loading && (
          <div style={{ marginTop: '2rem' }}>
            <div className="spinner" style={{ margin: '0 auto' }}></div>
            <p className="text-muted" style={{ marginTop: '1rem' }}>Loading dashboard...</p>
          </div>
        )}

        <p className="text-muted" style={{ fontSize: '0.875rem', marginTop: '3rem' }}>
          Demo application for school project<br />
          Auto-login enabled for testing
        </p>
      </div>
    </div>
  );
}

export default Login;
