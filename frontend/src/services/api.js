/**
 * API Service
 * Axios instance with authentication and interceptors
 */
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor - Add auth token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor - Handle errors globally
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Unauthorized - clear token and redirect to login
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth methods
export const authAPI = {
  login: async (username, password) => {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);
    
    const response = await api.post('/api/auth/login', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  },
  
  register: async (userData) => {
    const response = await api.post('/api/auth/register', userData);
    return response.data;
  },
  
  getCurrentUser: async () => {
    const response = await api.get('/api/auth/me');
    return response.data;
  },
  
  logout: async () => {
    const response = await api.post('/api/auth/logout');
    return response.data;
  },
};

// Products methods
export const productsAPI = {
  getAll: async (params = {}) => {
    const response = await api.get('/api/products', { params });
    return response.data;
  },
  
  getById: async (id) => {
    const response = await api.get(`/api/products/${id}`);
    return response.data;
  },
  
  create: async (productData) => {
    const response = await api.post('/api/products', productData);
    return response.data;
  },
  
  update: async (id, productData) => {
    const response = await api.put(`/api/products/${id}`, productData);
    return response.data;
  },
  
  delete: async (id) => {
    const response = await api.delete(`/api/products/${id}`);
    return response.data;
  },
  
  updateStock: async (id, stock) => {
    const response = await api.patch(`/api/products/${id}/stock`, null, {
      params: { stock },
    });
    return response.data;
  },
  
  getCategories: async () => {
    const response = await api.get('/api/products/categories/from-products');
    return response.data;
  },
  
  getLowStock: async (threshold = 10) => {
    const response = await api.get('/api/products/low-stock/list', {
      params: { threshold },
    });
    return response.data;
  },
};

// Orders methods
export const ordersAPI = {
  getAll: async (params = {}) => {
    const response = await api.get('/api/orders', { params });
    return response.data;
  },
  
  getById: async (id) => {
    const response = await api.get(`/api/orders/${id}`);
    return response.data;
  },
  
  create: async (orderData) => {
    const response = await api.post('/api/orders', orderData);
    return response.data;
  },
  
  updateStatus: async (id, status) => {
    const response = await api.patch(`/api/orders/${id}/status`, { status });
    return response.data;
  },
  
  getStatistics: async () => {
    const response = await api.get('/api/orders/statistics/dashboard');
    return response.data;
  },
};

// Coupons methods
export const couponsAPI = {
  getAll: async (activeOnly = false) => {
    const response = await api.get('/api/coupons', {
      params: { active_only: activeOnly },
    });
    return response.data;
  },
  
  validate: async (code) => {
    const response = await api.post('/api/coupons/validate', { code });
    return response.data;
  },
  
  create: async (couponData) => {
    const response = await api.post('/api/coupons', couponData);
    return response.data;
  },
  
  update: async (id, couponData) => {
    const response = await api.put(`/api/coupons/${id}`, couponData);
    return response.data;
  },
  
  delete: async (id) => {
    const response = await api.delete(`/api/coupons/${id}`);
    return response.data;
  },
  
  toggle: async (id) => {
    const response = await api.patch(`/api/coupons/${id}/toggle`);
    return response.data;
  },
};

// Vehicles methods
export const vehiclesAPI = {
  getAll: async () => {
    const response = await api.get('/api/vehicles');
    return response.data;
  },
  
  getPrimary: async () => {
    const response = await api.get('/api/vehicles/primary/get');
    return response.data;
  },
  
  create: async (vehicleData) => {
    const response = await api.post('/api/vehicles', vehicleData);
    return response.data;
  },
  
  update: async (id, vehicleData) => {
    const response = await api.put(`/api/vehicles/${id}`, vehicleData);
    return response.data;
  },
  
  delete: async (id) => {
    const response = await api.delete(`/api/vehicles/${id}`);
    return response.data;
  },
};

// Settings methods
export const settingsAPI = {
  getAll: async () => {
    const response = await api.get('/api/settings');
    return response.data;
  },
  
  getPublic: async () => {
    const response = await api.get('/api/settings/public');
    return response.data;
  },
  
  update: async (key, value) => {
    const response = await api.put(`/api/settings/${key}`, {
      setting_value: value,
    });
    return response.data;
  },
};

export default api;
