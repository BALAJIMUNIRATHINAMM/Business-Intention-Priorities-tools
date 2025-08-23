import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { User, Mail, Calendar, Shield, Save, Camera } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import { useAnalytics } from '../contexts/AnalyticsContext';
import LoadingSpinner from '../components/LoadingSpinner';

const Profile: React.FC = () => {
  const { user, updateProfile } = useAuth();
  const { getUserActivity } = useAnalytics();
  const [isEditing, setIsEditing] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [formData, setFormData] = useState({
    name: user?.name || '',
    email: user?.email || '',
  });

  const userActivity = user ? getUserActivity(user.id) : [];
  const totalExtractions = userActivity.filter(e => e.event === 'file_processed').length;
  const joinDate = user ? new Date(user.createdAt).toLocaleDateString() : '';

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    
    try {
      await updateProfile(formData);
      setIsEditing(false);
    } catch (error) {
      // Error handled by auth context
    } finally {
      setIsLoading(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  if (!user) return null;

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      {/* Profile Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="card"
      >
        <div className="flex items-center space-x-6">
          <div className="relative">
            {user.avatar ? (
              <img
                src={user.avatar}
                alt={user.name}
                className="h-24 w-24 rounded-full object-cover"
              />
            ) : (
              <div className="h-24 w-24 rounded-full bg-primary-100 flex items-center justify-center">
                <User className="h-12 w-12 text-primary-600" />
              </div>
            )}
            <button className="absolute bottom-0 right-0 p-2 bg-white rounded-full shadow-md border border-gray-200 hover:bg-gray-50 transition-colors">
              <Camera className="h-4 w-4 text-gray-600" />
            </button>
          </div>
          
          <div className="flex-1">
            <h1 className="text-2xl font-bold text-gray-900">{user.name}</h1>
            <p className="text-gray-600">{user.email}</p>
            <div className="flex items-center space-x-4 mt-2">
              <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                user.role === 'admin' 
                  ? 'bg-purple-100 text-purple-800' 
                  : 'bg-blue-100 text-blue-800'
              }`}>
                <Shield className="h-3 w-3 mr-1" />
                {user.role}
              </span>
              <span className="text-sm text-gray-500">
                <Calendar className="h-4 w-4 inline mr-1" />
                Joined {joinDate}
              </span>
            </div>
          </div>

          <button
            onClick={() => setIsEditing(!isEditing)}
            className="btn-primary"
          >
            {isEditing ? 'Cancel' : 'Edit Profile'}
          </button>
        </div>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Profile Information */}
        <div className="lg:col-span-2">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="card"
          >
            <h2 className="text-lg font-semibold text-gray-900 mb-6">Profile Information</h2>
            
            {isEditing ? (
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Full Name
                  </label>
                  <input
                    type="text"
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                    className="input-field"
                    required
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Email Address
                  </label>
                  <input
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    className="input-field"
                    required
                  />
                </div>

                <div className="flex space-x-3 pt-4">
                  <button
                    type="submit"
                    disabled={isLoading}
                    className="btn-primary flex items-center disabled:opacity-50"
                  >
                    {isLoading ? <LoadingSpinner size="sm" /> : <Save className="h-4 w-4 mr-2" />}
                    Save Changes
                  </button>
                  <button
                    type="button"
                    onClick={() => setIsEditing(false)}
                    className="btn-secondary"
                  >
                    Cancel
                  </button>
                </div>
              </form>
            ) : (
              <div className="space-y-4">
                <div className="flex items-center space-x-3">
                  <User className="h-5 w-5 text-gray-400" />
                  <div>
                    <p className="text-sm text-gray-500">Full Name</p>
                    <p className="font-medium text-gray-900">{user.name}</p>
                  </div>
                </div>
                
                <div className="flex items-center space-x-3">
                  <Mail className="h-5 w-5 text-gray-400" />
                  <div>
                    <p className="text-sm text-gray-500">Email Address</p>
                    <p className="font-medium text-gray-900">{user.email}</p>
                  </div>
                </div>
                
                <div className="flex items-center space-x-3">
                  <Calendar className="h-5 w-5 text-gray-400" />
                  <div>
                    <p className="text-sm text-gray-500">Member Since</p>
                    <p className="font-medium text-gray-900">{joinDate}</p>
                  </div>
                </div>
              </div>
            )}
          </motion.div>
        </div>

        {/* Activity Stats */}
        <div className="space-y-6">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="card"
          >
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Your Activity</h3>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">Total Extractions</span>
                <span className="font-semibold text-gray-900">{totalExtractions}</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">Tools Accessed</span>
                <span className="font-semibold text-gray-900">
                  {new Set(userActivity.filter(e => e.event === 'tool_accessed').map(e => e.data.tool)).size}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">Last Login</span>
                <span className="font-semibold text-gray-900">
                  {user.lastLogin ? new Date(user.lastLogin).toLocaleDateString() : 'Today'}
                </span>
              </div>
            </div>
          </motion.div>

          {/* Recent Extractions */}
          {recentExtractions.length > 0 && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
              className="card"
            >
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Extractions</h3>
              <div className="space-y-3">
                {recentExtractions.map((extraction, index) => (
                  <div key={extraction.id} className="flex items-center space-x-3 p-2 rounded-lg hover:bg-gray-50">
                    <div className="p-1 bg-green-100 rounded">
                      <FileText className="h-3 w-3 text-green-600" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-gray-900 truncate">
                        {extraction.data.tool || 'Processing'}
                      </p>
                      <p className="text-xs text-gray-500">
                        {new Date(extraction.timestamp).toLocaleDateString()}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </motion.div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Profile;