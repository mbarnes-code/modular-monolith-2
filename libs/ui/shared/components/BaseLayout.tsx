/**
 * Base Layout Components for Mental Prosthetic Platform
 * 
 * Provides foundation layout functionality with responsive design,
 * accessibility, and executive function accommodations built-in.
 */

import React, { forwardRef, ReactNode } from 'react';
import { Theme } from '../foundation/theme';

// Layout variants
export type LayoutVariant = 'default' | 'centered' | 'sidebar' | 'split' | 'dashboard';

// Responsive breakpoints
export type Breakpoint = 'xs' | 'sm' | 'md' | 'lg' | 'xl' | '2xl';

// Grid system
export type GridCols = 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12;

// Spacing scale
export type Spacing = 0 | 1 | 2 | 3 | 4 | 5 | 6 | 8 | 10 | 12 | 16 | 20 | 24 | 32;

// Base Container Props
export interface BaseContainerProps {
  children?: ReactNode;
  
  // Layout
  variant?: LayoutVariant;
  maxWidth?: Breakpoint | 'none' | 'full';
  centered?: boolean;
  
  // Spacing
  padding?: Spacing;
  paddingX?: Spacing;
  paddingY?: Spacing;
  margin?: Spacing;
  marginX?: Spacing;
  marginY?: Spacing;
  
  // Responsive design
  fluid?: boolean; // Full width at all breakpoints
  
  // Executive function support
  landmark?: 'main' | 'aside' | 'nav' | 'header' | 'footer' | 'section';
  skipLink?: string; // ID for skip navigation
  
  // Accessibility
  'aria-label'?: string;
  'aria-labelledby'?: string;
  'aria-describedby'?: string;
  role?: string;
  id?: string;
  
  // CSS customization
  className?: string;
  style?: React.CSSProperties;
  
  // Theme context
  theme?: Theme;
}

// Grid Container Props
export interface BaseGridProps {
  children?: ReactNode;
  
  // Grid configuration
  cols?: GridCols | { [K in Breakpoint]?: GridCols };
  gap?: Spacing | { [K in Breakpoint]?: Spacing };
  rows?: number | 'auto';
  
  // Alignment
  alignItems?: 'start' | 'center' | 'end' | 'stretch';
  justifyContent?: 'start' | 'center' | 'end' | 'between' | 'around' | 'evenly';
  
  // Responsive behavior
  responsive?: boolean;
  
  // CSS customization
  className?: string;
  style?: React.CSSProperties;
  
  // Theme context
  theme?: Theme;
}

// Grid Item Props
export interface BaseGridItemProps {
  children?: ReactNode;
  
  // Grid positioning
  col?: number | 'auto' | { [K in Breakpoint]?: number | 'auto' };
  colSpan?: number | { [K in Breakpoint]?: number };
  colStart?: number | { [K in Breakpoint]?: number };
  colEnd?: number | { [K in Breakpoint]?: number };
  
  row?: number | 'auto' | { [K in Breakpoint]?: number | 'auto' };
  rowSpan?: number | { [K in Breakpoint]?: number };
  rowStart?: number | { [K in Breakpoint]?: number };
  rowEnd?: number | { [K in Breakpoint]?: number };
  
  // Alignment
  alignSelf?: 'auto' | 'start' | 'center' | 'end' | 'stretch';
  justifySelf?: 'auto' | 'start' | 'center' | 'end' | 'stretch';
  
  // CSS customization
  className?: string;
  style?: React.CSSProperties;
  
  // Theme context
  theme?: Theme;
}

// Flex Container Props
export interface BaseFlexProps {
  children?: ReactNode;
  
  // Flex configuration
  direction?: 'row' | 'column' | 'row-reverse' | 'column-reverse' | { [K in Breakpoint]?: 'row' | 'column' | 'row-reverse' | 'column-reverse' };
  wrap?: 'nowrap' | 'wrap' | 'wrap-reverse';
  
  // Alignment
  alignItems?: 'start' | 'center' | 'end' | 'stretch' | 'baseline';
  justifyContent?: 'start' | 'center' | 'end' | 'between' | 'around' | 'evenly';
  alignContent?: 'start' | 'center' | 'end' | 'stretch' | 'between' | 'around';
  
