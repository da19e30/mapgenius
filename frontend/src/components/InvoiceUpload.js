// InvoiceUpload.js
// Drag‑and‑drop uploader for invoices. Uses native file input for accessibility.

import React, { useState, useRef } from "react";
import { colors, spacing, radii, shadows } from "./DesignSystem";

export default function InvoiceUpload({ onUpload }) {
  const [files, setFiles] = useState([]);
  const inputRef = useRef(null);

  const handleFiles = (selected) => {
    const list = Array.from(selected);
    setFiles((prev) => [...prev, ...list]);
    if (onUpload) onUpload(list);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    handleFiles(e.dataTransfer.files);
  };

  const handleDragOver = (e) => e.preventDefault();

  const openFileDialog = () => inputRef.current?.click();

  return (
    <div className="flex flex-col items-center justify-center p-6 bg-gray-50 rounded-lg"
      style={{ border: `2px dashed ${colors.border}`, borderRadius: radii.lg }}
      onDrop={handleDrop}
      onDragOver={handleDragOver}
      role="region"
      aria-label="Subida de facturas"
      tabIndex={0}
    >
      <input
        type="file"
        multiple
        accept="image/*,application/pdf"
        ref={inputRef}
        className="hidden"
        onChange={(e) => handleFiles(e.target.files)}
      />
      <svg
        className="w-12 h-12 text-gray-400 mb-4"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth={2}
          d="M7 16V4h10v12M5 20h14"
        />
      </svg>
      <p className="text-gray-600 mb-2">Arrastra tus facturas aquí</p>
      <button
        onClick={openFileDialog}
        className="mt-2 px-4 py-2 bg-primary text-white rounded"
        style={{ backgroundColor: colors.primary }}
      >
        Seleccionar archivos
      </button>
      {files.length > 0 && (
        <ul className="mt-4 w-full max-w-md">
          {files.map((file, i) => (
            <li key={i} className="text-sm text-gray-700 truncate">
              {file.name}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
