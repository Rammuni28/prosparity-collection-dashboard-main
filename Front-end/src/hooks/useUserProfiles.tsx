import { useState } from 'react';

// Mock user profiles for demo
const mockProfiles = {
  'demo-user-123': {
    id: 'demo-user-123',
    full_name: 'Demo User',
    email: 'demo@prosparity.com',
    role: 'admin'
  }
};

export const useUserProfiles = () => {
  const [profiles, setProfiles] = useState(mockProfiles);

  const getUserName = (userId: string, fallback: string) => {
    return profiles[userId]?.full_name || fallback;
  };

  const fetchProfiles = async (userIds: string[]) => {
    // Mock API call - profiles are already loaded
    return userIds.map(id => profiles[id]).filter(Boolean);
  };

  return {
    profiles,
    getUserName,
    fetchProfiles
  };
};