  // Gap
  gap?: Spacing | { [K in Breakpoint]?: Spacing };
  
  // CSS customization
  className?: string;
  style?: React.CSSProperties;
  
  // Theme context
  theme?: Theme;
}

// Stack Props (Vertical layout utility)
export interface BaseStackProps {
  children?: ReactNode;
  
  // Stack configuration
  spacing?: Spacing;
  align?: 'start' | 'center' | 'end' | 'stretch';
  
  // Dividers
  divider?: ReactNode;
  
  // CSS customization
  className?: string;
  style?: React.CSSProperties;
  
  // Theme context
  theme?: Theme;
}

// Breakpoint utilities
const breakpoints: Record<Breakpoint, string> = {
  xs: '0px',
  sm: '640px',
  md: '768px',
  lg: '1024px',
  xl: '1280px',
  '2xl': '1536px',
};

// Container max-width utilities
const maxWidths: Record<Breakpoint, string> = {
  xs: '20rem',
  sm: '24rem',
  md: '28rem',
  lg: '32rem',
  xl: '36rem',
  '2xl': '42rem',
};

// Spacing utilities
const spacingScale: Record<Spacing, string> = {
  0: '0',
  1: '0.25rem',
  2: '0.5rem',
  3: '0.75rem',
  4: '1rem',
  5: '1.25rem',
  6: '1.5rem',
  8: '2rem',
  10: '2.5rem',
  12: '3rem',
  16: '4rem',
  20: '5rem',
  24: '6rem',
  32: '8rem',
};

// Get spacing value
const getSpacing = (value?: Spacing): string => {
  if (value === undefined) return '0';
  return spacingScale[value] || '0';
};

// Get responsive value (simplified - in production you'd use CSS-in-JS with media queries)
const getResponsiveValue = function<T>(value: T | { [K in Breakpoint]?: T }): T | undefined {
  if (typeof value !== 'object' || value === null) {
    return value as T;
  }
  
  // Return the base value (xs breakpoint) for this simplified implementation
  const responsiveValue = value as { [K in Breakpoint]?: T };
  return responsiveValue.xs || responsiveValue.sm || responsiveValue.md || responsiveValue.lg || responsiveValue.xl || responsiveValue['2xl'];
};

// Base Container Component
export const BaseContainer = forwardRef<HTMLElement, BaseContainerProps>(
  ({
    children,
    variant = 'default',
    maxWidth = 'lg',
    centered = true,
    padding = 4,
    paddingX,
    paddingY,
    margin = 0,
    marginX,
    marginY,
    fluid = false,
    landmark,
    skipLink,
    className = '',
    style = {},
    theme,
    ...ariaProps
  }, ref) => {
    
    // Determine the HTML element
    const Element = landmark || 'div';
    
    // Calculate padding
    const paddingTop = getSpacing(paddingY ?? padding);
    const paddingBottom = getSpacing(paddingY ?? padding);
    const paddingLeft = getSpacing(paddingX ?? padding);
    const paddingRight = getSpacing(paddingX ?? padding);
    
    // Calculate margin
    const marginTop = getSpacing(marginY ?? margin);
    const marginBottom = getSpacing(marginY ?? margin);
    const marginLeft = getSpacing(marginX ?? margin);
    const marginRight = getSpacing(marginX ?? margin);
    
    // Container styles
    const containerStyles: React.CSSProperties = {
      width: '100%',
      maxWidth: fluid ? '100%' : (maxWidth === 'none' ? 'none' : (maxWidth === 'full' ? '100%' : maxWidths[maxWidth])),
      marginLeft: centered ? 'auto' : marginLeft,
      marginRight: centered ? 'auto' : marginRight,
      marginTop,
      marginBottom,
      paddingTop,
      paddingBottom,
      paddingLeft,
      paddingRight,
      ...style,
    };
    
    // Skip link element
    const skipLinkElement = skipLink ? (
      <a
        href={`#${skipLink}`}
        className="sr-only focus:not-sr-only"
        style={{
          position: 'absolute',
          left: '-9999px',
          zIndex: 999999,
          padding: '0.5rem 1rem',
          backgroundColor: theme?.colors?.primary || '#3b82f6',
          color: theme?.colors?.background || '#ffffff',
          textDecoration: 'none',
          borderRadius: '0.25rem',
        }}
        onFocus={(e) => {
          e.currentTarget.style.left = '0.5rem';
          e.currentTarget.style.top = '0.5rem';
        }}
        onBlur={(e) => {
          e.currentTarget.style.left = '-9999px';
        }}
      >
        Skip to main content
      </a>
    ) : null;
    
    return (
      <>
        {skipLinkElement}
        <Element
          ref={ref as any}
          className={`base-container base-container--${variant} ${className}`}
          style={containerStyles}
          {...ariaProps}
        >
          {children}
        </Element>
      </>
    );
  }
);

