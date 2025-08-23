export interface User {
  id: string;
  email: string;
  name: string;
  role: 'user' | 'admin';
  avatar?: string;
  createdAt: string;
  lastLogin?: string;
  isActive: boolean;
}

export interface AuthState {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;
}

export interface AnalyticsEvent {
  id: string;
  userId: string;
  event: string;
  data: Record<string, any>;
  timestamp: string;
}

export interface UsageStats {
  totalUsers: number;
  activeUsers: number;
  totalExtractions: number;
  dailyActivity: Array<{
    date: string;
    users: number;
    extractions: number;
  }>;
  toolUsage: Array<{
    tool: string;
    count: number;
  }>;
}

export interface ExtractedPriority {
  company: string;
  bf: string;
  priority: string;
  description: string;
  source?: string;
  recentYearMonth?: string;
  recentYearQuarter?: string;
}

export interface ProcessingResult {
  data: ExtractedPriority[];
  filename: string;
  processedAt: string;
}