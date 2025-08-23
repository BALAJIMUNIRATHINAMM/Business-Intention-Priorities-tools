import React, { createContext, useContext, useEffect } from 'react';
import { analytics } from '../lib/analytics';
import { useAuth } from './AuthContext';
import { AnalyticsEvent, UsageStats } from '../types';

interface AnalyticsContextType {
  track: (event: string, data?: Record<string, any>) => void;
  getUsageStats: () => UsageStats;
  getUserActivity: (userId: string) => AnalyticsEvent[];
}

const AnalyticsContext = createContext<AnalyticsContextType | undefined>(undefined);

export const useAnalytics = () => {
  const context = useContext(AnalyticsContext);
  if (!context) {
    throw new Error('useAnalytics must be used within an AnalyticsProvider');
  }
  return context;
};

export const AnalyticsProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { user } = useAuth();

  const track = (event: string, data: Record<string, any> = {}) => {
    if (user) {
      analytics.track(user.id, event, data);
    }
  };

  const getUsageStats = () => {
    return analytics.getUsageStats();
  };

  const getUserActivity = (userId: string) => {
    return analytics.getUserActivity(userId);
  };

  // Track page views
  useEffect(() => {
    if (user) {
      track('page_view', { page: window.location.pathname });
    }
  }, [user, window.location.pathname]);

  return (
    <AnalyticsContext.Provider value={{
      track,
      getUsageStats,
      getUserActivity,
    }}>
      {children}
    </AnalyticsContext.Provider>
  );
};