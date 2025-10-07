export interface Dataset {
  id: string;
  filename: string;
  originalSize: number;
  cleanedSize: number;
  hash: string;
  timestamp: string;
  solanaTx?: string;
  status: 'processing' | 'completed' | 'failed';
}

export interface UploadResponse {
  success: boolean;
  hash: string;
  filename: string;
  downloadUrl: string;
  solanaTx?: string;
}

export interface VerificationResponse {
  verified: boolean;
  hash: string;
  timestamp: string | null;  // ✅ Now allows null
  solanaTx: string | null;   // ✅ Now allows null
  metadata?: {
    filename?: string;
    size?: number;
    rows?: number;
    cleanedAt?: string;
  } | null;  // ✅ Also make metadata nullable
}