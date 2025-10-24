# import pandas as pd
# import numpy as np
# from typing import Tuple, Dict, Any
# from datetime import datetime
# import re
# import os
# import json
# from dotenv import load_dotenv
# load_dotenv()

# try:
#     import google.generativeai as genai
#     GENAI_AVAILABLE = True
# except ImportError:
#     GENAI_AVAILABLE = False
#     print("⚠️ google-generativeai not installed. Install with: pip install google-generativeai")

# class DataCleaner:
#     """
#     AI-Powered data cleaning engine using Gemini
#     Handles missing values, duplicates, type normalization, and formatting
#     """
    
#     def __init__(self):
#         self.report = {}
#         # Initialize Gemini
#         api_key = os.getenv("GEMINI_API_KEY")
#         if api_key:
#             genai.configure(api_key=api_key)
#             self.model = genai.GenerativeModel('gemini-pro')
#             self.ai_enabled = True
#         else:
#             self.ai_enabled = False
#             print("⚠️ GEMINI_API_KEY not set. Using rule-based cleaning only.")
    
#     def clean(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
#         """
#         Main cleaning pipeline with AI-powered analysis
#         Returns: (cleaned_df, cleaning_report)
#         """
#         print("\n" + "="*80)
#         print("🚀 STARTING DATA CLEANING PIPELINE")
#         print("="*80)
        
#         self.report = {
#             "original_shape": df.shape,
#             "operations": [],
#             "ai_insights": []
#         }
        
#         df_cleaned = df.copy()
        
#         print(f"\n📊 Original Dataset: {df.shape[0]} rows × {df.shape[1]} columns")
        
#         # Step 0: AI-Powered Data Analysis (if enabled)
#         if self.ai_enabled:
#             print("\n🤖 Running AI Analysis...")
#             df_cleaned = self._ai_analyze_and_clean(df_cleaned)
        
#         # Step 1: Remove completely empty rows/columns
#         print("\n🧹 Removing empty rows/columns...")
#         df_cleaned = self._remove_empty(df_cleaned)
        
#         # Step 2: Standardize column names
#         print("📝 Standardizing column names...")
#         df_cleaned = self._standardize_columns(df_cleaned)
        
#         # Step 3: Handle duplicates
#         print("🔍 Checking for duplicates...")
#         df_cleaned = self._remove_duplicates(df_cleaned)
        
#         # Step 4: Infer and normalize data types
#         print("🔧 Normalizing data types...")
#         df_cleaned = self._normalize_types(df_cleaned)
        
#         # Step 5: Handle missing values
#         print("📌 Handling missing values...")
#         df_cleaned = self._handle_missing(df_cleaned)
        
#         # Step 6: Standardize formats (dates, strings, numbers)
#         print("✨ Standardizing formats...")
#         df_cleaned = self._standardize_formats(df_cleaned)
        
#         # Step 7: Remove outliers (conservative approach)
#         print("📊 Detecting outliers...")
#         df_cleaned = self._handle_outliers(df_cleaned)
        
#         # Step 8: AI-Powered Final Validation
#         if self.ai_enabled:
#             print("\n🎯 Running AI Validation...")
#             df_cleaned = self._ai_validate(df_cleaned)
        
#         self.report["final_shape"] = df_cleaned.shape
#         self.report["rows_removed"] = df.shape[0] - df_cleaned.shape[0]
#         self.report["columns_removed"] = df.shape[1] - df_cleaned.shape[1]
        
#         print("\n" + "="*80)
#         print("✅ CLEANING COMPLETE")
#         print(f"📊 Final Dataset: {df_cleaned.shape[0]} rows × {df_cleaned.shape[1]} columns")
#         print(f"🗑  Rows removed: {self.report['rows_removed']}")
#         print(f"🗑  Columns removed: {self.report['columns_removed']}")
#         print("="*80 + "\n")
        
#         return df_cleaned, self.report
    
#     def _ai_analyze_and_clean(self, df: pd.DataFrame) -> pd.DataFrame:
#         """Use Gemini AI to analyze dataset and suggest cleaning strategies"""
#         try:
#             summary = self._create_dataset_summary(df)
            
#             prompt = f"""You are a data cleaning expert. Analyze this dataset summary and provide a detailed cleaning plan in JSON format. 
# The dataset can contain numeric, categorical, string, datetime, or mixed types. It may have missing values, duplicates, typos, inconsistent formats, or outliers.

# Dataset Summary:
# {summary}

# Instructions:
# 1. Identify columns with potential data type issues and suggest the correct type.
# 2. Detect columns that are mostly empty or irrelevant and suggest dropping them.
# 3. Suggest value replacements for typos, inconsistent formatting, or outliers.
# 4. Identify duplicates and suggest a strategy (drop or aggregate).
# 5. Recommend how to handle missing values for each column (median, mode, forward fill, or drop).
# 6. Highlight columns that may benefit from standardization (string case, date formats, numeric rounding).
# 7. Give any additional insights or data quality issues detected.

