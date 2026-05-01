// DesignSystem.js
// Basic design tokens for Mapgenius Solutions UI
// Colors, typography, spacing, radii, and shadows are defined here.
// These tokens can be imported by Tailwind config or used directly in components.

export const colors = {
  primary: "#1A73E8", // Trustworthy blue
  secondary: "#34A853", // Growth green
  background: "#F5F7FA", // Light neutral background
  surface: "#FFFFFF", // Card surface
  textPrimary: "#212529", // Dark gray for main text
  textSecondary: "#6C757D", // Muted text
  border: "#E2E6EA", // Light border
  success: "#28A745",
  danger: "#DC3545",
  warning: "#FFC107",
};

export const typography = {
  fontFamily: "'Inter', ui-sans-serif, system-ui, sans-serif",
  heading: "font-bold text-2xl",
  subheading: "font-semibold text-xl",
  body: "text-base",
  caption: "text-sm",
};

export const spacing = {
  xs: "0.25rem",
  sm: "0.5rem",
  md: "1rem",
  lg: "1.5rem",
  xl: "2rem",
};

export const radii = {
  sm: "0.25rem",
  md: "0.5rem",
  lg: "0.75rem",
};

export const shadows = {
  card: "0 1px 3px rgba(0,0,0,0.1)",
  modal: "0 4px 12px rgba(0,0,0,0.15)",
};
