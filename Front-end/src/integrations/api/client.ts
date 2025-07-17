// Real API client for FastAPI backend

const API_BASE_URL = "http://localhost:8000/api/v1"; // Change if backend runs elsewhere

export async function getApplicationDetails(applicationId) {
  const res = await fetch(`${API_BASE_URL}/application/${applicationId}`);
  if (!res.ok) throw new Error("Failed to fetch application details");
  return res.json();
}

export async function getApplicationsList() {
  const res = await fetch(`${API_BASE_URL}/application/`);
  if (!res.ok) throw new Error("Failed to fetch applications list");
  return res.json();
}

export async function getCollectionsSummary(emiMonth) {
  const res = await fetch(`${API_BASE_URL}/collections/summary?emi_month=${encodeURIComponent(emiMonth)}`);
  if (!res.ok) throw new Error("Failed to fetch collections summary");
  return res.json();
}

// Dummy export to prevent import errors in other files
export const supabase = {};

// You can add more functions for other endpoints as needed, e.g.:
// export async function getApplicationsList() { ... } 