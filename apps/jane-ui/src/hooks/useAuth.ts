/**
 * Auth Hook
 * 
 * Manages authentication state and user data
 */

'use client';

import { useEffect, useState } from 'react';

interface User {
  id: string;
  username: string;
  email: string;
  is_active: boolean;
  adhd_accommodations?: Record<string, unknown>;
  autism_accommodations?: Record<string, unknown>;
  preferred_domains?: string[];
  ui_preferences?: Record<string, unknown>;
}

export const useAuth = () => {
  const [user, setUser] = useState<User | null>(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);

  // Mock authentication for development
  useEffect(() => {
    const mockUser: User = {
      id: '1',
      username: 'demo_user',
      email: 'demo@example.com',
      is_active: true,
      adhd_accommodations: {
        enabled: true,
        reduce_cognitive_load: true
      },
      autism_accommodations: {
        enabled: true,
        sensory_reduction: true
      },
      preferred_domains: ['security', 'productivity'],
      ui_preferences: {
        reduce_animations: true,
        high_contrast: false
      }
    };

    // Simulate auth check
    setTimeout(() => {
      setUser(mockUser);
      setIsAuthenticated(true);
      setLoading(false);
    }, 500);
  }, []);

  return {
    user,
    isAuthenticated,
    loading
  };
};