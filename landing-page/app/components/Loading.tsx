import React from 'react';

export default function Loading() {
  return (
    <div className="flex flex-col items-center justify-center h-screen bg-white">
      <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">FLYFOX AI</h1>
      <p className="text-lg text-gray-600">Goliath of All Trade</p>
      <p className="text-lg text-gray-600">Sigma Select</p>
      <div className="mt-4 animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      <p className="mt-4 text-gray-500">Loading...</p>
    </div>
  );
}