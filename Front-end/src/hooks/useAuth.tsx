
import { useState, useEffect, createContext, useContext } from 'react';
import { User, Session } from '@/types/database';
// import { supabase } from '@/integrations/api/client'; // REMOVE
import { useNavigate } from 'react-router-dom';

interface AuthContextType {
  user: User | null;
  session: Session | null;
  loading: boolean;
  signIn: (email: string, password: string) => Promise<any>;
  signOut: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Dummy user for development
const DUMMY_USER: User = {
  id: 'user1',
  email: 'admin@example.com',
  full_name: 'Admin User',
  created_at: new Date().toISOString(),
  updated_at: new Date().toISOString(),
};

const DUMMY_SESSION: Session = {
  user: DUMMY_USER,
};

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [user, setUser] = useState<User | null>(DUMMY_USER);
  const [session, setSession] = useState<Session | null>(DUMMY_SESSION);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  // Dummy signIn always succeeds
  const signIn = async (email: string, password: string) => {
    setUser(DUMMY_USER);
    setSession(DUMMY_SESSION);
    return { user: DUMMY_USER, session: DUMMY_SESSION };
  };

  // Dummy signOut just clears user
  const signOut = async () => {
    setUser(null);
    setSession(null);
    navigate('/auth');
  };

  // No real auth state listener needed
  useEffect(() => {
    // Always logged in as dummy user
    setUser(DUMMY_USER);
    setSession(DUMMY_SESSION);
  }, []);

  return (
    <AuthContext.Provider value={{ user, session, loading, signIn, signOut }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
