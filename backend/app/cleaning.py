# # # # import pandas as pd
# # # # import numpy as np
# # # # from typing import Tuple, Dict, Any
# # # # from datetime import datetime
# # # # import re
# # # # import os
# # # # import json
# # # # from dotenv import load_dotenv
# # # # load_dotenv()

# # # # try:
# # # #     import google.generativeai as genai
# # # #     GENAI_AVAILABLE = True
# # # # except ImportError:
# # # #     GENAI_AVAILABLE = False
# # # #     print("⚠️ google-generativeai not installed. Install with: pip install google-generativeai")

# # # # class DataCleaner:
# # # #     """
# # # #     AI-Powered data cleaning engine using Gemini
# # # #     Handles missing values, duplicates, type normalization, and formatting
# # # #     """
    
# # # #     def __init__(self):
# # # #         self.report = {}
# # # #         # Initialize Gemini
# # # #         api_key = os.getenv("GEMINI_API_KEY")
# # # #         if api_key:
# # # #             genai.configure(api_key=api_key)
# # # #             self.model = genai.GenerativeModel('gemini-pro')
# # # #             self.ai_enabled = True
# # # #         else:
# # # #             self.ai_enabled = False
# # # #             print("⚠️ GEMINI_API_KEY not set. Using rule-based cleaning only.")
    
# # # #     def clean(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
# # # #         """
# # # #         Main cleaning pipeline with AI-powered analysis
# # # #         Returns: (cleaned_df, cleaning_report)
# # # #         """
# # # #         print("\n" + "="*80)
# # # #         print("🚀 STARTING DATA CLEANING PIPELINE")
# # # #         print("="*80)
        
# # # #         self.report = {
# # # #             "original_shape": df.shape,
# # # #             "operations": [],
# # # #             "ai_insights": []
# # # #         }
        
# # # #         df_cleaned = df.copy()
        
# # # #         print(f"\n📊 Original Dataset: {df.shape[0]} rows × {df.shape[1]} columns")
        
# # # #         # Step 0: AI-Powered Data Analysis (if enabled)
# # # #         if self.ai_enabled:
# # # #             print("\n🤖 Running AI Analysis...")
# # # #             df_cleaned = self._ai_analyze_and_clean(df_cleaned)
        
# # # #         # Step 1: Remove completely empty rows/columns
# # # #         print("\n🧹 Removing empty rows/columns...")
# # # #         df_cleaned = self._remove_empty(df_cleaned)
        
# # # #         # Step 2: Standardize column names
# # # #         print("📝 Standardizing column names...")
# # # #         df_cleaned = self._standardize_columns(df_cleaned)
        
# # # #         # Step 3: Handle duplicates
# # # #         print("🔍 Checking for duplicates...")
# # # #         df_cleaned = self._remove_duplicates(df_cleaned)
        
# # # #         # Step 4: Infer and normalize data types
# # # #         print("🔧 Normalizing data types...")
# # # #         df_cleaned = self._normalize_types(df_cleaned)
        
# # # #         # Step 5: Handle missing values
# # # #         print("📌 Handling missing values...")
# # # #         df_cleaned = self._handle_missing(df_cleaned)
        
# # # #         # Step 6: Standardize formats (dates, strings, numbers)
# # # #         print("✨ Standardizing formats...")
# # # #         df_cleaned = self._standardize_formats(df_cleaned)
        
# # # #         # Step 7: Remove outliers (conservative approach)
# # # #         print("📊 Detecting outliers...")
# # # #         df_cleaned = self._handle_outliers(df_cleaned)
        
# # # #         # Step 8: AI-Powered Final Validation
# # # #         if self.ai_enabled:
# # # #             print("\n🎯 Running AI Validation...")
# # # #             df_cleaned = self._ai_validate(df_cleaned)
        
# # # #         self.report["final_shape"] = df_cleaned.shape
# # # #         self.report["rows_removed"] = df.shape[0] - df_cleaned.shape[0]
# # # #         self.report["columns_removed"] = df.shape[1] - df_cleaned.shape[1]
        
# # # #         print("\n" + "="*80)
# # # #         print("✅ CLEANING COMPLETE")
# # # #         print(f"📊 Final Dataset: {df_cleaned.shape[0]} rows × {df_cleaned.shape[1]} columns")
# # # #         print(f"🗑  Rows removed: {self.report['rows_removed']}")
# # # #         print(f"🗑  Columns removed: {self.report['columns_removed']}")
# # # #         print("="*80 + "\n")
        
# # # #         return df_cleaned, self.report
    
# # # #     def _ai_analyze_and_clean(self, df: pd.DataFrame) -> pd.DataFrame:
# # # #         """Use Gemini AI to analyze dataset and suggest cleaning strategies"""
# # # #         try:
# # # #             summary = self._create_dataset_summary(df)
            
# # # #             prompt = f"""You are a data cleaning expert. Analyze this dataset summary and provide a detailed cleaning plan in JSON format. 
# # # # The dataset can contain numeric, categorical, string, datetime, or mixed types. It may have missing values, duplicates, typos, inconsistent formats, or outliers.

# # # # Dataset Summary:
# # # # {summary}

# # # # Instructions:
# # # # 1. Identify columns with potential data type issues and suggest the correct type.
# # # # 2. Detect columns that are mostly empty or irrelevant and suggest dropping them.
# # # # 3. Suggest value replacements for typos, inconsistent formatting, or outliers.
# # # # 4. Identify duplicates and suggest a strategy (drop or aggregate).
# # # # 5. Recommend how to handle missing values for each column (median, mode, forward fill, or drop).
# # # # 6. Highlight columns that may benefit from standardization (string case, date formats, numeric rounding).
# # # # 7. Give any additional insights or data quality issues detected.

# # # # Output JSON format (no markdown, just JSON):
# # # # {{
# # # #     "column_types": {{"column_name": "recommended_type"}},
# # # #     "columns_to_drop": ["column1", "column2"],
# # # #     "encoding_fixes": {{"column_name": "fix_description"}},
# # # #     "value_replacements": {{"column_name": {{"old_value": "new_value"}}}},
# # # #     "duplicate_strategy": {{"columns": ["columns_to_check"], "action": "drop/aggregate"}},
# # # #     "missing_value_strategy": {{"column_name": "strategy_description"}},
# # # #     "standardization": {{"column_name": "standardization_description"}},
# # # #     "insights": ["insight1", "insight2"]
# # # # }}"""
            
# # # #             response = self.model.generate_content(prompt)
# # # #             recommendations = self._parse_ai_response(response.text)
            
# # # #             if recommendations:
# # # #                 print("💡 AI Recommendations:")
# # # #                 df = self._apply_ai_recommendations(df, recommendations)
# # # #                 self.report["ai_insights"].extend(recommendations.get("insights", []))
        
# # # #         except Exception as e:
# # # #             print(f"⚠️ AI analysis failed: {e}")
# # # #             self.report["ai_insights"] = ["AI analysis unavailable"]
        
# # # #         return df
    
# # # #     def _create_dataset_summary(self, df: pd.DataFrame) -> str:
# # # #         """Create a concise summary for AI analysis"""
# # # #         summary_parts = []
        
# # # #         summary_parts.append(f"Shape: {df.shape[0]} rows × {df.shape[1]} columns")
# # # #         summary_parts.append(f"\nColumns: {', '.join(df.columns.tolist()[:10])}")
        
# # # #         summary_parts.append(f"\nData Types:\n{df.dtypes.to_string()}")
        
# # # #         missing = df.isnull().sum()
# # # #         if missing.any():
# # # #             summary_parts.append(f"\nMissing Values:\n{missing[missing > 0].to_string()}")
        
# # # #         summary_parts.append(f"\nSample Data (first 3 rows):\n{df.head(3).to_string()}")
        
# # # #         return "\n".join(summary_parts)
    
# # # #     def _parse_ai_response(self, response_text: str) -> Dict[str, Any]:
# # # #         """Parse AI response and extract JSON recommendations"""
# # # #         try:
# # # #             response_text = re.sub(r'```json\s*', '', response_text)
# # # #             response_text = re.sub(r'```\s*', '', response_text)
            
# # # #             recommendations = json.loads(response_text)
# # # #             return recommendations
# # # #         except Exception as e:
# # # #             print(f"⚠️ Failed to parse AI recommendations: {e}")
# # # #             return {}
    
# # # #     def _apply_ai_recommendations(self, df: pd.DataFrame, recommendations: Dict[str, Any]) -> pd.DataFrame:
# # # #         """Apply AI-generated cleaning recommendations and log changes"""
# # # #         operations = []
        
# # # #         # Drop recommended columns
# # # #         columns_to_drop = recommendations.get("columns_to_drop", [])
# # # #         if columns_to_drop:
# # # #             existing_cols = [col for col in columns_to_drop if col in df.columns]
# # # #             if existing_cols:
# # # #                 df = df.drop(columns=existing_cols)
# # # #                 operations.append(f"Dropped columns: {', '.join(existing_cols)}")
# # # #                 print(f"  ✅ Dropped columns: {', '.join(existing_cols)}")
        
# # # #         # Apply value replacements
# # # #         replacements = recommendations.get("value_replacements", {})
# # # #         for col, replace_map in replacements.items():
# # # #             if col in df.columns:
# # # #                 df[col] = df[col].replace(replace_map)
# # # #                 operations.append(f"Replaced values in {col}: {replace_map}")
# # # #                 print(f"  🔄 Replaced values in '{col}': {replace_map}")
        
# # # #         # Apply recommended type conversions
# # # #         column_types = recommendations.get("column_types", {})
# # # #         for col, dtype in column_types.items():
# # # #             if col in df.columns:
# # # #                 try:
# # # #                     if dtype == "numeric":
# # # #                         df[col] = pd.to_numeric(df[col], errors='coerce')
# # # #                     elif dtype == "datetime":
# # # #                         df[col] = pd.to_datetime(df[col], errors='coerce')
# # # #                     elif dtype == "string":
# # # #                         df[col] = df[col].astype(str)
# # # #                     operations.append(f"Converted {col} to {dtype}")
# # # #                     print(f"  🔧 Converted '{col}' to {dtype}")
# # # #                 except Exception as e:
# # # #                     print(f"  ⚠️ Failed to convert {col}: {e}")
        
# # # #         # Handle duplicate strategy
# # # #         dup_strategy = recommendations.get("duplicate_strategy", {})
# # # #         if dup_strategy.get("action") == "drop":
# # # #             cols = dup_strategy.get("columns", df.columns.tolist())
# # # #             initial = len(df)
# # # #             df = df.drop_duplicates(subset=cols)
# # # #             removed = initial - len(df)
# # # #             operations.append(f"Dropped {removed} duplicate rows based on {cols}")
# # # #             print(f"  🗑  Dropped {removed} duplicate rows based on {cols}")
        
# # # #         # Apply standardization
# # # #         standardization = recommendations.get("standardization", {})
# # # #         for col, std_desc in standardization.items():
# # # #             if col in df.columns:
# # # #                 print(f"  ✨ Standardizing '{col}': {std_desc}")
# # # #                 operations.append(f"Standardized {col}: {std_desc}")
        
# # # #         if operations:
# # # #             self.report["operations"].append({
# # # #                 "step": "ai_recommendations",
# # # #                 "actions": operations
# # # #             })
        
# # # #         return df
    
# # # #     def _ai_validate(self, df: pd.DataFrame) -> pd.DataFrame:
# # # #         """Final AI validation of cleaned data with console output"""
# # # #         try:
# # # #             summary = self._create_dataset_summary(df)
            
# # # #             prompt = f"""Review this cleaned dataset and identify any remaining data quality issues.

# # # # {summary}

# # # # Provide issues in JSON format:
# # # # {{
# # # #     "quality_score": 0-100,
# # # #     "remaining_issues": ["issue1", "issue2"],
# # # #     "suggestions": ["suggestion1", "suggestion2"]
# # # # }}"""
            
# # # #             response = self.model.generate_content(prompt)
# # # #             validation = self._parse_ai_response(response.text)
            
# # # #             if validation:
# # # #                 print("\n  💡 Validation Results:")
# # # #                 score = validation.get('quality_score', 'N/A')
# # # #                 print(f"  📈 Quality Score: {score}")
                
# # # #                 if validation.get("remaining_issues"):
# # # #                     print(f"  ⚠️  Remaining Issues:")
# # # #                     for issue in validation["remaining_issues"]:
# # # #                         print(f"    - {issue}")
                
# # # #                 if validation.get("suggestions"):
# # # #                     print(f"  📝 Suggestions:")
# # # #                     for suggestion in validation["suggestions"]:
# # # #                         print(f"    - {suggestion}")
                
# # # #                 self.report["ai_insights"].append({
# # # #                     "quality_score": score,
# # # #                     "remaining_issues": validation.get("remaining_issues", []),
# # # #                     "suggestions": validation.get("suggestions", [])
# # # #                 })
        
# # # #         except Exception as e:
# # # #             print(f"  ⚠️ AI validation failed: {e}")
        
# # # #         return df
    
# # # #     def _remove_empty(self, df: pd.DataFrame) -> pd.DataFrame:
# # # #         """Remove completely empty rows and columns"""
# # # #         initial_shape = df.shape
# # # #         df = df.dropna(how='all')
# # # #         df = df.dropna(axis=1, how='all')
        
# # # #         removed_rows = initial_shape[0] - df.shape[0]
# # # #         removed_cols = initial_shape[1] - df.shape[1]
        
# # # #         if removed_rows > 0 or removed_cols > 0:
# # # #             self.report["operations"].append({
# # # #                 "step": "remove_empty",
# # # #                 "rows_removed": removed_rows,
# # # #                 "columns_removed": removed_cols
# # # #             })
# # # #             if removed_rows > 0:
# # # #                 print(f"  ✅ Removed {removed_rows} empty rows")
# # # #             if removed_cols > 0:
# # # #                 print(f"  ✅ Removed {removed_cols} empty columns")
        
# # # #         return df
    
# # # #     def _standardize_columns(self, df: pd.DataFrame) -> pd.DataFrame:
# # # #         """Standardize column names: lowercase, underscores, no special chars"""
# # # #         original_cols = df.columns.tolist()
# # # #         new_cols = []
        
# # # #         for col in df.columns:
# # # #             col_clean = str(col).lower().strip()
# # # #             col_clean = re.sub(r'[^\w\s]', '', col_clean)
# # # #             col_clean = re.sub(r'\s+', '_', col_clean)
# # # #             col_clean = re.sub(r'_+', '_', col_clean)
# # # #             col_clean = col_clean.strip('_')
# # # #             new_cols.append(col_clean)
        
# # # #         seen = {}
# # # #         for i, col in enumerate(new_cols):
# # # #             if col in seen:
# # # #                 seen[col] += 1
# # # #                 new_cols[i] = f"{col}_{seen[col]}"
# # # #             else:
# # # #                 seen[col] = 0
        
# # # #         df.columns = new_cols
        
# # # #         self.report["operations"].append({
# # # #             "step": "standardize_columns",
# # # #             "mapping": dict(zip(original_cols, new_cols))
# # # #         })
        
# # # #         print(f"  ✅ Standardized {len(original_cols)} column names")
        
# # # #         return df
    
# # # #     def _remove_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
# # # #         """Remove duplicate rows"""
# # # #         initial_rows = len(df)
# # # #         df = df.drop_duplicates()
# # # #         duplicates_removed = initial_rows - len(df)
        
# # # #         if duplicates_removed > 0:
# # # #             self.report["operations"].append({
# # # #                 "step": "remove_duplicates",
# # # #                 "duplicates_removed": duplicates_removed
# # # #             })
# # # #             print(f"  ✅ Removed {duplicates_removed} duplicate rows")
        
# # # #         return df
    
# # # #     def _normalize_types(self, df: pd.DataFrame) -> pd.DataFrame:
# # # #         """Infer and normalize column data types"""
# # # #         type_changes = {}
        
# # # #         for col in df.columns:
# # # #             original_type = str(df[col].dtype)
            
