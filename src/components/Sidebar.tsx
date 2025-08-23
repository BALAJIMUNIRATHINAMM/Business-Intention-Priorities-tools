import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  LayoutDashboard, 
  Signal, 
  Building2, 
  BarChart3, 
  Settings,
  Users,
  TrendingUp,
  Menu,
  X,
  ChefHat
} from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';

const Sidebar: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const location = useLocation();
  const { user } = useAuth();

  const navigation = [
    { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
    { name: 'Signal BF Tool', href: '/tools/signal', icon: Signal },
    { name: 'Company BF Tool', href: '/tools/company', icon: Building2 },
    { name: 'Aggregated Tool', href: '/tools/aggregated', icon: BarChart3 },
    { name: 'Profile', href: '/profile', icon: Settings },
  ];

  const adminNavigation = [
    { name: 'Admin Dashboard', href: '/admin', icon: TrendingUp },
    { name: 'User Management', href: '/admin/users', icon: Users },
    { name: 'Analytics', href: '/admin/analytics', icon: BarChart3 },
  ];

  const isActive = (path: string) => location.pathname === path;

  const NavLink: React.FC<{ item: any; onClick?: () => void }> = ({ item, onClick }) => (
    <Link
      to={item.href}
      onClick={onClick}
      className={`group flex items-center px-3 py-2 text-sm font-medium rounded-lg transition-all duration-200 ${
        isActive(item.href)
          ? 'bg-primary-100 text-primary-700 shadow-sm'
          : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900'
      }`}
    >
      <item.icon className={`mr-3 h-5 w-5 transition-colors ${
        isActive(item.href) ? 'text-primary-600' : 'text-gray-400 group-hover:text-gray-600'
      }`} />
      {item.name}
    </Link>
  );

  const sidebarContent = (
    <div className="flex flex-col h-full">
      {/* Logo */}
      <div className="flex items-center px-4 py-6 border-b border-gray-200">
        <ChefHat className="h-8 w-8 text-primary-600" />
        <span className="ml-2 text-xl font-bold text-gray-900">Draup Tools</span>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-4 py-6 space-y-2">
        {navigation.map((item) => (
          <NavLink key={item.name} item={item} onClick={() => setIsOpen(false)} />
        ))}
        
        {user?.role === 'admin' && (
          <>
            <div className="pt-6 mt-6 border-t border-gray-200">
              <p className="px-3 text-xs font-semibold text-gray-500 uppercase tracking-wider">
                Administration
              </p>
            </div>
            {adminNavigation.map((item) => (
              <NavLink key={item.name} item={item} onClick={() => setIsOpen(false)} />
            ))}
          </>
        )}
      </nav>

      {/* Footer */}
      <div className="px-4 py-4 border-t border-gray-200">
        <p className="text-xs text-gray-500 text-center">
          © 2025 Draup Dataflow Engine
        </p>
      </div>
    </div>
  );

  return (
    <>
      {/* Mobile menu button */}
      <div className="lg:hidden fixed top-4 left-4 z-50">
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="p-2 rounded-lg bg-white shadow-md text-gray-600 hover:text-gray-900 transition-colors"
        >
          {isOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
        </button>
      </div>

      {/* Desktop sidebar */}
      <div className="hidden lg:flex lg:w-64 lg:flex-col lg:fixed lg:inset-y-0 bg-white border-r border-gray-200 shadow-sm">
        {sidebarContent}
      </div>

      {/* Mobile sidebar */}
      <AnimatePresence>
        {isOpen && (
          <>
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="lg:hidden fixed inset-0 z-40 bg-black bg-opacity-50"
              onClick={() => setIsOpen(false)}
            />
            <motion.div
              initial={{ x: -300 }}
              animate={{ x: 0 }}
              exit={{ x: -300 }}
              transition={{ type: 'spring', damping: 25, stiffness: 200 }}
              className="lg:hidden fixed inset-y-0 left-0 z-50 w-64 bg-white shadow-xl"
            >
              {sidebarContent}
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </>
  );
};

export default Sidebar;