BaseContainer.displayName = 'BaseContainer';

// Base Grid Component
export const BaseGrid = forwardRef<HTMLDivElement, BaseGridProps>(
  ({
    children,
    cols = 1,
    gap = 4,
    rows = 'auto',
    alignItems = 'stretch',
    justifyContent = 'start',
    responsive = true,
    className = '',
    style = {},
    theme,
  }, ref) => {
    
    // Convert alignment values to CSS values
    const alignItemsMap: Record<string, string> = {
      start: 'flex-start',
      center: 'center',
      end: 'flex-end',
      stretch: 'stretch',
    };
    
    const justifyContentMap: Record<string, string> = {
      start: 'flex-start',
      center: 'center',
      end: 'flex-end',
      between: 'space-between',
      around: 'space-around',
      evenly: 'space-evenly',
    };
    
    // Grid styles
    const gridStyles: React.CSSProperties = {
      display: 'grid',
      gridTemplateColumns: typeof cols === 'number' ? `repeat(${cols}, 1fr)` : 'repeat(1, 1fr)',
      gridTemplateRows: rows === 'auto' ? 'auto' : `repeat(${rows}, 1fr)`,
      gap: getSpacing(typeof gap === 'number' ? gap : gap.xs || 4),
      alignItems: alignItemsMap[alignItems],
      justifyContent: justifyContentMap[justifyContent],
      ...style,
    };
    
    return (
      <div
        ref={ref}
        className={`base-grid ${className}`}
        style={gridStyles}
      >
        {children}
      </div>
    );
  }
);

BaseGrid.displayName = 'BaseGrid';

// Base Grid Item Component
export const BaseGridItem = forwardRef<HTMLDivElement, BaseGridItemProps>(
  ({
    children,
    col,
    colSpan,
    colStart,
    colEnd,
    row,
    rowSpan,
    rowStart,
    rowEnd,
    alignSelf = 'auto',
    justifySelf = 'auto',
    className = '',
    style = {},
    theme,
  }, ref) => {
    
    // Get responsive values
    const resolvedColSpan = getResponsiveValue(colSpan);
    const resolvedCol = getResponsiveValue(col);
    const resolvedColStart = getResponsiveValue(colStart);
    const resolvedColEnd = getResponsiveValue(colEnd);
    const resolvedRowSpan = getResponsiveValue(rowSpan);
    const resolvedRow = getResponsiveValue(row);
    const resolvedRowStart = getResponsiveValue(rowStart);
    const resolvedRowEnd = getResponsiveValue(rowEnd);
    
    // Grid item styles
    const gridItemStyles: React.CSSProperties = {
      gridColumn: resolvedColSpan ? `span ${resolvedColSpan}` : (resolvedCol === 'auto' ? 'auto' : (resolvedCol ? `${resolvedCol}` : undefined)),
      gridColumnStart: resolvedColStart,
      gridColumnEnd: resolvedColEnd,
      gridRow: resolvedRowSpan ? `span ${resolvedRowSpan}` : (resolvedRow === 'auto' ? 'auto' : (resolvedRow ? `${resolvedRow}` : undefined)),
      gridRowStart: resolvedRowStart,
      gridRowEnd: resolvedRowEnd,
      alignSelf: alignSelf === 'auto' ? 'auto' : alignSelf,
      justifySelf: justifySelf === 'auto' ? 'auto' : justifySelf,
      ...style,
    };
    
    return (
      <div
        ref={ref}
        className={`base-grid-item ${className}`}
        style={gridItemStyles}
      >
        {children}
      </div>
    );
  }
);

