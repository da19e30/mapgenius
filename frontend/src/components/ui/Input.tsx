import React from 'react';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  className?: string;
}

export const Input: React.FC<InputProps> = ({ label, error, className = '', ...rest }) => {
  return (
    <div className={`flex flex-col ${className}`}>
      {label && (
        <label className="mb-1 text-sm font-medium text-gray-700 dark:text-gray-200">{label}</label>
      )}
      <input
        className={`rounded-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 px-3 py-2 text-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 ${error ? 'border-red-500' : ''}`}
        {...rest}
      />
      {error && <p className="mt-1 text-xs text-red-600">{error}</p>}
    </div>
  );
};
