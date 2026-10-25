/**
 * Products Page - Browse and search spare parts
 * Displays product catalogue with search and category filter
 */
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { productsAPI } from '../services/api';
import { formatCurrency } from '../utils/format';
import Sidebar from '../components/Sidebar';

function Products() {
  const navigate = useNavigate();
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [cart, setCart] = useState([]);

  useEffect(() => {
    loadData();
    loadCartFromStorage();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const [productsData, categoriesData] = await Promise.all([
        productsAPI.getAll(),
        productsAPI.getCategories()
      ]);
      
      // Filter out Water Wash products (they have separate page)
      const spareParts = productsData.filter(p => p.category !== 'Water Wash');
      setProducts(spareParts);
      setCategories(categoriesData);
    } catch (error) {
      console.error('Failed to load products:', error);
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

  const addToCart = (product) => {
    const existingItem = cart.find(item => item.id === product.id);
    let newCart;

    if (existingItem) {
      newCart = cart.map(item =>
        item.id === product.id
          ? { ...item, quantity: item.quantity + 1 }
          : item
      );
    } else {
      newCart = [...cart, { ...product, quantity: 1 }];
    }

    setCart(newCart);
    saveCartToStorage(newCart);
  };

  const getCartQuantity = (productId) => {
    const item = cart.find(i => i.id === productId);
    return item ? item.quantity : 0;
  };

  // Filter products
  const filteredProducts = products.filter(product => {
    const matchesSearch = product.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         product.sku.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = selectedCategory === 'all' || product.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  if (loading) {
    return (
      <div className="loading-container">
        <div className="spinner"></div>
        <p className="loading-text">Loading products...</p>
      </div>
    );
  }

  return (
    <div className="dashboard-container">
      <Sidebar />

      <main className="main-content">
        <div className="page-header">
          <div>
            <h1 className="page-title">Spare Parts Catalogue</h1>
            <p className="page-subtitle">Browse and add products to your cart</p>
          </div>
          <button 
            className="btn btn-primary"
            onClick={() => navigate('/cart')}
          >
            🛒 Cart ({cart.reduce((sum, item) => sum + item.quantity, 0)})
          </button>
        </div>

        {/* Search and Filter */}
        <div className="card" style={{ marginBottom: 'var(--spacing-lg)' }}>
          <div className="card-body">
            <div style={{ display: 'flex', gap: 'var(--spacing-md)', flexWrap: 'wrap' }}>
              <input
                type="text"
                className="input"
                placeholder="🔍 Search by name or SKU..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                style={{ flex: '1', minWidth: '250px' }}
              />
              
              <select
                className="input"
                value={selectedCategory}
                onChange={(e) => setSelectedCategory(e.target.value)}
                style={{ minWidth: '200px' }}
              >
                <option value="all">All Categories</option>
                {categories
                  .filter(cat => cat !== 'Water Wash')
                  .map(cat => (
                    <option key={cat} value={cat}>{cat}</option>
                  ))
                }
              </select>

              {(searchTerm || selectedCategory !== 'all') && (
                <button
                  className="btn btn-secondary"
                  onClick={() => {
                    setSearchTerm('');
                    setSelectedCategory('all');
                  }}
                >
                  Clear Filters
                </button>
              )}
            </div>
          </div>
        </div>

        {/* Products Grid */}
        {filteredProducts.length === 0 ? (
          <div className="card">
            <div className="card-body" style={{ textAlign: 'center', padding: 'var(--spacing-xxl)' }}>
              <p className="text-muted">No products found.</p>
            </div>
          </div>
        ) : (
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: 'var(--spacing-lg)' }}>
            {filteredProducts.map(product => (
              <div key={product.id} className="card" style={{ display: 'flex', flexDirection: 'column' }}>
                <div className="card-body" style={{ flex: 1 }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: 'var(--spacing-md)' }}>
                    <div>
                      <h3 style={{ color: 'var(--text)', fontSize: '1.125rem', marginBottom: '0.25rem' }}>
                        {product.name}
                      </h3>
                      <p className="text-muted" style={{ fontSize: '0.75rem' }}>
                        SKU: {product.sku}
                      </p>
                    </div>
                    <span className={`badge ${product.stock > 10 ? 'badge-success' : product.stock > 0 ? 'badge-warning' : 'badge-error'}`}>
                      {product.stock > 0 ? `${product.stock} in stock` : 'Out of stock'}
                    </span>
                  </div>

                  {product.description && (
                    <p className="text-muted" style={{ fontSize: '0.875rem', marginBottom: 'var(--spacing-md)', lineHeight: '1.5' }}>
                      {product.description}
                    </p>
                  )}

                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: 'auto', paddingTop: 'var(--spacing-md)', borderTop: '1px solid var(--border)' }}>
                    <div>
                      <div style={{ fontSize: '1.5rem', fontWeight: '600', color: 'var(--orange)' }}>
                        {formatCurrency(product.price)}
                      </div>
                      {product.category && (
                        <div className="text-muted" style={{ fontSize: '0.75rem' }}>
                          {product.category}
                        </div>
                      )}
                    </div>
                    
                    {product.stock > 0 ? (
                      <button
                        className="btn btn-primary"
                        onClick={() => addToCart(product)}
                        style={{ minWidth: '100px' }}
                      >
                        {getCartQuantity(product.id) > 0 
                          ? `Add More (${getCartQuantity(product.id)})` 
                          : '+ Add to Cart'}
                      </button>
                    ) : (
                      <button className="btn btn-secondary" disabled>
                        Out of Stock
                      </button>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}

export default Products;