BaseGridItem.displayName = 'BaseGridItem';

// Base Flex Component
export const BaseFlex = forwardRef<HTMLDivElement, BaseFlexProps>(
  ({
    children,
    direction = 'row',
    wrap = 'nowrap',
    alignItems = 'stretch',
    justifyContent = 'start',
    alignContent = 'stretch',
    gap = 0,
    className = '',
    style = {},
    theme,
  }, ref) => {
    
    // Convert alignment values to CSS values
    const alignItemsMap: Record<string, string> = {
      start: 'flex-start',
      center: 'center',
      end: 'flex-end',
      stretch: 'stretch',
      baseline: 'baseline',
    };
    
    const justifyContentMap: Record<string, string> = {
      start: 'flex-start',
      center: 'center',
      end: 'flex-end',
      between: 'space-between',
      around: 'space-around',
      evenly: 'space-evenly',
    };
    
    const alignContentMap: Record<string, string> = {
      start: 'flex-start',
      center: 'center',
      end: 'flex-end',
      stretch: 'stretch',
      between: 'space-between',
      around: 'space-around',
    };
    
    // Flex styles
    const flexStyles: React.CSSProperties = {
      display: 'flex',
      flexDirection: typeof direction === 'string' ? direction : direction.xs || 'row',
      flexWrap: wrap,
      alignItems: alignItemsMap[alignItems],
      justifyContent: justifyContentMap[justifyContent],
      alignContent: alignContentMap[alignContent],
      gap: getSpacing(typeof gap === 'number' ? gap : gap.xs || 0),
      ...style,
    };
    
    return (
      <div
        ref={ref}
        className={`base-flex ${className}`}
        style={flexStyles}
      >
        {children}
      </div>
    );
  }
);

BaseFlex.displayName = 'BaseFlex';

// Base Stack Component (Vertical layout utility)
export const BaseStack = forwardRef<HTMLDivElement, BaseStackProps>(
  ({
    children,
    spacing = 4,
    align = 'stretch',
    divider,
    className = '',
    style = {},
    theme,
  }, ref) => {
    
    const childrenArray = React.Children.toArray(children);
    
    // Stack styles
    const stackStyles: React.CSSProperties = {
      display: 'flex',
      flexDirection: 'column',
      alignItems: align === 'start' ? 'flex-start' : align === 'end' ? 'flex-end' : align,
      ...style,
    };
    
    return (
      <div
        ref={ref}
        className={`base-stack ${className}`}
        style={stackStyles}
      >
        {childrenArray.map((child, index) => (
          <React.Fragment key={index}>
            {child}
            {divider && index < childrenArray.length - 1 && (
              <div style={{ marginTop: getSpacing(spacing), marginBottom: getSpacing(spacing) }}>
                {divider}
              </div>
            )}
            {!divider && index < childrenArray.length - 1 && (
              <div style={{ height: getSpacing(spacing) }} />
            )}
          </React.Fragment>
        ))}
      </div>
    );
  }
);

BaseStack.displayName = 'BaseStack';

// Higher-order components for themed layouts
export const withTheme = (theme: Theme) => ({
  Container: forwardRef<HTMLElement, Omit<BaseContainerProps, 'theme'>>((props, ref) => (
    <BaseContainer ref={ref} {...props} theme={theme} />
  )),
  Grid: forwardRef<HTMLDivElement, Omit<BaseGridProps, 'theme'>>((props, ref) => (
    <BaseGrid ref={ref} {...props} theme={theme} />
  )),
  GridItem: forwardRef<HTMLDivElement, Omit<BaseGridItemProps, 'theme'>>((props, ref) => (
    <BaseGridItem ref={ref} {...props} theme={theme} />
  )),
  Flex: forwardRef<HTMLDivElement, Omit<BaseFlexProps, 'theme'>>((props, ref) => (
    <BaseFlex ref={ref} {...props} theme={theme} />
  )),
  Stack: forwardRef<HTMLDivElement, Omit<BaseStackProps, 'theme'>>((props, ref) => (
    <BaseStack ref={ref} {...props} theme={theme} />
  )),
});

// Export utilities
export { breakpoints, getSpacing, maxWidths, spacingScale };

// Types are exported with their declarations above