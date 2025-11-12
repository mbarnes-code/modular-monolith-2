/**
 * Accessibility Utilities for Mental Prosthetic Platform
 * 
 * Provides comprehensive accessibility support including WCAG 2.1 AA compliance,
 * executive function accommodations, and assistive technology compatibility.
 */

// ARIA utilities for better semantic markup
export const aria = {
  // Common ARIA attributes builder
  buildAttributes: (config: {
    label?: string;
    labelledBy?: string;
    describedBy?: string;
    expanded?: boolean;
    selected?: boolean;
    checked?: boolean;
    disabled?: boolean;
    required?: boolean;
    invalid?: boolean;
    live?: 'off' | 'polite' | 'assertive';
    atomic?: boolean;
    relevant?: string;
    busy?: boolean;
    hidden?: boolean;
    level?: number;
    orientation?: 'horizontal' | 'vertical';
    current?: boolean | 'page' | 'step' | 'location' | 'date' | 'time';
  }) => {
    const attributes: Record<string, string | boolean> = {};
    
    if (config.label) attributes['aria-label'] = config.label;
    if (config.labelledBy) attributes['aria-labelledby'] = config.labelledBy;
    if (config.describedBy) attributes['aria-describedby'] = config.describedBy;
    if (config.expanded !== undefined) attributes['aria-expanded'] = config.expanded;
    if (config.selected !== undefined) attributes['aria-selected'] = config.selected;
    if (config.checked !== undefined) attributes['aria-checked'] = config.checked;
    if (config.disabled !== undefined) attributes['aria-disabled'] = config.disabled;
    if (config.required !== undefined) attributes['aria-required'] = config.required;
    if (config.invalid !== undefined) attributes['aria-invalid'] = config.invalid;
    if (config.live) attributes['aria-live'] = config.live;
    if (config.atomic !== undefined) attributes['aria-atomic'] = config.atomic;
    if (config.relevant) attributes['aria-relevant'] = config.relevant;
    if (config.busy !== undefined) attributes['aria-busy'] = config.busy;
    if (config.hidden !== undefined) attributes['aria-hidden'] = config.hidden;
    if (config.level) attributes['aria-level'] = config.level.toString();
    if (config.orientation) attributes['aria-orientation'] = config.orientation;
    if (config.current !== undefined) attributes['aria-current'] = config.current.toString();
    
    return attributes;
  },

  // Live region announcements for screen readers
  announce: (message: string, priority: 'polite' | 'assertive' = 'polite') => {
    const announcer = document.createElement('div');
    announcer.setAttribute('aria-live', priority);
    announcer.setAttribute('aria-atomic', 'true');
    announcer.className = 'sr-only'; // Screen reader only
    announcer.textContent = message;
    
    document.body.appendChild(announcer);
    
    // Clean up after announcement
    setTimeout(() => {
      document.body.removeChild(announcer);
    }, 1000);
  },

  // Executive function status announcements
  announceProgress: (current: number, total: number, taskName?: string) => {
    const percentage = Math.round((current / total) * 100);
    const message = taskName 
      ? `${taskName}: ${percentage}% complete, ${current} of ${total} items`
      : `Progress: ${percentage}% complete, ${current} of ${total}`;
    
    aria.announce(message, 'polite');
  },

  announceError: (fieldName: string, errorMessage: string, suggestion?: string) => {
    let message = `Error in ${fieldName}: ${errorMessage}`;
    if (suggestion) {
      message += `. Suggestion: ${suggestion}`;
    }
    aria.announce(message, 'assertive');
  },
};

