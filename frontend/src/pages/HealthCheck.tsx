import React, { useEffect, useState } from 'react';

export default function HealthCheck() {
  const [status, setStatus] = useState<string>('Loading...');

  useEffect(() => {
    const base = import.meta.env.VITE_API_URL || 'http://localhost:8000';
    fetch(`${base}/api/v1/health`)
      .then((res) => res.json())
      .then((data) => setStatus(data.status ?? 'unknown'))
      .catch(() => setStatus('error'));
  }, []);

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Health Check</h1>
      <p>Backend status: <span className="font-mono">{status}</span></p>
    </div>
  );
}
