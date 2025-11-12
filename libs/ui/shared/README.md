# Shared UI Components

Foundation UI components for the Mental Prosthetic Platform with accessibility, theming, and executive function accommodations built-in.

## Overview

This library provides a comprehensive set of base UI components that serve as the foundation for all domain-specific interfaces while maintaining:

- **Accessibility**: WCAG 2.1 AA compliance with ARIA utilities, keyboard navigation, and screen reader support
- **Executive Function Support**: ADHD/autism accommodations with clear feedback, context preservation, and reduced cognitive load
- **Theming**: Multi-variant theming system supporting light/dark/high-contrast modes with domain-specific customization
- **Responsive Design**: Mobile-first approach with flexible breakpoint system
- **Type Safety**: Full TypeScript support with comprehensive prop types

## Architecture

```
libs/ui/shared/
├── foundation/
│   ├── design-tokens.ts    # Color system, typography, spacing, executive function tokens
│   ├── theme.ts           # Theme system with domain-specific variants
│   └── accessibility.ts   # ARIA utilities, focus management, keyboard navigation
└── components/
    ├── BaseButton.tsx     # Foundation button with accessibility & theming
    ├── BaseInput.tsx      # Form input with validation & executive function support
    ├── BaseCard.tsx       # Container component with status indicators
    ├── BaseModal.tsx      # Dialog component with focus management
    └── BaseLayout.tsx     # Grid, flex, and container layout utilities
```

## Design Tokens

The design system includes:

### Colors
- **Domain Palettes**: Security (blues/reds), Productivity (greens/blues), TCG (purples/golds), Infrastructure (grays/blues), Finance (greens/oranges)
- **Semantic Colors**: Success, warning, error, info with consistent meanings across domains
- **Accessibility**: High contrast ratios, color-blind friendly palettes

### Typography
- **Dyslexic Support**: OpenDyslexic font option, increased line spacing, clear character distinction
- **Scale**: Consistent type scale from 0.75rem to 3rem
- **Weights**: Light to black with semantic naming

### Executive Function Accommodations
- **Context Preservation**: Persistent state indicators, breadcrumb navigation
- **Clear Feedback**: Immediate response indicators, progress tracking
- **Reduced Cognitive Load**: Simplified interactions, consistent patterns

## Components

### BaseButton
Foundation button component with variants, sizes, loading states, and confirmation flows.

```tsx
import { BaseButton } from '@libs/ui/shared';

<BaseButton 
  variant="primary" 
  size="md" 
  loading={isLoading}
  confirmationRequired
  onClick={handleAction}
>
  Submit
</BaseButton>
```

### BaseInput
Form input with validation, character counting, and executive function support.

```tsx
import { BaseInput } from '@libs/ui/shared';

<BaseInput
  label="Email"
  type="email"
  required
  validationState="invalid"
  errorMessage="Please enter a valid email"
  showCharacterCount
  maxLength={100}
  contextHint="This will be your login email"
/>
```

### BaseCard
Container component with headers, footers, status indicators, and progress tracking.

```tsx
import { BaseCard } from '@libs/ui/shared';

<BaseCard
  variant="elevated"
  title="Security Analysis"
  status="warning"
  statusMessage="Review required"
  progressIndicator={{ current: 2, total: 5, steps: ['Scan', 'Analyze', 'Report'] }}
  clickable
  onClick={handleCardClick}
>
  Card content here
</BaseCard>
```

### BaseModal
Dialog component with focus management, progressive disclosure, and accessibility.

```tsx
import { BaseModal } from '@libs/ui/shared';

<BaseModal
  open={isOpen}
  onClose={handleClose}
  title="Confirm Action"
  size="md"
  showProgress
  progressSteps={{ current: 1, total: 3, steps: ['Confirm', 'Process', 'Complete'] }}
  primaryAction={{ label: 'Confirm', onClick: handleConfirm }}
  secondaryAction={{ label: 'Cancel', onClick: handleClose }}
>
  Modal content here
</BaseModal>
```

### Layout Components
Flexible layout system with responsive design and accessibility landmarks.

```tsx
import { BaseContainer, BaseGrid, BaseFlex, BaseStack } from '@libs/ui/shared';

<BaseContainer maxWidth="lg" landmark="main">
  <BaseGrid cols={3} gap={4}>
    <BaseGridItem colSpan={2}>
      Main content
    </BaseGridItem>
    <BaseGridItem>
      Sidebar
    </BaseGridItem>
  </BaseGrid>
</BaseContainer>
```

## Theming

### Domain Themes
Each domain has its own theme variant:

- **Security**: Professional blues with red alerts
- **Productivity**: Calming greens with blue accents  
- **TCG**: Rich purples with gold highlights
- **Infrastructure**: Technical grays with blue systems
- **Finance**: Trust greens with orange warnings

### Usage
```tsx
import { createTheme, domainThemes } from '@libs/ui/shared';

const securityTheme = createTheme(domainThemes.security);
const customTheme = createTheme({
  colors: { primary: '#custom-color' },
  variant: 'dark'
});
```

## Accessibility Features

### ARIA Support
- Automatic ARIA attributes based on component state
- Screen reader announcements for dynamic content
- Proper focus management and keyboard navigation

### Executive Function Support
- Context hints and progressive disclosure
- Clear visual feedback for all interactions
- Consistent interaction patterns across components

### Keyboard Navigation
- Full keyboard accessibility for all interactive components
- Logical tab order and focus indicators
- Escape key support for dismissible components

## Domain Integration

These base components are designed to be extended by domain-specific libraries:

- `libs/ui/security/` - Security-specific components (ThreatIndicator, SecurityCard)
- `libs/ui/productivity/` - Productivity components (TaskCard, ProjectBoard)
- `libs/ui/mtg/` - TCG components (ManaSymbol, CardDisplay)
- `libs/ui/finance/` - Financial components (AccountCard, TransactionList)

Each domain library imports and extends these base components while preserving the foundational accessibility and theming infrastructure.

## Performance

- **Lazy Loading**: Components load only when needed
- **Tree Shaking**: Unused components are excluded from bundles
- **Optimized Rendering**: Minimal re-renders with proper memoization
- **Size**: Lightweight base components with minimal dependencies

## Testing

All components include:
- Unit tests for functionality and accessibility
- Visual regression tests for consistent rendering
- Integration tests for theme and responsive behavior
- E2E tests for keyboard navigation and screen reader compatibility

## Migration Guide

When migrating from existing UI components:

1. **Preserve Functionality**: All existing features must be maintained
2. **Add Accessibility**: Enhance with ARIA attributes and keyboard support  
3. **Apply Theming**: Use design tokens for consistent styling
4. **Executive Function Support**: Add context hints and clear feedback
5. **Testing**: Validate accessibility and executive function accommodations