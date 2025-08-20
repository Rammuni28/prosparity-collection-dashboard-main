
import { useState } from 'react';

export const useUserRoles = () => {
  const [isAdmin] = useState(true); // Demo user is always admin for demo purposes

  return {
    isAdmin,
    userRole: 'admin'
  };
};
