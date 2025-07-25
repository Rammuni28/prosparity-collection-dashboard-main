import { toast } from "@/hooks/use-toast";
import { formatEmiMonth } from '@/utils/formatters';

// Updated API client for FastAPI backend
const API_BASE_URL = "http://localhost:8000/api/v1"; // Change if backend runs elsewhere

// Types for API responses
interface ApiApplicationItem {
  application_id: string;
  applicant_name: string;
  emi_amount: number;
  status: string;
  emi_month: string;
  branch: string;
  rm_name: string;
  tl_name: string;
  dealer: string;
  lender: string | null;
  ptp_date: string | null;
  calling_status: string | null;
  comments: string[];
}

interface ApiFilteredResponse {
  total: number;
  results: ApiApplicationItem[];
}

// Function to map API response to frontend Application interface
export function mapApiResponseToApplication(apiItem: ApiApplicationItem): any {
  return {
    id: apiItem.application_id,
    applicant_id: apiItem.application_id,
    applicant_name: apiItem.applicant_name,
    branch_name: apiItem.branch,
    branch: apiItem.branch, // Add this for ApplicationRow
    team_lead: apiItem.tl_name,
    tl_name: apiItem.tl_name, // Add this for ApplicationRow
    rm_name: apiItem.rm_name,
    dealer_name: apiItem.dealer,
    dealer: apiItem.dealer, // Add this for ApplicationRow
    lender_name: apiItem.lender,
    lender: apiItem.lender, // Add this for ApplicationRow
    lms_status: apiItem.status || 'Unknown',
    field_status: apiItem.status,
    status: apiItem.status, // Add this for ApplicationRow
    emi_amount: apiItem.emi_amount,
    principle_due: 0, // Not available in new API, set default
    interest_due: 0, // Not available in new API, set default
    demand_date: apiItem.emi_month,
    emi_month: apiItem.emi_month, // Add this for ApplicationRow
    user_id: '1', // Default value
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
    ptp_date: apiItem.ptp_date,
    latest_calling_status: apiItem.calling_status,
    calling_status: apiItem.calling_status, // Add this for ApplicationRow
    recent_comments: apiItem.comments.map((comment: string) => ({
      content: comment,
      user_name: 'Unknown'
    })),
    comments: apiItem.comments, // Add this for ApplicationRow
    // Add default values for other fields
    applicant_mobile: '',
    applicant_address: '',
    house_ownership: '',
    co_applicant_name: '',
    co_applicant_mobile: '',
    co_applicant_address: '',
    guarantor_name: '',
    guarantor_mobile: '',
    guarantor_address: '',
    reference_name: '',
    reference_mobile: '',
    reference_address: '',
    fi_location: '',
    repayment: '',
    last_month_bounce: 0,
    collection_rm: '',
    paid_date: '',
    applicant_calling_status: '',
    co_applicant_calling_status: '',
    guarantor_calling_status: '',
    reference_calling_status: '',
    disbursement_date: '',
    loan_amount: 0,
    vehicle_status: '',
    amount_collected: 0
  };
}

export async function getApplicationDetails(applicationId: string): Promise<any> {
  // Since we don't have individual application endpoint, 
  // we'll use the filtered endpoint to get the specific application
  const res = await fetch(`${API_BASE_URL}/application/filtered?search=${encodeURIComponent(applicationId)}&limit=1&emi_month=Jul-24`);
  if (!res.ok) throw new Error("Failed to fetch application details");
  
  const data: ApiFilteredResponse = await res.json();
  if (data.results && data.results.length > 0) {
    return mapApiResponseToApplication(data.results[0]);
  } else {
    throw new Error("Application not found");
  }
}

export async function getFilteredApplications(emiMonth: string, search: string = "", offset: number = 0, limit: number = 20): Promise<{total: number, applications: any[]}> {
  const params = new URLSearchParams({
    emi_month: emiMonth,
    search: search,
    offset: offset.toString(),
    limit: limit.toString()
  });
  
  const res = await fetch(`${API_BASE_URL}/application/filtered?${params}`);
  if (!res.ok) throw new Error("Failed to fetch applications");
  
  const data: ApiFilteredResponse = await res.json();
  return {
    total: data.total,
    applications: data.results.map(mapApiResponseToApplication)
  };
}

export async function getApplicationsList(): Promise<any[]> {
  // Use the filtered endpoint without specific filters to get all applications
  const res = await fetch(`${API_BASE_URL}/application/filtered?emi_month=Jul-24&limit=1000`);
  if (!res.ok) throw new Error("Failed to fetch applications list");
  
  const data: ApiFilteredResponse = await res.json();
  return data.results.map(mapApiResponseToApplication);
}

export async function getCollectionsSummary(emiMonth: string) {
  const params = new URLSearchParams();
  // Ensure emi_month is in the correct format (Mon-YY) for backend
  const formattedMonth = formatEmiMonth(emiMonth);
  params.append('emi_month', formattedMonth);

  const response = await fetch(`http://localhost:8000/api/v1/summary_status/summary?${params.toString()}`);
  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Failed to fetch summary: ${response.status} ${errorText}`);
  }
  return await response.json();
}

export async function getFilterOptions() {
  const res = await fetch("http://localhost:8000/api/v1/filters/options");
  if (!res.ok) throw new Error("Failed to fetch filter options");
  return res.json();
}

export async function getApplicationsFromBackend(emiMonth: string, offset = 0, limit = 20) {
  const params = new URLSearchParams();
  if (emiMonth) params.append('emi_month', emiMonth);
  params.append('offset', offset.toString());
  params.append('limit', limit.toString());

  const response = await fetch(`http://localhost:8000/api/v1/applications/?${params.toString()}`);
  if (!response.ok) throw new Error('Failed to fetch applications');
  return await response.json();
}

// Dummy export to prevent import errors in other files
export const supabase = {}; 