# 🔐 RBAC (Role-Based Access Control) Documentation

## 🎯 **Overview**
The Collection Dashboard implements a comprehensive Role-Based Access Control (RBAC) system with three distinct user roles, each with specific permissions and access levels.

## 👥 **User Roles**

### 1. **Admin** 👑
- **Full Access** to all system features
- **User Management** - Create, update, delete users
- **Paid Pending Approval** - Full access to approve/reject applications
- **System Configuration** - All administrative functions

### 2. **RM (Relationship Manager)** 📊
- **Collection Operations** - Update application statuses
- **Comments** - Create and view application comments
- **Application Data** - View and manage application details
- **Calling Status** - Update contact and demand calling statuses
- **❌ NO ACCESS** to Paid Pending Approval system

### 3. **TL (Team Lead)** 👨‍💼
- **Same permissions as RM**
- **Collection Operations** - Update application statuses
- **Comments** - Create and view application comments
- **Application Data** - View and manage application details
- **Calling Status** - Update contact and demand calling statuses
- **❌ NO ACCESS** to Paid Pending Approval system

## 🚫 **Restricted Endpoints (Admin Only)**

### **Paid Pending Approval System**
```
GET  /api/v1/paidpending-approval/           - List all paid pending applications
GET  /api/v1/paidpending-approval/{loan_id}  - Get specific application status
POST /api/v1/paidpending-approval/approve    - Approve/Reject applications
GET  /api/v1/paidpending-applications/       - Get paid pending applications list
```

**Why Restricted?**
- These endpoints handle financial approvals
- Only admins should have authority to approve/reject payments
- Prevents unauthorized status changes

### **User Management System**
```
POST   /api/v1/users/register           - Create new users
GET    /api/v1/users/                   - List all users
GET    /api/v1/users/{user_id}          - Get specific user
GET    /api/v1/users/role/{role}        - Get users by role
PUT    /api/v1/users/{user_id}/role     - Update user role
DELETE /api/v1/users/{user_id}          - Delete user
```

**Why Restricted?**
- User creation and role management
- System security and access control
- Administrative functions only

## ✅ **Accessible Endpoints (All Authenticated Users)**

### **Application Management**
```
GET /api/v1/application-row/           - List applications with filters
GET /api/v1/status-management/{loan_id} - Get application status
PUT /api/v1/status-management/{loan_id} - Update application status
```

### **Comments System**
```
POST /api/v1/comments/                                    - Create new comment
GET  /api/v1/comments/repayment/{repayment_id}            - Get comments by repayment
GET  /api/v1/comments/repayment/{repayment_id}/type/{type} - Get comments by type
```

### **Filtering & Analytics**
```
GET /api/v1/filter-main/           - Get filter options
GET /api/v1/summary-status/        - Get summary statistics
GET /api/v1/month-dropdown/{loan_id} - Get EMI month options
```

### **Contacts Management**
```
GET /api/v1/contacts/{loan_id}     - Get contact details
```

## 🔐 **Authentication Flow**

### **1. Login Process**
```
POST /api/v1/users/login
Body: { "username": "email", "password": "password" }
Response: JWT Token
```

### **2. Token Usage**
```
Authorization: Bearer <JWT_TOKEN>
All protected endpoints require this header
```

### **3. Role Verification**
```
- JWT contains user role information
- Dependencies automatically check permissions
- Unauthorized access returns 403 Forbidden
```

## 🛡️ **Security Features**

### **JWT Token Security**
- **Secret Key**: Environment variable based
- **Expiration**: Configurable token lifetime
- **Algorithm**: HS256 (HMAC with SHA-256)
- **Payload**: User ID, role, and metadata

### **Password Security**
- **Hashing**: Bcrypt with salt (industry standard)
- **Validation**: Minimum 8 characters
- **Storage**: Hashed only, never plain text

### **Access Control**
- **Route Protection**: All sensitive routes protected
- **Role Validation**: Automatic role checking
- **Error Handling**: Proper HTTP status codes

## 📋 **Implementation Details**

### **Dependencies Used**
```python
from app.core.deps import (
    get_db,              # Database session
    get_current_user,    # JWT authentication
    require_admin        # Admin-only access
)
```

### **Route Protection Examples**
```python
# Admin only
@router.post("/approve")
def approve_application(
    data: ApprovalData,
    current_user: dict = Depends(require_admin)
):
    # Only admins can access this

# Authenticated users only
@router.post("/comments")
def create_comment(
    comment: CommentData,
    current_user: dict = Depends(get_current_user)
):
    # Any authenticated user can access this
```

## 🚨 **Error Responses**

### **401 Unauthorized**
```json
{
    "detail": "Could not validate credentials",
    "headers": {"WWW-Authenticate": "Bearer"}
}
```

### **403 Forbidden**
```json
{
    "detail": "Admin access required"
}
```

### **500 Internal Server Error**
```json
{
    "detail": "Failed to process request: <error_message>"
}
```

## 🔄 **Role Update Process**

### **Admin Can Update User Roles**
```
PUT /api/v1/users/{user_id}/role
Body: "new_role"
Valid roles: "admin", "RM", "TL"
```

### **Role Validation**
- Only admins can change roles
- Cannot change your own role
- Valid role names enforced

## 📱 **Frontend Integration**

### **Required Headers**
```javascript
const headers = {
    'Authorization': `Bearer ${jwtToken}`,
    'Content-Type': 'application/json'
};
```

### **Error Handling**
```javascript
if (response.status === 403) {
    // User doesn't have permission
    showError('Access denied. Admin privileges required.');
} else if (response.status === 401) {
    // Token expired or invalid
    redirectToLogin();
}
```

### **Role-Based UI**
```javascript
if (userRole === 'admin') {
    // Show admin features
    showPaidPendingApproval();
    showUserManagement();
} else {
    // Hide admin features
    hidePaidPendingApproval();
    hideUserManagement();
}
```

## 🧪 **Testing RBAC**

### **Test Admin Access**
```bash
# Login as admin
curl -X POST "http://localhost:8002/api/v1/users/login" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=admin@example.com&password=adminpass"

# Use token to access admin endpoint
curl -X GET "http://localhost:8002/api/v1/paidpending-approval/" \
     -H "Authorization: Bearer <JWT_TOKEN>"
```

### **Test RM/TL Access**
```bash
# Login as RM
curl -X POST "http://localhost:8002/api/v1/users/login" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=rm@example.com&password=rmpass"

# Try to access admin endpoint (should fail)
curl -X GET "http://localhost:8002/api/v1/paidpending-approval/" \
     -H "Authorization: Bearer <JWT_TOKEN>"
# Expected: 403 Forbidden
```

## 🔧 **Configuration**

### **Environment Variables**
```bash
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### **JWT Settings**
```python
# app/core/config.py
SECRET_KEY: str = "your-secret-key"
ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
```

## 📈 **Future Enhancements**

### **Planned Features**
- **Audit Logging**: Track all role-based actions
- **Permission Granularity**: More specific permissions
- **Session Management**: Multiple active sessions
- **Two-Factor Authentication**: Enhanced security

### **Scalability**
- **Role Hierarchy**: Nested role permissions
- **Dynamic Permissions**: Database-driven permissions
- **API Rate Limiting**: Prevent abuse

---

## 📞 **Support**

For RBAC-related issues or questions:
1. Check authentication headers
2. Verify user role in database
3. Review endpoint permissions
4. Check JWT token expiration

**Remember**: Always use HTTPS in production for secure token transmission!
