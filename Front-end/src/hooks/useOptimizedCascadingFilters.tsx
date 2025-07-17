import { useState, useEffect, useCallback, useMemo } from 'react';
import { supabase } from '@/integrations/api/client';
import { useAuth } from '@/hooks/useAuth';
import { FilterState } from '@/types/filters';
import { useQueryCache } from './useQueryCache';
import { normalizeEmiMonth, groupDatesByMonth } from '@/utils/dateUtils';
import { VEHICLE_STATUS_OPTIONS, STATUS_FILTER_OPTIONS } from '@/constants/options';

interface CascadingFilterOptions {
  branches: string[];
  teamLeads: string[];
  rms: string[];
  dealers: string[];
  lenders: string[];
  statuses: string[];
  emiMonths: string[];
  repayments: string[];
  lastMonthBounce: string[];
  ptpDateOptions: string[];
  vehicleStatusOptions: string[];
}

export const useOptimizedCascadingFilters = () => {
  const { user } = useAuth();
  const { getCachedData, setCachedData } = useQueryCache<CascadingFilterOptions>();
  
  const [filters, setFilters] = useState<FilterState>({
    branch: [],
    teamLead: [],
    rm: [],
    dealer: [],
    lender: [],
    status: [],
    emiMonth: [],
    repayment: [],
    lastMonthBounce: [],
    ptpDate: [],
    vehicleStatus: []
  });

  const [availableOptions, setAvailableOptions] = useState<CascadingFilterOptions>({
    branches: [],
    teamLeads: [],
    rms: [],
    dealers: [],
    lenders: [],
    statuses: [],
    emiMonths: [],
    repayments: [],
    lastMonthBounce: ['Not paid', 'Paid on time', '1-5 days late', '6-15 days late', '15+ days late'],
    ptpDateOptions: ['overdue', 'today', 'tomorrow', 'future', 'no_date'],
    vehicleStatusOptions: VEHICLE_STATUS_OPTIONS.map(opt => opt.value)
  });

  // Hardcode EMI month options
  const emiMonthOptions = ['Jul-24'];
  const [selectedEmiMonth, setSelectedEmiMonth] = useState<string>('Jul-24');
  const [defaultEmiMonth, setDefaultEmiMonth] = useState<string>('Jul-24');
  const [loading, setLoading] = useState(false);

  // Remove or comment out fetchAllEmiMonths and any dynamic EMI month logic
  // Always return emiMonthOptions, selectedEmiMonth, defaultEmiMonth

  const buildFieldStatusQuery = useCallback((monthStart: string, monthEnd: string) => {
    try {
      const selectFields = ['status'].filter(Boolean).join(', ');
      
      return supabase
        .from('field_status')
        .select(selectFields)
        .gte('demand_date', monthStart)
        .lte('demand_date', monthEnd)
        .limit(2000);
    } catch (error) {
      console.error('Error building field status query:', error);
      return null;
    }
  }, []);

  // Optimized filter options fetch with status and PTP fixes
  const fetchFilterOptions = useCallback(async () => {
    if (!user || !selectedEmiMonth) return;

    const cacheKey = `filter-options-${selectedEmiMonth}-${JSON.stringify(filters)}`;
    const cached = getCachedData(cacheKey);
    
    if (cached) {
      console.log('Using cached filter options');
      setAvailableOptions(cached);
      return;
    }

    setLoading(true);
    try {
      console.log('Fetching filter options with improved error handling');

      const monthStart = `${selectedEmiMonth}-01`;
      const monthEnd = `${selectedEmiMonth}-31`;

      // Fetch collection and application data
      const { data: combinedData } = await supabase
        .from('collection')
        .select(`
          team_lead,
          rm_name,
          collection_rm,
          repayment,
          lms_status,
          applications!inner(
            branch_name,
            dealer_name,
            lender_name,
            vehicle_status
          )
        `)
        .gte('demand_date', monthStart)
        .lte('demand_date', monthEnd)
        .limit(5000);

      // Fetch field status with improved error handling
      let fieldStatusData: any[] = [];
      try {
        const fieldStatusQuery = buildFieldStatusQuery(monthStart, monthEnd);
        if (fieldStatusQuery) {
          const { data, error } = await fieldStatusQuery;
          if (error) {
            console.warn('⚠️ Field status query failed, continuing without field statuses:', error.message);
          } else {
            fieldStatusData = data || [];
          }
        }
      } catch (error) {
        console.warn('⚠️ Field status fetch failed, continuing without field statuses:', error);
      }

      console.log('Field status data fetched:', fieldStatusData.length);

      if (!combinedData) return;

      console.log(`Processing ${combinedData.length} combined records for filter options`);

      const options: CascadingFilterOptions = {
        branches: [...new Set(combinedData.map(item => item.applications?.branch_name).filter(Boolean))].sort(),
        teamLeads: [...new Set(combinedData.map(item => item.team_lead).filter(Boolean))].sort(),
        rms: [...new Set(combinedData.map(item => item.rm_name).filter(Boolean))].sort(),
        dealers: [...new Set(combinedData.map(item => item.applications?.dealer_name).filter(Boolean))].sort(),
        lenders: [...new Set(combinedData.map(item => item.applications?.lender_name).filter(Boolean))].sort(),
        repayments: [...new Set(combinedData.map(item => item.repayment).filter(Boolean))].sort(),
        emiMonths: [selectedEmiMonth],
        lastMonthBounce: ['Not paid', 'Paid on time', '1-5 days late', '6-15 days late', '15+ days late'],
        ptpDateOptions: ['overdue', 'today', 'tomorrow', 'future', 'no_date'],
        vehicleStatusOptions: VEHICLE_STATUS_OPTIONS.map(opt => opt.value),
        statuses: []
      };

      // Combine LMS status and field status values with error handling
      const lmsStatuses = [...new Set(combinedData.map(item => item.lms_status).filter(Boolean))];
      const fieldStatuses = [...new Set(fieldStatusData.map(s => s.status).filter(Boolean))];
      // Always show canonical status options in the filter dropdown
      options.statuses = STATUS_FILTER_OPTIONS;
      console.log('Available status options (canonical):', options.statuses);

      // Cache for 8 minutes
      setCachedData(cacheKey, options, 8 * 60 * 1000);
      setAvailableOptions(options);
      console.log('Filter options cached and set with', options.statuses.length, 'status options');

    } catch (error) {
      console.error('Error fetching cascading filter options:', error);
    } finally {
      setLoading(false);
    }
  }, [user, selectedEmiMonth, filters, getCachedData, setCachedData, buildFieldStatusQuery]);

  // Rest of the hook remains the same but with memoized callbacks
  const handleFilterChange = useCallback((key: string, values: string[]) => {
    console.log('Filter change:', key, values);
    setFilters(prev => ({
      ...prev,
      [key]: values
    }));
  }, []);

  const handleEmiMonthChange = useCallback((month: string) => {
    console.log('EMI month changed to:', month);
    setSelectedEmiMonth(month);
    setFilters({
      branch: [],
      teamLead: [],
      rm: [],
      dealer: [],
      lender: [],
      status: [],
      emiMonth: [],
      repayment: [],
      lastMonthBounce: [],
      ptpDate: [],
      vehicleStatus: []
    });
  }, []);

  const clearAllFilters = useCallback(() => {
    setFilters({
      branch: [],
      teamLead: [],
      rm: [],
      dealer: [],
      lender: [],
      status: [],
      emiMonth: [],
      repayment: [],
      lastMonthBounce: [],
      ptpDate: [],
      vehicleStatus: []
    });
  }, []);

  // Initialize EMI months on mount
  useEffect(() => {
    if (user) {
      // fetchAllEmiMonths(); // This line is removed as per the edit hint
    }
  }, [user]); // Removed fetchAllEmiMonths from dependency array

  // Debounced filter options fetch
  useEffect(() => {
    if (user && selectedEmiMonth) {
      const timeout = setTimeout(() => {
        fetchFilterOptions();
      }, 200);

      return () => clearTimeout(timeout);
    }
  }, [user, selectedEmiMonth, filters, fetchFilterOptions]);

  return {
    filters,
    availableOptions,
    handleFilterChange,
    clearAllFilters,
    selectedEmiMonth,
    handleEmiMonthChange: (month: string) => setSelectedEmiMonth(month),
    emiMonthOptions,
    defaultEmiMonth,
    loading
  };
};