# Output JSON format (no markdown, just JSON):
# {{
#     "column_types": {{"column_name": "recommended_type"}},
#     "columns_to_drop": ["column1", "column2"],
#     "encoding_fixes": {{"column_name": "fix_description"}},
#     "value_replacements": {{"column_name": {{"old_value": "new_value"}}}},
#     "duplicate_strategy": {{"columns": ["columns_to_check"], "action": "drop/aggregate"}},
#     "missing_value_strategy": {{"column_name": "strategy_description"}},
#     "standardization": {{"column_name": "standardization_description"}},
#     "insights": ["insight1", "insight2"]
# }}"""
            
#             response = self.model.generate_content(prompt)
#             recommendations = self._parse_ai_response(response.text)
            
#             if recommendations:
#                 print("💡 AI Recommendations:")
#                 df = self._apply_ai_recommendations(df, recommendations)
#                 self.report["ai_insights"].extend(recommendations.get("insights", []))
        
#         except Exception as e:
#             print(f"⚠️ AI analysis failed: {e}")
#             self.report["ai_insights"] = ["AI analysis unavailable"]
        
#         return df
    
#     def _create_dataset_summary(self, df: pd.DataFrame) -> str:
#         """Create a concise summary for AI analysis"""
#         summary_parts = []
        
#         summary_parts.append(f"Shape: {df.shape[0]} rows × {df.shape[1]} columns")
#         summary_parts.append(f"\nColumns: {', '.join(df.columns.tolist()[:10])}")
        
#         summary_parts.append(f"\nData Types:\n{df.dtypes.to_string()}")
        
#         missing = df.isnull().sum()
#         if missing.any():
#             summary_parts.append(f"\nMissing Values:\n{missing[missing > 0].to_string()}")
        
#         summary_parts.append(f"\nSample Data (first 3 rows):\n{df.head(3).to_string()}")
        
#         return "\n".join(summary_parts)
    
#     def _parse_ai_response(self, response_text: str) -> Dict[str, Any]:
#         """Parse AI response and extract JSON recommendations"""
#         try:
#             response_text = re.sub(r'```json\s*', '', response_text)
#             response_text = re.sub(r'```\s*', '', response_text)
            
#             recommendations = json.loads(response_text)
#             return recommendations
#         except Exception as e:
#             print(f"⚠️ Failed to parse AI recommendations: {e}")
#             return {}
    
#     def _apply_ai_recommendations(self, df: pd.DataFrame, recommendations: Dict[str, Any]) -> pd.DataFrame:
#         """Apply AI-generated cleaning recommendations and log changes"""
#         operations = []
        
#         # Drop recommended columns
#         columns_to_drop = recommendations.get("columns_to_drop", [])
#         if columns_to_drop:
#             existing_cols = [col for col in columns_to_drop if col in df.columns]
#             if existing_cols:
#                 df = df.drop(columns=existing_cols)
#                 operations.append(f"Dropped columns: {', '.join(existing_cols)}")
#                 print(f"  ✅ Dropped columns: {', '.join(existing_cols)}")
        
#         # Apply value replacements
#         replacements = recommendations.get("value_replacements", {})
#         for col, replace_map in replacements.items():
#             if col in df.columns:
#                 df[col] = df[col].replace(replace_map)
#                 operations.append(f"Replaced values in {col}: {replace_map}")
#                 print(f"  🔄 Replaced values in '{col}': {replace_map}")
        
#         # Apply recommended type conversions
#         column_types = recommendations.get("column_types", {})
#         for col, dtype in column_types.items():
#             if col in df.columns:
#                 try:
#                     if dtype == "numeric":
#                         df[col] = pd.to_numeric(df[col], errors='coerce')
#                     elif dtype == "datetime":
#                         df[col] = pd.to_datetime(df[col], errors='coerce')
#                     elif dtype == "string":
#                         df[col] = df[col].astype(str)
#                     operations.append(f"Converted {col} to {dtype}")
#                     print(f"  🔧 Converted '{col}' to {dtype}")
#                 except Exception as e:
#                     print(f"  ⚠️ Failed to convert {col}: {e}")
        
#         # Handle duplicate strategy
#         dup_strategy = recommendations.get("duplicate_strategy", {})
#         if dup_strategy.get("action") == "drop":
#             cols = dup_strategy.get("columns", df.columns.tolist())
#             initial = len(df)
#             df = df.drop_duplicates(subset=cols)
#             removed = initial - len(df)
#             operations.append(f"Dropped {removed} duplicate rows based on {cols}")
#             print(f"  🗑  Dropped {removed} duplicate rows based on {cols}")
        
#         # Apply standardization
#         standardization = recommendations.get("standardization", {})
#         for col, std_desc in standardization.items():
#             if col in df.columns:
#                 print(f"  ✨ Standardizing '{col}': {std_desc}")
#                 operations.append(f"Standardized {col}: {std_desc}")
        
#         if operations:
#             self.report["operations"].append({
#                 "step": "ai_recommendations",
#                 "actions": operations
#             })
        
#         return df
    
#     def _ai_validate(self, df: pd.DataFrame) -> pd.DataFrame:
#         """Final AI validation of cleaned data with console output"""
#         try:
#             summary = self._create_dataset_summary(df)
            
#             prompt = f"""Review this cleaned dataset and identify any remaining data quality issues.

# {summary}

# Provide issues in JSON format:
# {{
#     "quality_score": 0-100,
#     "remaining_issues": ["issue1", "issue2"],
#     "suggestions": ["suggestion1", "suggestion2"]
# }}"""
            
