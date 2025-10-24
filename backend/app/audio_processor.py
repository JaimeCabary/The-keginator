# audio_processor.py

import os
import io
import time
from typing import Dict, Any
from faster_whisper import WhisperModel
# REMOVED: from pydub import AudioSegment
import logging
import tempfile
import av # Explicitly use AV for robust file analysis
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# --- Faster Whisper Configuration ---
MODEL_SIZE = "small" 
DEVICE = os.getenv("WHISPER_DEVICE", "cpu")
COMPUTE_TYPE = os.getenv("WHISPER_COMPUTE_TYPE", "int8")

WHISPER_MODEL = None
try:
    logger.info(f"Initializing faster-whisper model: {MODEL_SIZE} on {DEVICE} ({COMPUTE_TYPE})")
    WHISPER_MODEL = WhisperModel(MODEL_SIZE, device=DEVICE, compute_type=COMPUTE_TYPE, local_files_only=False)
except Exception as e:
    logger.error(f"Failed to load faster-whisper model: {e}")
    WHISPER_MODEL = None


class AudioProcessor:
    """
    Handles fast audio transcription using faster-whisper.
    """
    
    def __init__(self):
        self.model = WHISPER_MODEL
        if not self.model:
            logger.error("AudioProcessor is disabled because faster-whisper model failed to load.")

    def process_audio(self, file_content: bytes, original_filename: str) -> Dict[str, Any]:
        """
        Transcribes audio content (MP3/WAV) to text.
        Returns: transcription and metadata.
        """
        if not self.model:
            raise Exception("Audio transcription service is unavailable.")

        logger.info(f"🎤 Starting transcription for: {original_filename}")
        start_time = time.time()
        
        duration_s = 0.0
        audio_file_path = None
        
        # 1. Write content to a temporary file and calculate duration using AV
        try:
            # Use tempfile for secure and automatic temporary file management
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{original_filename.split('.')[-1]}") as tmp:
                tmp.write(file_content)
                audio_file_path = tmp.name
                
            # Use AV (already installed as a dependency) to reliably determine duration
            with av.open(audio_file_path) as container:
                # Find the first audio stream
                stream = next(s for s in container.streams if s.type == 'audio')
                # Calculate duration in seconds
                duration_s = stream.duration * stream.time_base
            
        except Exception as e:
            logger.error(f"Error handling audio file {original_filename} with AV: {e}")
            if audio_file_path and os.path.exists(audio_file_path):
                 os.remove(audio_file_path)
            raise Exception(f"Invalid or corrupt audio file: {e}")
        
        try:
            # 2. Transcribe using faster-whisper (reads from the temporary file path)
            segments, info = self.model.transcribe(
                audio_file_path, 
                beam_size=5, 
                word_timestamps=True,
                vad_filter=True, 
            )
            
            full_transcript = []
            confidence_scores = []
            
            for segment in segments:
                full_transcript.append(segment.text)
                confidence_scores.append(segment.avg_logprob)
                
            # 3. Clean up temp file
            if os.path.exists(audio_file_path):
                os.remove(audio_file_path)

            end_time = time.time()
            
            # 4. Build Report
            transcript_text = " ".join(full_transcript).strip()
            
            report = {
                "file_name": original_filename,
                "duration_seconds": round(duration_s, 2),
                "transcript_text": transcript_text,
                "confidence_score_avg": round(sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0.0, 4),
                "language_detected": info.language,
                "processing_time_s": round(end_time - start_time, 2)
            }
            
            logger.info(f"✅ Transcription complete. Duration: {report['duration_seconds']}s, Time: {report['processing_time_s']}s")
            return report

        except Exception as e:
            # Ensure temp file is removed on error
            if audio_file_path and os.path.exists(audio_file_path):
                os.remove(audio_file_path)
            logger.error(f"Faster-whisper transcription failed for {original_filename}: {e}")
            raise Exception(f"Transcription failed: {e}")