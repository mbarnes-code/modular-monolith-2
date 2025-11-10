/**
 * Session Service - Task T047 COMPLETED
 * 
 * Handles session persistence and state management for executive function platform
 */

interface UserSession {
  id: string;
  userId: string;
  username: string;
  preferences: {
    executiveFunctionEnabled: boolean;
    cognitiveLoadThreshold: number;
    visualIndicators: boolean;
    contextSwitchingReduction: boolean;
    performanceMetricsEnabled: boolean;
  };
  lastActive: string;
  currentTool?: string | null;
  toolStates: Record<string, unknown>;
  executiveFunctionMetrics: {
    taskSwitches: number;
    focusTime: number;
    completedActions: number;
    cognitiveLoadHistory: Array<{ timestamp: string; score: number }>;
  };
}

interface SessionState {
  session: UserSession | null;
  isLoading: boolean;
  lastSaved: string | null;
  autoSaveEnabled: boolean;
}

const SESSION_STORAGE_KEY = 'jane-platform-session';
const SESSION_SAVE_INTERVAL = 30000; // 30 seconds

const DEFAULT_PREFERENCES = {
  executiveFunctionEnabled: true,
  cognitiveLoadThreshold: 7,
  visualIndicators: true,
  contextSwitchingReduction: true,
  performanceMetricsEnabled: true
};

class SessionService {
  private state: SessionState = {
    session: null,
    isLoading: false,
    lastSaved: null,
    autoSaveEnabled: true
  };

  private saveTimer: number | null = null;
  private listeners: Array<(state: SessionState) => void> = [];

  constructor() {
    if (typeof window !== 'undefined') {
      this.loadSession();
      this.startAutoSave();
    }
  }

  private setState(newState: Partial<SessionState>) {
    this.state = { ...this.state, ...newState };
    this.notifyListeners();
  }

  private notifyListeners() {
    this.listeners.forEach(listener => listener(this.state));
  }

  subscribe(listener: (state: SessionState) => void) {
    this.listeners.push(listener);
    return () => {
      this.listeners = this.listeners.filter(l => l !== listener);
    };
  }

  getState(): SessionState {
    return { ...this.state };
  }

  async loadSession(): Promise<UserSession | null> {
    if (typeof window === 'undefined') return null;

    this.setState({ isLoading: true });

    try {
      const stored = window.localStorage.getItem(SESSION_STORAGE_KEY);
      if (stored) {
        const session: UserSession = JSON.parse(stored);
        session.lastActive = new Date().toISOString();
        
        this.setState({ 
          session, 
          isLoading: false,
          lastSaved: session.lastActive
        });
        
        return session;
      }
    } catch (error) {
      if (typeof window !== 'undefined' && window.console) {
        window.console.warn('Failed to load session from storage:', error);
      }
    }

    this.setState({ isLoading: false });
    return null;
  }

