/**
 * Formatting utilities
 */

export const formatCurrency = (value) => {
  return `₹${parseFloat(value).toLocaleString('en-IN', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  })}`;
};

export const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-IN', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  });
};

export const formatDateTime = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleString('en-IN', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
};

export const formatNumber = (value) => {
  return parseFloat(value).toLocaleString('en-IN');
};

export const calculateGST = (amount, gstRate = 18) => {
  return (amount * gstRate) / 100;
};

export const calculateTotal = (subtotal, discount = 0, gstRate = 18) => {
  const discountAmount = (subtotal * discount) / 100;
  const taxableAmount = subtotal - discountAmount;
  const gst = calculateGST(taxableAmount, gstRate);
  const total = taxableAmount + gst;
  
  return {
    subtotal,
    discount: discountAmount,
    taxableAmount,
    gst,
    total,
  };
};