#             response = self.model.generate_content(prompt)
#             validation = self._parse_ai_response(response.text)
            
#             if validation:
#                 print("\n  💡 Validation Results:")
#                 score = validation.get('quality_score', 'N/A')
#                 print(f"  📈 Quality Score: {score}")
                
#                 if validation.get("remaining_issues"):
#                     print(f"  ⚠️  Remaining Issues:")
#                     for issue in validation["remaining_issues"]:
#                         print(f"    - {issue}")
                
#                 if validation.get("suggestions"):
#                     print(f"  📝 Suggestions:")
#                     for suggestion in validation["suggestions"]:
#                         print(f"    - {suggestion}")
                
#                 self.report["ai_insights"].append({
#                     "quality_score": score,
#                     "remaining_issues": validation.get("remaining_issues", []),
#                     "suggestions": validation.get("suggestions", [])
#                 })
        
#         except Exception as e:
#             print(f"  ⚠️ AI validation failed: {e}")
        
#         return df
    
#     def _remove_empty(self, df: pd.DataFrame) -> pd.DataFrame:
#         """Remove completely empty rows and columns"""
#         initial_shape = df.shape
#         df = df.dropna(how='all')
#         df = df.dropna(axis=1, how='all')
        
#         removed_rows = initial_shape[0] - df.shape[0]
#         removed_cols = initial_shape[1] - df.shape[1]
        
#         if removed_rows > 0 or removed_cols > 0:
#             self.report["operations"].append({
#                 "step": "remove_empty",
#                 "rows_removed": removed_rows,
#                 "columns_removed": removed_cols
#             })
#             if removed_rows > 0:
#                 print(f"  ✅ Removed {removed_rows} empty rows")
#             if removed_cols > 0:
#                 print(f"  ✅ Removed {removed_cols} empty columns")
        
#         return df
    
#     def _standardize_columns(self, df: pd.DataFrame) -> pd.DataFrame:
#         """Standardize column names: lowercase, underscores, no special chars"""
#         original_cols = df.columns.tolist()
#         new_cols = []
        
#         for col in df.columns:
#             col_clean = str(col).lower().strip()
#             col_clean = re.sub(r'[^\w\s]', '', col_clean)
#             col_clean = re.sub(r'\s+', '_', col_clean)
#             col_clean = re.sub(r'_+', '_', col_clean)
#             col_clean = col_clean.strip('_')
#             new_cols.append(col_clean)
        
#         seen = {}
#         for i, col in enumerate(new_cols):
#             if col in seen:
#                 seen[col] += 1
#                 new_cols[i] = f"{col}_{seen[col]}"
#             else:
#                 seen[col] = 0
        
#         df.columns = new_cols
        
#         self.report["operations"].append({
#             "step": "standardize_columns",
#             "mapping": dict(zip(original_cols, new_cols))
#         })
        
#         print(f"  ✅ Standardized {len(original_cols)} column names")
        
#         return df
    
#     def _remove_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
#         """Remove duplicate rows"""
#         initial_rows = len(df)
#         df = df.drop_duplicates()
#         duplicates_removed = initial_rows - len(df)
        
#         if duplicates_removed > 0:
#             self.report["operations"].append({
#                 "step": "remove_duplicates",
#                 "duplicates_removed": duplicates_removed
#             })
#             print(f"  ✅ Removed {duplicates_removed} duplicate rows")
        
#         return df
    
#     def _normalize_types(self, df: pd.DataFrame) -> pd.DataFrame:
#         """Infer and normalize column data types"""
#         type_changes = {}
        
#         for col in df.columns:
#             original_type = str(df[col].dtype)
            
#             if pd.api.types.is_numeric_dtype(df[col]):
#                 continue
            
#             if df[col].dtype == 'object':
#                 sample = df[col].dropna().head(100)
#                 numeric_count = sum(self._is_numeric_string(str(x)) for x in sample)
                
#                 if len(sample) > 0 and numeric_count / len(sample) > 0.8:
#                     df[col] = pd.to_numeric(df[col], errors='coerce')
#                     type_changes[col] = f"{original_type} → {df[col].dtype}"
#                     continue
                
#                 try:
#                     parsed = pd.to_datetime(df[col], errors='coerce')
#                     if parsed.notna().sum() / len(df) > 0.5:
#                         df[col] = parsed
#                         type_changes[col] = f"{original_type} → datetime64"
#                 except:
#                     pass
        
#         if type_changes:
#             self.report["operations"].append({
#                 "step": "normalize_types",
#                 "type_changes": type_changes
#             })
#             print(f"  ✅ Normalized {len(type_changes)} column types")
        
#         return df
    
#     def _is_numeric_string(self, s: str) -> bool:
#         """Check if string represents a number"""
#         try:
#             s = s.strip().replace(',', '').replace('$', '').replace('%', '')
#             float(s)
#             return True
#         except:
#             return False
    
#     def _handle_missing(self, df: pd.DataFrame) -> pd.DataFrame:
#         """Handle missing values intelligently"""
#         missing_strategy = {}
        
#         for col in df.columns:
#             missing_count = df[col].isna().sum()
#             if missing_count == 0:
#                 continue
            
#             missing_pct = missing_count / len(df)
            