# # # #             if pd.api.types.is_numeric_dtype(df[col]):
# # # #                 continue
            
# # # #             if df[col].dtype == 'object':
# # # #                 sample = df[col].dropna().head(100)
# # # #                 numeric_count = sum(self._is_numeric_string(str(x)) for x in sample)
                
# # # #                 if len(sample) > 0 and numeric_count / len(sample) > 0.8:
# # # #                     df[col] = pd.to_numeric(df[col], errors='coerce')
# # # #                     type_changes[col] = f"{original_type} → {df[col].dtype}"
# # # #                     continue
                
# # # #                 try:
# # # #                     parsed = pd.to_datetime(df[col], errors='coerce')
# # # #                     if parsed.notna().sum() / len(df) > 0.5:
# # # #                         df[col] = parsed
# # # #                         type_changes[col] = f"{original_type} → datetime64"
# # # #                 except:
# # # #                     pass
        
# # # #         if type_changes:
# # # #             self.report["operations"].append({
# # # #                 "step": "normalize_types",
# # # #                 "type_changes": type_changes
# # # #             })
# # # #             print(f"  ✅ Normalized {len(type_changes)} column types")
        
# # # #         return df
    
# # # #     def _is_numeric_string(self, s: str) -> bool:
# # # #         """Check if string represents a number"""
# # # #         try:
# # # #             s = s.strip().replace(',', '').replace('$', '').replace('%', '')
# # # #             float(s)
# # # #             return True
# # # #         except:
# # # #             return False
    
# # # #     def _handle_missing(self, df: pd.DataFrame) -> pd.DataFrame:
# # # #         """Handle missing values intelligently"""
# # # #         missing_strategy = {}
        
# # # #         for col in df.columns:
# # # #             missing_count = df[col].isna().sum()
# # # #             if missing_count == 0:
# # # #                 continue
            
# # # #             missing_pct = missing_count / len(df)
            
# # # #             if missing_pct > 0.5:
# # # #                 df = df.drop(columns=[col])
# # # #                 missing_strategy[col] = "dropped (>50% missing)"
# # # #                 continue
            
# # # #             if pd.api.types.is_numeric_dtype(df[col]):
# # # #                 df[col].fillna(df[col].median(), inplace=True)
# # # #                 missing_strategy[col] = "filled with median"
            
# # # #             elif pd.api.types.is_datetime64_any_dtype(df[col]):
# # # #                 df[col].fillna(method='ffill', inplace=True)
# # # #                 missing_strategy[col] = "forward filled"
            
# # # #             else:
# # # #                 mode_val = df[col].mode()
# # # #                 if len(mode_val) > 0:
# # # #                     df[col].fillna(mode_val[0], inplace=True)
# # # #                     missing_strategy[col] = "filled with mode"
# # # #                 else:
# # # #                     df[col].fillna('Unknown', inplace=True)
# # # #                     missing_strategy[col] = "filled with 'Unknown'"
        
# # # #         if missing_strategy:
# # # #             self.report["operations"].append({
# # # #                 "step": "handle_missing",
# # # #                 "strategy": missing_strategy
# # # #             })
# # # #             print(f"  ✅ Handled missing values in {len(missing_strategy)} columns")
        
# # # #         return df
    
# # # #     def _standardize_formats(self, df: pd.DataFrame) -> pd.DataFrame:
# # # #         """Standardize string and numeric formats"""
# # # #         format_changes = []
        
# # # #         for col in df.columns:
# # # #             if df[col].dtype == 'object':
# # # #                 df[col] = df[col].astype(str).str.strip()
                
# # # #                 if 'name' in col.lower():
# # # #                     df[col] = df[col].str.title()
# # # #                     format_changes.append(f"{col}: applied title case")
            
# # # #             elif pd.api.types.is_float_dtype(df[col]):
# # # #                 df[col] = df[col].round(2)
# # # #                 format_changes.append(f"{col}: rounded to 2 decimals")
        
# # # #         if format_changes:
# # # #             self.report["operations"].append({
# # # #                 "step": "standardize_formats",
# # # #                 "changes": format_changes
# # # #             })
# # # #             print(f"  ✅ Standardized formats in {len(format_changes)} columns")
        
# # # #         return df
    
# # # #     def _handle_outliers(self, df: pd.DataFrame) -> pd.DataFrame:
# # # #         """Remove statistical outliers using IQR method"""
# # # #         outliers_removed = {}
        
# # # #         for col in df.columns:
# # # #             if not pd.api.types.is_numeric_dtype(df[col]):
# # # #                 continue
            
# # # #             Q1 = df[col].quantile(0.25)
# # # #             Q3 = df[col].quantile(0.75)
# # # #             IQR = Q3 - Q1
            
# # # #             lower_bound = Q1 - 3 * IQR
# # # #             upper_bound = Q3 + 3 * IQR
            
# # # #             initial_count = len(df)
# # # #             df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
# # # #             removed = initial_count - len(df)
            
# # # #             if removed > 0:
# # # #                 outliers_removed[col] = removed
        
# # # #         if outliers_removed:
# # # #             self.report["operations"].append({
# # # #                 "step": "remove_outliers",
# # # #                 "outliers_removed": outliers_removed
# # # #             })
# # # #             print(f"  ✅ Removed outliers from {len(outliers_removed)} columns")
        
# # # #         return df




# # # # cleaning.py

# # # import pandas as pd
# # # import numpy as np
# # # from typing import Tuple, Dict, Any, List
# # # import re
# # # import os
# # # import json
# # # from dotenv import load_dotenv
# # # from sklearn.preprocessing import StandardScaler, LabelEncoder
# # # from sentence_transformers import SentenceTransformer
# # # import logging

# # # load_dotenv()
# # # logger = logging.getLogger(__name__)
# # # logging.basicConfig(level=logging.INFO)

# # # # ----------------------------------------------------------------------
# # # # TOGGLE: Set to False for standard, clean data (Human-Readable). 
# # # # Set to True for Machine Learning ready data (769+ columns with embeddings).
# # # ML_MODE_ENABLED = False
# # # # ----------------------------------------------------------------------

# # # # --- SentenceTransformer Configuration ---
# # # SBERT_AVAILABLE = False
# # # EMBEDDING_MODEL = None
# # # EMBEDDING_DIM = 0
# # # try:
# # #     SBERT_AVAILABLE = True
# # #     EMBEDDING_MODEL = SentenceTransformer('all-MiniLM-L6-v2', device='cpu') 
# # #     EMBEDDING_DIM = 384
# # #     logger.info("✅ SentenceTransformer (all-MiniLM-L6-v2) loaded.")
# # # except ImportError:
# # #     logger.warning("⚠️ Sentence-Transformers not installed. Text embedding will be skipped.")
# # # except Exception as e:
# # #     logger.error(f"⚠️ Failed to load SentenceTransformer: {e}. Text embedding disabled.")


# # # # --- Gemini Configuration ---
# # # AI_ENABLED = False
# # # try:
# # #     import google.generativeai as genai
# # #     api_key = os.getenv("GEMINI_API_KEY")
# # #     if api_key:
# # #         genai.configure(api_key=api_key)
# # #         # FIX: Use supported model for API calls
# # #         GEMINI_MODEL = genai.GenerativeModel('gemini-2.5-flash') 
# # #         AI_ENABLED = True
# # #     else:
# # #         logger.warning("⚠️ GEMINI_API_KEY not set. Using rule-based cleaning only.")
# # # except ImportError:
# # #     logger.warning("⚠️ google-generativeai not installed. AI features disabled.")


# # # class DataCleaner:
# # #     """
# # #     AI-Powered data cleaning engine.
# # #     Handles general cleaning, normalization, encoding, and text embedding.
# # #     """
    
# # #     def __init__(self):
# # #         self.report = {}
# # #         self.ai_enabled = AI_ENABLED
# # #         self.embedding_model = EMBEDDING_MODEL
# # #         self.embedding_dim = EMBEDDING_DIM
# # #         self.le_mapping = {}
# # #         self.ss_mapping = {}
# # #         self.ml_mode = ML_MODE_ENABLED

    
# # #     def _create_dataset_summary(self, df: pd.DataFrame) -> str:
# # #         """Create a concise summary for AI analysis"""
# # #         summary_parts = []
# # #         summary_parts.append(f"Shape: {df.shape[0]} rows × {df.shape[1]} columns")
# # #         summary_parts.append(f"\nColumns: {', '.join(df.columns.tolist()[:10])}")
# # #         summary_parts.append(f"\nData Types:\n{df.dtypes.to_string()}")
# # #         missing = df.isnull().sum()
# # #         if missing.any():
# # #             summary_parts.append(f"\nMissing Values:\n{missing[missing > 0].to_string()}")
# # #         summary_parts.append(f"\nSample Data (first 3 rows):\n{df.head(3).to_string()}")
# # #         return "\n".join(summary_parts)

# # #     def _parse_ai_response(self, response_text: str) -> Dict[str, Any]:
# # #         """Parse AI response and extract JSON recommendations"""
# # #         try:
# # #             response_text = re.sub(r'```json\s*', '', response_text)
# # #             response_text = re.sub(r'```\s*', '', response_text)
# # #             recommendations = json.loads(response_text)
# # #             return recommendations
# # #         except Exception as e:
# # #             logger.error(f"⚠️ Failed to parse AI recommendations: {e}")
# # #             return {}

# # #     def _apply_ai_recommendations(self, df: pd.DataFrame, recommendations: Dict[str, Any]) -> pd.DataFrame:
# # #         """Apply AI-generated cleaning recommendations and log changes"""
# # #         operations = []
        
# # #         # Drop recommended columns
# # #         columns_to_drop = recommendations.get("columns_to_drop", [])
# # #         if columns_to_drop:
# # #             existing_cols = [col for col in columns_to_drop if col in df.columns]
# # #             if existing_cols:
# # #                 df = df.drop(columns=existing_cols)
# # #                 operations.append(f"Dropped columns: {', '.join(existing_cols)}")
# # #                 logger.info(f"  ✅ Dropped columns: {', '.join(existing_cols)}")
        
# # #         # Apply value replacements
# # #         replacements = recommendations.get("value_replacements", {})
# # #         for col, replace_map in replacements.items():
# # #             if col in df.columns:
# # #                 df[col] = df[col].replace(replace_map)
# # #                 operations.append(f"Replaced values in {col}")
# # #                 logger.info(f"  🔄 Replaced values in '{col}'")
        
# # #         # Apply recommended type conversions
# # #         column_types = recommendations.get("column_types", {})
# # #         for col, dtype in column_types.items():
# # #             if col in df.columns:
# # #                 try:
# # #                     if dtype == "numeric":
# # #                         df[col] = pd.to_numeric(df[col], errors='coerce')
# # #                     elif dtype == "datetime":
# # #                         df[col] = pd.to_datetime(df[col], errors='coerce')
# # #                     elif dtype == "string":
# # #                         df[col] = df[col].astype(str)
# # #                     operations.append(f"Converted {col} to {dtype}")
# # #                     logger.info(f"  🔧 Converted '{col}' to {dtype}")
# # #                 except Exception as e:
# # #                     logger.warning(f"  ⚠️ Failed to convert {col}: {e}")
        
# # #         # Handle duplicate strategy
# # #         dup_strategy = recommendations.get("duplicate_strategy", {})
# # #         if dup_strategy.get("action") == "drop":
# # #             cols = dup_strategy.get("columns", df.columns.tolist())
# # #             initial = len(df)
# # #             df = df.drop_duplicates(subset=cols)
# # #             removed = initial - len(df)
# # #             operations.append(f"Dropped {removed} duplicate rows based on {cols}")
# # #             logger.info(f"  🗑  Dropped {removed} duplicate rows based on {cols}")
        
# # #         if operations:
# # #             self.report["operations"].append({
# # #                 "step": "ai_recommendations",
# # #                 "actions": operations
# # #             })
        
# # #         return df

    
# # #     def _ai_analyze_and_clean(self, df: pd.DataFrame) -> pd.DataFrame:
# # #         """Use Gemini AI to analyze dataset and suggest cleaning strategies"""
# # #         if not self.ai_enabled:
# # #              logger.info("🤖 AI analysis skipped: GEMINI_API_KEY not set.")
# # #              return df
             
# # #         try:
# # #             if not globals().get('GEMINI_MODEL'):
# # #                  logger.warning("🤖 AI model not loaded. Skipping analysis.")
# # #                  return df

# # #             summary = self._create_dataset_summary(df)
            
# # #             prompt = f"""You are a data cleaning expert. Analyze this dataset summary and provide a detailed cleaning plan in JSON format. 
# # # The dataset can contain numeric, categorical, string, datetime, or mixed types. It may have missing values, duplicates, typos, inconsistent formats, or outliers.

# # # Dataset Summary:
# # # {summary}

# # # Instructions:
# # # 1. Identify columns with potential data type issues and suggest the correct type.
# # # 2. Detect columns that are mostly empty or irrelevant and suggest dropping them.
# # # 3. Suggest value replacements for typos, inconsistent formatting, or outliers.
# # # 4. Identify duplicates and suggest a strategy (drop or aggregate).
# # # 5. Recommend how to handle missing values for each column (median, mode, forward fill, or drop).
# # # 6. Highlight columns that may benefit from standardization (string case, date formats, numeric rounding).
# # # 7. Give any additional insights or data quality issues detected.

# # # Output JSON format (no markdown, just JSON):
# # # {{
# # #     "column_types": {{"column_name": "recommended_type"}},
# # #     "columns_to_drop": ["column1", "column2"],
# # #     "encoding_fixes": {{"column_name": "fix_description"}},
# # #     "value_replacements": {{"column_name": {{"old_value": "new_value"}}}},
# # #     "duplicate_strategy": {{"columns": ["columns_to_check"], "action": "drop/aggregate"}},
# # #     "missing_value_strategy": {{"column_name": "strategy_description"}},
# # #     "standardization": {{"column_name": "standardization_description"}},
# # #     "insights": ["insight1", "insight2"]
# # # }}"""
            
# # #             response = globals()['GEMINI_MODEL'].generate_content(prompt)
# # #             recommendations = self._parse_ai_response(response.text)
            
# # #             if recommendations:
# # #                 logger.info("💡 AI Recommendations:")
# # #                 df = self._apply_ai_recommendations(df, recommendations)
# # #                 self.report["ai_insights"].extend(recommendations.get("insights", []))
        
# # #         except Exception as e:
# # #             logger.error(f"⚠️ AI analysis failed: {e}")
# # #             self.report["ai_insights"] = ["AI analysis unavailable"]
        
# # #         return df


    
# # #     def _ai_validate(self, df: pd.DataFrame) -> pd.DataFrame:
# # #         """Final AI validation of cleaned data with console output"""
# # #         if not self.ai_enabled:
# # #              return df
             
# # #         try:
# # #             if not globals().get('GEMINI_MODEL'):
# # #                  logger.warning("🤖 AI model not loaded. Skipping validation.")
# # #                  return df
                 
# # #             summary = self._create_dataset_summary(df)
            
# # #             prompt = f"""Review this cleaned dataset and identify any remaining data quality issues.

# # # {summary}

# # # Provide issues in JSON format:
# # # {{
# # #     "quality_score": 0-100,
# # #     "remaining_issues": ["issue1", "issue2"],
# # #     "suggestions": ["suggestion1", "suggestion2"]
# # # }}"""
            
# # #             response = globals()['GEMINI_MODEL'].generate_content(prompt)
# # #             validation = self._parse_ai_response(response.text)
            
# # #             if validation:
# # #                 logger.info("\n  💡 Validation Results:")
# # #                 score = validation.get('quality_score', 'N/A')
# # #                 logger.info(f"  📈 Quality Score: {score}")
                
# # #                 if validation.get("remaining_issues"):
# # #                     logger.info(f"  ⚠️  Remaining Issues:")
# # #                     for issue in validation["remaining_issues"]:
# # #                         logger.info(f"    - {issue}")
                
