import React from 'react';

interface SkeletonProps {
  width?: string | number;
  height?: string | number;
  className?: string;
}

export const Skeleton: React.FC<SkeletonProps> = ({ width = '100%', height = '1rem', className = '' }) => {
  return (
    <div
      className={`animate-pulse bg-gray-200 dark:bg-gray-700 ${className}`}
      style={{ width, height }}
    />
  );
};
