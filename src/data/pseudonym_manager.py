"""
Pseudonym Manager
Manages mapping between original and pseudonymized data
Simulates HIVE data warehouse functionality
"""

import pandas as pd
import hashlib
import json
from pathlib import Path

class PseudonymManager:
    def __init__(self, storage_path='data/hive/pseudonym_mappings'):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.mapping_file = self.storage_path / 'mappings.json'
        self.mappings = self._load_mappings()
        print("Pseudonym Manager Initialized")
    
    def _load_mappings(self):
        """Load existing mappings"""
        if self.mapping_file.exists():
            with open(self.mapping_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_mappings(self):
        """Save mappings to disk"""
        with open(self.mapping_file, 'w') as f:
            json.dump(self.mappings, f, indent=2)
    
    def create_pseudonym(self, original_value, column_name):
        """Create and store pseudonym mapping"""
        pseudo = hashlib.sha256(str(original_value).encode()).hexdigest()
        
        if column_name not in self.mappings:
            self.mappings[column_name] = {}
        
        self.mappings[column_name][pseudo] = original_value
        self._save_mappings()
        return pseudo
    
    def reverse_pseudonym(self, pseudonym, column_name):
        """Reverse pseudonym to original value (for authorized access)"""
        if column_name in self.mappings:
            return self.mappings[column_name].get(pseudonym, "UNKNOWN")
        return "UNKNOWN"
    
    def get_mapping_count(self):
        """Get total number of mappings"""
        total = sum(len(mappings) for mappings in self.mappings.values())
        return total

if __name__ == "__main__":
    manager = PseudonymManager()
    
    # Test pseudonym creation
    pseudo = manager.create_pseudonym("john.doe@example.com", "email")
    print(f"Created pseudonym: {pseudo}")
    
    # Test reverse lookup
    original = manager.reverse_pseudonym(pseudo, "email")
    print(f"Reversed to: {original}")
    
    print(f"Total mappings: {manager.get_mapping_count()}")