# # #                 if validation.get("suggestions"):
# # #                     logger.info(f"  📝 Suggestions:")
# # #                     for suggestion in validation["suggestions"]:
# # #                         logger.info(f"    - {suggestion}")
                
# # #                 self.report["ai_insights"].append({
# # #                     "quality_score": score,
# # #                     "remaining_issues": validation.get("remaining_issues", []),
# # #                     "suggestions": validation.get("suggestions", [])
# # #                 })
        
# # #         except Exception as e:
# # #             logger.error(f"  ⚠️ AI validation failed: {e}")
        
# # #         return df
    
# # #     def _remove_empty(self, df: pd.DataFrame) -> pd.DataFrame:
# # #         """Remove completely empty rows and columns"""
# # #         initial_shape = df.shape
# # #         df = df.dropna(how='all')
# # #         df = df.dropna(axis=1, how='all')
        
# # #         removed_rows = initial_shape[0] - df.shape[0]
# # #         removed_cols = initial_shape[1] - df.shape[1]
        
# # #         if removed_rows > 0 or removed_cols > 0:
# # #             self.report["operations"].append({
# # #                 "step": "remove_empty",
# # #                 "rows_removed": removed_rows,
# # #                 "columns_removed": removed_cols
# # #             })
# # #             if removed_rows > 0:
# # #                 logger.info(f"  ✅ Removed {removed_rows} empty rows")
# # #             if removed_cols > 0:
# # #                 logger.info(f"  ✅ Removed {removed_cols} empty columns")
        
# # #         return df
    
# # #     def _standardize_columns(self, df: pd.DataFrame) -> pd.DataFrame:
# # #         """Standardize column names: lowercase, underscores, no special chars"""
# # #         original_cols = df.columns.tolist()
# # #         new_cols = []
        
# # #         for col in df.columns:
# # #             col_clean = str(col).lower().strip()
# # #             col_clean = re.sub(r'[^\w\s]', '', col_clean)
# # #             col_clean = re.sub(r'\s+', '_', col_clean)
# # #             col_clean = re.sub(r'_+', '_', col_clean)
# # #             col_clean = col_clean.strip('_')
# # #             new_cols.append(col_clean)
        
# # #         seen = {}
# # #         for i, col in enumerate(new_cols):
# # #             if col in seen:
# # #                 seen[col] += 1
# # #                 new_cols[i] = f"{col}_{seen[col]}"
# # #             else:
# # #                 seen[col] = 0
        
# # #         df.columns = new_cols
        
# # #         self.report["operations"].append({
# # #             "step": "standardize_columns",
# # #             "mapping": dict(zip(original_cols, new_cols))
# # #         })
        
# # #         logger.info(f"  ✅ Standardized {len(original_cols)} column names")
        
# # #         return df
    
# # #     def _remove_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
# # #         """Remove duplicate rows"""
# # #         initial_rows = len(df)
# # #         df = df.drop_duplicates()
# # #         duplicates_removed = initial_rows - len(df)
        
# # #         if duplicates_removed > 0:
# # #             self.report["operations"].append({
# # #                 "step": "remove_duplicates",
# # #                 "duplicates_removed": duplicates_removed
# # #             })
# # #             logger.info(f"  ✅ Removed {duplicates_removed} duplicate rows")
        
# # #         return df
    
# # #     def _normalize_types(self, df: pd.DataFrame) -> pd.DataFrame:
# # #         """Infer and normalize column data types"""
# # #         type_changes = {}
        
# # #         for col in df.columns:
# # #             original_type = str(df[col].dtype)
            
# # #             if pd.api.types.is_numeric_dtype(df[col]):
# # #                 continue
            
# # #             if df[col].dtype == 'object':
# # #                 sample = df[col].dropna().head(100)
# # #                 numeric_count = sum(self._is_numeric_string(str(x)) for x in sample)
                
# # #                 if len(sample) > 0 and numeric_count / len(sample) > 0.8:
# # #                     df[col] = pd.to_numeric(df[col], errors='coerce')
# # #                     type_changes[col] = f"{original_type} → {df[col].dtype}"
# # #                     continue
                
# # #                 try:
# # #                     parsed = pd.to_datetime(df[col], errors='coerce')
# # #                     if parsed.notna().sum() / len(df) > 0.5:
# # #                         df[col] = parsed
# # #                         type_changes[col] = f"{original_type} → datetime64"
# # #                 except:
# # #                     pass
        
# # #         if type_changes:
# # #             self.report["operations"].append({
# # #                 "step": "normalize_types",
# # #                 "type_changes": type_changes
# # #             })
# # #             logger.info(f"  ✅ Normalized {len(type_changes)} column types")
        
# # #         return df
    
# # #     def _is_numeric_string(self, s: str) -> bool:
# # #         """Check if string represents a number"""
# # #         try:
# # #             s = s.strip().replace(',', '').replace('$', '').replace('%', '')
# # #             float(s)
# # #             return True
# # #         except:
# # #             return False
    
# # #     def _handle_missing(self, df: pd.DataFrame) -> pd.DataFrame:
# # #         """Handle missing values intelligently"""
# # #         missing_strategy = {}
        
# # #         for col in df.columns:
# # #             missing_count = df[col].isna().sum()
# # #             if missing_count == 0:
# # #                 continue
            
# # #             missing_pct = missing_count / len(df)
            
# # #             if missing_pct > 0.5:
# # #                 df = df.drop(columns=[col])
# # #                 missing_strategy[col] = "dropped (>50% missing)"
# # #                 continue
            
# # #             if pd.api.types.is_numeric_dtype(df[col]):
# # #                 df[col].fillna(df[col].median(), inplace=True)
# # #                 missing_strategy[col] = "filled with median"
            
# # #             elif pd.api.types.is_datetime64_any_dtype(df[col]):
# # #                 df[col].fillna(method='ffill', inplace=True)
# # #                 missing_strategy[col] = "forward filled"
            
# # #             else:
# # #                 mode_val = df[col].mode()
# # #                 if len(mode_val) > 0:
# # #                     df[col].fillna(mode_val[0], inplace=True)
# # #                     missing_strategy[col] = "filled with mode"
# # #                 else:
# # #                     df[col].fillna('Unknown', inplace=True)
# # #                     missing_strategy[col] = "filled with 'Unknown'"
        
# # #         if missing_strategy:
# # #             self.report["operations"].append({
# # #                 "step": "handle_missing",
# # #                 "strategy": missing_strategy
# # #             })
# # #             logger.info(f"  ✅ Handled missing values in {len(missing_strategy)} columns")
        
# # #         return df
    
# # #     def _standardize_formats(self, df: pd.DataFrame) -> pd.DataFrame:
# # #         """Standardize string and numeric formats"""
# # #         format_changes = []
        
# # #         for col in df.columns:
# # #             if df[col].dtype == 'object':
# # #                 df[col] = df[col].astype(str).str.strip()
                
# # #                 if 'name' in col.lower():
# # #                     df[col] = df[col].str.title()
# # #                     format_changes.append(f"{col}: applied title case")
            
# # #             elif pd.api.types.is_float_dtype(df[col]):
# # #                 df[col] = df[col].round(2)
# # #                 format_changes.append(f"{col}: rounded to 2 decimals")
        
# # #         if format_changes:
# # #             self.report["operations"].append({
# # #                 "step": "standardize_formats",
# # #                 "changes": format_changes
# # #             })
# # #             logger.info(f"  ✅ Standardized formats in {len(format_changes)} columns")
        
# # #         return df
    
# # #     def _handle_outliers(self, df: pd.DataFrame) -> pd.DataFrame:
# # #         """Remove statistical outliers using IQR method"""
# # #         outliers_removed = {}
        
# # #         for col in df.columns:
# # #             if not pd.api.types.is_numeric_dtype(df[col]):
# # #                 continue
            
# # #             Q1 = df[col].quantile(0.25)
# # #             Q3 = df[col].quantile(0.75)
# # #             IQR = Q3 - Q1
            
# # #             lower_bound = Q1 - 3 * IQR
# # #             upper_bound = Q3 + 3 * IQR
            
# # #             initial_count = len(df)
# # #             df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
# # #             removed = initial_count - len(df)
            
# # #             if removed > 0:
# # #                 outliers_removed[col] = removed
        
# # #         if outliers_removed:
# # #             self.report["operations"].append({
# # #                 "step": "remove_outliers",
# # #                 "outliers_removed": outliers_removed
# # #             })
# # #             logger.info(f"  ✅ Removed outliers from {len(outliers_removed)} columns")
        
# # #         return df

# # #     def _scale_and_encode(self, df: pd.DataFrame) -> pd.DataFrame:
# # #         """Apply StandardScaler and LabelEncoder."""
# # #         scaled_cols = []
# # #         encoded_cols = []
# # #         # Clear mappings for this specific run
# # #         self.le_mapping = {}
# # #         self.ss_mapping = {}

# # #         df_processed = df.copy()

# # #         for col in df_processed.columns:
# # #             if col.endswith('_embedding_0'): 
# # #                 continue

# # #             if pd.api.types.is_numeric_dtype(df_processed[col]):
# # #                 if df_processed[col].nunique() > 1:
# # #                     scaler = StandardScaler()
# # #                     data = df_processed[col].values.reshape(-1, 1)
# # #                     df_processed[col] = scaler.fit_transform(data)
# # #                     self.ss_mapping[col] = {'mean': scaler.mean_[0], 'scale': scaler.scale_[0]}
# # #                     scaled_cols.append(col)
            
# # #             elif df_processed[col].dtype == 'object' or pd.api.types.is_categorical_dtype(df_processed[col]):
# # #                 # Apply LabelEncoder to categorical/string columns
# # #                 le = LabelEncoder()
# # #                 data = df_processed[col].astype(str)
# # #                 df_processed[col] = le.fit_transform(data)
# # #                 self.le_mapping[col] = {'classes': le.classes_.tolist()}
# # #                 encoded_cols.append(col)
        
# # #         self.report["operations"].append({
# # #             "step": "scaling_encoding",
# # #             "scaled_columns": scaled_cols,
# # #             "encoded_columns": encoded_cols
# # #         })
# # #         logger.info(f"  ✅ Scaled {len(scaled_cols)} columns, Encoded {len(encoded_cols)} columns.")
# # #         return df_processed
    
# # #     def _embed_text_columns(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
# # #         """Generate SentenceTransformer embeddings for textual columns."""
# # #         if not self.embedding_model:
# # #             return pd.DataFrame(index=df.index), {"embedding_summary": "Embedding skipped (model not loaded)."}

# # #         text_cols = [col for col in df.columns if df[col].dtype == 'object']
        
# # #         if not text_cols:
# # #             return pd.DataFrame(index=df.index), {"embedding_summary": "No suitable text columns found for embedding."}
        
# # #         embedding_summary = {}
# # #         df_for_concat = pd.DataFrame(index=df.index)

# # #         for col in text_cols:
# # #             sentences = df[col].astype(str).tolist()
# # #             sentences = [s if s.strip() != 'nan' else '' for s in sentences]
            
# # #             embeddings = self.embedding_model.encode(
# # #                 sentences, 
# # #                 show_progress_bar=False, 
# # #                 convert_to_numpy=True,
# # #                 batch_size=32  # Optimized batch size for efficiency
# # #             )
            
# # #             embedding_col_names = [f"{col}_embedding_{i}" for i in range(self.embedding_dim)]
# # #             embedding_df = pd.DataFrame(embeddings, columns=embedding_col_names, index=df.index)
# # #             df_for_concat = pd.concat([df_for_concat, embedding_df], axis=1)
            
# # #             embedding_summary[col] = {
# # #                 "vector_size": self.embedding_dim,
# # #                 "new_columns": embedding_col_names
# # #             }
        
# # #         self.report["operations"].append({
# # #             "step": "text_embedding",
# # #             "embedded_columns": list(embedding_summary.keys())
# # #         })
# # #         logger.info(f"  ✅ Embedded {len(text_cols)} text columns into {len(text_cols) * self.embedding_dim} new columns.")

# # #         return df_for_concat, {"embedding_summary": embedding_summary}


# # #     def clean(self, df: pd.DataFrame, ml_mode: bool) -> Tuple[pd.DataFrame, Dict[str, Any]]:
# # #         """
# # #         Main cleaning pipeline.
# # #         Returns: (cleaned_df, final_report)
# # #         """
# # #         logger.info("="*80)
# # #         logger.info(f"🚀 STARTING DATA CLEANING PIPELINE (ML_MODE={ml_mode})")
# # #         logger.info("="*80)
        
# # #         self.report = {
# # #             "original_shape": df.shape,
# # #             "operations": [],
# # #             "ai_insights": []
# # #         }
        
# # #         df_cleaned = df.copy()
        
# # #         logger.info(f"\n📊 Original Dataset: {df.shape[0]} rows × {df.shape[1]} columns")
        
# # #         # --- Stage 1: Basic Cleaning and Imputation (Common to both modes) ---
# # #         if self.ai_enabled:
# # #             logger.info("\n🤖 Running AI Analysis...")
# # #             df_cleaned = self._ai_analyze_and_clean(df_cleaned)
        
# # #         logger.info("\n🧹 Removing empty rows/columns...")
# # #         df_cleaned = self._remove_empty(df_cleaned)
# # #         logger.info("📝 Standardizing column names...")
# # #         df_cleaned = self._standardize_columns(df_cleaned)
# # #         logger.info("🔍 Checking for duplicates...")
# # #         df_cleaned = self._remove_duplicates(df_cleaned)
# # #         logger.info("🔧 Normalizing data types...")
# # #         df_cleaned = self._normalize_types(df_cleaned)
# # #         logger.info("📌 Handling missing values...")
# # #         df_cleaned = self._handle_missing(df_cleaned)
# # #         logger.info("✨ Standardizing formats...")
# # #         df_cleaned = self._standardize_formats(df_cleaned)
# # #         logger.info("📊 Detecting outliers...")
# # #         df_cleaned = self._handle_outliers(df_cleaned)
        
# # #         # Save the final text-cleaned version (for Human-Readable output)
# # #         df_final_text = df_cleaned.copy()
        
# # #         # --- Stage 2: ML/Numerical Transformation (Only if ml_mode is True) ---
# # #         if ml_mode:
# # #             text_cols_for_embedding = [col for col in df_cleaned.columns if df_cleaned[col].dtype == 'object']
# # #             df_for_scaling = df_cleaned.drop(columns=text_cols_for_embedding, errors='ignore')

# # #             # 2a. Embed text columns
# # #             df_embeddings, embedding_report = self._embed_text_columns(df_cleaned[text_cols_for_embedding])
            
# # #             # 2b. Scale and Encode the remaining non-embedded columns
# # #             logger.info("🧠 Scaling and Encoding numerical/categorical columns...")
# # #             df_scaled_encoded = self._scale_and_encode(df_for_scaling)
            
# # #             # 2c. Concatenate the final processed parts
# # #             # Must use reset_index(drop=True) because previous steps might have reindexed the dataframes differently
# # #             df_final_ml = pd.concat([df_scaled_encoded.reset_index(drop=True), df_embeddings.reset_index(drop=True)], axis=1)
            
# # #             # Use the ML output for final steps
# # #             df_final = df_final_ml
            
# # #         else:
# # #             # SIMPLE MODE: Apply LabelEncoder only to categorical data for basic numerical output, 
# # #             # retaining the original column structure but ensuring non-text columns are numeric/encoded.
# # #             logger.info("🧠 Running Simple Encoding (LabelEncoder) for categorical data...")
# # #             df_final = self._scale_and_encode(df_final_text.copy())
# # #             embedding_report = {"embedding_summary": "Embedding skipped (SIMPLE_MODE enforced)."}
        
# # #         # --- Stage 3: Finalization ---
# # #         if self.ai_enabled:
# # #             logger.info("\n🎯 Running AI Validation...")
# # #             df_final = self._ai_validate(df_final)
        
