import React, { useEffect } from 'react';

interface ToastProps {
  id: string;
  message: string;
  variant?: 'success' | 'error' | 'info';
  duration?: number; // ms
  onClose: (id: string) => void;
}

export const Toast: React.FC<ToastProps> = ({ id, message, variant = 'info', duration = 3000, onClose }) => {
  // Auto‑close after the specified duration
  useEffect(() => {
    const timer = setTimeout(() => onClose(id), duration);
    return () => clearTimeout(timer);
  }, [id, duration, onClose]);

  const base = 'flex items-center p-4 rounded-md shadow-md pointer-events-auto';
  const variants: Record<string, string> = {
    success: 'bg-green-600 text-white',
    error: 'bg-red-600 text-white',
    info: 'bg-gray-700 text-white',
  };

  return (
    <div className={`${base} ${variants[variant]}`} role="alert">
      <span className="flex-1">{message}</span>
      <button
        onClick={() => onClose(id)}
        className="ml-4 text-sm font-medium underline"
        aria-label="Close toast"
      >
        ✕
      </button>
    </div>
  );
};
