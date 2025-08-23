import React, { useEffect } from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { 
  Signal, 
  Building2, 
  BarChart3, 
  Users, 
  FileText, 
  TrendingUp,
  ArrowRight,
  Activity
} from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import { useAnalytics } from '../contexts/AnalyticsContext';
import StatsCard from '../components/StatsCard';

const Dashboard: React.FC = () => {
  const { user } = useAuth();
  const { track, getUsageStats, getUserActivity } = useAnalytics();

  useEffect(() => {
    track('dashboard_viewed');
  }, []);

  const stats = getUsageStats();
  const userActivity = user ? getUserActivity(user.id) : [];
  const recentExtractions = userActivity.filter(e => e.event === 'file_processed').slice(0, 5);

  const tools = [
    {
      name: 'Signal BF Priority Tool',
      description: 'Extract priority signals from business function data',
      icon: Signal,
      href: '/tools/signal',
      color: 'blue' as const,
    },
    {
      name: 'Company BF Priority Tool',
      description: 'Extract company-specific business function priorities',
      icon: Building2,
      href: '/tools/company',
      color: 'green' as const,
    },
    {
      name: 'Aggregated Priority Tool',
      description: 'Process aggregated priority data with advanced analytics',
      icon: BarChart3,
      href: '/tools/aggregated',
      color: 'purple' as const,
    },
  ];

  return (
    <div className="space-y-8">
      {/* Welcome Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="card gradient-bg text-white"
      >
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold mb-2">
              Welcome back, {user?.name}! 👋
            </h1>
            <p className="text-primary-100">
              Ready to extract some business priorities today?
            </p>
          </div>
          <div className="hidden md:block">
            <Activity className="h-16 w-16 text-primary-200" />
          </div>
        </div>
      </motion.div>

      {/* Stats Overview */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatsCard
          title="Total Extractions"
          value={userActivity.filter(e => e.event === 'file_processed').length}
          icon={FileText}
          color="blue"
        />
        <StatsCard
          title="Tools Used"
          value={new Set(userActivity.filter(e => e.event === 'tool_accessed').map(e => e.data.tool)).size}
          icon={Signal}
          color="green"
        />
        <StatsCard
          title="This Week"
          value={userActivity.filter(e => {
            const eventDate = new Date(e.timestamp);
            const weekAgo = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000);
            return eventDate >= weekAgo;
          }).length}
          icon={TrendingUp}
          color="purple"
        />
        <StatsCard
          title="Success Rate"
          value="98%"
          icon={BarChart3}
          color="orange"
        />
      </div>

      {/* Tools Grid */}
      <div>
        <h2 className="text-xl font-semibold text-gray-900 mb-6">Available Tools</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {tools.map((tool, index) => (
            <motion.div
              key={tool.name}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              whileHover={{ y: -4 }}
              className="card group cursor-pointer"
            >
              <Link to={tool.href} className="block">
                <div className="flex items-center mb-4">
                  <div className={`p-3 rounded-lg ${
                    tool.color === 'blue' ? 'bg-blue-50' :
                    tool.color === 'green' ? 'bg-green-50' :
                    tool.color === 'purple' ? 'bg-purple-50' : 'bg-orange-50'
                  }`}>
                    <tool.icon className={`h-6 w-6 ${
                      tool.color === 'blue' ? 'text-blue-600' :
                      tool.color === 'green' ? 'text-green-600' :
                      tool.color === 'purple' ? 'text-purple-600' : 'text-orange-600'
                    }`} />
                  </div>
                  <ArrowRight className="ml-auto h-5 w-5 text-gray-400 group-hover:text-primary-600 transition-colors" />
                </div>
                <h3 className="font-semibold text-gray-900 mb-2">{tool.name}</h3>
                <p className="text-sm text-gray-600">{tool.description}</p>
              </Link>
            </motion.div>
          ))}
        </div>
      </div>

      {/* Recent Activity */}
      {recentExtractions.length > 0 && (
        <div>
          <h2 className="text-xl font-semibold text-gray-900 mb-6">Recent Extractions</h2>
          <div className="card">
            <div className="space-y-4">
              {recentExtractions.map((activity, index) => (
                <motion.div
                  key={activity.id}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className="flex items-center justify-between py-3 border-b border-gray-100 last:border-b-0"
                >
                  <div className="flex items-center space-x-3">
                    <div className="p-2 bg-green-100 rounded-lg">
                      <FileText className="h-4 w-4 text-green-600" />
                    </div>
                    <div>
                      <p className="font-medium text-gray-900">
                        {activity.data.tool || 'Data Processing'}
                      </p>
                      <p className="text-sm text-gray-500">
                        {activity.data.filename || 'File processed'}
                      </p>
                    </div>
                  </div>
                  <span className="text-xs text-gray-500">
                    {new Date(activity.timestamp).toLocaleDateString()}
                  </span>
                </motion.div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;