# # #         self.report["final_shape"] = df_final.shape
# # #         self.report["rows_original"] = df.shape[0]
# # #         self.report["rows_cleaned"] = df_final.shape[0]
# # #         self.report["columns_original"] = df.shape[1]
# # #         self.report["columns_final"] = df_final.shape[1]
        
# # #         final_report = {
# # #             "cleaning_operations": self.report,
# # #             "preprocessing_details": {
# # #                 "scaling_maps": self.ss_mapping,
# # #                 "encoding_maps": self.le_mapping,
# # #                 **embedding_report
# # #             }
# # #         }
        
# # #         logger.info("="*80)
# # #         logger.info("✅ CLEANING COMPLETE")
# # #         logger.info(f"📊 Final Dataset: {df_final.shape[0]} rows × {df_final.shape[1]} columns")
# # #         logger.info("="*80 + "\n")
        
# # #         # Return the final DataFrame ready for storage/download AND the corresponding text version
# # #         return df_final, df_final_text, final_report



# # # cleaning.py - FIXED VERSION

# # import pandas as pd
# # import numpy as np
# # from typing import Tuple, Dict, Any, List
# # import re
# # import os
# # import json
# # from dotenv import load_dotenv
# # from sklearn.preprocessing import StandardScaler, LabelEncoder
# # from sentence_transformers import SentenceTransformer
# # import logging

# # load_dotenv()
# # logger = logging.getLogger(__name__)
# # logging.basicConfig(level=logging.INFO)

# # # --- SentenceTransformer Configuration ---
# # SBERT_AVAILABLE = False
# # EMBEDDING_MODEL = None
# # EMBEDDING_DIM = 0
# # try:
# #     SBERT_AVAILABLE = True
# #     EMBEDDING_MODEL = SentenceTransformer('all-MiniLM-L6-v2', device='cpu') 
# #     EMBEDDING_DIM = 384
# #     logger.info("✅ SentenceTransformer (all-MiniLM-L6-v2) loaded.")
# # except ImportError:
# #     logger.warning("⚠️ Sentence-Transformers not installed. Text embedding will be skipped.")
# # except Exception as e:
# #     logger.error(f"⚠️ Failed to load SentenceTransformer: {e}. Text embedding disabled.")


# # # --- Gemini Configuration ---
# # AI_ENABLED = False
# # try:
# #     import google.generativeai as genai
# #     api_key = os.getenv("GEMINI_API_KEY")
# #     if api_key:
# #         genai.configure(api_key=api_key)
# #         GEMINI_MODEL = genai.GenerativeModel('gemini-2.0-flash-exp')
# #         AI_ENABLED = True
# #         logger.info("✅ Gemini AI enabled.")
# #     else:
# #         logger.warning("⚠️ GEMINI_API_KEY not set. Using rule-based cleaning only.")
# # except ImportError:
# #     logger.warning("⚠️ google-generativeai not installed. AI features disabled.")
# # except Exception as e:
# #     logger.error(f"⚠️ Failed to initialize Gemini: {e}")


# # class DataCleaner:
# #     """
# #     AI-Powered data cleaning engine.
# #     Handles general cleaning, normalization, encoding, and text embedding.
# #     """
    
# #     def __init__(self):
# #         self.report = {}
# #         self.ai_enabled = AI_ENABLED
# #         self.embedding_model = EMBEDDING_MODEL
# #         self.embedding_dim = EMBEDDING_DIM
# #         self.le_mapping = {}
# #         self.ss_mapping = {}

    
# #     def _create_dataset_summary(self, df: pd.DataFrame) -> str:
# #         """Create a concise summary for AI analysis"""
# #         summary_parts = []
# #         summary_parts.append(f"Shape: {df.shape[0]} rows × {df.shape[1]} columns")
# #         summary_parts.append(f"\nColumns: {', '.join(df.columns.tolist()[:10])}")
# #         summary_parts.append(f"\nData Types:\n{df.dtypes.to_string()}")
# #         missing = df.isnull().sum()
# #         if missing.any():
# #             summary_parts.append(f"\nMissing Values:\n{missing[missing > 0].to_string()}")
# #         summary_parts.append(f"\nSample Data (first 3 rows):\n{df.head(3).to_string()}")
# #         return "\n".join(summary_parts)

# #     def _parse_ai_response(self, response_text: str) -> Dict[str, Any]:
# #         """Parse AI response and extract JSON recommendations"""
# #         try:
# #             response_text = re.sub(r'```json\s*', '', response_text)
# #             response_text = re.sub(r'```\s*', '', response_text)
# #             recommendations = json.loads(response_text)
# #             return recommendations
# #         except Exception as e:
# #             logger.error(f"⚠️ Failed to parse AI recommendations: {e}")
# #             return {}

# #     def _apply_ai_recommendations(self, df: pd.DataFrame, recommendations: Dict[str, Any]) -> pd.DataFrame:
# #         """Apply AI-generated cleaning recommendations and log changes"""
# #         operations = []
        
# #         # Drop recommended columns
# #         columns_to_drop = recommendations.get("columns_to_drop", [])
# #         if columns_to_drop:
# #             existing_cols = [col for col in columns_to_drop if col in df.columns]
# #             if existing_cols:
# #                 df = df.drop(columns=existing_cols)
# #                 operations.append(f"Dropped columns: {', '.join(existing_cols)}")
# #                 logger.info(f"  ✅ Dropped columns: {', '.join(existing_cols)}")
        
# #         # Apply value replacements
# #         replacements = recommendations.get("value_replacements", {})
# #         for col, replace_map in replacements.items():
# #             if col in df.columns:
# #                 df[col] = df[col].replace(replace_map)
# #                 operations.append(f"Replaced values in {col}")
# #                 logger.info(f"  🔄 Replaced values in '{col}'")
        
# #         # Apply recommended type conversions
# #         column_types = recommendations.get("column_types", {})
# #         for col, dtype in column_types.items():
# #             if col in df.columns:
# #                 try:
# #                     if dtype == "numeric":
# #                         df[col] = pd.to_numeric(df[col], errors='coerce')
# #                     elif dtype == "datetime":
# #                         df[col] = pd.to_datetime(df[col], errors='coerce')
# #                     elif dtype == "string":
# #                         df[col] = df[col].astype(str)
# #                     operations.append(f"Converted {col} to {dtype}")
# #                     logger.info(f"  🔧 Converted '{col}' to {dtype}")
# #                 except Exception as e:
# #                     logger.warning(f"  ⚠️ Failed to convert {col}: {e}")
        
# #         # Handle duplicate strategy
# #         dup_strategy = recommendations.get("duplicate_strategy", {})
# #         if dup_strategy.get("action") == "drop":
# #             cols = dup_strategy.get("columns", df.columns.tolist())
# #             initial = len(df)
# #             df = df.drop_duplicates(subset=cols)
# #             removed = initial - len(df)
# #             operations.append(f"Dropped {removed} duplicate rows")
# #             logger.info(f"  🗑  Dropped {removed} duplicate rows")
        
# #         if operations:
# #             self.report["operations"].append({
# #                 "step": "ai_recommendations",
# #                 "actions": operations
# #             })
        
# #         return df

    
# #     def _ai_analyze_and_clean(self, df: pd.DataFrame) -> pd.DataFrame:
# #         """Use Gemini AI to analyze dataset and suggest cleaning strategies"""
# #         if not self.ai_enabled:
# #              logger.info("🤖 AI analysis skipped: GEMINI_API_KEY not set.")
# #              return df
             
# #         try:
# #             if not globals().get('GEMINI_MODEL'):
# #                  logger.warning("🤖 AI model not loaded. Skipping analysis.")
# #                  return df

# #             summary = self._create_dataset_summary(df)
            
# #             prompt = f"""You are a data cleaning expert. Analyze this dataset summary and provide a detailed cleaning plan in JSON format. 

# # Dataset Summary:
# # {summary}

# # Instructions:
# # 1. Identify columns with potential data type issues and suggest the correct type.
# # 2. Detect columns that are mostly empty or irrelevant and suggest dropping them.
# # 3. Suggest value replacements for typos or inconsistent formatting.
# # 4. Identify duplicates and suggest a strategy.
# # 5. Recommend how to handle missing values for each column.

# # Output ONLY valid JSON (no markdown):
# # {{
# #     "column_types": {{"column_name": "recommended_type"}},
# #     "columns_to_drop": ["column1"],
# #     "value_replacements": {{"column_name": {{"old_value": "new_value"}}}},
# #     "duplicate_strategy": {{"columns": [], "action": "drop"}},
# #     "insights": ["insight1"]
# # }}"""
            
# #             response = globals()['GEMINI_MODEL'].generate_content(prompt)
# #             recommendations = self._parse_ai_response(response.text)
            
# #             if recommendations:
# #                 logger.info("💡 Applying AI Recommendations...")
# #                 df = self._apply_ai_recommendations(df, recommendations)
# #                 self.report["ai_insights"].extend(recommendations.get("insights", []))
        
# #         except Exception as e:
# #             logger.error(f"⚠️ AI analysis failed: {e}")
# #             self.report["ai_insights"] = ["AI analysis unavailable"]
        
# #         return df


    
# #     def _ai_validate(self, df: pd.DataFrame) -> pd.DataFrame:
# #         """Final AI validation of cleaned data"""
# #         if not self.ai_enabled:
# #              return df
             
# #         try:
# #             if not globals().get('GEMINI_MODEL'):
# #                  return df
                 
# #             summary = self._create_dataset_summary(df)
            
# #             prompt = f"""Review this cleaned dataset and identify any remaining data quality issues.

# # {summary}

# # Output ONLY valid JSON:
# # {{
# #     "quality_score": 85,
# #     "remaining_issues": ["issue1"],
# #     "suggestions": ["suggestion1"]
# # }}"""
            
# #             response = globals()['GEMINI_MODEL'].generate_content(prompt)
# #             validation = self._parse_ai_response(response.text)
            
# #             if validation:
# #                 logger.info(f"  📈 Quality Score: {validation.get('quality_score', 'N/A')}")
                
# #                 self.report["ai_insights"].append({
# #                     "quality_score": validation.get('quality_score'),
# #                     "remaining_issues": validation.get("remaining_issues", []),
# #                     "suggestions": validation.get("suggestions", [])
# #                 })
        
# #         except Exception as e:
# #             logger.error(f"  ⚠️ AI validation failed: {e}")
        
# #         return df
    
# #     def _remove_empty(self, df: pd.DataFrame) -> pd.DataFrame:
# #         """Remove completely empty rows and columns"""
# #         initial_shape = df.shape
# #         df = df.dropna(how='all')
# #         df = df.dropna(axis=1, how='all')
        
# #         removed_rows = initial_shape[0] - df.shape[0]
# #         removed_cols = initial_shape[1] - df.shape[1]
        
# #         if removed_rows > 0 or removed_cols > 0:
# #             self.report["operations"].append({
# #                 "step": "remove_empty",
# #                 "rows_removed": removed_rows,
# #                 "columns_removed": removed_cols
# #             })
# #             if removed_rows > 0:
# #                 logger.info(f"  ✅ Removed {removed_rows} empty rows")
# #             if removed_cols > 0:
# #                 logger.info(f"  ✅ Removed {removed_cols} empty columns")
        
# #         return df
    
# #     def _standardize_columns(self, df: pd.DataFrame) -> pd.DataFrame:
# #         """Standardize column names: lowercase, underscores, no special chars"""
# #         original_cols = df.columns.tolist()
# #         new_cols = []
        
# #         for col in df.columns:
# #             col_clean = str(col).lower().strip()
# #             col_clean = re.sub(r'[^\w\s]', '', col_clean)
# #             col_clean = re.sub(r'\s+', '_', col_clean)
# #             col_clean = re.sub(r'_+', '_', col_clean)
# #             col_clean = col_clean.strip('_')
# #             new_cols.append(col_clean)
        
# #         # Handle duplicates
# #         seen = {}
# #         for i, col in enumerate(new_cols):
# #             if col in seen:
# #                 seen[col] += 1
# #                 new_cols[i] = f"{col}_{seen[col]}"
# #             else:
# #                 seen[col] = 0
        
# #         df.columns = new_cols
        
# #         self.report["operations"].append({
# #             "step": "standardize_columns",
# #             "mapping": dict(zip(original_cols, new_cols))
# #         })
        
# #         logger.info(f"  ✅ Standardized {len(original_cols)} column names")
        
# #         return df
    
# #     def _remove_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
# #         """Remove duplicate rows"""
# #         initial_rows = len(df)
# #         df = df.drop_duplicates()
# #         duplicates_removed = initial_rows - len(df)
        
# #         if duplicates_removed > 0:
# #             self.report["operations"].append({
# #                 "step": "remove_duplicates",
# #                 "duplicates_removed": duplicates_removed
# #             })
# #             logger.info(f"  ✅ Removed {duplicates_removed} duplicate rows")
        
# #         return df
    
# #     def _normalize_types(self, df: pd.DataFrame) -> pd.DataFrame:
# #         """Infer and normalize column data types"""
# #         type_changes = {}
        
# #         for col in df.columns:
# #             original_type = str(df[col].dtype)
            
# #             if pd.api.types.is_numeric_dtype(df[col]):
# #                 continue
            
# #             if df[col].dtype == 'object':
# #                 sample = df[col].dropna().head(100)
# #                 if len(sample) == 0:
# #                     continue
                    
# #                 numeric_count = sum(self._is_numeric_string(str(x)) for x in sample)
                
# #                 if numeric_count / len(sample) > 0.8:
# #                     df[col] = pd.to_numeric(df[col], errors='coerce')
# #                     type_changes[col] = f"{original_type} → {df[col].dtype}"
# #                     continue
                
# #                 # Try datetime conversion
# #                 try:
# #                     parsed = pd.to_datetime(df[col], errors='coerce')
# #                     if parsed.notna().sum() / len(df) > 0.5:
# #                         df[col] = parsed
# #                         type_changes[col] = f"{original_type} → datetime64"
# #                 except:
# #                     pass
        
# #         if type_changes:
# #             self.report["operations"].append({
# #                 "step": "normalize_types",
# #                 "type_changes": type_changes
# #             })
# #             logger.info(f"  ✅ Normalized {len(type_changes)} column types")
        
# #         return df
    
# #     def _is_numeric_string(self, s: str) -> bool:
# #         """Check if string represents a number"""
# #         try:
# #             s = s.strip().replace(',', '').replace('$', '').replace('%', '')
# #             float(s)
# #             return True
# #         except:
# #             return False
    
# #     def _handle_missing(self, df: pd.DataFrame) -> pd.DataFrame:
# #         """Handle missing values intelligently"""
# #         missing_strategy = {}
        
# #         for col in df.columns:
# #             missing_count = df[col].isna().sum()
# #             if missing_count == 0:
# #                 continue
            
# #             missing_pct = missing_count / len(df)
            
# #             # Drop columns with >50% missing
# #             if missing_pct > 0.5:
# #                 df = df.drop(columns=[col])
# #                 missing_strategy[col] = "dropped (>50% missing)"
# #                 continue
            
# #             # Fill numeric with median
# #             if pd.api.types.is_numeric_dtype(df[col]):
# #                 df[col].fillna(df[col].median(), inplace=True)
# #                 missing_strategy[col] = "filled with median"
            
# #             # Forward fill datetime
# #             elif pd.api.types.is_datetime64_any_dtype(df[col]):
# #                 df[col].fillna(method='ffill', inplace=True)
# #                 missing_strategy[col] = "forward filled"
            
# #             # Fill categorical with mode
# #             else:
# #                 mode_val = df[col].mode()
# #                 if len(mode_val) > 0:
# #                     df[col].fillna(mode_val[0], inplace=True)
# #                     missing_strategy[col] = "filled with mode"
# #                 else:
# #                     df[col].fillna('Unknown', inplace=True)
# #                     missing_strategy[col] = "filled with 'Unknown'"
        
# #         if missing_strategy:
# #             self.report["operations"].append({
# #                 "step": "handle_missing",
# #                 "strategy": missing_strategy
# #             })
# #             logger.info(f"  ✅ Handled missing values in {len(missing_strategy)} columns")
        