// Focus management for executive function support
export const focus = {
  // Focus trap for modals and dialogs
  createTrap: (element: HTMLElement) => {
    const focusableElements = element.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    
    const firstElement = focusableElements[0] as HTMLElement;
    const lastElement = focusableElements[focusableElements.length - 1] as HTMLElement;
    
    const handleTabKey = (e: KeyboardEvent) => {
      if (e.key !== 'Tab') return;
      
      if (e.shiftKey) {
        if (document.activeElement === firstElement) {
          lastElement.focus();
          e.preventDefault();
        }
      } else {
        if (document.activeElement === lastElement) {
          firstElement.focus();
          e.preventDefault();
        }
      }
    };
    
    element.addEventListener('keydown', handleTabKey);
    
    // Return cleanup function
    return () => {
      element.removeEventListener('keydown', handleTabKey);
    };
  },

  // Preserve focus context for executive function
  preserveContext: () => {
    const activeElement = document.activeElement as HTMLElement;
    
    return {
      restore: () => {
        if (activeElement && activeElement.focus) {
          activeElement.focus();
        }
      },
      element: activeElement,
    };
  },

  // Smart focus management for task switching
  setFocus: (
    element: HTMLElement | null, 
    options: { 
      preventScroll?: boolean;
      reason?: 'navigation' | 'error' | 'completion' | 'context-switch';
    } = {}
  ) => {
    if (!element) return;
    
    // Announce focus change for context awareness
    if (options.reason) {
      const announcements = {
        navigation: 'Navigation focus changed',
        error: 'Focus moved to error field',
        completion: 'Task completed, focus advanced',
        'context-switch': 'Context switched, focus preserved',
      };
      
      aria.announce(announcements[options.reason], 'polite');
    }
    
    element.focus({ preventScroll: options.preventScroll });
  },

  // Focus visible indicator management
  addFocusIndicators: () => {
    const style = document.createElement('style');
    style.textContent = `
      .focus-visible {
        outline: 2px solid var(--color-border-focus, #3b82f6);
        outline-offset: 2px;
        border-radius: 4px;
      }
      
      .focus-visible-enhanced {
        outline: 3px solid #000000;
        outline-offset: 1px;
        background-color: #ffff00;
        color: #000000;
      }
    `;
    
    document.head.appendChild(style);
    
    // Add focus-visible polyfill behavior
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Tab') {
        document.body.classList.add('using-keyboard');
      }
    });
    
    document.addEventListener('mousedown', () => {
      document.body.classList.remove('using-keyboard');
    });
  },
};

// Keyboard navigation helpers
export const keyboard = {
  // Common keyboard event handlers
  handlers: {
    escape: (callback: () => void) => (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        callback();
        e.preventDefault();
      }
    },

    enter: (callback: () => void) => (e: KeyboardEvent) => {
      if (e.key === 'Enter') {
        callback();
        e.preventDefault();
      }
    },

    space: (callback: () => void) => (e: KeyboardEvent) => {
      if (e.key === ' ') {
        callback();
        e.preventDefault();
      }
    },

    arrows: (callbacks: {
      up?: () => void;
      down?: () => void;
      left?: () => void;
      right?: () => void;
    }) => (e: KeyboardEvent) => {
      const { key } = e;
      
      if (key === 'ArrowUp' && callbacks.up) {
        callbacks.up();
        e.preventDefault();
      } else if (key === 'ArrowDown' && callbacks.down) {
        callbacks.down();
        e.preventDefault();
      } else if (key === 'ArrowLeft' && callbacks.left) {
        callbacks.left();
        e.preventDefault();
      } else if (key === 'ArrowRight' && callbacks.right) {
        callbacks.right();
        e.preventDefault();
      }
    },
  },

  // Executive function keyboard shortcuts
  executiveFunctionShortcuts: {
    // Quick task actions
    'Alt+N': 'Create new item',
    'Alt+S': 'Save current work',
    'Alt+U': 'Undo last action',
    'Alt+R': 'Redo action',
    'Alt+F': 'Find/Search',
    'Alt+H': 'Show help',
    'Alt+M': 'Toggle menu',
    'Escape': 'Cancel/Close current context',
    
    // Context preservation
    'Ctrl+Shift+S': 'Save context state',
    'Ctrl+Shift+R': 'Restore context state',
    
    // Navigation
    'Alt+1': 'Go to main navigation',
    'Alt+2': 'Go to content area',
    'Alt+3': 'Go to sidebar',
    'Alt+4': 'Go to footer',
  },

  // Install global shortcuts
  installShortcuts: (shortcuts: Record<string, () => void>) => {
    const handleKeyDown = (e: KeyboardEvent) => {
      const key = [
        e.ctrlKey && 'Ctrl',
        e.altKey && 'Alt', 
        e.shiftKey && 'Shift',
        e.key
      ].filter(Boolean).join('+');
      
      if (shortcuts[key]) {
        shortcuts[key]();
        e.preventDefault();
      }
    };
    
    document.addEventListener('keydown', handleKeyDown);
    
    return () => {
      document.removeEventListener('keydown', handleKeyDown);
    };
  },
};

