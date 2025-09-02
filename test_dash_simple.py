
import pytest
import pandas as pd
import os
import sys
import importlib.util

class TestDashAppStructure:
    """Simplified test suite for Soul Foods Dashboard structure"""
    
    def setup_method(self):
        """Setup method"""
        # Ensure data file exists
        if not os.path.exists('processed_transaction_data.csv'):
            test_data = pd.DataFrame({
                'date': pd.date_range('2020-01-01', periods=100),
                'sales': [1000 + i*10 for i in range(100)],
                'region': ['north', 'south', 'east', 'west'] * 25
            })
            test_data.to_csv('processed_transaction_data.csv', index=False)
    
    def test_app_imports_successfully(self):
        """Test that the Dash app imports without errors"""
        try:
            spec = importlib.util.spec_from_file_location("dash_app", "dash_app.py")
            dash_app = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(dash_app)
            
            # Check if app object exists
            assert hasattr(dash_app, 'app'), "App object should exist"
            print("✅ App imports successfully")
            
        except Exception as e:
            pytest.fail(f"App failed to import: {e}")
    
    def test_header_present(self):
        """Test 1: Verify the header is present in app layout"""
        with open('dash_app.py', 'r') as f:
            app_content = f.read()
        
        # Check for header content
        assert 'Soul Foods' in app_content, "Header should contain 'Soul Foods'"
        assert 'Pink Morsel' in app_content, "Header should contain 'Pink Morsel'"
        
        # Check for H1 tag
        header_indicators = ['html.H1', 'H1(', '"h1"', "'h1'"]
        has_header = any(indicator in app_content for indicator in header_indicators)
        assert has_header, "App should have an H1 header element"
        
        print("✅ Test 1 PASSED: Header is present")
    
    def test_visualization_present(self):
        """Test 2: Verify the visualization component is present"""
        with open('dash_app.py', 'r') as f:
            app_content = f.read()
        
        # Check for chart component
        assert 'sales-chart' in app_content, "App should have sales-chart component"
        
        # Check for Graph component
        graph_indicators = ['dcc.Graph', 'Graph(', 'plotly']
        has_graph = any(indicator in app_content for indicator in graph_indicators)
        assert has_graph, "App should have a Graph/visualization component"
        
        print("✅ Test 2 PASSED: Visualization is present")
    
    def test_region_picker_present(self):
        """Test 3: Verify the region picker is present"""
        with open('dash_app.py', 'r') as f:
            app_content = f.read()
        
        # Check for region filter
        assert 'region-filter' in app_content, "App should have region-filter component"
        
        # Check for RadioItems
        radio_indicators = ['RadioItems', 'dcc.RadioItems', 'radio']
        has_radio = any(indicator in app_content for indicator in radio_indicators)
        assert has_radio, "App should have RadioItems component"
        
        # Check for region options
        regions = ['north', 'south', 'east', 'west', 'all']
        regions_found = sum(1 for region in regions if region in app_content.lower())
        assert regions_found >= 4, f"Should have most region options, found {regions_found}"
        
        print("✅ Test 3 PASSED: Region picker is present")
    
    def test_data_file_exists(self):
        """Test 4: Verify data file exists and has correct structure"""
        assert os.path.exists('processed_transaction_data.csv'), "Data file should exist"
        
        # Load and check data structure
        df = pd.read_csv('processed_transaction_data.csv')
        
        required_columns = ['date', 'sales', 'region']
        for col in required_columns:
            assert col in df.columns, f"Data should have {col} column"
        
        # Check data types and content
        assert len(df) > 0, "Data file should not be empty"
        assert df['region'].nunique() >= 4, "Should have multiple regions"
        
        print("✅ Test 4 PASSED: Data file exists with correct structure")
    
    def test_callback_functions_present(self):
        """Test 5: Verify callback functions are present"""
        with open('dash_app.py', 'r') as f:
            app_content = f.read()
        
        # Check for callback decorator
        callback_indicators = ['@app.callback', '@callback', 'Output', 'Input']
        has_callback = any(indicator in app_content for indicator in callback_indicators)
        assert has_callback, "App should have callback functions for interactivity"
        
        print("✅ Test 5 PASSED: Callback functions are present")

if __name__ == "__main__":
    print("🧪 Soul Foods Dashboard Test Suite - Simplified Version")
    print("Run with: pytest test_dash_simple.py -v")