# #         return df
    
# #     def _standardize_formats(self, df: pd.DataFrame) -> pd.DataFrame:
# #         """Standardize string and numeric formats"""
# #         format_changes = []
        
# #         for col in df.columns:
# #             if df[col].dtype == 'object':
# #                 df[col] = df[col].astype(str).str.strip()
                
# #                 # Apply title case to name columns
# #                 if 'name' in col.lower():
# #                     df[col] = df[col].str.title()
# #                     format_changes.append(f"{col}: applied title case")
            
# #             # Round floats to 2 decimals
# #             elif pd.api.types.is_float_dtype(df[col]):
# #                 df[col] = df[col].round(2)
# #                 format_changes.append(f"{col}: rounded to 2 decimals")
        
# #         if format_changes:
# #             self.report["operations"].append({
# #                 "step": "standardize_formats",
# #                 "changes": format_changes
# #             })
# #             logger.info(f"  ✅ Standardized formats in {len(format_changes)} columns")
        
# #         return df
    
# #     def _handle_outliers(self, df: pd.DataFrame) -> pd.DataFrame:
# #         """Remove statistical outliers using IQR method (conservative)"""
# #         outliers_removed = {}
        
# #         for col in df.columns:
# #             if not pd.api.types.is_numeric_dtype(df[col]):
# #                 continue
            
# #             Q1 = df[col].quantile(0.25)
# #             Q3 = df[col].quantile(0.75)
# #             IQR = Q3 - Q1
            
# #             # Use 3*IQR for conservative outlier removal
# #             lower_bound = Q1 - 3 * IQR
# #             upper_bound = Q3 + 3 * IQR
            
# #             initial_count = len(df)
# #             df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
# #             removed = initial_count - len(df)
            
# #             if removed > 0:
# #                 outliers_removed[col] = removed
        
# #         if outliers_removed:
# #             self.report["operations"].append({
# #                 "step": "remove_outliers",
# #                 "outliers_removed": outliers_removed
# #             })
# #             logger.info(f"  ✅ Removed outliers from {len(outliers_removed)} columns")
        
# #         return df

# #     def _should_scale_column(self, col_name: str, col_data: pd.Series) -> bool:
# #         """Determine if a numeric column should be scaled"""
# #         # Don't scale ID columns
# #         if any(term in col_name.lower() for term in ['id', 'index', 'key']):
# #             return False
        
# #         # Don't scale if column has very few unique values (likely categorical encoded)
# #         if col_data.nunique() < 10:
# #             return False
        
# #         # Don't scale binary columns
# #         unique_vals = col_data.dropna().unique()
# #         if len(unique_vals) == 2:
# #             return False
        
# #         return True

# #     def _scale_and_encode(self, df: pd.DataFrame) -> pd.DataFrame:
# #         """Apply StandardScaler to appropriate numeric columns and LabelEncoder to categorical"""
# #         scaled_cols = []
# #         encoded_cols = []
# #         self.le_mapping = {}
# #         self.ss_mapping = {}

# #         df_processed = df.copy()

# #         for col in df_processed.columns:
# #             # Skip embedding columns
# #             if '_embedding_' in col:
# #                 continue

# #             # Handle numeric columns - SELECTIVE SCALING
# #             if pd.api.types.is_numeric_dtype(df_processed[col]):
# #                 if df_processed[col].nunique() > 1 and self._should_scale_column(col, df_processed[col]):
# #                     scaler = StandardScaler()
# #                     data = df_processed[col].values.reshape(-1, 1)
# #                     df_processed[col] = scaler.fit_transform(data)
# #                     self.ss_mapping[col] = {
# #                         'mean': float(scaler.mean_[0]), 
# #                         'scale': float(scaler.scale_[0])
# #                     }
# #                     scaled_cols.append(col)
            
# #             # Handle categorical/string columns
# #             elif df_processed[col].dtype == 'object' or pd.api.types.is_categorical_dtype(df_processed[col]):
# #                 le = LabelEncoder()
# #                 data = df_processed[col].astype(str).fillna('Unknown')
# #                 df_processed[col] = le.fit_transform(data)
# #                 self.le_mapping[col] = {'classes': le.classes_.tolist()}
# #                 encoded_cols.append(col)
        
# #         self.report["operations"].append({
# #             "step": "scaling_encoding",
# #             "scaled_columns": scaled_cols,
# #             "encoded_columns": encoded_cols
# #         })
# #         logger.info(f"  ✅ Scaled {len(scaled_cols)} columns, Encoded {len(encoded_cols)} columns")
# #         return df_processed
    
# #     def _embed_text_columns(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
# #         """Generate SentenceTransformer embeddings for textual columns"""
# #         if not self.embedding_model:
# #             return pd.DataFrame(index=df.index), {"embedding_summary": "Embedding skipped (model not loaded)"}

# #         text_cols = [col for col in df.columns if df[col].dtype == 'object']
        
# #         if not text_cols:
# #             return pd.DataFrame(index=df.index), {"embedding_summary": "No text columns found"}
        
# #         embedding_summary = {}
# #         df_for_concat = pd.DataFrame(index=df.index)

# #         for col in text_cols:
# #             sentences = df[col].astype(str).fillna('').tolist()
            
# #             embeddings = self.embedding_model.encode(
# #                 sentences, 
# #                 show_progress_bar=False, 
# #                 convert_to_numpy=True,
# #                 batch_size=32
# #             )
            
# #             embedding_col_names = [f"{col}_embedding_{i}" for i in range(self.embedding_dim)]
# #             embedding_df = pd.DataFrame(embeddings, columns=embedding_col_names, index=df.index)
# #             df_for_concat = pd.concat([df_for_concat, embedding_df], axis=1)
            
# #             embedding_summary[col] = {
# #                 "vector_size": self.embedding_dim,
# #                 "new_columns": embedding_col_names
# #             }
        
# #         self.report["operations"].append({
# #             "step": "text_embedding",
# #             "embedded_columns": list(embedding_summary.keys())
# #         })
# #         logger.info(f"  ✅ Embedded {len(text_cols)} text columns")

# #         return df_for_concat, {"embedding_summary": embedding_summary}


# #     def clean(self, df: pd.DataFrame, ml_mode: bool) -> Tuple[pd.DataFrame, pd.DataFrame, Dict[str, Any]]:
# #         """
# #         Main cleaning pipeline.
# #         Returns: (df_final_processed, df_final_text, final_report)
# #         """
# #         logger.info("="*80)
# #         logger.info(f"🚀 STARTING DATA CLEANING PIPELINE (ML_MODE={ml_mode})")
# #         logger.info("="*80)
        
# #         self.report = {
# #             "original_shape": df.shape,
# #             "operations": [],
# #             "ai_insights": []
# #         }
        
# #         df_cleaned = df.copy()
        
# #         logger.info(f"\n📊 Original Dataset: {df.shape[0]} rows × {df.shape[1]} columns")
        
# #         # --- Stage 1: Basic Cleaning (Common to both modes) ---
# #         if self.ai_enabled:
# #             logger.info("\n🤖 Running AI Analysis...")
# #             df_cleaned = self._ai_analyze_and_clean(df_cleaned)
        
# #         logger.info("\n🧹 Removing empty rows/columns...")
# #         df_cleaned = self._remove_empty(df_cleaned)
# #         logger.info("📝 Standardizing column names...")
# #         df_cleaned = self._standardize_columns(df_cleaned)
# #         logger.info("🔍 Checking for duplicates...")
# #         df_cleaned = self._remove_duplicates(df_cleaned)
# #         logger.info("🔧 Normalizing data types...")
# #         df_cleaned = self._normalize_types(df_cleaned)
# #         logger.info("📌 Handling missing values...")
# #         df_cleaned = self._handle_missing(df_cleaned)
# #         logger.info("✨ Standardizing formats...")
# #         df_cleaned = self._standardize_formats(df_cleaned)
# #         logger.info("📊 Detecting outliers...")
# #         df_cleaned = self._handle_outliers(df_cleaned)
        
# #         # Save the clean text version
# #         df_final_text = df_cleaned.copy()
        
# #         # --- Stage 2: ML Transformation (if enabled) ---
# #         if ml_mode:
# #             logger.info("\n🧠 Running ML Mode Transformations...")
            
# #             text_cols = [col for col in df_cleaned.columns if df_cleaned[col].dtype == 'object']
# #             non_text_cols = [col for col in df_cleaned.columns if col not in text_cols]
            
# #             # Embed text columns
# #             df_embeddings, embedding_report = self._embed_text_columns(df_cleaned[text_cols])
            
# #             # Scale and encode non-text columns
# #             df_scaled_encoded = self._scale_and_encode(df_cleaned[non_text_cols])
            
# #             # Combine
# #             df_final = pd.concat([
# #                 df_scaled_encoded.reset_index(drop=True), 
# #                 df_embeddings.reset_index(drop=True)
# #             ], axis=1)
            
# #         else:
# #             # Simple mode: Just encode categorical columns
# #             logger.info("\n🧠 Running Simple Encoding...")
# #             df_final = self._scale_and_encode(df_final_text.copy())
# #             embedding_report = {"embedding_summary": "Embedding skipped (Simple mode)"}
        
# #         # --- Stage 3: Finalization ---
# #         if self.ai_enabled:
# #             logger.info("\n🎯 Running AI Validation...")
# #             df_final = self._ai_validate(df_final)
        
# #         self.report["final_shape"] = df_final.shape
# #         self.report["rows_original"] = df.shape[0]
# #         self.report["rows_cleaned"] = df_final.shape[0]
# #         self.report["columns_original"] = df.shape[1]
# #         self.report["columns_final"] = df_final.shape[1]
        
# #         final_report = {
# #             "cleaning_operations": self.report,
# #             "preprocessing_details": {
# #                 "scaling_maps": self.ss_mapping,
# #                 "encoding_maps": self.le_mapping,
# #                 **embedding_report
# #             }
# #         }
        
# #         logger.info("="*80)
# #         logger.info("✅ CLEANING COMPLETE")
# #         logger.info(f"📊 Final Dataset: {df_final.shape[0]} rows × {df_final.shape[1]} columns")
# #         logger.info("="*80 + "\n")
        
# #         return df_final, df_final_text, final_report


# import pandas as pd
# import numpy as np
# from typing import Tuple, Dict, Any, List, Optional, Callable
# import re
# import os
# import json
# from dotenv import load_dotenv
# from sklearn.preprocessing import StandardScaler, LabelEncoder
# from sentence_transformers import SentenceTransformer
# import logging
# import time

# load_dotenv()
# logger = logging.getLogger(__name__)
# # Setting log level lower than INFO means we can use debug logs for the "20k line" verbose output
# logging.basicConfig(level=logging.DEBUG) 

# # --- Sentinel Values ---
# CHRONO_ENCODING_FILL_VALUE = -1
# UNKNOWN_CATEGORY = 'Unknown_Category_Keginator'

# # --- SentenceTransformer Configuration ---
# SBERT_AVAILABLE = False
# EMBEDDING_MODEL = None
# EMBEDDING_DIM = 0
# try:
#     SBERT_AVAILABLE = True
#     EMBEDDING_MODEL = SentenceTransformer('all-MiniLM-L6-v2', device='cpu') 
#     EMBEDDING_DIM = 384
#     logger.info("✅ SentenceTransformer (all-MiniLM-L6-v2) loaded.")
# except ImportError:
#     logger.warning("⚠️ Sentence-Transformers not installed. Text embedding will be skipped.")
# except Exception as e:
#     logger.error(f"⚠️ Failed to load SentenceTransformer: {e}. Text embedding disabled.")


# # --- Gemini Configuration ---
# AI_ENABLED = False
# try:
#     import google.generativeai as genai
#     api_key = os.getenv("GEMINI_API_KEY")
#     if api_key:
#         # HIGH-IQ FIX: Using powerful experimental model as requested
#         GEMINI_MODEL = genai.GenerativeModel('gemini-2.5-flash-exp')
#         genai.configure(api_key=api_key)
#         AI_ENABLED = True
#         logger.info("✅ Gemini AI enabled (gemini-2.5-flash-exp).")
#     else:
#         logger.warning("⚠️ GEMINI_API_KEY not set. Using rule-based cleaning only.")
# except ImportError:
#     logger.warning("⚠️ google-generativeai not installed. AI features disabled.")
# except Exception as e:
#     logger.error(f"⚠️ Failed to initialize Gemini: {e}")


# class DataCleaner:
#     """
#     ULTRA-INTELLIGENT AI-Powered data cleaning engine (Keginator Genius Core).
#     Handles general cleaning, advanced normalization, chronological encoding, and ML pre-processing.
#     """
    
#     def __init__(self):
#         self.report = {}
#         self.ai_enabled = AI_ENABLED
#         self.embedding_model = EMBEDDING_MODEL
#         self.embedding_dim = EMBEDDING_DIM
#         self.le_mapping = {}
#         self.ss_mapping = {}

    
#     def _create_dataset_summary(self, df: pd.DataFrame) -> str:
#         """Generates a massive, detailed summary for the High-IQ AI."""
#         summary_parts = []
#         summary_parts.append(f"Shape: {df.shape[0]} rows × {df.shape[1]} columns")
#         summary_parts.append(f"\nColumns: {', '.join(df.columns.tolist()[:10])}")
#         summary_parts.append(f"\nData Types:\n{df.dtypes.to_string()}")
        
#         # Missing values with percentage
#         missing = df.isnull().sum()
#         if missing.any():
#             missing_data = missing[missing > 0].reset_index()
#             missing_data.columns = ['Column', 'Count']
#             missing_data['Percent'] = (missing_data['Count'] / len(df) * 100).round(2)
            
#             missing_str = "Missing Values (Count / Percent):\n"
#             for _, row in missing_data.iterrows():
#                 missing_str += f"  - {row['Column']}: {row['Count']} ({row['Percent']}%)"
#                 # Suggest dropping columns > 70% missing
#                 if row['Percent'] > 70.0:
#                     missing_str += " [SUGGEST DROP]"
#                 missing_str += "\n"
#             summary_parts.append(f"\n{missing_str.strip()}")

#         # Outlier Detection (Z-Score > 3 for numeric columns)
#         outlier_str = "\nOutlier Observations (Z-Score > 3 or IQR/3):\n"
#         has_outliers = False
#         for col in df.columns:
#             if pd.api.types.is_numeric_dtype(df[col]):
#                 series = df[col].dropna()
#                 if not series.empty:
#                     mean = series.mean()
#                     std = series.std()
#                     if std > 0:
#                         outliers = series[np.abs((series - mean) / std) > 3]
#                         if not outliers.empty:
#                             outlier_str += f"  - {col}: {len(outliers)} extreme values detected (Z-score > 3)\n"
#                             has_outliers = True
        
#         if has_outliers:
#             summary_parts.append(outlier_str.strip())
            
#         # Sample data (first 3 rows)
#         summary_parts.append(f"\nSample Data (first 3 rows):\n{df.head(3).to_string()}")
        
#         # Unique/Typo Sample (for categorical data)
#         typo_sample_str = "\nCategorical/Typo Sample (Top 5 values and their counts):\n"
#         has_categorical = False
#         for col in df.columns:
#             if df[col].dtype == 'object' or pd.api.types.is_categorical_dtype(df[col]):
#                 value_counts = df[col].astype(str).str.lower().value_counts().head(5)
#                 if not value_counts.empty:
#                     typo_sample_str += f"  - {col}:\n"
#                     for val, count in value_counts.items():
#                         typo_sample_str += f"    * '{val}': {count}\n"
#                     has_categorical = True
                    
#         if has_categorical:
#             summary_parts.append(typo_sample_str.strip())
            
#         logger.debug(f"Generated Detailed Summary for AI:\n{summary_parts}")
#         return "\n".join(summary_parts)

