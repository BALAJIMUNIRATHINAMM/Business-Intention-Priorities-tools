import React, { useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  Users, 
  Activity, 
  FileText, 
  TrendingUp,
  Server,
  Database,
  Clock,
  CheckCircle
} from 'lucide-react';
import { useAnalytics } from '../../contexts/AnalyticsContext';
import { authService } from '../../lib/auth';
import StatsCard from '../../components/StatsCard';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts';

const AdminDashboard: React.FC = () => {
  const { track, getUsageStats } = useAnalytics();
  const stats = getUsageStats();
  const allUsers = authService.getAllUsers();

  useEffect(() => {
    track('admin_dashboard_viewed');
  }, []);

  const systemHealth = [
    { name: 'API Status', status: 'healthy', icon: Server },
    { name: 'Database', status: 'healthy', icon: Database },
    { name: 'File Processing', status: 'healthy', icon: FileText },
    { name: 'Authentication', status: 'healthy', icon: CheckCircle },
  ];

  return (
    <div className="space-y-8">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="card gradient-bg text-white"
      >
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold mb-2">Admin Dashboard</h1>
            <p className="text-primary-100">
              Monitor system performance and user activity
            </p>
          </div>
          <Activity className="h-16 w-16 text-primary-200" />
        </div>
      </motion.div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatsCard
          title="Total Users"
          value={stats.totalUsers}
          icon={Users}
          color="blue"
          trend={{ value: 12, isPositive: true }}
        />
        <StatsCard
          title="Active Users"
          value={stats.activeUsers}
          icon={Activity}
          color="green"
          trend={{ value: 8, isPositive: true }}
        />
        <StatsCard
          title="Total Extractions"
          value={stats.totalExtractions}
          icon={FileText}
          color="purple"
          trend={{ value: 15, isPositive: true }}
        />
        <StatsCard
          title="Success Rate"
          value="98.5%"
          icon={TrendingUp}
          color="orange"
          trend={{ value: 2, isPositive: true }}
        />
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Daily Activity Chart */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="card"
        >
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Daily Activity</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={stats.dailyActivity}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Line 
                type="monotone" 
                dataKey="users" 
                stroke="#3b82f6" 
                strokeWidth={2}
                name="Active Users"
              />
              <Line 
                type="monotone" 
                dataKey="extractions" 
                stroke="#10b981" 
                strokeWidth={2}
                name="Extractions"
              />
            </LineChart>
          </ResponsiveContainer>
        </motion.div>

        {/* Tool Usage Chart */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="card"
        >
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Tool Usage</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={stats.toolUsage}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="tool" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="count" fill="#8b5cf6" />
            </BarChart>
          </ResponsiveContainer>
        </motion.div>
      </div>

      {/* System Health */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
        className="card"
      >
        <h3 className="text-lg font-semibold text-gray-900 mb-6">System Health</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {systemHealth.map((item, index) => (
            <motion.div
              key={item.name}
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.1 * index }}
              className="flex items-center space-x-3 p-4 bg-green-50 rounded-lg border border-green-200"
            >
              <item.icon className="h-6 w-6 text-green-600" />
              <div>
                <p className="font-medium text-gray-900">{item.name}</p>
                <p className="text-sm text-green-600 capitalize">{item.status}</p>
              </div>
            </motion.div>
          ))}
        </div>
      </motion.div>

      {/* Recent Users */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
        className="card"
      >
        <h3 className="text-lg font-semibold text-gray-900 mb-6">Recent Users</h3>
        <div className="space-y-4">
          {allUsers.slice(0, 5).map((user, index) => (
            <motion.div
              key={user.id}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.1 * index }}
              className="flex items-center justify-between py-3 border-b border-gray-100 last:border-b-0"
            >
              <div className="flex items-center space-x-3">
                {user.avatar ? (
                  <img
                    src={user.avatar}
                    alt={user.name}
                    className="h-10 w-10 rounded-full object-cover"
                  />
                ) : (
                  <div className="h-10 w-10 rounded-full bg-primary-100 flex items-center justify-center">
                    <Users className="h-5 w-5 text-primary-600" />
                  </div>
                )}
                <div>
                  <p className="font-medium text-gray-900">{user.name}</p>
                  <p className="text-sm text-gray-500">{user.email}</p>
                </div>
              </div>
              <div className="text-right">
                <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                  user.isActive 
                    ? 'bg-green-100 text-green-800' 
                    : 'bg-red-100 text-red-800'
                }`}>
                  {user.isActive ? 'Active' : 'Inactive'}
                </span>
                <p className="text-xs text-gray-500 mt-1">
                  {user.lastLogin ? new Date(user.lastLogin).toLocaleDateString() : 'Never'}
                </p>
              </div>
            </motion.div>
          ))}
        </div>
      </motion.div>
    </div>
  );
};

export default AdminDashboard;