#             if missing_pct > 0.5:
#                 df = df.drop(columns=[col])
#                 missing_strategy[col] = "dropped (>50% missing)"
#                 continue
            
#             if pd.api.types.is_numeric_dtype(df[col]):
#                 df[col].fillna(df[col].median(), inplace=True)
#                 missing_strategy[col] = "filled with median"
            
#             elif pd.api.types.is_datetime64_any_dtype(df[col]):
#                 df[col].fillna(method='ffill', inplace=True)
#                 missing_strategy[col] = "forward filled"
            
#             else:
#                 mode_val = df[col].mode()
#                 if len(mode_val) > 0:
#                     df[col].fillna(mode_val[0], inplace=True)
#                     missing_strategy[col] = "filled with mode"
#                 else:
#                     df[col].fillna('Unknown', inplace=True)
#                     missing_strategy[col] = "filled with 'Unknown'"
        
#         if missing_strategy:
#             self.report["operations"].append({
#                 "step": "handle_missing",
#                 "strategy": missing_strategy
#             })
#             print(f"  ✅ Handled missing values in {len(missing_strategy)} columns")
        
#         return df
    
#     def _standardize_formats(self, df: pd.DataFrame) -> pd.DataFrame:
#         """Standardize string and numeric formats"""
#         format_changes = []
        
#         for col in df.columns:
#             if df[col].dtype == 'object':
#                 df[col] = df[col].astype(str).str.strip()
                
#                 if 'name' in col.lower():
#                     df[col] = df[col].str.title()
#                     format_changes.append(f"{col}: applied title case")
            
#             elif pd.api.types.is_float_dtype(df[col]):
#                 df[col] = df[col].round(2)
#                 format_changes.append(f"{col}: rounded to 2 decimals")
        
#         if format_changes:
#             self.report["operations"].append({
#                 "step": "standardize_formats",
#                 "changes": format_changes
#             })
#             print(f"  ✅ Standardized formats in {len(format_changes)} columns")
        
#         return df
    
#     def _handle_outliers(self, df: pd.DataFrame) -> pd.DataFrame:
#         """Remove statistical outliers using IQR method"""
#         outliers_removed = {}
        
#         for col in df.columns:
#             if not pd.api.types.is_numeric_dtype(df[col]):
#                 continue
            
#             Q1 = df[col].quantile(0.25)
#             Q3 = df[col].quantile(0.75)
#             IQR = Q3 - Q1
            
#             lower_bound = Q1 - 3 * IQR
#             upper_bound = Q3 + 3 * IQR
            
#             initial_count = len(df)
#             df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
#             removed = initial_count - len(df)
            
#             if removed > 0:
#                 outliers_removed[col] = removed
        
#         if outliers_removed:
#             self.report["operations"].append({
#                 "step": "remove_outliers",
#                 "outliers_removed": outliers_removed
#             })
#             print(f"  ✅ Removed outliers from {len(outliers_removed)} columns")
        
#         return df


# cleaning.py

import pandas as pd
import numpy as np
from typing import Tuple, Dict, Any, List
import re
import os
import json
from dotenv import load_dotenv
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sentence_transformers import SentenceTransformer
import logging

load_dotenv()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# ----------------------------------------------------------------------
# TOGGLE: Set to True for standard, clean data (3 columns). 
# Set to False for Machine Learning ready data (769+ columns with embeddings).
SIMPLE_MODE_ENABLED = True 
# ----------------------------------------------------------------------

# --- SentenceTransformer Configuration ---
SBERT_AVAILABLE = False
EMBEDDING_MODEL = None
EMBEDDING_DIM = 0
try:
    SBERT_AVAILABLE = True
    EMBEDDING_MODEL = SentenceTransformer('all-MiniLM-L6-v2', device='cpu') 
    EMBEDDING_DIM = 384
    logger.info("✅ SentenceTransformer (all-MiniLM-L6-v2) loaded.")
except ImportError:
    logger.warning("⚠️ Sentence-Transformers not installed. Text embedding will be skipped.")
except Exception as e:
    logger.error(f"⚠️ Failed to load SentenceTransformer: {e}. Text embedding disabled.")


# --- Gemini Configuration ---
AI_ENABLED = False
try:
    import google.generativeai as genai
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        genai.configure(api_key=api_key)
        # FIX: Use supported model for API calls
        GEMINI_MODEL = genai.GenerativeModel('gemini-2.5-flash') 
        AI_ENABLED = True
    else:
        logger.warning("⚠️ GEMINI_API_KEY not set. Using rule-based cleaning only.")
except ImportError:
    logger.warning("⚠️ google-generativeai not installed. AI features disabled.")