#     def _parse_ai_response(self, response_text: str) -> Dict[str, Any]:
#         """Parse AI response and extract JSON recommendations"""
#         try:
#             response_text = re.sub(r'```json\s*', '', response_text)
#             response_text = re.sub(r'```\s*', '', response_text)
#             recommendations = json.loads(response_text)
#             return recommendations
#         except Exception as e:
#             logger.error(f"⚠️ Failed to parse AI recommendations: {e}")
#             return {}
        
#     def _enhance_ai_prompt(self, summary: str) -> str:
#         """Generates the advanced prompt for Gemini (The Data Genius)"""
#         prompt = f"""You are a **Billion-Dollar High-IQ Data Genius AI** designed to perform the most comprehensive and intelligent data cleaning and pre-processing known to man. Your analysis must be deeper than simple rules, focusing on semantic and contextual inconsistencies.

# **Analyze the provided Dataset Summary:**
# {summary}

# **Pay EXTREME attention to the following semantic/contextual data quality issues and suggest fixes:**
# 1.  **Categorical Order/Chronology (CRITICAL FIX):** For columns containing ordered sequences like 'day' (Monday, Tuesday, etc.), identify the correct chronological order and provide an **EXACT** mapping to numerical ranks (starting from 1). This is vital for time-series ML models.
# 2.  **Typographical Inconsistencies/Misspellings (High-Confidence Fixes):** Suggest replacements (`value_replacements`) for clear typos (e.g., 'Suny' -> 'Sunny', 'Rin' -> 'Rain', 'Sunnny' -> 'Sunny').
# 3.  **Data Imputation Logic:** For missing values, suggest imputation methods. For the sample data provided, impute missing non-numeric cells with the most likely correct value (e.g., the Mode of the column). For the 'abc' entry in the 'temp' column, suggest replacing it with NaN so that the standard numeric imputation (median/mean) can handle it later.

# **Output ONLY valid JSON (no markdown). The JSON keys must be precise.**

# **Output JSON Keys to Include:**
# * `column_types`: Recommended final data type.
# * `columns_to_drop`: Irrelevant/mostly empty columns to drop.
# * `value_replacements`: Typo corrections/value replacements.
# * `duplicate_strategy`: Action for duplicates.
# * `categorical_encoding_order`: **CRITICAL KEY!** A dictionary where the key is the column name and the value is a `{{value: numerical_rank}}` mapping for chronological/logical encoding.
# * `insights`: Your key findings and genius-level observations.

# **Required Output JSON Format (must be ONLY JSON):**
# {{
#     "column_types": {{"column_name": "recommended_type"}},
#     "columns_to_drop": ["column1"],
#     "value_replacements": {{"column_name": {{"old_value": "new_value"}}}},
#     "duplicate_strategy": {{"columns": [], "action": "drop"}},
#     "categorical_encoding_order": {{"day": {{"Monday": 1, "Tuesday": 2, "Wednesday": 3, "Thursday": 4, "Friday": 5, "Saturday": 6, "Sunday": 7}}}},
#     "insights": ["insight1"]
# }}"""
#         return prompt


#     def _apply_ai_recommendations(self, df: pd.DataFrame, recommendations: Dict[str, Any]) -> pd.DataFrame:
#         """Apply AI-generated cleaning recommendations and log changes"""
#         operations = []
        
#         # New: Store categorical encoding order for ML step
#         self.report['categorical_encoding_order'] = recommendations.get("categorical_encoding_order", {})
        
#         # Drop recommended columns
#         columns_to_drop = recommendations.get("columns_to_drop", [])
#         if columns_to_drop:
#             existing_cols = [col for col in columns_to_drop if col in df.columns]
#             if existing_cols:
#                 df = df.drop(columns=existing_cols)
#                 operations.append(f"Dropped columns: {', '.join(existing_cols)}")
#                 logger.info(f"  ✅ Dropped columns: {', '.join(existing_cols)}")
        
#         # Apply value replacements
#         replacements = recommendations.get("value_replacements", {})
#         for col, replace_map in replacements.items():
#             if col in df.columns:
#                 # Need to cast to str temporarily for replacements to work consistently
#                 df.loc[:, col] = df[col].astype(str).replace(replace_map)
#                 operations.append(f"Replaced values in {col}")
#                 logger.info(f"  🔄 Replaced values in '{col}'")
        
#         # Apply recommended type conversions
#         column_types = recommendations.get("column_types", {})
#         for col, dtype in column_types.items():
#             if col in df.columns:
#                 try:
#                     if dtype == "numeric":
#                         df.loc[:, col] = pd.to_numeric(df[col], errors='coerce')
#                     elif dtype == "datetime":
#                         df.loc[:, col] = pd.to_datetime(df[col], errors='coerce')
#                     elif dtype == "string":
#                         df.loc[:, col] = df[col].astype(str)
#                     operations.append(f"Converted {col} to {dtype}")
#                     logger.info(f"  🔧 Converted '{col}' to {dtype}")
#                 except Exception as e:
#                     logger.warning(f"  ⚠️ Failed to convert {col}: {e}")
        
#         # Handle duplicate strategy
#         dup_strategy = recommendations.get("duplicate_strategy", {})
#         if dup_strategy.get("action") == "drop":
#             cols = dup_strategy.get("columns", df.columns.tolist())
#             initial = len(df)
#             df = df.drop_duplicates(subset=cols)
#             removed = initial - len(df)
#             operations.append(f"Dropped {removed} duplicate rows")
#             logger.info(f"  🗑  Dropped {removed} duplicate rows")
        
#         if operations:
#             self.report["operations"].append({
#                 "step": "ai_recommendations",
#                 "actions": operations
#             })
        
#         return df

    
#     def _ai_analyze_and_clean(self, df: pd.DataFrame) -> pd.DataFrame:
#         """Use Gemini AI to analyze dataset and suggest cleaning strategies (Updated for high-IQ)"""
#         if not self.ai_enabled:
#              logger.info("🤖 AI analysis skipped: GEMINI_API_KEY not set.")
#              return df
             
#         try:
#             if not globals().get('GEMINI_MODEL'):
#                  logger.warning("🤖 AI model not loaded. Skipping analysis.")
#                  return df

#             summary = self._create_dataset_summary(df)
            
#             # Use the new, enhanced prompt
#             prompt = self._enhance_ai_prompt(summary)
            
#             response = globals()['GEMINI_MODEL'].generate_content(prompt)
#             recommendations = self._parse_ai_response(response.text)
            
#             if recommendations:
#                 logger.info("💡 Applying High-IQ AI Recommendations...")
#                 df = self._apply_ai_recommendations(df, recommendations)
#                 self.report["ai_insights"].extend(recommendations.get("insights", []))
        
#         except Exception as e:
#             logger.error(f"⚠️ High-IQ AI analysis failed: {e}")
#             self.report["ai_insights"] = ["High-IQ AI analysis unavailable"]
        
#         return df
    
#     # ... [New/Fixed utility methods start here] ...
    
#     def _typo_and_inconsistency_check(self, df: pd.DataFrame) -> pd.DataFrame:
#         """Advanced rule-based correction for common categorical issues before final cleaning."""
#         typo_fixes = {}
        
#         # 1. Day of Week Fix and Standardization (Case-insensitive)
#         for col in df.columns:
#             if 'day' in col.lower() and (df[col].dtype == 'object' or pd.api.types.is_categorical_dtype(df[col])):
#                 day_mapping = {
#                     'monday': 'Monday', 'mon': 'Monday',
#                     'tuesday': 'Tuesday', 'tue': 'Tuesday',
#                     'wednesday': 'Wednesday', 'wed': 'Wednesday',
#                     'thursday': 'Thursday', 'thu': 'Thursday',
#                     'friday': 'Friday', 'fri': 'Friday',
#                     'saturday': 'Saturday', 'sat': 'Saturday',
#                     'sunday': 'Sunday', 'sun': 'Sunday'
#                 }
                
#                 initial_unique = df[col].astype(str).str.lower().nunique()
#                 # Apply mapping
#                 df.loc[:, col] = df[col].astype(str).str.lower().str.strip().replace(day_mapping)
#                 final_unique = df[col].astype(str).str.lower().nunique()
            
#                 if initial_unique != final_unique:
#                     typo_fixes[col] = f"Standardized {initial_unique - final_unique} unique day names."

#         # 2. General Spelling/Typo Check for Low-Cardinality String Columns (e.g., 'condition')
#         for col in df.columns:
#             if df[col].dtype == 'object' and df[col].nunique() < 50:
#                 data = df[col].astype(str).str.strip().str.lower().replace('nan', np.nan)
#                 data = data.dropna()
                
#                 if data.empty:
#                     continue
                    
#                 value_counts = data.value_counts()
#                 top_values = value_counts.head(min(5, len(value_counts))).index.tolist()
                
#                 corrections = {}
#                 for typo in data.unique():
#                     if typo in corrections or typo in top_values:
#                         continue
                        
#                     for target in top_values:
#                         # Simple check for single character difference (basic spell-check)
#                         if (len(typo) == len(target) and sum(a != b for a, b in zip(typo, target)) == 1) or \
#                            (typo in target and len(target) - len(typo) == 1):
#                             if value_counts.get(target, 0) > 2:
#                                 corrections[typo] = target
#                                 break

#                 if corrections:
#                     # Apply corrections back to the column
#                     df.loc[:, col] = df[col].astype(str).str.lower().str.strip().replace(corrections)
#                     typo_fixes[col] = f"Corrected {len(corrections)} typos against top values."
        
#         if typo_fixes:
#             self.report["operations"].append({
#                 "step": "typo_correction_rule_based",
#                 "fixes": typo_fixes
#             })
#             logger.info(f"  ✅ Applied rule-based typo fixes in {len(typo_fixes)} columns")

#         return df

    
#     def _ai_validate(self, df: pd.DataFrame) -> pd.DataFrame:
#         """Final AI validation of cleaned data"""
#         if not self.ai_enabled:
#              return df
             
#         try:
#             if not globals().get('GEMINI_MODEL'):
#                  return df
                 
#             summary = self._create_dataset_summary(df)
            
#             prompt = f"""Review this cleaned dataset and identify any remaining data quality issues.

# {summary}

# Output ONLY valid JSON:
# {{
#     "quality_score": 85,
#     "remaining_issues": ["issue1"],
#     "suggestions": ["suggestion1"]
# }}"""
            
#             response = globals()['GEMINI_MODEL'].generate_content(prompt)
#             validation = self._parse_ai_response(response.text)
            
#             if validation:
#                 logger.info(f"  📈 Quality Score: {validation.get('quality_score', 'N/A')}")
                
#                 self.report["ai_insights"].append({
#                     "quality_score": validation.get('quality_score'),
#                     "remaining_issues": validation.get("remaining_issues", []),
#                     "suggestions": validation.get("suggestions", [])
#                 })
        
#         except Exception as e:
#             logger.error(f"  ⚠️ AI validation failed: {e}")
        
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
#                 logger.info(f"  ✅ Removed {removed_rows} empty rows")
#             if removed_cols > 0:
#                 logger.info(f"  ✅ Removed {removed_cols} empty columns")
        
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
        
#         # Handle duplicates
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
        
#         logger.info(f"  ✅ Standardized {len(original_cols)} column names")
        
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
#             logger.info(f"  ✅ Removed {duplicates_removed} duplicate rows")
        
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
#                 if len(sample) == 0:
#                     continue
                    
#                 numeric_count = sum(self._is_numeric_string(str(x)) for x in sample)
                
#                 if numeric_count / len(sample) > 0.8:
#                     df.loc[:, col] = pd.to_numeric(df[col], errors='coerce')
#                     type_changes[col] = f"{original_type} → {df[col].dtype}"
#                     continue
                
#                 # Try datetime conversion
#                 try:
#                     parsed = pd.to_datetime(df[col], errors='coerce')
#                     if parsed.notna().sum() / len(df) > 0.5:
#                         df.loc[:, col] = parsed
#                         type_changes[col] = f"{original_type} → datetime64"
#                 except:
#                     pass
        
#         if type_changes:
#             self.report["operations"].append({
#                 "step": "normalize_types",
#                 "type_changes": type_changes
#             })
#             logger.info(f"  ✅ Normalized {len(type_changes)} column types")
        
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
            
#             # Drop columns with >50% missing
#             if missing_pct > 0.5:
#                 df = df.drop(columns=[col])
#                 missing_strategy[col] = "dropped (>50% missing)"
#                 continue
            
#             # Fill numeric with median
#             if pd.api.types.is_numeric_dtype(df[col]):
#                 # Using loc assignment to avoid FutureWarning/SettingWithCopyWarning
#                 df.loc[:, col] = df[col].fillna(df[col].median())
#                 missing_strategy[col] = "filled with median"
            
#             # Forward fill datetime
#             elif pd.api.types.is_datetime64_any_dtype(df[col]):
#                 df.loc[:, col] = df[col].fillna(method='ffill')
#                 missing_strategy[col] = "forward filled"
            
#             # Fill categorical with mode
#             else:
#                 mode_val = df[col].mode()
#                 if len(mode_val) > 0:
#                     df.loc[:, col] = df[col].fillna(mode_val[0])
#                     missing_strategy[col] = "filled with mode"
#                 else:
#                     df.loc[:, col] = df[col].fillna(UNKNOWN_CATEGORY)
#                     missing_strategy[col] = f"filled with '{UNKNOWN_CATEGORY}'"
        
#         if missing_strategy:
#             self.report["operations"].append({
#                 "step": "handle_missing",
#                 "strategy": missing_strategy
#             })
#             logger.info(f"  ✅ Handled missing values in {len(missing_strategy)} columns")
        
#         return df
    
#     def _standardize_formats(self, df: pd.DataFrame) -> pd.DataFrame:
#         """Standardize string and numeric formats"""
#         format_changes = []
        
#         for col in df.columns:
#             if df[col].dtype == 'object':
#                 df.loc[:, col] = df[col].astype(str).str.strip()
                
#                 # Apply title case to name columns
#                 if 'name' in col.lower():
#                     df.loc[:, col] = df[col].str.title()
#                     format_changes.append(f"{col}: applied title case")
            
#             # Round floats to 2 decimals
#             elif pd.api.types.is_float_dtype(df[col]):
#                 df.loc[:, col] = df[col].round(2)
#                 format_changes.append(f"{col}: rounded to 2 decimals")
        
#         if format_changes:
#             self.report["operations"].append({
#                 "step": "standardize_formats",
#                 "changes": format_changes
#             })
#             logger.info(f"  ✅ Standardized formats in {len(format_changes)} columns")
        
#         return df
    
#     def _handle_outliers(self, df: pd.DataFrame) -> pd.DataFrame:
#         """Remove statistical outliers using IQR method (conservative)"""
#         outliers_removed = {}
        
#         for col in df.columns:
#             # FIX: Explicitly skip non-numeric and boolean columns to prevent numpy subtract error on boolean data
#             if not pd.api.types.is_numeric_dtype(df[col]) or pd.api.types.is_bool_dtype(df[col]):
#                 continue
            
#             Q1 = df[col].quantile(0.25)
#             Q3 = df[col].quantile(0.75)
#             IQR = Q3 - Q1
            
#             # Use 3*IQR for conservative outlier removal
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
#             logger.info(f"  ✅ Removed outliers from {len(outliers_removed)} columns")
        
#         return df

#     def _should_scale_column(self, col_name: str, col_data: pd.Series) -> bool:
#         """Determine if a numeric column should be scaled"""
#         # Don't scale ID columns
#         if any(term in col_name.lower() for term in ['id', 'index', 'key']):
#             return False
        
#         # Don't scale if column has very few unique values (likely categorical encoded)
#         if col_data.nunique() < 10:
#             return False
        
#         # Don't scale binary columns
#         unique_vals = col_data.dropna().unique()
#         if len(unique_vals) == 2:
#             return False
        
#         return True

#     def _scale_and_encode(self, df: pd.DataFrame) -> pd.DataFrame:
#         """Apply StandardScaler to appropriate numeric columns and LabelEncoder to categorical"""
#         scaled_cols = []
#         encoded_cols = []
#         self.le_mapping = {}
#         self.ss_mapping = {}

