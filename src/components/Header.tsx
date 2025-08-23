import React from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Bell, User, LogOut } from 'lucide-react';
import { motion } from 'framer-motion';

const Header: React.FC = () => {
  const { user, logout } = useAuth();

  return (
    <motion.header 
      className="bg-white border-b border-gray-200 px-6 py-4"
      initial={{ opacity: 0, y: -10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      <div className="flex items-center justify-between">
        <div className="flex-1">
          <h1 className="text-2xl font-semibold text-gray-900">
            Business Intention Priority Tools
          </h1>
          <p className="text-sm text-gray-500 mt-1">
            Streamline data requests and enhance collaboration
          </p>
        </div>

        <div className="flex items-center space-x-4">
          {/* Notifications */}
          <button className="p-2 text-gray-400 hover:text-gray-600 transition-colors rounded-lg hover:bg-gray-100">
            <Bell className="h-5 w-5" />
          </button>

          {/* User menu */}
          <div className="flex items-center space-x-3">
            <div className="flex items-center space-x-2">
              {user?.avatar ? (
                <img
                  src={user.avatar}
                  alt={user.name}
                  className="h-8 w-8 rounded-full object-cover"
                />
              ) : (
                <div className="h-8 w-8 rounded-full bg-primary-100 flex items-center justify-center">
                  <User className="h-4 w-4 text-primary-600" />
                </div>
              )}
              <div className="hidden md:block">
                <p className="text-sm font-medium text-gray-900">{user?.name}</p>
                <p className="text-xs text-gray-500 capitalize">{user?.role}</p>
              </div>
            </div>
            
            <button
              onClick={logout}
              className="p-2 text-gray-400 hover:text-gray-600 transition-colors rounded-lg hover:bg-gray-100"
              title="Logout"
            >
              <LogOut className="h-5 w-5" />
            </button>
          </div>
        </div>
      </div>
    </motion.header>
  );
};

export default Header;