import { createContext, useContext, useEffect, useState, ReactNode } from 'react';

type Theme = 'light' | 'dark' | 'system';

type ThemeContextType = {
  theme: Theme;
  setTheme: (theme: Theme) => void;
  toggleTheme: () => void;
};

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export const ThemeProvider = ({ children }: { children: ReactNode }) => {
  // Determine initial theme: check localStorage, then system preference
  const getInitialTheme = (): Theme => {
    const saved = localStorage.getItem('theme') as Theme | null;
    if (saved) return saved;
    // system default
    return 'system';
  };

  const [theme, setThemeState] = useState<Theme>(getInitialTheme());

  // Apply theme class to root html element
  useEffect(() => {
    const root = window.document.documentElement;
    const apply = (t: Theme) => {
      root.classList.remove('light', 'dark');
      if (t === 'system') {
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        root.classList.add(prefersDark ? 'dark' : 'light');
      } else {
        root.classList.add(t);
      }
    };
    apply(theme);
    // Persist to localStorage unless system (optional persist system as well)
    localStorage.setItem('theme', theme);
  }, [theme]);

  const setTheme = (t: Theme) => {
    setThemeState(t);
  };

  const toggleTheme = () => {
    setThemeState(prev => {
      if (prev === 'light') return 'dark';
      if (prev === 'dark') return 'light';
      // if system, toggle based on current media query
      const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
      return prefersDark ? 'light' : 'dark';
    });
  };

  return (
    <ThemeContext.Provider value={{ theme, setTheme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
};

export const useTheme = () => {
  const ctx = useContext(ThemeContext);
  if (!ctx) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return ctx;
};