#         df_processed = df.copy()

#         for col in df_processed.columns:
#             # Skip embedding columns
#             if '_embedding_' in col:
#                 continue

#             # Handle numeric columns - SELECTIVE SCALING
#             if pd.api.types.is_numeric_dtype(df_processed[col]):
#                 if df_processed[col].nunique() > 1 and self._should_scale_column(col, df_processed[col]):
#                     scaler = StandardScaler()
#                     # Ensure data is non-null for fit_transform
#                     data = df_processed.loc[df_processed[col].notna(), col].values.reshape(-1, 1)
                    
#                     if len(data) > 0:
#                         df_processed.loc[df_processed[col].notna(), col] = scaler.fit_transform(data)
#                         self.ss_mapping[col] = {
#                             'mean': float(scaler.mean_[0]), 
#                             'scale': float(scaler.scale_[0])
#                         }
#                         scaled_cols.append(col)
                    
            
#             # Handle categorical/string columns
#             elif df_processed[col].dtype == 'object' or pd.api.types.is_categorical_dtype(df_processed[col]):
#                 le = LabelEncoder()
#                 # Ensure Unknown is treated as a category
#                 data = df_processed[col].astype(str).fillna(UNKNOWN_CATEGORY)
#                 df_processed.loc[:, col] = le.fit_transform(data)
#                 self.le_mapping[col] = {'classes': le.classes_.tolist()}
#                 encoded_cols.append(col)
        
#         self.report["operations"].append({
#             "step": "scaling_encoding",
#             "scaled_columns": scaled_cols,
#             "encoded_columns": encoded_cols
#         })
#         logger.info(f"  ✅ Scaled {len(scaled_cols)} columns, Encoded {len(encoded_cols)} columns")
#         return df_processed
    
#     def _embed_text_columns(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
#         """Generate SentenceTransformer embeddings for textual columns"""
#         if not self.embedding_model:
#             return pd.DataFrame(index=df.index), {"embedding_summary": "Embedding skipped (model not loaded)"}

#         text_cols = [col for col in df.columns if df[col].dtype == 'object']
        
#         if not text_cols:
#             return pd.DataFrame(index=df.index), {"embedding_summary": "No text columns found"}
        
#         embedding_summary = {}
#         df_for_concat = pd.DataFrame(index=df.index)

#         for col in text_cols:
#             sentences = df[col].astype(str).fillna('').tolist()
            
#             embeddings = self.embedding_model.encode(
#                 sentences, 
#                 show_progress_bar=False, 
#                 convert_to_numpy=True,
#                 batch_size=32
#             )
            
#             embedding_col_names = [f"{col}_embedding_{i}" for i in range(self.embedding_dim)]
#             embedding_df = pd.DataFrame(embeddings, columns=embedding_col_names, index=df.index)
#             df_for_concat = pd.concat([df_for_concat, embedding_df], axis=1)
            
#             embedding_summary[col] = {
#                 "vector_size": self.embedding_dim,
#                 "new_columns": embedding_col_names
#             }
        
#         self.report["operations"].append({
#             "step": "text_embedding",
#             "embedded_columns": list(embedding_summary.keys())
#         })
#         logger.info(f"  ✅ Embedded {len(text_cols)} text columns")

#         return df_for_concat, {"embedding_summary": embedding_summary}


#     def clean(self, df: pd.DataFrame, ml_mode: bool) -> Tuple[pd.DataFrame, pd.DataFrame, Dict[str, Any]]:
#         """
#         Main cleaning pipeline.
#         Returns: (df_final_processed, df_final_text, final_report)
#         """
#         logger.info("="*80)
#         logger.info(f"🚀 STARTING DATA CLEANING PIPELINE (ML_MODE={ml_mode})")
#         logger.info("="*80)
        
#         self.report = {
#             "original_shape": df.shape,
#             "operations": [],
#             "ai_insights": [],
#             "categorical_encoding_order": {} # Initialize new key for AI encoding
#         }
        
#         df_cleaned = df.copy()
        
#         logger.info(f"\n📊 Original Dataset: {df.shape[0]} rows × {df.shape[1]} columns")
        
#         # --- Stage 1: Basic Cleaning and Human-Readable Imputation (Common to both modes) ---
#         if self.ai_enabled:
#             logger.info("\n🤖 Running High-IQ AI Analysis...")
#             df_cleaned = self._ai_analyze_and_clean(df_cleaned)
        
#         logger.info("\n🧹 Removing empty rows/columns...")
#         df_cleaned = self._remove_empty(df_cleaned)
#         logger.info("📝 Standardizing column names...")
#         df_cleaned = self._standardize_columns(df_cleaned)
#         logger.info("🔍 Checking for duplicates...")
#         df_cleaned = self._remove_duplicates(df_cleaned)
#         logger.info("🔧 Normalizing data types...")
#         df_cleaned = self._normalize_types(df_cleaned)
#         logger.info("📌 Handling missing values...")
#         df_cleaned = self._handle_missing(df_cleaned)
        
#         # NEW STEP: Rule-based typo correction
#         logger.info("✍️ Applying Rule-Based Typo Correction...")
#         df_cleaned = self._typo_and_inconsistency_check(df_cleaned)
        
#         logger.info("✨ Standardizing formats...")
#         df_cleaned = self._standardize_formats(df_cleaned)
#         logger.info("📊 Detecting outliers...")
#         df_cleaned = self._handle_outliers(df_cleaned)
        
#         # Save the clean text version for Human-Readable output
#         df_final_text = df_cleaned.copy()
        
#         # --- Stage 2: ML Transformation (if enabled) ---
#         if ml_mode:
#             logger.info("\n🧠 Running ML Mode Transformations...")
            
#             # Retrieve AI-determined chronological encoding
#             encoding_order = self.report.get('categorical_encoding_order', {})
            
#             # Apply chronological encoding for ML-Ready output (CRITICAL FIX)
#             for col, mapping in encoding_order.items():
#                 if col in df_cleaned.columns:
#                     # Coerce mapping keys to string for reliable replacement against object columns
#                     mapping_str = {str(k).lower(): v for k, v in mapping.items()}
                    
#                     logger.info(f"🧠 Applying AI Chronological Encoding for '{col}' using map: {mapping_str}")
                    
#                     # Apply the encoding map to a lowercased copy of the column
#                     # Fill any non-mapped values with the sentinel value -1
#                     encoded_series = df_cleaned[col].astype(str).str.lower().replace(mapping_str)
                    
#                     # Insert the encoded data back into df_cleaned and convert to numeric
#                     df_cleaned.loc[:, col] = pd.to_numeric(encoded_series, errors='coerce').fillna(CHRONO_ENCODING_FILL_VALUE)
            
#             # Now proceed with the ML pipeline (which mostly ignores columns that are already numeric, including our new chronological columns)
#             text_cols = [col for col in df_cleaned.columns if df_cleaned[col].dtype == 'object']
#             non_text_cols = [col for col in df_cleaned.columns if col not in text_cols]
            
#             # Embed text columns
#             df_embeddings, embedding_report = self._embed_text_columns(df_cleaned[text_cols])
            
#             # Scale and encode non-text columns (this applies scaling/default LabelEncoder to any remaining unencoded categorical columns)
#             df_scaled_encoded = self._scale_and_encode(df_cleaned[non_text_cols])
            
#             # Combine
#             df_final = pd.concat([
#                 df_scaled_encoded.reset_index(drop=True), 
#                 df_embeddings.reset_index(drop=True)
#             ], axis=1)
            
#         else:
#             # Simple mode: Just encode categorical columns (retains human-readable structure by not scaling/embedding)
#             logger.info("\n🧠 Running Simple Encoding (LabelEncoder) for categorical data...")
#             df_final = self._scale_and_encode(df_final_text.copy())
#             embedding_report = {"embedding_summary": "Embedding skipped (Simple mode)"}
        
#         # --- Stage 3: Finalization ---
#         if self.ai_enabled:
#             logger.info("\n🎯 Running AI Validation...")
#             df_final = self._ai_validate(df_final)
        
#         self.report["final_shape"] = df_final.shape
#         self.report["rows_original"] = df.shape[0]
#         self.report["rows_cleaned"] = df_final.shape[0]
#         self.report["columns_original"] = df.shape[1]
#         self.report["columns_final"] = df_final.shape[1]
        
#         final_report = {
#             "cleaning_operations": self.report,
#             "preprocessing_details": {
#                 "scaling_maps": self.ss_mapping,
#                 "encoding_maps": self.le_mapping,
#                 **embedding_report
#             }
#         }
        
#         logger.info("="*80)
#         logger.info("✅ CLEANING COMPLETE")
#         logger.info(f"📊 Final Dataset: {df_final.shape[0]} rows × {df_final.shape[1]} columns")
#         logger.info("="*80 + "\n")
        
#         return df_final, df_final_text, final_report



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
from difflib import SequenceMatcher # Used for semantic typo checking

load_dotenv()
logger = logging.getLogger(__name__)
# Setting log level to INFO by default. Use logging.DEBUG for "20k line" verbose output.
logging.basicConfig(level=logging.INFO) 

# --- Sentinel Values ---
CHRONO_ENCODING_FILL_VALUE = -1
UNKNOWN_CATEGORY = 'Unknown_Category_Keginator'

# --- SentenceTransformer Configuration ---
EMBEDDING_MODEL = None
EMBEDDING_DIM = 0
try:
    EMBEDDING_MODEL = SentenceTransformer('all-MiniLM-L6-v2', device='cpu') 
    EMBEDDING_DIM = 384
    logger.info("✅ SentenceTransformer (all-MiniLM-L6-v2) loaded.")
except Exception as e:
    logger.error(f"⚠️ Failed to load SentenceTransformer: {e}. Text embedding disabled.")


# --- Gemini Configuration ---
AI_ENABLED = False
try:
    import google.generativeai as genai
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        # HIGH-IQ FIX: Using powerful experimental model as requested
        GEMINI_MODEL = genai.GenerativeModel('gemini-2.5-flash-exp')
        genai.configure(api_key=api_key)
        AI_ENABLED = True
        logger.info("✅ Gemini AI enabled (gemini-2.5-flash-exp).")
    else:
        logger.warning("⚠️ GEMINI_API_KEY not set. Using rule-based cleaning only.")
except Exception as e:
    logger.error(f"⚠️ Failed to initialize Gemini: {e}")


