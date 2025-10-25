// export interface Dataset {
//   id: string;
//   filename: string;
//   originalSize: number;
//   cleanedSize: number;
//   hash: string;
//   timestamp: string;
//   solanaTx?: string;
//   status: 'processing' | 'completed' | 'failed';
// }

// export interface UploadResponse {
//   success: boolean;
//   hash: string;
//   filename: string;
//   downloadUrl: string;
//   solanaTx?: string;
// }

// export interface VerificationResponse {
//   verified: boolean;
//   hash: string;
//   timestamp: string | null;  // ✅ Now allows null
//   solanaTx: string | null;   // ✅ Now allows null
//   metadata?: {
//     filename?: string;
//     size?: number;
//     rows?: number;
//     cleanedAt?: string;
//   } | null;  // ✅ Also make metadata nullable
// }




// src/types/index.ts - COMPLETE REPLACEMENT

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
  solanaTx?: string;
  
  // NEW FIELDS added for Multimodal / Dual Output Synchronization
  type: 'tabular' | 'tabular_duplicate' | 'audio' | 'unsupported';
  download_ml_url: string;   // URL for ML-Ready (Encoded/Embedded) output
  download_text_url: string; // URL for Human-Readable (Clean Text) output
  cleaned_rows: number;
  columns: number;
}

export interface VerificationResponse {
  verified: boolean;
  hash: string;
  timestamp: string | null;
  solanaTx: string | null;
  metadata?: {
    filename?: string;
    size?: number;
    rows?: number;
    cleanedAt?: string;
  } | null;
}