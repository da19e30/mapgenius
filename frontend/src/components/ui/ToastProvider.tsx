import React, { createContext, useContext, useState } from 'react';
import { Toast } from './Toast';

type ToastInfo = {
  id: string;
  message: string;
  variant?: 'success' | 'error' | 'info';
  duration?: number;
};

type ToastContextType = {
  addToast: (msg: string, variant?: ToastInfo['variant'], duration?: number) => void;
};

const ToastContext = createContext<ToastContextType | undefined>(undefined);

export const ToastProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [toasts, setToasts] = useState<ToastInfo[]>([]);

  const addToast = (msg: string, variant: ToastInfo['variant'] = 'info', duration?: number) => {
    const id = Date.now().toString() + Math.random().toString(36).slice(2);
    setToasts((prev) => [...prev, { id, message: msg, variant, duration }]);
  };

  const removeToast = (id: string) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  };

  return (
    <ToastContext.Provider value={{ addToast }}>
      {children}
      <div className="fixed bottom-4 left-4 flex flex-col gap-2 z-50 max-w-xs">
        {toasts.map((t) => (
          <Toast key={t.id} id={t.id} message={t.message} variant={t.variant} duration={t.duration} onClose={removeToast} />
        ))}
      </div>
    </ToastContext.Provider>
  );
};

export const useToast = () => {
  const ctx = useContext(ToastContext);
  if (!ctx) throw new Error('useToast must be used within ToastProvider');
  return ctx;
};
