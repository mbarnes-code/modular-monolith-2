# Firecrawl UI Library

A collection of React components for building Firecrawl interfaces within the Jane Mental Prosthetic Platform.

## Overview

This library provides a comprehensive set of React components specifically designed for Firecrawl web scraping and crawling interfaces. Built with modern React patterns and following the design system principles of the Jane platform.

## Components

### Main Components

- **FirecrawlApp**: The main application wrapper component
- **Ingestion**: Advanced scraping configuration interface
- **IngestionV1**: Legacy ingestion interface for backward compatibility

### Base UI Components

All base components are built on top of Radix UI primitives and styled with Tailwind CSS:

- **Button**: Action buttons with multiple variants
- **Card**: Container component for grouped content
- **Checkbox**: Boolean input controls
- **Collapsible**: Expandable content sections
- **Input**: Text input fields
- **Label**: Form labels with accessibility features
- **RadioGroup**: Single-choice option controls

## Installation

This library is part of the NX monorepo and is consumed by other projects within the workspace:

```bash
# Build the library
npx nx build firecrawl-ui

# Test the library
npx nx test firecrawl-ui

# Lint the library
npx nx lint firecrawl-ui
```

## Usage

### Basic Import

```typescript
import { FirecrawlApp, Button, Card } from '@firecrawl/ui';

function MyComponent() {
  return (
    <Card>
      <FirecrawlApp />
      <Button variant="primary">Scrape Website</Button>
    </Card>
  );
}
```

### Advanced Configuration

```typescript
import { Ingestion } from '@firecrawl/ui';

function AdvancedScraper() {
  return (
    <Ingestion
      onSubmit={(config) => {
        // Handle scraping configuration
        console.log('Scrape config:', config);
      }}
      defaultValues={{
        url: 'https://example.com',
        formats: ['markdown', 'html'],
        includeLinks: true,
      }}
    />
  );
}
```

## Component Props

### Button

```typescript
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'destructive' | 'outline' | 'ghost';
  size?: 'sm' | 'default' | 'lg';
  asChild?: boolean;
}
```

### Card

```typescript
interface CardProps {
  className?: string;
  children: ReactNode;
}
```

### Ingestion

```typescript
interface IngestionProps {
  onSubmit: (config: ScrapeConfig) => void;
  defaultValues?: Partial<ScrapeConfig>;
  isLoading?: boolean;
}
```

## Styling

The library uses Tailwind CSS for styling with a custom design system:

- **Colors**: Jane platform color palette
- **Typography**: Consistent font scales and weights
- **Spacing**: 8px grid system
- **Shadows**: Consistent depth hierarchy

### Custom CSS Variables

```css
:root {
  --firecrawl-primary: hsl(var(--primary));
  --firecrawl-secondary: hsl(var(--secondary));
  --firecrawl-accent: hsl(var(--accent));
}
```

## Accessibility

All components follow WCAG 2.1 AA guidelines:

- **Keyboard Navigation**: Full keyboard support
- **Screen Readers**: Proper ARIA labels and descriptions
- **Focus Management**: Visible focus indicators
- **Color Contrast**: Minimum 4.5:1 contrast ratios

## Theming

Components support both light and dark themes through CSS custom properties:

```typescript
import { FirecrawlApp } from '@firecrawl/ui';

function App() {
  return (
    <div className="theme-dark"> {/* or theme-light */}
      <FirecrawlApp />
    </div>
  );
}
```

## Development

### Adding New Components

1. Create component in `src/components/`
2. Add comprehensive TypeScript types
3. Include Storybook stories
4. Write unit tests
5. Export from `src/index.ts`

### Component Template

```typescript
import React from 'react';
import { cn } from '../lib/utils';

interface MyComponentProps {
  className?: string;
  children?: React.ReactNode;
}

export function MyComponent({ className, children, ...props }: MyComponentProps) {
  return (
    <div className={cn('base-styles', className)} {...props}>
      {children}
    </div>
  );
}

MyComponent.displayName = 'MyComponent';
```

### Testing

```bash
# Run all tests
npx nx test firecrawl-ui

# Run tests in watch mode
npx nx test firecrawl-ui --watch

# Generate coverage report
npx nx test firecrawl-ui --coverage
```

## Dependencies

### Peer Dependencies

- `react >= 18.0.0`
- `react-dom >= 18.0.0`

### Core Dependencies

- `@radix-ui/react-*`: Base component primitives
- `class-variance-authority`: Component variant management
- `clsx`: Conditional className utility
- `lucide-react`: Icon library
- `tailwind-merge`: Tailwind class merging

## Browser Support

- **Chrome**: Last 2 versions
- **Firefox**: Last 2 versions
- **Safari**: Last 2 versions
- **Edge**: Last 2 versions

## Contributing

### Design System Guidelines

1. **Consistency**: Follow existing component patterns
2. **Accessibility**: Ensure WCAG compliance
3. **Performance**: Optimize for bundle size
4. **Documentation**: Include comprehensive examples

### Code Standards

- **TypeScript**: Strict mode enabled
- **ESLint**: Airbnb configuration with React hooks
- **Prettier**: Consistent code formatting
- **Testing**: Jest + React Testing Library

## License

This library is part of the Jane Mental Prosthetic Platform and follows the project's overall licensing terms.