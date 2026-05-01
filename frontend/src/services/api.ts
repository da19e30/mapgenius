import axios, { AxiosError } from 'axios';
import { getToken, clearToken } from '@/context/AuthContext';

// Base URL configurada via env (Vite usa import.meta.env)
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL ?? 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Adjuntar JWT a cada request
api.interceptors.request.use((config: any) => {
  console.log('Interceptor adding token:', getToken());
  const token = getToken();
  if (token) {
    config.headers = {
      ...config.headers,
      Authorization: `Bearer ${token}`,
    };
  }
  return config;
});

// Manejo centralizado de errores
api.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    if (error.response?.status === 401) {
      clearToken();
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;
