import { memo } from "react";
import { TableCell, TableRow } from "@/components/ui/table";
import { Application } from "@/types/application";
import { formatEmiMonth, formatCurrency, formatPtpDate } from "@/utils/formatters";
import StatusBadge from "./StatusBadge";
import ApplicationDetails from "./ApplicationDetails";
import CallStatusDisplay from "../CallStatusDisplay";
import CommentsDisplay from "./CommentsDisplay";
import type { BatchComment } from "@/hooks/useBatchComments";
import type { BatchContactStatus } from "@/hooks/useBatchContactCallingStatus";

interface ApplicationRowProps {
  application: Application;
  selectedApplicationId?: string;
  onRowClick: (application: Application) => void;
  selectedEmiMonth?: string | null;
  // Batched data props
  batchedStatus?: string;
  batchedPtpDate?: string | null;
  batchedContactStatus?: BatchContactStatus;
  batchedComments?: BatchComment[];
  isLoading?: boolean;
}

const ApplicationRow = memo(({ 
  application, 
  selectedApplicationId, 
  onRowClick,
  selectedEmiMonth,
  // Remove batchedStatus, batchedPtpDate, batchedContactStatus, batchedComments, isLoading
}: ApplicationRowProps) => {
  const handleRowClick = (e: React.MouseEvent) => {
    onRowClick(application);
  };

  return (
    <TableRow
      className={`cursor-pointer transition-colors align-top ${
        selectedApplicationId === application.id
          ? 'bg-blue-50 border-l-4 border-l-blue-500 hover:bg-blue-100'
          : 'hover:bg-gray-50'
      }`}
      onClick={handleRowClick}
    >
      {/* Application Details */}
      <TableCell className="py-4 align-top w-[24%]">
        <div className="flex flex-col gap-1">
          <span className="font-bold text-blue-800">{application.applicant_name}</span>
          <span className="text-xs text-gray-700">ID: {application.applicant_id}</span>
          <span className="text-xs text-gray-700">EMI Month: {formatEmiMonth(selectedEmiMonth ? selectedEmiMonth : application.emi_month)}</span>
          <span className="text-xs text-gray-700">Branch: {application.branch}</span>
          <span className="text-xs text-gray-700">TL: {application.tl_name}</span>
          <span className="text-xs text-gray-700">RM: {application.rm_name}</span>
          <span className="text-xs text-gray-700">Dealer: {application.dealer}</span>
          <span className="text-xs text-gray-700">Lender: {application.lender}</span>
        </div>
      </TableCell>

      {/* EMI Amount */}
      <TableCell className="py-4 align-top text-blue-600 font-semibold text-base w-[10%]">
        {formatCurrency(application.emi_amount)}
      </TableCell>

      {/* Status */}
      <TableCell className="py-4 align-top w-[10%]">
        <StatusBadge status={application.status} />
      </TableCell>

      {/* PTP Date */}
      <TableCell className="py-4 align-top w-[10%]">
        {application.ptp_date ? formatPtpDate(application.ptp_date) : 'Not Set'}
      </TableCell>

      {/* Calling Status */}
      <TableCell className="py-4 align-top w-[10%]">
        {application.calling_status || 'Applicant'}
      </TableCell>

      {/* Recent Comments */}
      <TableCell className="py-4 align-top w-[20%]">
        {application.comments && application.comments.length > 0 ? (
          <ul className="list-disc pl-4">
            {application.comments.map((comment: string, idx: number) => (
              <li key={idx} className="text-xs text-gray-700">{comment}</li>
            ))}
          </ul>
        ) : (
          <span className="text-xs text-gray-400">Click to add comments</span>
        )}
      </TableCell>
    </TableRow>
  );
});

ApplicationRow.displayName = "ApplicationRow";

export default ApplicationRow;
