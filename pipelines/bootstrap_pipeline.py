"""
Bootstrap Pipeline - Data Anonymization
Implements pseudonymization and PrivBayes for privacy protection
"""

import pandas as pd
from pathlib import Path
import hashlib
import sys

sys.path.append(str(Path(__file__).parent.parent))

from src.security.anonymization.privbayes import PrivBayes
from src.data.pseudonym_manager import PseudonymManager

class BootstrapPipeline:
    def __init__(self, config_path='configs/security_config.yaml', use_privbayes=True):
        self.config_path = config_path
        self.use_privbayes = use_privbayes
        self.pseudonym_manager = PseudonymManager()
        if use_privbayes:
            self.privbayes = PrivBayes(epsilon=0.1)
        print("Bootstrap Pipeline Initialized")

    def pseudonymize(self, data, column):
        """Pseudonymize sensitive columns with mapping storage"""
        return data[column].apply(
            lambda x: self.pseudonym_manager.create_pseudonym(x, column)
        )

    def anonymize_dataset(self, input_path, output_path):
        """Anonymize dataset using pseudonymization and PrivBayes"""
        print(f"Loading data from {input_path}...")
        df = pd.read_csv(input_path)
        print(f"Original dataset shape: {df.shape}")
        
        # Step 1: Pseudonymize highly sensitive columns
        sensitive_cols = ['name', 'email', 'ssn', 'phone']
        existing_cols = [col for col in sensitive_cols if col in df.columns]
        
        for col in existing_cols:
            df[f'{col}_pseudo'] = self.pseudonymize(df, col)
            df.drop(col, axis=1, inplace=True)
        
        # Step 2: Apply PrivBayes to numeric columns
        if self.use_privbayes:
            numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
            if numeric_cols:
                print(f"Applying PrivBayes to: {numeric_cols}")
                df = self.privbayes.anonymize_dataframe(df, numeric_cols)
        
        # Save anonymized data
        df.to_csv(output_path, index=False)
        print(f"Anonymized data saved to {output_path}")
        print(f"Pseudonym mappings stored: {self.pseudonym_manager.get_mapping_count()}")
        return df

if __name__ == "__main__":
    pipeline = BootstrapPipeline()
    print("Bootstrap Pipeline Ready!")
