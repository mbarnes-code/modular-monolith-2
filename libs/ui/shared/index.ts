/**
 * Shared UI Components Index
 * 
 * Exports all base components for the Mental Prosthetic Platform
 */

// Foundation exports
export { a11y } from './foundation/accessibility';
export { designTokens, executiveFunction as efTokens, focus as focusTokens } from './foundation/design-tokens';
export { Theme, ThemeConfig, createTheme } from './foundation/theme';

// Component exports
export { BaseButton } from './components/BaseButton';
export type { BaseButtonProps, ButtonSize, ButtonVariant } from './components/BaseButton';

export { BaseInput } from './components/BaseInput';
export type { BaseInputProps, InputSize, InputType, InputVariant, ValidationState } from './components/BaseInput';

export { BaseCard } from './components/BaseCard';
export type { BaseCardProps, CardPadding, CardSize, CardVariant } from './components/BaseCard';

export { BaseModal } from './components/BaseModal';
export type { BaseModalProps, ModalPosition, ModalSize } from './components/BaseModal';

export { BaseContainer, BaseFlex, BaseGrid, BaseGridItem, BaseStack } from './components/BaseLayout';
export type {
    BaseContainerProps, BaseFlexProps, BaseGridItemProps, BaseGridProps, BaseStackProps, Breakpoint,
    GridCols, LayoutVariant, Spacing
} from './components/BaseLayout';

// Convenience re-exports with common names
export { BaseButton as Button } from './components/BaseButton';
export { BaseCard as Card } from './components/BaseCard';
export { BaseInput as Input } from './components/BaseInput';
export {
    BaseContainer as Container, BaseFlex as Flex, BaseGrid as Grid,
    BaseGridItem as GridItem, BaseStack as Stack
} from './components/BaseLayout';
export { BaseModal as Modal } from './components/BaseModal';
