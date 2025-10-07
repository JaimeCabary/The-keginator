import pandas as pd
import numpy as np
from typing import Tuple, Dict, Any
from datetime import datetime
import re


class DataCleaner:
    """
    High-performance data cleaning engine
    Handles missing values, duplicates, type normalization, and formatting
    """
    
    def __init__(self):
        self.report = {}
    
    def clean(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Main cleaning pipeline
        Returns: (cleaned_df, cleaning_report)
        """
        self.report = {
            "original_shape": df.shape,
            "operations": []
        }
        
        df_cleaned = df.copy()
        
        # 1. Remove completely empty rows/columns
        df_cleaned = self._remove_empty(df_cleaned)
        
        # 2. Standardize column names
        df_cleaned = self._standardize_columns(df_cleaned)
        
        # 3. Handle duplicates
        df_cleaned = self._remove_duplicates(df_cleaned)
        
        # 4. Infer and normalize data types
        df_cleaned = self._normalize_types(df_cleaned)
        
        # 5. Handle missing values
        df_cleaned = self._handle_missing(df_cleaned)
        
        # 6. Standardize formats (dates, strings, numbers)
        df_cleaned = self._standardize_formats(df_cleaned)
        
        # 7. Remove outliers (optional, conservative approach)
        df_cleaned = self._handle_outliers(df_cleaned)
        
        self.report["final_shape"] = df_cleaned.shape
        self.report["rows_removed"] = df.shape[0] - df_cleaned.shape[0]
        self.report["columns_removed"] = df.shape[1] - df_cleaned.shape[1]
        
        return df_cleaned, self.report
    
    def _remove_empty(self, df: pd.DataFrame) -> pd.DataFrame:
        """Remove completely empty rows and columns"""
        initial_shape = df.shape
        
        # Remove empty rows
        df = df.dropna(how='all')
        
        # Remove empty columns
        df = df.dropna(axis=1, how='all')
        
        removed_rows = initial_shape[0] - df.shape[0]
        removed_cols = initial_shape[1] - df.shape[1]
        
        if removed_rows > 0 or removed_cols > 0:
            self.report["operations"].append({
                "step": "remove_empty",
                "rows_removed": removed_rows,
                "columns_removed": removed_cols
            })
        
        return df
    
    def _standardize_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Standardize column names: lowercase, underscores, no special chars"""
        original_cols = df.columns.tolist()
        
        new_cols = []
        for col in df.columns:
            # Convert to string, lowercase
            col_clean = str(col).lower().strip()
            
            # Replace spaces and special chars with underscore
            col_clean = re.sub(r'[^\w\s]', '', col_clean)
            col_clean = re.sub(r'\s+', '_', col_clean)
            
            # Remove multiple underscores
            col_clean = re.sub(r'_+', '_', col_clean)
            col_clean = col_clean.strip('_')
            
            new_cols.append(col_clean)
        
        # Handle duplicate column names
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
        
        return df
    
    def _normalize_types(self, df: pd.DataFrame) -> pd.DataFrame:
        """Infer and normalize column data types"""
        type_changes = {}
        
        for col in df.columns:
            original_type = str(df[col].dtype)
            
            # Skip if already numeric
            if pd.api.types.is_numeric_dtype(df[col]):
                continue
            
            # Try converting to numeric
            if df[col].dtype == 'object':
                # Check if it looks like a number
                sample = df[col].dropna().head(100)
                numeric_count = sum(self._is_numeric_string(str(x)) for x in sample)
                
                if numeric_count / len(sample) > 0.8:  # 80% threshold
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                    type_changes[col] = f"{original_type} -> {df[col].dtype}"
                    continue
                
                # Try converting to datetime
                try:
                    parsed = pd.to_datetime(df[col], errors='coerce')
                    if parsed.notna().sum() / len(df) > 0.5:  # 50% threshold
                        df[col] = parsed
                        type_changes[col] = f"{original_type} -> datetime64"
                except:
                    pass
        
        if type_changes:
            self.report["operations"].append({
                "step": "normalize_types",
                "type_changes": type_changes
            })
        
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
            
            # Drop column if >50% missing
            if missing_pct > 0.5:
                df = df.drop(columns=[col])
                missing_strategy[col] = "dropped (>50% missing)"
                continue
            
            # Numeric columns: fill with median
            if pd.api.types.is_numeric_dtype(df[col]):
                df[col].fillna(df[col].median(), inplace=True)
                missing_strategy[col] = "filled with median"
            
            # Datetime columns: forward fill
            elif pd.api.types.is_datetime64_any_dtype(df[col]):
                df[col].fillna(method='ffill', inplace=True)
                missing_strategy[col] = "forward filled"
            
            # Categorical/string columns: fill with mode or 'Unknown'
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
        
        return df
    
    def _standardize_formats(self, df: pd.DataFrame) -> pd.DataFrame:
        """Standardize string and numeric formats"""
        format_changes = []
        
        for col in df.columns:
            # String columns: trim whitespace, title case for names
            if df[col].dtype == 'object':
                df[col] = df[col].astype(str).str.strip()
                
                # If column looks like a name (contains 'name' in column)
                if 'name' in col.lower():
                    df[col] = df[col].str.title()
                    format_changes.append(f"{col}: applied title case")
            
            # Numeric columns: round floats to 2 decimals
            elif pd.api.types.is_float_dtype(df[col]):
                df[col] = df[col].round(2)
                format_changes.append(f"{col}: rounded to 2 decimals")
        
        if format_changes:
            self.report["operations"].append({
                "step": "standardize_formats",
                "changes": format_changes
            })
        
        return df
    
    def _handle_outliers(self, df: pd.DataFrame) -> pd.DataFrame:
        """Remove statistical outliers (conservative IQR method)"""
        outliers_removed = {}
        
        for col in df.columns:
            if not pd.api.types.is_numeric_dtype(df[col]):
                continue
            
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            
            # Conservative bounds (3 * IQR instead of 1.5)
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
        
        return df