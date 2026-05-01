import { createContext, useContext, useState, ReactNode, useEffect } from 'react';

interface AuthContextType {
  email: string | null;
  token: string | null;
  login: (token: string, email?: string) => void;
  logout: () => void;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType>({
  token: null,
  login: () => {},
  email: null,
  logout: () => {},
  isAuthenticated: false,
});

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [token, setToken] = useState<string | null>(
    localStorage.getItem('jwt')
  );
  const [email, setEmail] = useState<string | null>(
    localStorage.getItem('email')
  );

  useEffect(() => {
    if (token) {
      localStorage.setItem('jwt', token);
    } else {
      localStorage.removeItem('jwt');
    }
    if (email) {
      localStorage.setItem('email', email);
    } else {
      localStorage.removeItem('email');
    }
  }, [token]);

  const login = (newToken: string, userEmail?: string) => {
    setToken(newToken);
    if (userEmail) setEmail(userEmail);
  };
  const logout = () => {
    setToken(null);
    clearToken();
  };

  return (
    <AuthContext.Provider value={{ token, email, login, logout, isAuthenticated: !!token }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);

export const getToken = (): string | null => localStorage.getItem('jwt');
export const clearToken = (): void => localStorage.removeItem('jwt');
