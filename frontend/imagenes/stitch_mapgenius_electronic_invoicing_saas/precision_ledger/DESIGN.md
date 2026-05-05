---
name: Precision Ledger
colors:
  surface: '#fcf8fa'
  surface-dim: '#dcd9db'
  surface-bright: '#fcf8fa'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f6f3f5'
  surface-container: '#f0edef'
  surface-container-high: '#eae7e9'
  surface-container-highest: '#e4e2e4'
  on-surface: '#1b1b1d'
  on-surface-variant: '#45464d'
  inverse-surface: '#303032'
  inverse-on-surface: '#f3f0f2'
  outline: '#76777d'
  outline-variant: '#c6c6cd'
  surface-tint: '#565e74'
  primary: '#000000'
  on-primary: '#ffffff'
  primary-container: '#131b2e'
  on-primary-container: '#7c839b'
  inverse-primary: '#bec6e0'
  secondary: '#505f76'
  on-secondary: '#ffffff'
  secondary-container: '#d0e1fb'
  on-secondary-container: '#54647a'
  tertiary: '#000000'
  on-tertiary: '#ffffff'
  tertiary-container: '#271901'
  on-tertiary-container: '#98805d'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#dae2fd'
  primary-fixed-dim: '#bec6e0'
  on-primary-fixed: '#131b2e'
  on-primary-fixed-variant: '#3f465c'
  secondary-fixed: '#d3e4fe'
  secondary-fixed-dim: '#b7c8e1'
  on-secondary-fixed: '#0b1c30'
  on-secondary-fixed-variant: '#38485d'
  tertiary-fixed: '#fcdeb5'
  tertiary-fixed-dim: '#dec29a'
  on-tertiary-fixed: '#271901'
  on-tertiary-fixed-variant: '#574425'
  background: '#fcf8fa'
  on-background: '#1b1b1d'
  surface-variant: '#e4e2e4'
typography:
  h1:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.02em
  h2:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: -0.01em
  h3:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
    letterSpacing: -0.01em
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  body-sm:
    fontFamily: Inter
    fontSize: 13px
    fontWeight: '400'
    lineHeight: 18px
  label-md:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.05em
  mono-data:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 4px
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  2xl: 48px
  3xl: 64px
  container-max: 1280px
  gutter: 24px
---

## Brand & Style
The design system is engineered to project absolute reliability and institutional-grade precision. It targets finance professionals and business owners who require a high-density information environment that remains legible and stress-free. 

The aesthetic follows a **Corporate Modern** movement, characterized by a structured layout, purposeful use of whitespace, and a monochromatic foundation punctuated by high-intent color accents. By prioritizing clarity over decoration, the design system ensures that complex financial data is the hero, while the interface provides a silent, sturdy framework for decision-making.

## Colors
The palette is rooted in a deep "Ink" Navy to establish authority and trust. This is balanced by a Slate Gray secondary scale used for supporting UI elements and body text, ensuring a soft but clear hierarchy. 

**Emerald Green** is utilized exclusively as an action color and a symbol of positive financial growth, reserved for "Primary" actions or successful status indicators. Backgrounds utilize a very light cool gray to reduce eye strain during long-form data entry. Status colors adhere to industry standards to ensure immediate cognitive recognition of financial health (e.g., Red for deficits/errors).

## Typography
Inter is the sole typeface for the design system, chosen for its exceptional legibility in digital interfaces and its robust support for tabular numbers. 

For data-heavy tables, the system defaults to `tnum` (tabular figures) to ensure columns of numbers align perfectly for easy vertical scanning. Headline styles use tighter letter spacing and heavier weights to provide clear section anchors, while labels use an uppercase treatment to differentiate from editable content.

## Layout & Spacing
The design system employs a **Fixed Grid** philosophy for primary content containers to maintain readability, while utilizing fluid dashboard widgets for data visualization. A 12-column grid is used for main layouts, with a 24px gutter to provide ample breathing room between dense data sets.

The spacing scale is strictly linear, based on a 4px increment. Horizontal padding in tables and forms should prioritize the `md` (16px) unit, while vertical section spacing should leverage `2xl` (48px) to prevent the UI from feeling cluttered.

## Elevation & Depth
Depth is communicated through **Tonal Layers** and **Ambient Shadows**. Surfaces are tiered to indicate hierarchy:

1.  **Level 0 (Background):** The base layer (#F8FAFC).
2.  **Level 1 (Cards/Containers):** Pure white (#FFFFFF) with a 1px border (#E2E8F0) and a very soft, diffused shadow.
3.  **Level 2 (Popovers/Modals):** Elevated with a more pronounced shadow (12% opacity) to indicate temporary focus.

Shadows must be "ink-tinted" by using a dark navy base rather than pure black, ensuring they feel integrated into the professional color palette.

## Shapes
The design system uses a consistent **Rounded** (8px) corner radius across all interactive elements including buttons, input fields, and cards. This radius strikes a balance between the precision of sharp corners and the approachability of fully rounded shapes. 

Smaller elements like tags or checkboxes should scale down to a 4px radius, while large modals or hero containers may scale up to 16px to maintain visual proportion.

## Components

### Buttons
- **Primary:** Deep Navy background, white text. High contrast for main conversion points.
- **Secondary:** White background, Slate Gray border and text. Used for "Cancel" or neutral actions.
- **Accent/Success:** Emerald Green background. Reserved for "Finalize," "Pay," or "Approve."

### Input Fields
Inputs use a white background with a 1px Slate Gray border (#CBD5E1). On focus, the border shifts to Emerald Green with a subtle 2px glow of the same color at 20% opacity. Labels are always positioned above the input for maximum clarity.

### Data Tables
Tables are the core of this system. They feature:
- Sticky headers with a subtle bottom border.
- Row hovering with a light gray background (#F1F5F9).
- Column alignment: Text is left-aligned; Currency and numbers are right-aligned using tabular figures.

### Chips & Status Indicators
Status indicators use "Pill" shapes with a low-opacity background and a high-contrast text label of the same hue (e.g., Success is Emerald at 10% BG / 100% Text).

### Cards
Cards are the primary container for dashboard widgets. They feature a white background, an 8px corner radius, and a 1px border. Titles within cards are always bolded using the `h3` or `body-lg` style.