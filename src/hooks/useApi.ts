import { useState } from 'react';
import axios from 'axios';
import { API_BASE_URL } from '../utils/constants';
import { UploadResponse, VerificationResponse, Dataset } from '../types';

const api = axios.create({
  baseURL: API_BASE_URL,
});

export const useApi = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const uploadDataset = async (file: File, userId: string = 'demo-user'): Promise<UploadResponse> => {
  setLoading(true);
  setError(null);
  
  try {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await api.post(`/upload?user_id=${userId}&auto_commit=true`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    
    return {
      success: true,
      hash: response.data.dataset_hash,
      downloadUrl: `${API_BASE_URL}${response.data.download_url}`,
      solanaTx: response.data.solana_signature,
      filename: file.name
    };
  } catch (err: any) {
    const errorMsg = err.response?.data?.detail || 'Upload failed';
    setError(errorMsg);
    throw new Error(errorMsg);
  } finally {
    setLoading(false);
  }
};


  const commitToBlockchain = async (hash: string): Promise<{ tx: string }> => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await api.post('/commit', { hash });
      return response.data;
    } catch (err: any) {
      const errorMsg = err.response?.data?.detail || 'Commit failed';
      setError(errorMsg);
      throw new Error(errorMsg);
    } finally {
      setLoading(false);
    }
  };

  const verifyHash = async (hash: string): Promise<VerificationResponse> => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await api.get(`/verify/${hash}`);
      return response.data;
    } catch (err: any) {
      const errorMsg = err.response?.data?.detail || 'Verification failed';
      setError(errorMsg);
      throw new Error(errorMsg);
    } finally {
      setLoading(false);
    }
  };

  const getHistory = async (userId: string): Promise<Dataset[]> => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await api.get(`/history/${userId}`);
      return response.data;
    } catch (err: any) {
      const errorMsg = err.response?.data?.detail || 'Failed to fetch history';
      setError(errorMsg);
      throw new Error(errorMsg);
    } finally {
      setLoading(false);
    }
  };

  return {
    loading,
    error,
    uploadDataset,
    commitToBlockchain,
    verifyHash,
    getHistory,
  };
};