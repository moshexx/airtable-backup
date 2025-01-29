# to run tests:
# python -m unittest tests/test_backup.py -v

# tests/test_backup.py
import unittest
from unittest.mock import patch, MagicMock
import os
import sys
import pandas as pd
from datetime import datetime
import json

# Add src directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from backup import backup_airtable_to_csv, get_tables, backup_table, cleanup_old_backups

class TestAirtableBackup(unittest.TestCase):
    """Test cases for Airtable backup functionality"""

    def setUp(self):
        """Set up test environment before each test"""
        self.test_api_key = "test_key_xxx"
        self.test_base_id = "test_base_xxx"
        self.test_table_name = "Test Table"
        
        # Mock environment variable
        os.environ['AIRTABLE_API_KEY'] = self.test_api_key
        
        # Create test directory for backups
        self.test_backup_dir = "test_backups"
        if not os.path.exists(self.test_backup_dir):
            os.makedirs(self.test_backup_dir)

    def tearDown(self):
        """Clean up after each test"""
        # Remove test backup directory and files
        if os.path.exists(self.test_backup_dir):
            for file in os.listdir(self.test_backup_dir):
                os.remove(os.path.join(self.test_backup_dir, file))
            os.rmdir(self.test_backup_dir)
        
        # Remove environment variable
        if 'AIRTABLE_API_KEY' in os.environ:
            del os.environ['AIRTABLE_API_KEY']

    @patch('requests.get')
    def test_get_tables(self, mock_get):
        """Test getting tables list from Airtable"""
        # Mock response data
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "tables": [
                {"id": "tbl1", "name": "Table 1"},
                {"id": "tbl2", "name": "Table 2"}
            ]
        }
        mock_get.return_value = mock_response

        # Test function
        tables = get_tables(self.test_base_id, self.test_api_key)
        
        # Assertions
        self.assertEqual(len(tables), 2)
        self.assertEqual(tables[0]["name"], "Table 1")
        self.assertEqual(tables[1]["name"], "Table 2")

    @patch('requests.get')
    def test_backup_table(self, mock_get):
        """Test backing up a single table"""
        # Mock response data
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "records": [
                {"id": "rec1", "fields": {"Name": "Test 1", "Value": 100}},
                {"id": "rec2", "fields": {"Name": "Test 2", "Value": 200}}
            ]
        }
        mock_get.return_value = mock_response

        # Test function
        df = backup_table(self.test_base_id, self.test_table_name, self.test_api_key)
        
        # Assertions
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 2)
        self.assertEqual(df.iloc[0]["Name"], "Test 1")
        self.assertEqual(df.iloc[1]["Value"], 200)

    def test_cleanup_old_backups(self):
        """Test cleanup of old backup files"""
        # Create test backup files
        test_files = [
            f"backup_2020-01-01.csv",
            f"backup_2020-01-02.csv",
            f"backup_{datetime.now().strftime('%Y-%m-%d')}.csv"
        ]
        
        for file in test_files:
            with open(os.path.join(self.test_backup_dir, file), 'w') as f:
                f.write("test data")

        # Test function
        cleanup_old_backups(self.test_backup_dir, retention_days=30)
        
        # Check that only recent file remains
        remaining_files = os.listdir(self.test_backup_dir)
        self.assertEqual(len(remaining_files), 1)
        self.assertTrue(remaining_files[0].startswith(f"backup_{datetime.now().strftime('%Y-%m-%d')}"))

    @patch('requests.get')
    def test_backup_airtable_to_csv_full(self, mock_get):
        """Test full backup process"""
        # Mock tables response
        mock_tables_response = MagicMock()
        mock_tables_response.json.return_value = {
            "tables": [{"id": "tbl1", "name": "Test Table"}]
        }
        
        # Mock data response
        mock_data_response = MagicMock()
        mock_data_response.json.return_value = {
            "records": [
                {"id": "rec1", "fields": {"Name": "Test 1", "Value": 100}}
            ]
        }
        
        # Setup mock to return different responses
        mock_get.side_effect = [mock_tables_response, mock_data_response]

        # Test full backup function
        try:
            backup_airtable_to_csv()
            
            # Check if backup file was created
            backup_files = os.listdir(self.test_backup_dir)
            self.assertEqual(len(backup_files), 1)
            
            # Verify file contents
            backup_file = os.path.join(self.test_backup_dir, backup_files[0])
            df = pd.read_csv(backup_file)
            self.assertEqual(len(df), 1)
            self.assertEqual(df.iloc[0]["Name"], "Test 1")
            
        except Exception as e:
            self.fail(f"Backup failed with error: {str(e)}")

    def test_api_key_missing(self):
        """Test behavior when API key is missing"""
        if 'AIRTABLE_API_KEY' in os.environ:
            del os.environ['AIRTABLE_API_KEY']
        
        with self.assertRaises(ValueError):
            backup_airtable_to_csv()

    @patch('requests.get')
    def test_api_error_handling(self, mock_get):
        """Test handling of API errors"""
        # Mock API error
        mock_get.side_effect = Exception("API Error")
        
        with self.assertRaises(Exception):
            get_tables(self.test_base_id, self.test_api_key)

if __name__ == '__main__':
    unittest.main()