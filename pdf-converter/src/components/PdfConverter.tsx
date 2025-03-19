// PdfConverter.tsx
import React, { useState } from 'react';
import axios from 'axios';

export default function PdfConverter() {
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleFileUpload = async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    await convertDocument(formData);
  };

  const convertDocument = async (data: FormData | string) => {
    try {
      setLoading(true);
      const payload = typeof data === 'string' ? { text: data } : data;
      const response = await axios.post('http://localhost:5000/convert', payload, {
        headers: {
          'Content-Type': typeof data === 'string' 
            ? 'application/json' 
            : 'multipart/form-data'
        },
        responseType: 'blob'
      });

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'document.pdf');
      document.body.appendChild(link);
      link.click();
      link.remove();
      
    } catch (err) {
      setError('Conversion failed. Please check your input.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4">
      <div className="max-w-3xl mx-auto bg-white rounded-lg shadow-md p-8">
        <h1 className="text-2xl font-bold text-gray-800 mb-6">
          DeepSeek to PDF Converter
        </h1>

        <div className="mb-6">
          <textarea
            className="w-full h-48 p-4 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="Paste your DeepSeek response here..."
            value={text}
            onChange={(e) => setText(e.target.value)}
          />
        </div>

        <div className="flex items-center gap-4 mb-6">
          <button
            onClick={() => convertDocument(text)}
            disabled={loading}
            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400"
          >
            {loading ? 'Converting...' : 'Convert Text'}
          </button>

          <label className="px-6 py-2 bg-gray-100 text-gray-700 rounded-lg cursor-pointer hover:bg-gray-200">
            <input
              type="file"
              className="hidden"
              onChange={(e) => e.target.files?.[0] && handleFileUpload(e.target.files[0])}
            />
            Upload File
          </label>
        </div>

        {error && (
          <div className="text-red-600 bg-red-100 p-3 rounded-lg">
            {error}
          </div>
        )}
      </div>
    </div>
  );
}
