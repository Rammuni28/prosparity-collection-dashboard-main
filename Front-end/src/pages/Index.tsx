import { useState, useMemo, useEffect } from "react";
import { Application, generateMockApplications, mockFilterOptions, delay } from '@/services/mockData';
import ApplicationDetailsPanel from "@/components/ApplicationDetailsPanel";
import AppHeader from "@/components/layout/AppHeader";
import FiltersSection from "@/components/layout/FiltersSection";
import MainContent from "@/components/layout/MainContent";
import PWAInstallPrompt from "@/components/PWAInstallPrompt";
import StatusCards from "@/components/StatusCards";
import { ApplicationTableSkeleton, StatusCardsSkeleton } from "@/components/LoadingStates";

const PAGE_SIZE = 20;

const Index = () => {
  const [currentPage, setCurrentPage] = useState(1);
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedApplication, setSelectedApplication] = useState<Application | null>(null);
  const [applications, setApplications] = useState<Application[]>([]);
  const [loading, setLoading] = useState(true);
  const [filterOptions, setFilterOptions] = useState<any>(null);

  // Add basic state management for filters
  const [filters, setFilters] = useState({
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
  const [selectedEmiMonthRaw, setSelectedEmiMonthRaw] = useState<string>('Aug-24');
  const emiMonthOptions = ['Jul-24', 'Aug-24', 'Sep-24'];
  
  const handleEmiMonthChange = (month: string) => {
    setSelectedEmiMonthRaw(month);
  };

  const availableOptions = {
    branches: mockFilterOptions.branches,
    teamLeads: mockFilterOptions.teamLeads,
    rms: mockFilterOptions.rms,
    dealers: mockFilterOptions.dealers,
    lenders: mockFilterOptions.lenders,
    statuses: mockFilterOptions.statuses,
    emiMonths: emiMonthOptions,
    repayments: ['Yes', 'No'],
    lastMonthBounce: ['Yes', 'No'],
    ptpDateOptions: ['This Week', 'Next Week', 'This Month'],
    vehicleStatusOptions: ['Available', 'Not Available']
  };
  const filtersLoading = false;
  
  const handleFilterChange = (key: string, values: string[]) => {
    setFilters(prev => ({ ...prev, [key]: values }));
  };
  
  const clearAllFilters = () => {
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
  };

  // Always extract selectedEmiMonth as a single value (for mobile multi-select compatibility)
  const selectedEmiMonth = Array.isArray(filters.emiMonth) && filters.emiMonth.length > 0
    ? filters.emiMonth[0]
    : selectedEmiMonthRaw || null;

  // Reset page when search term or filters change
  useEffect(() => {
    setCurrentPage(1);
  }, [searchTerm, filters, selectedEmiMonth]);

  useEffect(() => {
    const loadData = async () => {
      setLoading(true);
      await delay(1000); // Simulate loading
      const data = generateMockApplications();
      setApplications(data);
      setLoading(false);
    };
    
    loadData();
  }, []);

  // Apply filters and search
  useEffect(() => {
    let filtered = applications;
    
    // Apply search
    if (searchTerm) {
      filtered = filtered.filter(app => 
        app.applicant_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        app.branch_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        app.rm_name.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }
    
    // Apply filters
    if (filters.branch.length > 0) {
      filtered = filtered.filter(app => filters.branch.includes(app.branch_name));
    }
    if (filters.teamLead.length > 0) {
      filtered = filtered.filter(app => filters.teamLead.includes(app.team_lead));
    }
    if (filters.rm.length > 0) {
      filtered = filtered.filter(app => filters.rm.includes(app.rm_name));
    }
    if (filters.dealer.length > 0) {
      filtered = filtered.filter(app => filters.dealer.includes(app.dealer_name));
    }
    if (filters.lender.length > 0) {
      filtered = filtered.filter(app => filters.lender.includes(app.lender_name));
    }
    if (filters.status.length > 0) {
      filtered = filtered.filter(app => filters.status.includes(app.status));
    }
    
    // Update filtered applications for display
    setFilteredApplications(filtered);
  }, [applications, filters, searchTerm]);

  const [filteredApplications, setFilteredApplications] = useState<Application[]>([]);

  const handleApplicationDeleted = () => {
    // Refetch data
    const loadData = async () => {
      const data = generateMockApplications();
      setApplications(data);
    };
    loadData();
    setSelectedApplication(null);
  };

  const handleApplicationUpdated = (updatedApp: Application) => {
    setSelectedApplication(updatedApp);
    // Refetch data
    const loadData = async () => {
      const data = generateMockApplications();
      setApplications(data);
    };
    loadData();
  };

  const handleDataChanged = async () => {
    // Refetch data
    const loadData = async () => {
      const data = generateMockApplications();
      setApplications(data);
    };
    await loadData();
    if (selectedApplication) {
      const updatedApp = applications.find(app => app.id === selectedApplication.id);
      if (updatedApp) {
        setSelectedApplication(updatedApp);
      }
    }
  };

  const handleApplicationSelect = (app: Application) => {
    setSelectedApplication(app);
  };

  const handleApplicationClose = () => {
    setSelectedApplication(null);
  };

  const handleExportFull = async () => {
    try {
      console.log('Preparing full report...');
      
      const exportData = {
        applications: filteredApplications
      };

      // Simulate export
      await delay(1000);
      console.log('Full report exported successfully!');
      alert('Full report exported successfully!');
    } catch (error) {
      console.error('Export error:', error);
      alert('Failed to export data');
    }
  };

  const handleExportPtpComments = async () => {
    try {
      console.log('Preparing PTP + Comments report...');
      
      const exportData = {
        applications: filteredApplications
      };

      // Simulate export
      await delay(1000);
      console.log('PTP + Comments report exported successfully!');
      alert('PTP + Comments report exported successfully!');
    } catch (error) {
      console.error('Export error:', error);
      alert('Failed to export data');
    }
  };

  const handleExportPlanVsAchievement = async (plannedDateTime: Date) => {
    try {
      console.log('Preparing Plan vs Achievement report...');
      
      // Simulate export
      await delay(1000);
      console.log(`Plan vs Achievement report exported successfully! Found ${filteredApplications.length} applications.`);
      alert(`Plan vs Achievement report exported successfully! Found ${filteredApplications.length} applications.`);
    } catch (error) {
      console.error('Plan vs Achievement export error:', error);
      alert('Failed to export Plan vs Achievement data');
    }
  };

  // Calculate status counts for status cards
  const statusCounts = useMemo(() => {
    const total = filteredApplications.length;
    const statusUnpaid = filteredApplications.filter(app => app.status === 'Unpaid').length;
    const statusPartiallyPaid = filteredApplications.filter(app => app.status === 'Partially Paid').length;
    const statusCashCollected = filteredApplications.filter(app => app.status === 'Cash Collected').length;
    const statusCustomerDeposited = filteredApplications.filter(app => app.status === 'Customer Deposited').length;
    const statusPaid = filteredApplications.filter(app => app.status === 'Paid').length;
    const statusPendingApproval = 0; // Mock data doesn't have this

    return {
      total,
      statusUnpaid,
      statusPartiallyPaid,
      statusCashCollected,
      statusCustomerDeposited,
      statusPaid,
      statusPendingApproval
    };
  }, [filteredApplications]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen bg-gray-50">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 sm:py-6 lg:py-8">
        <div className="space-y-4 sm:space-y-6">
          <AppHeader 
            onExportFull={handleExportFull}
            onExportPtpComments={handleExportPtpComments}
            onExportPlanVsAchievement={handleExportPlanVsAchievement}
          />

          <FiltersSection
            filters={filters}
            availableOptions={availableOptions}
            onFilterChange={handleFilterChange}
            searchTerm={searchTerm}
            onSearchChange={setSearchTerm}
            selectedEmiMonth={selectedEmiMonth}
            onEmiMonthChange={handleEmiMonthChange}
            emiMonthOptions={emiMonthOptions}
            loading={filtersLoading}
            searchLoading={loading}
            totalCount={filteredApplications.length}
          />

          <StatusCards statusCounts={statusCounts} />

          {/* Main Table - show the applications list */}
          <MainContent
            applications={filteredApplications}
            onRowClick={handleApplicationSelect}
            onApplicationDeleted={handleApplicationDeleted}
            selectedApplicationId={selectedApplication?.id}
            currentPage={currentPage}
            totalPages={Math.ceil((filteredApplications.length || 1) / PAGE_SIZE)}
            onPageChange={setCurrentPage}
            totalCount={filteredApplications.length}
            pageSize={PAGE_SIZE}
            selectedEmiMonth={selectedEmiMonth}
          />
        </div>
      </div>

      <PWAInstallPrompt />

      {/* Application Details Side Panel */}
      {selectedApplication && (
        <>
          <div 
            className="fixed inset-0 bg-black bg-opacity-50 z-40"
            onClick={handleApplicationClose}
          />
          <div className="fixed inset-y-0 right-0 w-[95%] sm:w-96 lg:w-[500px] z-50">
            <ApplicationDetailsPanel
              application={selectedApplication}
              onClose={handleApplicationClose}
              onSave={handleApplicationUpdated}
              onDataChanged={handleDataChanged}
              selectedEmiMonth={selectedEmiMonth}
            />
          </div>
        </>
      )}
    </div>
  );
};

export default Index;