// Color contrast utilities for WCAG compliance
export const contrast = {
  // Calculate relative luminance
  getLuminance: (color: string): number => {
    // Simple implementation - would use proper color parsing in production
    const hex = color.replace('#', '');
    const r = parseInt(hex.substr(0, 2), 16) / 255;
    const g = parseInt(hex.substr(2, 2), 16) / 255;
    const b = parseInt(hex.substr(4, 2), 16) / 255;
    
    const [rs, gs, bs] = [r, g, b].map(c => 
      c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4)
    );
    
    return 0.2126 * rs + 0.7152 * gs + 0.0722 * bs;
  },

  // Calculate contrast ratio between two colors
  getContrastRatio: (color1: string, color2: string): number => {
    const lum1 = contrast.getLuminance(color1);
    const lum2 = contrast.getLuminance(color2);
    const brightest = Math.max(lum1, lum2);
    const darkest = Math.min(lum1, lum2);
    
    return (brightest + 0.05) / (darkest + 0.05);
  },

  // Check WCAG compliance levels
  checkWCAG: (foreground: string, background: string) => {
    const ratio = contrast.getContrastRatio(foreground, background);
    
    return {
      ratio,
      AA: ratio >= 4.5,
      AAA: ratio >= 7,
      AALarge: ratio >= 3, // For text 18pt+ or 14pt+ bold
      AAALarge: ratio >= 4.5,
    };
  },

  // Get accessible text color for background
  getAccessibleTextColor: (backgroundColor: string, lightText = '#ffffff', darkText = '#000000'): string => {
    const lightRatio = contrast.getContrastRatio(lightText, backgroundColor);
    const darkRatio = contrast.getContrastRatio(darkText, backgroundColor);
    
    return lightRatio > darkRatio ? lightText : darkText;
  },
};

// Screen reader utilities
export const screenReader = {
  // Hide content visually but keep for screen readers
  srOnlyClass: 'sr-only',
  
  // CSS for screen reader only content
  srOnlyCSS: `
    .sr-only {
      position: absolute;
      width: 1px;
      height: 1px;
      padding: 0;
      margin: -1px;
      overflow: hidden;
      clip: rect(0, 0, 0, 0);
      white-space: nowrap;
      border: 0;
    }
    
    .sr-only-focusable:focus {
      position: static;
      width: auto;
      height: auto;
      padding: 0.5rem;
      margin: 0;
      overflow: visible;
      clip: auto;
      white-space: normal;
    }
  `,

  // Add descriptive text for complex UI elements
  addDescription: (element: HTMLElement, description: string) => {
    const descId = `desc-${Math.random().toString(36).substr(2, 9)}`;
    
    const descElement = document.createElement('div');
    descElement.id = descId;
    descElement.className = 'sr-only';
    descElement.textContent = description;
    
    element.setAttribute('aria-describedby', descId);
    element.appendChild(descElement);
    
    return descId;
  },

  // Create skip links for navigation
  createSkipLinks: (links: Array<{ href: string; text: string }>) => {
    const skipContainer = document.createElement('div');
    skipContainer.className = 'skip-links';
    skipContainer.innerHTML = links
      .map(link => `<a href="${link.href}" class="sr-only-focusable">${link.text}</a>`)
      .join('');
    
    document.body.insertBefore(skipContainer, document.body.firstChild);
    
    return skipContainer;
  },
};

// Reduced motion utilities
export const motion = {
  // Check user's motion preferences
  prefersReducedMotion: (): boolean => {
    return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  },

  // Safe animation wrapper that respects motion preferences
  safeAnimate: (
    element: HTMLElement,
    keyframes: Keyframe[],
    options: KeyframeAnimationOptions
  ) => {
    if (motion.prefersReducedMotion()) {
      // Skip to end state immediately
      const endFrame = keyframes[keyframes.length - 1];
      Object.assign(element.style, endFrame);
      return { finished: Promise.resolve() };
    }
    
    return element.animate(keyframes, options);
  },

  // CSS class toggle with motion consideration
  toggleWithMotion: (element: HTMLElement, className: string, force?: boolean) => {
    if (motion.prefersReducedMotion()) {
      // Apply class immediately without transition
      element.style.transition = 'none';
      element.classList.toggle(className, force);
      
      // Restore transitions after a frame
      requestAnimationFrame(() => {
        element.style.transition = '';
      });
    } else {
      element.classList.toggle(className, force);
    }
  },
};