class DataCleaner:
    """
    AI-Powered data cleaning engine.
    Handles general cleaning, normalization, encoding, and text embedding.
    """
    
    def __init__(self):
        self.report = {}
        self.ai_enabled = AI_ENABLED
        self.embedding_model = EMBEDDING_MODEL
        self.embedding_dim = EMBEDDING_DIM
        self.le_mapping = {}
        self.ss_mapping = {}

    
    def _create_dataset_summary(self, df: pd.DataFrame) -> str:
        """Create a concise summary for AI analysis"""
        summary_parts = []
        summary_parts.append(f"Shape: {df.shape[0]} rows × {df.shape[1]} columns")
        summary_parts.append(f"\nColumns: {', '.join(df.columns.tolist()[:10])}")
        summary_parts.append(f"\nData Types:\n{df.dtypes.to_string()}")
        missing = df.isnull().sum()
        if missing.any():
            summary_parts.append(f"\nMissing Values:\n{missing[missing > 0].to_string()}")
        summary_parts.append(f"\nSample Data (first 3 rows):\n{df.head(3).to_string()}")
        return "\n".join(summary_parts)

    def _parse_ai_response(self, response_text: str) -> Dict[str, Any]:
        """Parse AI response and extract JSON recommendations"""
        try:
            response_text = re.sub(r'```json\s*', '', response_text)
            response_text = re.sub(r'```\s*', '', response_text)
            recommendations = json.loads(response_text)
            return recommendations
        except Exception as e:
            logger.error(f"⚠️ Failed to parse AI recommendations: {e}")
            return {}

    def _apply_ai_recommendations(self, df: pd.DataFrame, recommendations: Dict[str, Any]) -> pd.DataFrame:
        """Apply AI-generated cleaning recommendations and log changes"""
        operations = []
        
        # Drop recommended columns
        columns_to_drop = recommendations.get("columns_to_drop", [])
        if columns_to_drop:
            existing_cols = [col for col in columns_to_drop if col in df.columns]
            if existing_cols:
                df = df.drop(columns=existing_cols)
                operations.append(f"Dropped columns: {', '.join(existing_cols)}")
                logger.info(f"  ✅ Dropped columns: {', '.join(existing_cols)}")
        
        # Apply value replacements
        replacements = recommendations.get("value_replacements", {})
        for col, replace_map in replacements.items():
            if col in df.columns:
                df[col] = df[col].replace(replace_map)
                operations.append(f"Replaced values in {col}")
                logger.info(f"  🔄 Replaced values in '{col}'")
        
        # Apply recommended type conversions
        column_types = recommendations.get("column_types", {})
        for col, dtype in column_types.items():
            if col in df.columns:
                try:
                    if dtype == "numeric":
                        df[col] = pd.to_numeric(df[col], errors='coerce')
                    elif dtype == "datetime":
                        df[col] = pd.to_datetime(df[col], errors='coerce')
                    elif dtype == "string":
                        df[col] = df[col].astype(str)
                    operations.append(f"Converted {col} to {dtype}")
                    logger.info(f"  🔧 Converted '{col}' to {dtype}")
                except Exception as e:
                    logger.warning(f"  ⚠️ Failed to convert {col}: {e}")
        
        # Handle duplicate strategy
        dup_strategy = recommendations.get("duplicate_strategy", {})
        if dup_strategy.get("action") == "drop":
            cols = dup_strategy.get("columns", df.columns.tolist())
            initial = len(df)
            df = df.drop_duplicates(subset=cols)
            removed = initial - len(df)
            operations.append(f"Dropped {removed} duplicate rows based on {cols}")
            logger.info(f"  🗑  Dropped {removed} duplicate rows based on {cols}")
        
        if operations:
            self.report["operations"].append({
                "step": "ai_recommendations",
                "actions": operations
            })
        
        return df

    
    def _ai_analyze_and_clean(self, df: pd.DataFrame) -> pd.DataFrame:
        """Use Gemini AI to analyze dataset and suggest cleaning strategies"""
        if not self.ai_enabled:
             logger.info("🤖 AI analysis skipped: GEMINI_API_KEY not set.")
             return df
             
        try:
            if not globals().get('GEMINI_MODEL'):
                 logger.warning("🤖 AI model not loaded. Skipping analysis.")
                 return df

            summary = self._create_dataset_summary(df)
            
            prompt = f"""You are a data cleaning expert. Analyze this dataset summary and provide a detailed cleaning plan in JSON format. 
The dataset can contain numeric, categorical, string, datetime, or mixed types. It may have missing values, duplicates, typos, inconsistent formats, or outliers.

Dataset Summary:
{summary}

Instructions:
1. Identify columns with potential data type issues and suggest the correct type.
2. Detect columns that are mostly empty or irrelevant and suggest dropping them.
3. Suggest value replacements for typos, inconsistent formatting, or outliers.
4. Identify duplicates and suggest a strategy (drop or aggregate).
5. Recommend how to handle missing values for each column (median, mode, forward fill, or drop).
6. Highlight columns that may benefit from standardization (string case, date formats, numeric rounding).
7. Give any additional insights or data quality issues detected.

Output JSON format (no markdown, just JSON):
{{
    "column_types": {{"column_name": "recommended_type"}},
    "columns_to_drop": ["column1", "column2"],
    "encoding_fixes": {{"column_name": "fix_description"}},
    "value_replacements": {{"column_name": {{"old_value": "new_value"}}}},
    "duplicate_strategy": {{"columns": ["columns_to_check"], "action": "drop/aggregate"}},
    "missing_value_strategy": {{"column_name": "strategy_description"}},
    "standardization": {{"column_name": "standardization_description"}},
    "insights": ["insight1", "insight2"]
}}"""
            
            response = globals()['GEMINI_MODEL'].generate_content(prompt)
            recommendations = self._parse_ai_response(response.text)
            
            if recommendations:
                logger.info("💡 AI Recommendations:")
                df = self._apply_ai_recommendations(df, recommendations)
                self.report["ai_insights"].extend(recommendations.get("insights", []))
        
        except Exception as e:
            logger.error(f"⚠️ AI analysis failed: {e}")
            self.report["ai_insights"] = ["AI analysis unavailable"]
        
        return df


    
    def _ai_validate(self, df: pd.DataFrame) -> pd.DataFrame:
        """Final AI validation of cleaned data with console output"""
        if not self.ai_enabled:
             return df
             
        try:
            if not globals().get('GEMINI_MODEL'):
                 logger.warning("🤖 AI model not loaded. Skipping validation.")
                 return df
                 
            summary = self._create_dataset_summary(df)
            
            prompt = f"""Review this cleaned dataset and identify any remaining data quality issues.

{summary}

Provide issues in JSON format:
{{
    "quality_score": 0-100,
    "remaining_issues": ["issue1", "issue2"],
    "suggestions": ["suggestion1", "suggestion2"]
}}"""
            
            response = globals()['GEMINI_MODEL'].generate_content(prompt)
            validation = self._parse_ai_response(response.text)
            
            if validation:
                logger.info("\n  💡 Validation Results:")
                score = validation.get('quality_score', 'N/A')
                logger.info(f"  📈 Quality Score: {score}")
                
                if validation.get("remaining_issues"):
                    logger.info(f"  ⚠️  Remaining Issues:")
                    for issue in validation["remaining_issues"]:
                        logger.info(f"    - {issue}")
                
                if validation.get("suggestions"):
                    logger.info(f"  📝 Suggestions:")
                    for suggestion in validation["suggestions"]:
                        logger.info(f"    - {suggestion}")
                
                self.report["ai_insights"].append({
                    "quality_score": score,
                    "remaining_issues": validation.get("remaining_issues", []),
                    "suggestions": validation.get("suggestions", [])
                })
        
        except Exception as e:
            logger.error(f"  ⚠️ AI validation failed: {e}")
        
        return df
    
    def _remove_empty(self, df: pd.DataFrame) -> pd.DataFrame:
        """Remove completely empty rows and columns"""
        initial_shape = df.shape
        df = df.dropna(how='all')
        df = df.dropna(axis=1, how='all')
        
        removed_rows = initial_shape[0] - df.shape[0]
        removed_cols = initial_shape[1] - df.shape[1]
        
        if removed_rows > 0 or removed_cols > 0:
            self.report["operations"].append({
                "step": "remove_empty",
                "rows_removed": removed_rows,
                "columns_removed": removed_cols
            })
            if removed_rows > 0:
                logger.info(f"  ✅ Removed {removed_rows} empty rows")
            if removed_cols > 0:
                logger.info(f"  ✅ Removed {removed_cols} empty columns")
        
        return df
    
    def _standardize_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Standardize column names: lowercase, underscores, no special chars"""
        original_cols = df.columns.tolist()
        new_cols = []
        
        for col in df.columns:
            col_clean = str(col).lower().strip()
            col_clean = re.sub(r'[^\w\s]', '', col_clean)
            col_clean = re.sub(r'\s+', '_', col_clean)
            col_clean = re.sub(r'_+', '_', col_clean)
            col_clean = col_clean.strip('_')
            new_cols.append(col_clean)
        
        seen = {}
        for i, col in enumerate(new_cols):
            if col in seen:
                seen[col] += 1
                new_cols[i] = f"{col}_{seen[col]}"
            else:
                seen[col] = 0
        
        df.columns = new_cols
        
        self.report["operations"].append({
            "step": "standardize_columns",
            "mapping": dict(zip(original_cols, new_cols))
        })
        
        logger.info(f"  ✅ Standardized {len(original_cols)} column names")
        
        return df
    
    def _remove_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        """Remove duplicate rows"""
        initial_rows = len(df)
        df = df.drop_duplicates()
        duplicates_removed = initial_rows - len(df)
        
        if duplicates_removed > 0:
            self.report["operations"].append({
                "step": "remove_duplicates",
                "duplicates_removed": duplicates_removed
            })
            logger.info(f"  ✅ Removed {duplicates_removed} duplicate rows")
        
        return df
    
    def _normalize_types(self, df: pd.DataFrame) -> pd.DataFrame:
        """Infer and normalize column data types"""
        type_changes = {}
        
        for col in df.columns:
            original_type = str(df[col].dtype)
            
            if pd.api.types.is_numeric_dtype(df[col]):
                continue
            
            if df[col].dtype == 'object':
                sample = df[col].dropna().head(100)
                numeric_count = sum(self._is_numeric_string(str(x)) for x in sample)
                
                if len(sample) > 0 and numeric_count / len(sample) > 0.8:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                    type_changes[col] = f"{original_type} → {df[col].dtype}"
                    continue
                
                try:
                    parsed = pd.to_datetime(df[col], errors='coerce')
                    if parsed.notna().sum() / len(df) > 0.5:
                        df[col] = parsed
                        type_changes[col] = f"{original_type} → datetime64"
                except:
                    pass
        
        if type_changes:
            self.report["operations"].append({
                "step": "normalize_types",
                "type_changes": type_changes
            })
            logger.info(f"  ✅ Normalized {len(type_changes)} column types")
        
        return df
    
    def _is_numeric_string(self, s: str) -> bool:
        """Check if string represents a number"""
        try:
            s = s.strip().replace(',', '').replace('$', '').replace('%', '')
            float(s)
            return True
        except:
            return False
    
    def _handle_missing(self, df: pd.DataFrame) -> pd.DataFrame:
        """Handle missing values intelligently"""
        missing_strategy = {}
        
        for col in df.columns:
            missing_count = df[col].isna().sum()
            if missing_count == 0:
                continue
            
            missing_pct = missing_count / len(df)
            
            if missing_pct > 0.5:
                df = df.drop(columns=[col])
                missing_strategy[col] = "dropped (>50% missing)"
                continue
            
            if pd.api.types.is_numeric_dtype(df[col]):
                df[col].fillna(df[col].median(), inplace=True)
                missing_strategy[col] = "filled with median"
            
            elif pd.api.types.is_datetime64_any_dtype(df[col]):
                df[col].fillna(method='ffill', inplace=True)
                missing_strategy[col] = "forward filled"
            
            else:
                mode_val = df[col].mode()
                if len(mode_val) > 0:
                    df[col].fillna(mode_val[0], inplace=True)
                    missing_strategy[col] = "filled with mode"
                else:
                    df[col].fillna('Unknown', inplace=True)
                    missing_strategy[col] = "filled with 'Unknown'"
        
        if missing_strategy:
            self.report["operations"].append({
                "step": "handle_missing",
                "strategy": missing_strategy
            })
            logger.info(f"  ✅ Handled missing values in {len(missing_strategy)} columns")
        
        return df
    
    def _standardize_formats(self, df: pd.DataFrame) -> pd.DataFrame:
        """Standardize string and numeric formats"""
        format_changes = []
        
        for col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].astype(str).str.strip()
                
                if 'name' in col.lower():
                    df[col] = df[col].str.title()
                    format_changes.append(f"{col}: applied title case")
            
            elif pd.api.types.is_float_dtype(df[col]):
                df[col] = df[col].round(2)
                format_changes.append(f"{col}: rounded to 2 decimals")
        
        if format_changes:
            self.report["operations"].append({
                "step": "standardize_formats",
                "changes": format_changes
            })
            logger.info(f"  ✅ Standardized formats in {len(format_changes)} columns")
        
        return df
    
    def _handle_outliers(self, df: pd.DataFrame) -> pd.DataFrame:
        """Remove statistical outliers using IQR method"""
        outliers_removed = {}
        
        for col in df.columns:
            if not pd.api.types.is_numeric_dtype(df[col]):
                continue
            
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - 3 * IQR
            upper_bound = Q3 + 3 * IQR
            
            initial_count = len(df)
            df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
            removed = initial_count - len(df)
            
            if removed > 0:
                outliers_removed[col] = removed
        
        if outliers_removed:
            self.report["operations"].append({
                "step": "remove_outliers",
                "outliers_removed": outliers_removed
            })
            logger.info(f"  ✅ Removed outliers from {len(outliers_removed)} columns")
        
        return df

    def _scale_and_encode(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply StandardScaler and LabelEncoder."""
        scaled_cols = []
        encoded_cols = []
        self.le_mapping = {}
        self.ss_mapping = {}

        df_processed = df.copy()

        for col in df_processed.columns:
            # Drop the column if it's already an embedding column to prevent re-scaling
            if col.endswith('_embedding_0'): 
                continue

            if pd.api.types.is_numeric_dtype(df_processed[col]):
                # Apply StandardScaler
                # Only scale if not all values are the same (prevents division by zero in scaler)
                if df_processed[col].nunique() > 1:
                    scaler = StandardScaler()
                    # Reshape for fit_transform requires 2D array
                    data = df_processed[col].values.reshape(-1, 1)
                    df_processed[col] = scaler.fit_transform(data)
                    self.ss_mapping[col] = {'mean': scaler.mean_[0], 'scale': scaler.scale_[0]}
                    scaled_cols.append(col)
            
            elif df_processed[col].dtype == 'object' or pd.api.types.is_categorical_dtype(df_processed[col]):
                # Apply LabelEncoder to categorical/string columns
                le = LabelEncoder()
                # Ensure it's a string type for consistent encoding
                data = df_processed[col].astype(str)
                df_processed[col] = le.fit_transform(data)
                self.le_mapping[col] = {'classes': le.classes_.tolist()}
                encoded_cols.append(col)
        
        self.report["operations"].append({
            "step": "scaling_encoding",
            "scaled_columns": scaled_cols,
            "encoded_columns": encoded_cols
        })
        logger.info(f"  ✅ Scaled {len(scaled_cols)} columns, Encoded {len(encoded_cols)} columns.")
        return df_processed
    
    def _embed_text_columns(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Generate SentenceTransformer embeddings for textual columns."""
        # FIX: Ensure an empty DataFrame is returned if model is missing to avoid concat error later
        if not self.embedding_model:
            return pd.DataFrame(index=df.index), {"embedding_summary": "Embedding skipped (model not loaded)."}

        # Identify actual object type columns that are suitable for embedding
        text_cols = [col for col in df.columns if df[col].dtype == 'object']
        
        # FIX: Ensure an empty DataFrame is returned if no text columns are found
        if not text_cols:
            return pd.DataFrame(index=df.index), {"embedding_summary": "No suitable text columns found for embedding."}
        
        embedding_summary = {}
        df_for_concat = pd.DataFrame(index=df.index)

        for col in text_cols:
            
            # Use faster batch encoding
            sentences = df[col].astype(str).tolist()
            # Handle NaN/None by converting them to an empty string for the embedder
            sentences = [s if s.strip() != 'nan' else '' for s in sentences]
            
            # Encode in batches for performance
            embeddings = self.embedding_model.encode(
                sentences, 
                show_progress_bar=False, 
                convert_to_numpy=True,
                batch_size=32  # Optimized batch size for efficiency
            )
            
            # Create new columns for the embedding vector
            embedding_col_names = [f"{col}_embedding_{i}" for i in range(self.embedding_dim)]
            
            # Create DataFrame from embeddings array
            embedding_df = pd.DataFrame(embeddings, columns=embedding_col_names, index=df.index)
            
            # Concatenate the new embedding columns to the intermediate DF
            df_for_concat = pd.concat([df_for_concat, embedding_df], axis=1)
            
            embedding_summary[col] = {
                "vector_size": self.embedding_dim,
                "new_columns": embedding_col_names
            }
        
        self.report["operations"].append({
            "step": "text_embedding",
            "embedded_columns": list(embedding_summary.keys())
        })
        logger.info(f"  ✅ Embedded {len(text_cols)} text columns into {len(text_cols) * self.embedding_dim} new columns.")

        return df_for_concat, {"embedding_summary": embedding_summary}


    def clean(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Main cleaning pipeline including normalization, encoding, and embedding.
        Returns: (cleaned_df, final_report)
        """
        logger.info("="*80)
        logger.info("🚀 STARTING DATA CLEANING PIPELINE")
        logger.info("="*80)
        
        self.report = {
            "original_shape": df.shape,
            "operations": [],
            "ai_insights": []
        }
        
        df_cleaned = df.copy()
        
        logger.info(f"\n📊 Original Dataset: {df.shape[0]} rows × {df.shape[1]} columns")
        
        # --- Pre-processing Steps (In the existing flow) ---
        if self.ai_enabled:
            logger.info("\n🤖 Running AI Analysis...")
            df_cleaned = self._ai_analyze_and_clean(df_cleaned)
        
        logger.info("\n🧹 Removing empty rows/columns...")
        df_cleaned = self._remove_empty(df_cleaned)
        
        logger.info("📝 Standardizing column names...")
        df_cleaned = self._standardize_columns(df_cleaned)
        
        logger.info("🔍 Checking for duplicates...")
        df_cleaned = self._remove_duplicates(df_cleaned)
        
        logger.info("🔧 Normalizing data types...")
        df_cleaned = self._normalize_types(df_cleaned)
        
        logger.info("📌 Handling missing values...")
        df_cleaned = self._handle_missing(df_cleaned)
        
        logger.info("✨ Standardizing formats...")
        df_cleaned = self._standardize_formats(df_cleaned)
        
        logger.info("📊 Detecting outliers...")
        df_cleaned = self._handle_outliers(df_cleaned)
        
        # -----------------------------------------------------------
        # MODE SELECTION: SIMPLE vs. MACHINE LEARNING (ML) READY
        # -----------------------------------------------------------
        if not SIMPLE_MODE_ENABLED:
            # ML READY MODE: Apply scaling and embedding
            text_cols_for_embedding = [col for col in df_cleaned.columns if df_cleaned[col].dtype == 'object']
            df_for_scaling = df_cleaned.drop(columns=text_cols_for_embedding, errors='ignore')

            df_embeddings, embedding_report = self._embed_text_columns(df_cleaned[text_cols_for_embedding])
            
            logger.info("🧠 Scaling and Encoding numerical/categorical columns...")
            df_scaled_encoded = self._scale_and_encode(df_for_scaling)
            
            df_final = pd.concat([df_scaled_encoded.reset_index(drop=True), df_embeddings.reset_index(drop=True)], axis=1)
        else:
            # SIMPLE MODE: Return the cleaned DataFrame as is (only uses Label Encoding for categorical data)
            logger.info("🧠 Running Simple Encoding (LabelEncoder) for categorical data...")
            df_final = self._scale_and_encode(df_cleaned)
            embedding_report = {"embedding_summary": "Embedding skipped (SIMPLE_MODE enabled)."}
        
        # --- Post-processing Steps (In the existing flow) ---
        if self.ai_enabled:
            logger.info("\n🎯 Running AI Validation...")
            df_final = self._ai_validate(df_final)
        
        self.report["final_shape"] = df_final.shape
        self.report["rows_removed"] = df.shape[0] - df_final.shape[0]
        self.report["columns_removed"] = df.shape[1] - df_final.shape[1]
        
        final_report = {
            "cleaning_operations": self.report,
            "preprocessing_details": {
                "scaling_maps": self.ss_mapping,
                "encoding_maps": self.le_mapping,
                **embedding_report
            }
        }
        
        logger.info("="*80)
        logger.info("✅ CLEANING COMPLETE")
        logger.info(f"📊 Final Dataset: {df_final.shape[0]} rows × {df_final.shape[1]} columns")
        logger.info("="*80 + "\n")
        
        return df_final, final_report