// Simple mock data for demonstration
export interface Application {
  id: string;
  applicant_name: string;
  branch_name: string;
  team_lead: string;
  rm_name: string;
  dealer_name: string;
  lender_name: string;
  status: string;
  emi_amount: number;
  ptp_date?: string;
  mobile?: string;
  address?: string;
}

// Generate mock applications
export const generateMockApplications = (): Application[] => {
  const branches = ['Mumbai Central', 'Andheri West', 'Bandra East', 'Thane', 'Navi Mumbai'];
  const teamLeads = ['Rajesh Kumar', 'Priya Sharma', 'Amit Patel', 'Neha Singh', 'Vikram Mehta'];
  const rms = ['Rahul Verma', 'Sneha Gupta', 'Arjun Reddy', 'Kavya Iyer', 'Dev Malhotra'];
  const dealers = ['ABC Motors', 'XYZ Auto', 'Premium Cars', 'Elite Motors', 'City Auto'];
  const lenders = ['HDFC Bank', 'ICICI Bank', 'SBI Bank', 'Axis Bank', 'Kotak Bank'];
  const statuses = ['Unpaid', 'Partially Paid', 'Paid', 'Cash Collected', 'Customer Deposited'];
  
  const applications: Application[] = [];
  
  for (let i = 1; i <= 50; i++) {
    applications.push({
      id: `APP${String(i).padStart(4, '0')}`,
      applicant_name: `Applicant ${i}`,
      branch_name: branches[Math.floor(Math.random() * branches.length)],
      team_lead: teamLeads[Math.floor(Math.random() * teamLeads.length)],
      rm_name: rms[Math.floor(Math.random() * rms.length)],
      dealer_name: dealers[Math.floor(Math.random() * dealers.length)],
      lender_name: lenders[Math.floor(Math.random() * lenders.length)],
      status: statuses[Math.floor(Math.random() * statuses.length)],
      emi_amount: Math.floor(Math.random() * 50000) + 10000,
      ptp_date: Math.random() > 0.5 ? `2024-${String(Math.floor(Math.random() * 12) + 1).padStart(2, '0')}-${String(Math.floor(Math.random() * 28) + 1).padStart(2, '0')}` : undefined,
      mobile: `+91${Math.floor(Math.random() * 9000000000) + 1000000000}`,
      address: `Address ${i}, City ${i}`
    });
  }
  
  return applications;
};

// Mock filter options
export const mockFilterOptions = {
  branches: ['Mumbai Central', 'Andheri West', 'Bandra East', 'Thane', 'Navi Mumbai'],
  teamLeads: ['Rajesh Kumar', 'Priya Sharma', 'Amit Patel', 'Neha Singh', 'Vikram Mehta'],
  rms: ['Rahul Verma', 'Sneha Gupta', 'Arjun Reddy', 'Kavya Iyer', 'Dev Malhotra'],
  dealers: ['ABC Motors', 'XYZ Auto', 'Premium Cars', 'Elite Motors', 'City Auto'],
  lenders: ['HDFC Bank', 'ICICI Bank', 'SBI Bank', 'Axis Bank', 'Kotak Bank'],
  statuses: ['Unpaid', 'Partially Paid', 'Paid', 'Cash Collected', 'Customer Deposited']
};

// Simulate API delay
export const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));
