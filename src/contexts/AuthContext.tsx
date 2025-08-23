import React, { createContext, useContext, useEffect, useState } from 'react';
import { User, AuthState } from '../types';
import { authService } from '../lib/auth';
import toast from 'react-hot-toast';

interface AuthContextType extends AuthState {
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, name: string) => Promise<void>;
  logout: () => Promise<void>;
  updateProfile: (updates: Partial<User>) => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [state, setState] = useState<AuthState>({
    user: null,
    isLoading: true,
    isAuthenticated: false,
  });

  useEffect(() => {
    const initAuth = async () => {
      try {
        const user = await authService.getCurrentUser();
        setState({
          user,
          isLoading: false,
          isAuthenticated: !!user,
        });
      } catch (error) {
        setState({
          user: null,
          isLoading: false,
          isAuthenticated: false,
        });
      }
    };

    initAuth();
  }, []);

  const login = async (email: string, password: string) => {
    setState(prev => ({ ...prev, isLoading: true }));
    try {
      const user = await authService.login(email, password);
      setState({
        user,
        isLoading: false,
        isAuthenticated: true,
      });
      toast.success('Welcome back!');
    } catch (error) {
      setState(prev => ({ ...prev, isLoading: false }));
      toast.error(error instanceof Error ? error.message : 'Login failed');
      throw error;
    }
  };

  const register = async (email: string, password: string, name: string) => {
    setState(prev => ({ ...prev, isLoading: true }));
    try {
      const user = await authService.register(email, password, name);
      setState({
        user,
        isLoading: false,
        isAuthenticated: true,
      });
      toast.success('Account created successfully!');
    } catch (error) {
      setState(prev => ({ ...prev, isLoading: false }));
      toast.error(error instanceof Error ? error.message : 'Registration failed');
      throw error;
    }
  };

  const logout = async () => {
    try {
      await authService.logout();
      setState({
        user: null,
        isLoading: false,
        isAuthenticated: false,
      });
      toast.success('Logged out successfully');
    } catch (error) {
      toast.error('Logout failed');
    }
  };

  const updateProfile = async (updates: Partial<User>) => {
    if (!state.user) return;
    
    try {
      const updatedUser = await authService.updateProfile(state.user.id, updates);
      setState(prev => ({
        ...prev,
        user: updatedUser,
      }));
      toast.success('Profile updated successfully');
    } catch (error) {
      toast.error('Failed to update profile');
      throw error;
    }
  };

  return (
    <AuthContext.Provider value={{
      ...state,
      login,
      register,
      logout,
      updateProfile,
    }}>
      {children}
    </AuthContext.Provider>
  );
};