class DataCleaner:
    """
    ULTRA-INTELLIGENT AI-Powered data cleaning engine (Keginator Genius Core).
    Handles semantic and chronological consistency, normalization, encoding, and ML pre-processing.
    """
    
    def __init__(self):
        self.report = {}
        self.ai_enabled = AI_ENABLED
        self.embedding_model = EMBEDDING_MODEL
        self.embedding_dim = EMBEDDING_DIM
        self.le_mapping = {}
        self.ss_mapping = {}

    
    def _create_dataset_summary(self, df: pd.DataFrame) -> str:
        """Generates a detailed summary for the High-IQ AI."""
        summary_parts = []
        summary_parts.append(f"Shape: {df.shape[0]} rows × {df.shape[1]} columns")
        summary_parts.append(f"\nColumns: {', '.join(df.columns.tolist()[:10])}")
        summary_parts.append(f"\nData Types:\n{df.dtypes.to_string()}")
        
        # Missing values with percentage
        missing = df.isnull().sum()
        if missing.any():
            missing_data = missing[missing > 0].reset_index()
            missing_data.columns = ['Column', 'Count']
            missing_data['Percent'] = (missing_data['Count'] / len(df) * 100).round(2)
            
            missing_str = "Missing Values (Count / Percent):\n"
            for _, row in missing_data.iterrows():
                missing_str += f"  - {row['Column']}: {row['Count']} ({row['Percent']}%)"
                if row['Percent'] > 70.0:
                    missing_str += " [SUGGEST DROP]"
                missing_str += "\n"
            summary_parts.append(f"\n{missing_str.strip()}")
            
        # Unique/Typo Sample (for categorical data)
        typo_sample_str = "\nCategorical/Typo Sample (Top 5 values and their counts):\n"
        has_categorical = False
        for col in df.columns:
            if df[col].dtype == 'object' or pd.api.types.is_categorical_dtype(df[col]):
                value_counts = df[col].astype(str).str.lower().value_counts().head(5)
                if not value_counts.empty:
                    typo_sample_str += f"  - {col}:\n"
                    for val, count in value_counts.items():
                        typo_sample_str += f"    * '{val}': {count}\n"
                    has_categorical = True
                    
        if has_categorical:
            summary_parts.append(typo_sample_str.strip())
            
        return "\n".join(summary_parts)

    def _parse_ai_response(self, response_text: str) -> Dict[str, Any]:
        """Parse AI response and extract JSON recommendations"""
        try:
            response_text = re.sub(r'```json\s*', '', response_text)
            response_text = re.sub(r'```\s*', '', response_text)
            recommendations = json.loads(response_text)
            return recommendations
        except Exception as e:
            logger.error(f"⚠️ Failed to parse AI recommendations: {e}. Raw response: {response_text[:200]}")
            return {}
        
    def _enhance_ai_prompt(self, summary: str) -> str:
        """Generates the advanced prompt for Gemini (The Data Genius)"""
        prompt = f"""You are a **Billion-Dollar High-IQ Data Genius AI** designed to perform the most comprehensive and intelligent data cleaning and pre-processing known to man. Your analysis must be deeper than simple rules, focusing on **semantic, contextual, and chronological consistency**.

**Analyze the provided Dataset Summary:**
{summary}

**Pay EXTREME attention to the following semantic/contextual data quality issues and suggest fixes:**
1.  **Chronological/Ordinal Encoding (CRITICAL FIX):** For columns containing ordered sequences like 'day', 'month', 'size', or any data with a logical/ordered sequence, identify the correct chronological order and provide an **EXACT** mapping to numerical ranks (starting from 1). This is vital for time-series ML models. If no order is found, return an empty dictionary for the column.
2.  **Typographical Inconsistencies/Misspellings (High-Confidence Fixes):** Suggest replacements (`value_replacements`) for clear typos and bad data entries (e.g., 'Suny' -> 'Sunny', 'Rin' -> 'Rain', 'Sunnny' -> 'Sunny', 'abc' -> NaN).
3.  **Contextual Imputation:** For missing values, suggest imputation methods. For the sample data provided, impute missing non-numeric cells with the most likely correct value (e.g., the Mode of the column).

**Output ONLY valid JSON (no markdown). The JSON keys must be precise.**

**Output JSON Keys to Include:**
* `column_types`: Recommended final data type.
* `columns_to_drop`: Irrelevant/mostly empty columns to drop.
* `value_replacements`: Typo corrections/value replacements.
* `duplicate_strategy`: Action for duplicates.
* `categorical_encoding_order`: **CRITICAL KEY!** A dictionary where the key is the column name and the value is a `{{value: numerical_rank}}` mapping for chronological/logical encoding.
* `insights`: Your key findings and genius-level observations.

**Required Output JSON Format (must be ONLY JSON):**
{{
    "column_types": {{"column_name": "recommended_type"}},
    "columns_to_drop": ["column1"],
    "value_replacements": {{"column_name": {{"old_value": "new_value"}}}},
    "duplicate_strategy": {{"columns": [], "action": "drop"}},
    "categorical_encoding_order": {{"day": {{"Monday": 1, "Tuesday": 2, "Wednesday": 3, "Thursday": 4, "Friday": 5, "Saturday": 6, "Sunday": 7}}}},
    "insights": ["insight1"]
}}"""
        return prompt


    def _apply_ai_recommendations(self, df: pd.DataFrame, recommendations: Dict[str, Any]) -> pd.DataFrame:
        """Apply AI-generated cleaning recommendations and log changes"""
        operations = []
        
        self.report['categorical_encoding_order'] = recommendations.get("categorical_encoding_order", {})
        
        # Drop recommended columns
        columns_to_drop = recommendations.get("columns_to_drop", [])
        if columns_to_drop:
            existing_cols = [col for col in columns_to_drop if col in df.columns]
            if existing_cols:
                df = df.drop(columns=existing_cols)
                operations.append(f"Dropped columns: {', '.join(existing_cols)}")
                logger.info(f"  ✅ Dropped columns: {', '.join(existing_cols)}")
        
        # Apply value replacements (AI-suggested typos, etc.)
        replacements = recommendations.get("value_replacements", {})
        for col, replace_map in replacements.items():
            if col in df.columns:
                # Need to use .loc[:, col] and cast to str for consistent replacement of mixed types/typos
                df.loc[:, col] = df[col].astype(str).replace(replace_map)
                operations.append(f"Replaced values in {col}")
                logger.info(f"  🔄 Replaced values in '{col}'")
        
        # Apply recommended type conversions
        column_types = recommendations.get("column_types", {})
        for col, dtype in column_types.items():
            if col in df.columns:
                try:
                    if dtype == "numeric":
                        df.loc[:, col] = pd.to_numeric(df[col], errors='coerce')
                    elif dtype == "datetime":
                        df.loc[:, col] = pd.to_datetime(df[col], errors='coerce')
                    elif dtype == "string":
                        df.loc[:, col] = df[col].astype(str)
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
            operations.append(f"Dropped {removed} duplicate rows")
            logger.info(f"  🗑  Dropped {removed} duplicate rows")
        
        if operations:
            self.report["operations"].append({
                "step": "ai_recommendations",
                "actions": operations
            })
        
        return df

    
    def _ai_analyze_and_clean(self, df: pd.DataFrame) -> pd.DataFrame:
        """Use Gemini AI to analyze dataset and suggest cleaning strategies (High-IQ)"""
        if not self.ai_enabled:
             logger.info("🤖 AI analysis skipped: GEMINI_API_KEY not set.")
             return df
             
        try:
            if not globals().get('GEMINI_MODEL'):
                 logger.warning("🤖 AI model not loaded. Skipping analysis.")
                 return df

            summary = self._create_dataset_summary(df)
            
            prompt = self._enhance_ai_prompt(summary)
            
            response = globals()['GEMINI_MODEL'].generate_content(prompt)
            recommendations = self._parse_ai_response(response.text)
            
            if recommendations:
                logger.info("💡 Applying High-IQ AI Recommendations...")
                df = self._apply_ai_recommendations(df, recommendations)
                self.report["ai_insights"].extend(recommendations.get("insights", []))
        
        except Exception as e:
            logger.error(f"⚠️ High-IQ AI analysis failed: {e}")
            self.report["ai_insights"] = ["High-IQ AI analysis unavailable"]
        
        return df

    def _fuzzy_typo_correction(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        [SEMANTIC] Rule-based fuzzy correction for typos using SequenceMatcher.
        This fixes issues like 'Suny' -> 'Sunny' when the AI misses it.
        """
        typo_fixes = {}
        
        for col in df.columns:
            if df[col].dtype != 'object' or df[col].nunique() > 50:
                continue
            
            data = df[col].astype(str).str.strip().str.lower()
            unique_values = data.dropna().unique()
            
            if len(unique_values) < 2:
                continue
            
            value_counts = data.value_counts()
            top_values = value_counts.head(min(5, len(value_counts))).index.tolist()
            
            corrections = {}
            for typo in unique_values:
                if typo in top_values:
                    continue
                
                best_match = None
                best_ratio = 0.0
                
                for target in top_values:
                    ratio = SequenceMatcher(None, typo, target).ratio()
                    
                    # Heuristic: Match if ratio is very high (> 85%) and target is significantly more frequent
                    if ratio > 0.85 and value_counts.get(target, 0) > 2 * value_counts.get(typo, 0):
                        if ratio > best_ratio:
                            best_ratio = ratio
                            best_match = target
                
                if best_match:
                    corrections[typo] = best_match

            if corrections:
                # Apply corrections back to the column (handling case sensitivity by replacing on lowercased values)
                typo_series = df[col].astype(str).str.strip().str.lower().replace(corrections)
                
                # We use the corrected string values for the clean output, keeping the original case of the target
                # This is complex, so we rely on the clean output having standardized case/title case later.
                df.loc[:, col] = typo_series
                
                typo_fixes[col] = f"Corrected {len(corrections)} typos (e.g., '{list(corrections.keys())[0]}'->'{list(corrections.values())[0]}')."
        
        if typo_fixes:
            self.report["operations"].append({
                "step": "semantic_typo_correction",
                "fixes": typo_fixes
            })
            logger.info(f"  ✅ Applied semantic typo fixes in {len(typo_fixes)} columns")

        return df

    
    def _ai_validate(self, df: pd.DataFrame) -> pd.DataFrame:
        """Final AI validation of cleaned data"""
        if not self.ai_enabled:
             return df
             
        try:
            if not globals().get('GEMINI_MODEL'):
                 return df
                 
            summary = self._create_dataset_summary(df)
            
            prompt = f"""Review this cleaned dataset and identify any remaining data quality issues.

{summary}

Output ONLY valid JSON:
{{
    "quality_score": 85,
    "remaining_issues": ["issue1"],
    "suggestions": ["suggestion1"]
}}"""
            
            response = globals()['GEMINI_MODEL'].generate_content(prompt)
            validation = self._parse_ai_response(response.text)
            
            if validation:
                logger.info(f"  📈 Quality Score: {validation.get('quality_score', 'N/A')}")
                
                self.report["ai_insights"].append({
                    "quality_score": validation.get('quality_score'),
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
        
        # Handle duplicates
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
                if len(sample) == 0:
                    continue
                    
                numeric_count = sum(self._is_numeric_string(str(x)) for x in sample)
                
                if numeric_count / len(sample) > 0.8:
                    df.loc[:, col] = pd.to_numeric(df[col], errors='coerce')
                    type_changes[col] = f"{original_type} → {df[col].dtype}"
                    continue
                
                # Try datetime conversion
                try:
                    parsed = pd.to_datetime(df[col], errors='coerce')
                    if parsed.notna().sum() / len(df) > 0.5:
                        df.loc[:, col] = parsed
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
            
            # Drop columns with >50% missing
            if missing_pct > 0.5:
                df = df.drop(columns=[col])
                missing_strategy[col] = "dropped (>50% missing)"
                continue
            
            # Fill numeric with median
            if pd.api.types.is_numeric_dtype(df[col]):
                df.loc[:, col] = df[col].fillna(df[col].median())
                missing_strategy[col] = "filled with median"
            
            # Forward fill datetime
            elif pd.api.types.is_datetime64_any_dtype(df[col]):
                df.loc[:, col] = df[col].fillna(method='ffill')
                missing_strategy[col] = "forward filled"
            
            # Fill categorical with mode
            else:
                mode_val = df[col].mode()
                if len(mode_val) > 0:
                    df.loc[:, col] = df[col].fillna(mode_val[0])
                    missing_strategy[col] = "filled with mode"
                else:
                    df.loc[:, col] = df[col].fillna(UNKNOWN_CATEGORY)
                    missing_strategy[col] = f"filled with '{UNKNOWN_CATEGORY}'"
        
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
                df.loc[:, col] = df[col].astype(str).str.strip()
                
                # Apply title case to name columns
                if 'name' in col.lower():
                    df.loc[:, col] = df[col].str.title()
                    format_changes.append(f"{col}: applied title case")
            
            # Round floats to 2 decimals
            elif pd.api.types.is_float_dtype(df[col]):
                df.loc[:, col] = df[col].round(2)
                format_changes.append(f"{col}: rounded to 2 decimals")
        
        if format_changes:
            self.report["operations"].append({
                "step": "standardize_formats",
                "changes": format_changes
            })
            logger.info(f"  ✅ Standardized formats in {len(format_changes)} columns")
        
        return df
    
    def _handle_outliers(self, df: pd.DataFrame) -> pd.DataFrame:
        """Remove statistical outliers using IQR method (conservative)"""
        outliers_removed = {}
        
        for col in df.columns:
            # FIX: Explicitly skip non-numeric and boolean columns to prevent numpy subtract error on boolean data
            if not pd.api.types.is_numeric_dtype(df[col]) or pd.api.types.is_bool_dtype(df[col]):
                continue
            
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            
            # Use 3*IQR for conservative outlier removal
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

    def _should_scale_column(self, col_name: str, col_data: pd.Series) -> bool:
        """Determine if a numeric column should be scaled"""
        if any(term in col_name.lower() for term in ['id', 'index', 'key']):
            return False
        if col_data.nunique() < 10:
            return False
        unique_vals = col_data.dropna().unique()
        if len(unique_vals) == 2:
            return False
        
        return True

    def _scale_and_encode(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply StandardScaler to appropriate numeric columns and LabelEncoder to categorical"""
        scaled_cols = []
        encoded_cols = []
        self.le_mapping = {}
        self.ss_mapping = {}

        df_processed = df.copy()

        for col in df_processed.columns:
            if '_embedding_' in col:
                continue

            # Handle numeric columns - SELECTIVE SCALING
            if pd.api.types.is_numeric_dtype(df_processed[col]):
                if df_processed[col].nunique() > 1 and self._should_scale_column(col, df_processed[col]):
                    scaler = StandardScaler()
                    # Ensure data is non-null for fit_transform
                    data = df_processed.loc[df_processed[col].notna(), col].values.reshape(-1, 1)
                    
                    if len(data) > 0:
                        df_processed.loc[df_processed[col].notna(), col] = scaler.fit_transform(data)
                        self.ss_mapping[col] = {
                            'mean': float(scaler.mean_[0]), 
                            'scale': float(scaler.scale_[0])
                        }
                        scaled_cols.append(col)
            
            # Handle categorical/string columns (for default Label Encoding)
            elif df_processed[col].dtype == 'object' or pd.api.types.is_categorical_dtype(df_processed[col]):
                le = LabelEncoder()
                data = df_processed[col].astype(str).fillna(UNKNOWN_CATEGORY)
                df_processed.loc[:, col] = le.fit_transform(data)
                self.le_mapping[col] = {'classes': le.classes_.tolist()}
                encoded_cols.append(col)
        
        self.report["operations"].append({
            "step": "scaling_encoding",
            "scaled_columns": scaled_cols,
            "encoded_columns": encoded_cols
        })
        logger.info(f"  ✅ Scaled {len(scaled_cols)} columns, Encoded {len(encoded_cols)} columns")
        return df_processed
    
    def _embed_text_columns(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Generate SentenceTransformer embeddings for textual columns"""
        if not self.embedding_model:
            return pd.DataFrame(index=df.index), {"embedding_summary": "Embedding skipped (model not loaded)"}

        text_cols = [col for col in df.columns if df[col].dtype == 'object']
        
        if not text_cols:
            return pd.DataFrame(index=df.index), {"embedding_summary": "No text columns found"}
        
        embedding_summary = {}
        df_for_concat = pd.DataFrame(index=df.index)

        for col in text_cols:
            sentences = df[col].astype(str).fillna('').tolist()
            
            embeddings = self.embedding_model.encode(
                sentences, 
                show_progress_bar=False, 
                convert_to_numpy=True,
                batch_size=32
            )
            
            embedding_col_names = [f"{col}_embedding_{i}" for i in range(self.embedding_dim)]
            embedding_df = pd.DataFrame(embeddings, columns=embedding_col_names, index=df.index)
            df_for_concat = pd.concat([df_for_concat, embedding_df], axis=1)
            
            embedding_summary[col] = {
                "vector_size": self.embedding_dim,
                "new_columns": embedding_col_names
            }
        
        self.report["operations"].append({
            "step": "text_embedding",
            "embedded_columns": list(embedding_summary.keys())
        })
        logger.info(f"  ✅ Embedded {len(text_cols)} text columns")

        return df_for_concat, {"embedding_summary": embedding_summary}


    def clean(self, df: pd.DataFrame, ml_mode: bool) -> Tuple[pd.DataFrame, pd.DataFrame, Dict[str, Any]]:
        """
        Main cleaning pipeline.
        Returns: (df_final_processed, df_final_text, final_report)
        """
        logger.info("="*80)
        logger.info(f"🚀 STARTING DATA CLEANING PIPELINE (ML_MODE={ml_mode})")
        logger.info("="*80)
        
        self.report = {
            "original_shape": df.shape,
            "operations": [],
            "ai_insights": [],
            "categorical_encoding_order": {} # Initialize new key for AI encoding
        }
        
        df_cleaned = df.copy()
        
        logger.info(f"\n📊 Original Dataset: {df.shape[0]} rows × {df.shape[1]} columns")
        
        # --- Stage 1: Basic Cleaning and Human-Readable Imputation (Common to both modes) ---
        if self.ai_enabled:
            logger.info("\n🤖 Running High-IQ AI Analysis...")
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
        
        # NEW SEMANTIC STEP: Fuzzy typo correction
        logger.info("✍️ Applying Semantic/Fuzzy Typo Correction...")
        df_cleaned = self._fuzzy_typo_correction(df_cleaned)
        
        logger.info("✨ Standardizing formats...")
        df_cleaned = self._standardize_formats(df_cleaned)
        logger.info("📊 Detecting outliers...")
        df_cleaned = self._handle_outliers(df_cleaned)
        
        # Save the clean text version for Human-Readable output
        df_final_text = df_cleaned.copy()
        
        # --- Stage 2: ML Transformation (if enabled) ---
        if ml_mode:
            logger.info("\n🧠 Running ML Mode Transformations...")
            
            # Retrieve AI-determined chronological encoding
            encoding_order = self.report.get('categorical_encoding_order', {})
            
            # Apply chronological encoding for ML-Ready output (CRITICAL FIX for chronological data)
            for col, mapping in encoding_order.items():
                if col in df_cleaned.columns:
                    # Coerce mapping keys to string (lowercased for flexibility)
                    mapping_str = {str(k).lower(): v for k, v in mapping.items()}
                    
                    logger.info(f"🧠 Applying AI Chronological Encoding for '{col}' using map: {mapping_str}")
                    
                    # Apply the encoding map to a lowercased copy of the column
                    encoded_series = df_cleaned[col].astype(str).str.lower().replace(mapping_str)
                    
                    # Insert the encoded data back into df_cleaned and convert to numeric
                    df_cleaned.loc[:, col] = pd.to_numeric(encoded_series, errors='coerce').fillna(CHRONO_ENCODING_FILL_VALUE) 
            
            # Now proceed with the ML pipeline on the (partially encoded) df_cleaned
            text_cols = [col for col in df_cleaned.columns if df_cleaned[col].dtype == 'object']
            non_text_cols = [col for col in df_cleaned.columns if col not in text_cols]
            
            # Embed text columns
            df_embeddings, embedding_report = self._embed_text_columns(df_cleaned[text_cols])
            
            # Scale and encode non-text columns (this applies scaling/default LabelEncoder to any remaining unencoded categorical columns)
            df_scaled_encoded = self._scale_and_encode(df_cleaned[non_text_cols])
            
            # Combine
            df_final = pd.concat([
                df_scaled_encoded.reset_index(drop=True), 
                df_embeddings.reset_index(drop=True)
            ], axis=1)
            
        else:
            # Simple mode: Just encode categorical columns
            logger.info("\n🧠 Running Simple Encoding (LabelEncoder) for categorical data...")
            df_final = self._scale_and_encode(df_final_text.copy())
            embedding_report = {"embedding_summary": "Embedding skipped (Simple mode)"}
        
        # --- Stage 3: Finalization ---
        if self.ai_enabled:
            logger.info("\n🎯 Running AI Validation...")
            df_final = self._ai_validate(df_final)
        
        self.report["final_shape"] = df_final.shape
        self.report["rows_original"] = df.shape[0]
        self.report["rows_cleaned"] = df_final.shape[0]
        self.report["columns_original"] = df.shape[1]
        self.report["columns_final"] = df_final.shape[1]
        
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
        
        return df_final, df_final_text, final_report