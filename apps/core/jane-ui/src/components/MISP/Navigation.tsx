/**
 * MISP Navigation Component
 * 
 * Navigation menu for MISP threat intelligence platform
 * Preserves original MISP menu structure while integrating
 * with Jane's unified interface design system.
 */

import React from 'react';

interface MISPNavProps {
  currentPath?: string;
  userRole?: string;
  permissions?: string[];
}

const MISP_MENU_ITEMS = [
  {
    id: 'home',
    label: 'Home',
    path: '/misp',
    icon: '🏠'
  },
  {
    id: 'events',
    label: 'Event Actions',
    path: '/misp/events',
    icon: '📋',
    submenu: [
      { label: 'List Events', path: '/misp/events' },
      { label: 'Add Event', path: '/misp/events/add' },
      { label: 'List Attributes', path: '/misp/attributes' },
      { label: 'Search Attributes', path: '/misp/attributes/search' },
      { label: 'View Proposals', path: '/misp/shadow_attributes' },
      { label: 'Events with proposals', path: '/misp/events/proposalEventIndex' }
    ]
  },
  {
    id: 'dashboard',
    label: 'Dashboard',
    path: '/misp/users/dashboard',
    icon: '📊'
  },
  {
    id: 'galaxies',
    label: 'Galaxies',
    path: '/misp/galaxies',
    icon: '🌟'
  },
  {
    id: 'input_filters',
    label: 'Input Filters',
    path: '/misp/input_filters',
    icon: '🔍',
    submenu: [
      { label: 'Import Regexp', path: '/misp/regexp' },
      { label: 'Signature Allowedlist', path: '/misp/allowedlists' },
      { label: 'Download', path: '/misp/tasks' }
    ]
  },
  {
    id: 'global_actions',
    label: 'Global Actions',
    path: '/misp/global_actions',
    icon: '🌐',
    submenu: [
      { label: 'News', path: '/misp/news' },
      { label: 'My Profile', path: '/misp/users/view/me' },
      { label: 'Members List', path: '/misp/users/index' },
      { label: 'Organizations', path: '/misp/organisations/index' },
      { label: 'Role Permissions', path: '/misp/roles/index' }
    ]
  },
  {
    id: 'sync_actions',
    label: 'Sync Actions',
    path: '/misp/sync_actions',
    icon: '🔄',
    submenu: [
      { label: 'List Servers', path: '/misp/servers' },
      { label: 'List Feeds', path: '/misp/feeds' }
    ]
  },
  {
    id: 'administration',
    label: 'Administration',
    path: '/misp/admin',
    icon: '⚙️',
    requiredRole: 'admin',
    submenu: [
      { label: 'List Users', path: '/misp/admin/users' },
      { label: 'Contact users', path: '/misp/admin/users/email' },
      { label: 'List Organizations', path: '/misp/admin/organisations' },
      { label: 'List Roles', path: '/misp/admin/roles' },
      { label: 'Server Settings & Maintenance', path: '/misp/servers/serverSettings' },
      { label: 'Jobs', path: '/misp/jobs' },
      { label: 'Scheduled Tasks', path: '/misp/tasks' },
      { label: 'Logs', path: '/misp/admin/logs' }
    ]
  },
  {
    id: 'audit',
    label: 'Audit',
    path: '/misp/audit_logs',
    icon: '📝',
    requiredRole: 'admin'
  }
];

export default function MISPNavigation({ 
  currentPath = '', 
  userRole = 'user', 
  permissions = [] 
}: MISPNavProps) {
  const [expandedMenu, setExpandedMenu] = React.useState<string | null>(null);

  const hasPermission = (item: any) => {
    if (!item.requiredRole) return true;
    return userRole === item.requiredRole || userRole === 'admin';
  };

  const isActive = (path: string) => {
    return currentPath === path || currentPath.startsWith(path + '/');
  };

  const handleMenuClick = (itemId: string) => {
    if (expandedMenu === itemId) {
      setExpandedMenu(null);
    } else {
      setExpandedMenu(itemId);
    }
  };

  const filteredMenuItems = MISP_MENU_ITEMS.filter(hasPermission);

  return (
    <nav className="misp-navigation bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700">
      <div className="p-4">
        <div className="flex items-center gap-2 mb-6">
          <div className="text-2xl">🛡️</div>
          <div>
            <h2 className="text-lg font-bold text-gray-900 dark:text-white">MISP</h2>
            <p className="text-xs text-gray-500">Threat Intelligence</p>
          </div>
        </div>

        <ul className="space-y-1">
          {filteredMenuItems.map((item) => (
            <li key={item.id}>
              <div
                className={`flex items-center justify-between p-2 rounded-md cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-700 ${
                  isActive(item.path) 
                    ? 'bg-blue-50 dark:bg-blue-900 text-blue-700 dark:text-blue-300' 
                    : 'text-gray-700 dark:text-gray-300'
                }`}
                onClick={() => {
                  if (item.submenu) {
                    handleMenuClick(item.id);
                  } else {
                    // Navigate to path
                    window.location.href = item.path;
                  }
                }}
              >
                <div className="flex items-center gap-2">
                  <span className="text-sm">{item.icon}</span>
                  <span className="text-sm font-medium">{item.label}</span>
                </div>
                
                {item.submenu && (
                  <div className={`transform transition-transform ${
                    expandedMenu === item.id ? 'rotate-90' : ''
                  }`}>
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                    </svg>
                  </div>
                )}
              </div>

              {item.submenu && expandedMenu === item.id && (
                <ul className="ml-6 mt-2 space-y-1 border-l border-gray-200 dark:border-gray-600 pl-3">
                  {item.submenu.map((subItem, index) => (
                    <li key={index}>
                      <div
                        className={`p-2 rounded-md cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-700 ${
                          isActive(subItem.path)
                            ? 'bg-blue-50 dark:bg-blue-900 text-blue-700 dark:text-blue-300'
                            : 'text-gray-600 dark:text-gray-400'
                        }`}
                        onClick={() => {
                          window.location.href = subItem.path;
                        }}
                      >
                        <span className="text-sm">{subItem.label}</span>
                      </div>
                    </li>
                  ))}
                </ul>
              )}
            </li>
          ))}
        </ul>
      </div>

      {/* Footer */}
      <div className="absolute bottom-0 left-0 right-0 p-4 border-t border-gray-200 dark:border-gray-700">
        <div className="text-xs text-gray-500 text-center">
          MISP v2.5.22 • API v1.0.0
        </div>
        <div className="text-xs text-gray-400 text-center mt-1">
          Role: {userRole}
        </div>
      </div>
    </nav>
  );
}