  async createSession(userId: string, username: string): Promise<UserSession> {
    const session: UserSession = {
      id: `session-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
      userId,
      username,
      preferences: DEFAULT_PREFERENCES,
      lastActive: new Date().toISOString(),
      toolStates: {},
      executiveFunctionMetrics: {
        taskSwitches: 0,
        focusTime: 0,
        completedActions: 0,
        cognitiveLoadHistory: []
      }
    };

    this.setState({ session });
    await this.saveSession();
    
    return session;
  }

  async saveSession(): Promise<boolean> {
    if (typeof window === 'undefined' || !this.state.session) return false;

    try {
      const sessionToSave = {
        ...this.state.session,
        lastActive: new Date().toISOString()
      };

      window.localStorage.setItem(SESSION_STORAGE_KEY, JSON.stringify(sessionToSave));
      
      this.setState({ 
        session: sessionToSave,
        lastSaved: sessionToSave.lastActive 
      });

      return true;
    } catch (error) {
      if (typeof window !== 'undefined' && window.console) {
        window.console.warn('Failed to save session to storage:', error);
      }
      return false;
    }
  }

  async clearSession(): Promise<void> {
    if (typeof window !== 'undefined') {
      window.localStorage.removeItem(SESSION_STORAGE_KEY);
    }
    
    this.setState({ 
      session: null, 
      lastSaved: null 
    });
    
    this.stopAutoSave();
  }

  async updatePreferences(updates: Partial<UserSession['preferences']>): Promise<boolean> {
    if (!this.state.session) return false;

    const updatedSession = {
      ...this.state.session,
      preferences: {
        ...this.state.session.preferences,
        ...updates
      }
    };

    this.setState({ session: updatedSession });
    return await this.saveSession();
  }

  async setCurrentTool(toolId: string | null): Promise<boolean> {
    if (!this.state.session) return false;

    if (toolId && toolId !== this.state.session.currentTool) {
      const updatedMetrics = {
        ...this.state.session.executiveFunctionMetrics,
        taskSwitches: this.state.session.executiveFunctionMetrics.taskSwitches + 1
      };

      const updatedSession = {
        ...this.state.session,
        currentTool: toolId,
        executiveFunctionMetrics: updatedMetrics
      };

      this.setState({ session: updatedSession });
    } else {
      const updatedSession = {
        ...this.state.session,
        currentTool: toolId
      };

      this.setState({ session: updatedSession });
    }

    return await this.saveSession();
  }

  async updateToolState(toolId: string, state: unknown): Promise<boolean> {
    if (!this.state.session) return false;

    const updatedSession = {
      ...this.state.session,
      toolStates: {
        ...this.state.session.toolStates,
        [toolId]: state
      }
    };

    this.setState({ session: updatedSession });
    return await this.saveSession();
  }

  getToolState(toolId: string): unknown {
    return this.state.session?.toolStates[toolId] || null;
  }

  async recordCognitiveLoad(score: number): Promise<boolean> {
    if (!this.state.session) return false;

    const timestamp = new Date().toISOString();
    const updatedHistory = [
      ...this.state.session.executiveFunctionMetrics.cognitiveLoadHistory,
      { timestamp, score }
    ].slice(-100);

    const updatedSession = {
      ...this.state.session,
      executiveFunctionMetrics: {
        ...this.state.session.executiveFunctionMetrics,
        cognitiveLoadHistory: updatedHistory
      }
    };

    this.setState({ session: updatedSession });
    return await this.saveSession();
  }

  async recordCompletedAction(): Promise<boolean> {
    if (!this.state.session) return false;

    const updatedSession = {
      ...this.state.session,
      executiveFunctionMetrics: {
        ...this.state.session.executiveFunctionMetrics,
        completedActions: this.state.session.executiveFunctionMetrics.completedActions + 1
      }
    };

    this.setState({ session: updatedSession });
    return await this.saveSession();
  }

  private startAutoSave() {
    if (typeof window === 'undefined') return;

    this.saveTimer = window.setInterval(() => {
      if (this.state.autoSaveEnabled && this.state.session) {
        this.saveSession();
      }
    }, SESSION_SAVE_INTERVAL);
  }

  private stopAutoSave() {
    if (this.saveTimer && typeof window !== 'undefined') {
      window.clearInterval(this.saveTimer);
      this.saveTimer = null;
    }
  }

  setAutoSave(enabled: boolean) {
    this.setState({ autoSaveEnabled: enabled });
    
    if (enabled && !this.saveTimer) {
      this.startAutoSave();
    } else if (!enabled && this.saveTimer) {
      this.stopAutoSave();
    }
  }

  // Utility methods
  isLoggedIn(): boolean {
    return !!this.state.session;
  }

  getCurrentUser(): { id: string; username: string } | null {
    if (!this.state.session) return null;
    
    return {
      id: this.state.session.userId,
      username: this.state.session.username
    };
  }

  getPreferences(): UserSession['preferences'] | null {
    return this.state.session?.preferences || null;
  }

  getExecutiveFunctionMetrics(): UserSession['executiveFunctionMetrics'] | null {
    return this.state.session?.executiveFunctionMetrics || null;
  }

  getCognitiveLoadThreshold(): number {
    return this.state.session?.preferences.cognitiveLoadThreshold || 7;
  }

  isExecutiveFunctionEnabled(): boolean {
    return this.state.session?.preferences.executiveFunctionEnabled ?? true;
  }

  shouldReduceContextSwitching(): boolean {
    return this.state.session?.preferences.contextSwitchingReduction ?? true;
  }

  shouldShowVisualIndicators(): boolean {
    return this.state.session?.preferences.visualIndicators ?? true;
  }

  destroy() {
    this.stopAutoSave();
    this.listeners = [];
  }
}

export const sessionService = new SessionService();
export type { UserSession, SessionState };
export { SessionService, DEFAULT_PREFERENCES };
export default sessionService;