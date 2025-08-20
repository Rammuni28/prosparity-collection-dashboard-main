
import { useState, useEffect } from 'react';

// Mock user data for demo purposes
const mockUser = {
  id: 'demo-user-123',
  email: 'demo@prosparity.com',
  user_metadata: {
    full_name: 'Demo User'
  }
};

export const useAuth = () => {
  const [user, setUser] = useState(mockUser);
  const [loading, setLoading] = useState(false);

  const signIn = async (email: string, password: string) => {
    setLoading(true);
    // Simulate API call delay
    await new Promise(resolve => setTimeout(resolve, 1000));
    setUser(mockUser);
    setLoading(false);
    return { user: mockUser, error: null };
  };

  const signUp = async (email: string, password: string) => {
    setLoading(true);
    await new Promise(resolve => setTimeout(resolve, 1000));
    setUser(mockUser);
    setLoading(false);
    return { user: mockUser, error: null };
  };

  const signOut = async () => {
    setLoading(true);
    await new Promise(resolve => setTimeout(resolve, 500));
    setUser(null);
    setLoading(false);
    return { error: null };
  };

  const resetPassword = async (email: string) => {
    setLoading(true);
    await new Promise(resolve => setTimeout(resolve, 1000));
    setLoading(false);
    return { error: null };
  };

  return {
    user,
    loading,
    signIn,
    signUp,
    signOut,
    resetPassword
  };
};
