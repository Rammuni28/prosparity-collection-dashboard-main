import { useState, useEffect, useCallback, useRef } from 'react';
import { supabase, getCollectionsSummary } from '@/integrations/api/client';
import { useAuth } from '@/hooks/useAuth';
import { FilterState } from '@/types/filters';
import { getMonthDateRange, monthToEmiDate } from '@/utils/dateUtils';
import { useFieldStatusManager } from '@/hooks/useFieldStatusManager';

interface StatusCounts {
  total: number;
  statusUnpaid: number;
  statusPartiallyPaid: number;
  statusCashCollected: number;
  statusCustomerDeposited: number;
  statusPaid: number;
  statusPendingApproval: number;
}

interface UseStatusCountsProps {
  filters: FilterState;
  selectedEmiMonth?: string | null;
  searchTerm?: string;
}

export const useStatusCounts = ({ filters, selectedEmiMonth, searchTerm = '' }: UseStatusCountsProps) => {
  const { user } = useAuth();
  const { fetchFieldStatus } = useFieldStatusManager();
  const [statusCounts, setStatusCounts] = useState<StatusCounts>({
    total: 0,
    statusUnpaid: 0,
    statusPartiallyPaid: 0,
    statusCashCollected: 0,
    statusCustomerDeposited: 0,
    statusPaid: 0,
    statusPendingApproval: 0
  });
  const [loading, setLoading] = useState(false);
  const abortControllerRef = useRef<AbortController | null>(null);
  const lastRequestRef = useRef<string>('');

  const validateInputs = useCallback((month?: string | null): boolean => {
    if (!user) {
      console.warn('❌ No user for status counts');
      return false;
    }
    if (!month) {
      console.warn('❌ No selected EMI month for status counts');
      return false;
    }
    return true;
  }, [user]);

  const isOnlyEmiMonthFilter = (filters: FilterState) => {
    // All filters except emiMonth should be empty
    return Object.entries(filters).every(([key, value]) => {
      if (key === 'emiMonth') return true;
      return Array.isArray(value) && value.length === 0;
    });
  };

  const fetchStatusCounts = useCallback(async () => {
    if (!validateInputs(selectedEmiMonth)) {
      setStatusCounts({
        total: 0,
        statusUnpaid: 0,
        statusPartiallyPaid: 0,
        statusCashCollected: 0,
        statusCustomerDeposited: 0,
        statusPaid: 0,
        statusPendingApproval: 0
      });
      setLoading(false);
      return;
    }
    
    setLoading(true);
    try {
      // Always use FastAPI backend summary
      const summary = await getCollectionsSummary(selectedEmiMonth!);
      // Map backend keys to StatusCounts
      setStatusCounts({
        total: summary.total || 0,
        statusUnpaid: summary.unpaid || 0,
        statusPartiallyPaid: summary.partially_paid || 0,
        statusCashCollected: summary.cash_collected || 0,
        statusCustomerDeposited: summary.customer_deposited || 0,
        statusPaid: summary.paid || 0,
        statusPendingApproval: summary.paid_pending_approval || 0
      });
    } catch (error) {
      console.error('Error fetching status counts:', error);
      setStatusCounts({
        total: 0,
        statusUnpaid: 0,
        statusPartiallyPaid: 0,
        statusCashCollected: 0,
        statusCustomerDeposited: 0,
        statusPaid: 0,
        statusPendingApproval: 0
      });
    } finally {
      setLoading(false);
    }
  }, [selectedEmiMonth, validateInputs]);

  // Effect with proper cleanup
  useEffect(() => {
    const timeoutId = setTimeout(() => {
      fetchStatusCounts();
    }, 300); // Debounce requests

    return () => {
      clearTimeout(timeoutId);
      if (abortControllerRef.current) {
        abortControllerRef.current.abort();
      }
    };
  }, [fetchStatusCounts]);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (abortControllerRef.current) {
        abortControllerRef.current.abort();
      }
    };
  }, []);

  return {
    statusCounts,
    loading,
    refetch: fetchStatusCounts
  };
};