// Executive function specific utilities
export const executiveFunction = {
  // Context breadcrumbs for navigation awareness
  createBreadcrumbs: (
    items: Array<{ label: string; href?: string; current?: boolean }>
  ) => {
    const nav = document.createElement('nav');
    nav.setAttribute('aria-label', 'Breadcrumb');
    
    const ol = document.createElement('ol');
    ol.className = 'breadcrumb-list';
    
    items.forEach((item, index) => {
      const li = document.createElement('li');
      li.className = 'breadcrumb-item';
      
      if (item.current) {
        li.setAttribute('aria-current', 'page');
        li.textContent = item.label;
      } else if (item.href) {
        const link = document.createElement('a');
        link.href = item.href;
        link.textContent = item.label;
        li.appendChild(link);
      } else {
        li.textContent = item.label;
      }
      
      ol.appendChild(li);
    });
    
    nav.appendChild(ol);
    return nav;
  },

  // Progress indicator with clear completion status
  createProgressIndicator: (
    current: number,
    total: number,
    options: {
      showPercentage?: boolean;
      showFraction?: boolean;
      label?: string;
      announceChanges?: boolean;
    } = {}
  ) => {
    const {
      showPercentage = true,
      showFraction = true,
      label = 'Progress',
      announceChanges = true,
    } = options;
    
    const container = document.createElement('div');
    container.className = 'progress-container';
    container.setAttribute('role', 'progressbar');
    container.setAttribute('aria-valuenow', current.toString());
    container.setAttribute('aria-valuemin', '0');
    container.setAttribute('aria-valuemax', total.toString());
    
    if (label) {
      container.setAttribute('aria-label', label);
    }
    
    const percentage = Math.round((current / total) * 100);
    
    let labelText = '';
    if (showPercentage) labelText += `${percentage}%`;
    if (showFraction) {
      labelText += showPercentage ? ` (${current}/${total})` : `${current}/${total}`;
    }
    
    container.setAttribute('aria-valuetext', labelText);
    
    if (announceChanges) {
      aria.announceProgress(current, total, label);
    }
    
    return {
      element: container,
      update: (newCurrent: number) => {
        container.setAttribute('aria-valuenow', newCurrent.toString());
        const newPercentage = Math.round((newCurrent / total) * 100);
        
        let newLabelText = '';
        if (showPercentage) newLabelText += `${newPercentage}%`;
        if (showFraction) {
          newLabelText += showPercentage ? ` (${newCurrent}/${total})` : `${newCurrent}/${total}`;
        }
        
        container.setAttribute('aria-valuetext', newLabelText);
        
        if (announceChanges) {
          aria.announceProgress(newCurrent, total, label);
        }
      },
    };
  },

  // Status indicators with clear meaning
  createStatusIndicator: (
    status: 'success' | 'warning' | 'error' | 'info' | 'pending',
    message: string,
    options: {
      dismissible?: boolean;
      autoHide?: number; // milliseconds
      icon?: boolean;
    } = {}
  ) => {
    const { dismissible = false, autoHide, icon = true } = options;
    
    const container = document.createElement('div');
    container.className = `status-indicator status-${status}`;
    container.setAttribute('role', status === 'error' ? 'alert' : 'status');
    container.setAttribute('aria-live', status === 'error' ? 'assertive' : 'polite');
    
    if (icon) {
      const iconElement = document.createElement('span');
      iconElement.className = `status-icon status-icon-${status}`;
      iconElement.setAttribute('aria-hidden', 'true');
      container.appendChild(iconElement);
    }
    
    const messageElement = document.createElement('span');
    messageElement.textContent = message;
    container.appendChild(messageElement);
    
    if (dismissible) {
      const dismissButton = document.createElement('button');
      dismissButton.type = 'button';
      dismissButton.className = 'status-dismiss';
      dismissButton.setAttribute('aria-label', 'Dismiss');
      dismissButton.textContent = '×';
      dismissButton.addEventListener('click', () => {
        container.remove();
      });
      container.appendChild(dismissButton);
    }
    
    if (autoHide) {
      setTimeout(() => {
        container.remove();
      }, autoHide);
    }
    
    return container;
  },
};

// Initialize accessibility features
export const initializeA11y = () => {
  // Add screen reader styles
  const style = document.createElement('style');
  style.textContent = screenReader.srOnlyCSS;
  document.head.appendChild(style);
  
  // Add focus indicators
  focus.addFocusIndicators();
  
  // Create skip links
  screenReader.createSkipLinks([
    { href: '#main-navigation', text: 'Skip to main navigation' },
    { href: '#main-content', text: 'Skip to main content' },
    { href: '#sidebar', text: 'Skip to sidebar' },
  ]);
  
  // Announce page changes for SPAs
  let lastUrl = location.href;
  const observer = new MutationObserver(() => {
    if (location.href !== lastUrl) {
      lastUrl = location.href;
      setTimeout(() => {
        const title = document.title;
        aria.announce(`Page changed to ${title}`, 'polite');
      }, 100);
    }
  });
  
  observer.observe(document.body, {
    childList: true,
    subtree: true,
  });
};

// Export accessibility utilities
export const a11y = {
  aria,
  focus,
  keyboard,
  contrast,
  screenReader,
  motion,
  executiveFunction,
  initializeA11y,
};