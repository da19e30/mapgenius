import { useState, ChangeEvent, DragEvent } from 'react';
import { useToast } from '@/components/ui/ToastProvider';
import { useNavigate } from 'react-router-dom';
import api from '@/services/api';

export default function UploadInvoice() {
  const [file, setFile] = useState<File | null>(null);
  const [status, setStatus] = useState<'idle' | 'uploading' | 'success' | 'error'>('idle');
  const [message, setMessage] = useState('');
  const [isDragging, setIsDragging] = useState(false);

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files?.[0]) setFile(e.target.files[0]);
  };

  const handleDragOver = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(true);
  };
  const handleDragLeave = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);
  };
  const handleDrop = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files?.[0]) setFile(e.dataTransfer.files[0]);
  };

  const handleSubmit = async (e: React.FormEvent) => {
  const { addToast } = useToast();
    e.preventDefault();
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    setStatus('uploading');
    setMessage('');

    try {
      await api.post('/invoices/upload', formData);
      setStatus('success');
      setMessage('Factura subida y procesada correctamente.');
      addToast('Factura subida y procesada correctamente.', 'success');
      setFile(null);
              // Redirigir al Dashboard para refrescar la lista
              navigate('/dashboard');
    } catch (err: any) {
      setStatus('error');
      const errMsg = err?.response?.data?.detail || 'Error al subir la factura. Intente de nuevo.';
      setMessage(errMsg);
      addToast(errMsg, 'error');
    }
  };

  const formatSize = (bytes: number) => {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
  };

  return (
    <div className="max-w-xl mx-auto bg-white p-6 rounded shadow-md">
      <h2 className="text-2xl font-bold mb-4">Subir Factura</h2>

      {status === 'error' && (
        <div className="bg-red-100 text-red-700 p-3 mb-4 rounded border-l-4 border-red-500">{message}</div>
      )}
      {status === 'success' && (
        <div className="bg-green-100 text-green-700 p-3 mb-4 rounded border-l-4 border-green-500">{message}</div>
      )}

      <form onSubmit={handleSubmit}>
        {/* Drag & drop area */}
        <div
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors mb-4 ${
            isDragging ? 'border-indigo-600 bg-indigo-50' : 'border-gray-300 bg-gray-50'
          }`}
        >
          <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.875 1.875 0 0113.5 7.875v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m2.25 0H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a3.375 3.375 0 00-3.375-3.375z" />
          </svg>
          <p className="mt-2 text-sm text-gray-600">
            Arrastra y suelta un archivo aquí, o{' '}
            <label className="text-indigo-600 hover:text-indigo-500 cursor-pointer">
              seleccionalo desde tu dispositivo
              <input type="file" accept=".pdf,.jpg,.jpeg,.png" onChange={handleFileChange} className="hidden" required={!file} />
            </label>
          </p>
          <p className="text-xs text-gray-500 mt-1">PDF, JPG, PNG (máx. 2MB)</p>
        </div>

        {/* File preview */}
        {file && (
          <div className="bg-gray-50 p-3 rounded mb-4 flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <svg className="h-8 w-8 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.875 1.875 0 0113.5 7.875v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m2.25 0H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a3.375 3.375 0 00-3.375-3.375z" />
              </svg>
              <div>
                <p className="text-sm font-medium text-gray-900">{file.name}</p>
                <p className="text-xs text-gray-500">{formatSize(file.size)}</p>
              </div>
            </div>
            <button
              type="button"
              onClick={() => setFile(null)}
              className="text-gray-400 hover:text-gray-600"
            >
              <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        )}

        <button
          type="submit"
          disabled={status === 'uploading' || !file}
          className="w-full bg-indigo-600 text-white py-2.5 px-4 rounded-lg font-semibold hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition"
        >
          {status === 'uploading' ? (
            <span className="flex items-center justify-center">
              <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Subiendo...
            </span>
          ) : (
            'Subir Factura'
          )}
        </button>
      </form>
    </div>
  );
}
