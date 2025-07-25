
import { format } from "date-fns";

export const formatEmiMonth = (dateStr?: string) => {
  if (!dateStr) return '';
  // If already in 'Mon-YY' format, return as is
  if (/^[A-Za-z]{3}-\d{2}$/.test(dateStr)) return dateStr;
  try {
    const date = new Date(dateStr);
    if (isNaN(date.getTime())) return dateStr;
    const month = date.toLocaleString('en-US', { month: 'short' });
    const year = date.getFullYear().toString().slice(-2);
    return `${month}-${year}`;
  } catch {
    return dateStr;
  }
};

export const formatPhoneLink = (phone?: string) => {
  if (!phone) return null;
  // Remove any non-digit characters except +
  const cleanPhone = phone.replace(/[^\d+]/g, '');
  return `tel:${cleanPhone}`;
};

export const formatCurrency = (amount: number) => {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(amount);
};

// Optimized PTP date formatter with consistent output
export const formatPtpDate = (ptpDateStr?: string | null) => {
  if (!ptpDateStr) return "Not Set";
  // If already in DD-MMM-YY format, return as is
  if (/^\d{2}-[A-Za-z]{3}-\d{2}$/.test(ptpDateStr)) return ptpDateStr;
  try {
    // Try parsing as YY-MM-DD
    if (/^\d{2}-\d{2}-\d{2}$/.test(ptpDateStr)) {
      const [yy, mm, dd] = ptpDateStr.split('-');
      const date = new Date(`20${yy}-${mm}-${dd}`);
      if (!isNaN(date.getTime())) {
        return date.toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: '2-digit' }).replace(/ /g, '-');
      }
    }
    // Fallback: try Date constructor
    const date = new Date(ptpDateStr);
    if (!isNaN(date.getTime())) {
      return date.toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: '2-digit' }).replace(/ /g, '-');
    }
    return ptpDateStr;
  } catch {
    return ptpDateStr;
  }
};

export const formatMapLocation = (fiLocation?: string) => {
  if (!fiLocation) return null;
  
  // Remove "FI_PENDING " prefix if it exists
  const cleanLocation = fiLocation.replace(/^FI_PENDING\s+/i, '').trim();
  
  if (!cleanLocation) return null;
  
  // Create Google Maps URL
  const encodedLocation = encodeURIComponent(cleanLocation);
  return `https://www.google.com/maps/search/?api=1&query=${encodedLocation}`;
};
