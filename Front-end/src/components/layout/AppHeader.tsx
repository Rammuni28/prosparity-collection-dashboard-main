import { Button } from "@/components/ui/button";
import { LogOut, Settings } from "lucide-react";
import { useNavigate } from "react-router-dom";
import ExportDialog from "@/components/ExportDialog";
import { BarChart3 } from "lucide-react";

interface AppHeaderProps {
  onExportFull: () => void;
  onExportPtpComments: () => void;
  onExportPlanVsAchievement: (plannedDateTime: Date) => void;
}

const AppHeader = ({ onExportFull, onExportPtpComments, onExportPlanVsAchievement }: AppHeaderProps) => {
  const navigate = useNavigate();

  const handleSignOut = () => {
    // Simple sign out for demo
    console.log("Signed out successfully");
    alert("Signed out successfully");
  };

  return (
    <>
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
        <div className="flex items-center gap-3">
          <img 
            src="/lovable-uploads/879123ce-9339-4aec-90c9-3857e3b77417.png" 
            alt="Prosparity Logo" 
            className="h-7 w-auto"
          />
          <div>
            <h1 className="text-lg sm:text-xl font-bold text-gray-900">Collection Dashboard</h1>
          </div>
        </div>
        
        {/* Desktop Actions */}
        <div className="hidden sm:flex items-center gap-3">
          <div className="flex items-center gap-2">
            <Button
              variant="outline"
              size="sm"
              onClick={() => navigate('/analytics')}
              className="h-8 text-xs"
            >
              <BarChart3 className="h-3 w-3 mr-1" />
              Analytics
            </Button>
            <ExportDialog 
              onExportFull={onExportFull}
              onExportPtpComments={onExportPtpComments}
              onExportPlanVsAchievement={onExportPlanVsAchievement}
            />
            <Button
              variant="outline"
              size="sm"
              onClick={() => navigate('/admin-settings')}
              className="h-8 text-xs"
            >
              <Settings className="h-3 w-3 mr-1" />
              Admin Settings
            </Button>
          </div>
          <div className="flex items-center gap-2 text-sm text-gray-600">
            <span className="font-medium truncate max-w-[120px]">Demo User</span>
            <Button
              variant="outline"
              size="sm"
              onClick={handleSignOut}
              className="text-gray-600 hover:text-gray-900 h-8 text-xs"
            >
              <LogOut className="h-3 w-3 mr-1" />
              Sign Out
            </Button>
          </div>
        </div>

        {/* Mobile User Info and Log Out */}
        <div className="sm:hidden flex items-center gap-2">
          <span className="text-sm text-gray-600 font-medium">Demo User</span>
          <Button
            variant="outline"
            size="sm"
            onClick={handleSignOut}
            className="text-gray-600 hover:text-gray-900 h-8 text-xs"
          >
            <LogOut className="h-3 w-3 mr-1" />
            Sign Out
          </Button>
        </div>
      </div>
    </>
  );
};

export default AppHeader;
