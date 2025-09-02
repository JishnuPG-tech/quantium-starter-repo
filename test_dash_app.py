
import pytest
import pandas as pd
from dash.testing.application_runners import import_app
import dash
from dash import dcc, html
import time
import os

class TestDashApp:
    """Test suite for Soul Foods Pink Morsel Dashboard"""
    
    def setup_method(self):
        """Setup method to ensure data file exists"""
        # Ensure the CSV file exists for testing
        if not os.path.exists('processed_transaction_data.csv'):
            # Create minimal test data if file doesn't exist
            test_data = pd.DataFrame({
                'date': pd.date_range('2020-01-01', periods=100),
                'sales': [1000 + i*10 for i in range(100)],
                'region': ['north', 'south', 'east', 'west'] * 25
            })
            test_data.to_csv('processed_transaction_data.csv', index=False)
    
    def test_header_present(self, dash_duo):
        """Test 1: Verify the header is present"""
        # Import the app
        app = import_app("dash_app")
        
        # Start the app
        dash_duo.start_server(app)
        
        # Wait for the app to load
        dash_duo.wait_for_element("h1", timeout=10)
        
        # Check if header contains expected text
        header_element = dash_duo.find_element("h1")
        header_text = header_element.text
        
        # Verify header content
        assert "Soul Foods" in header_text, f"Expected 'Soul Foods' in header, got: {header_text}"
        assert "Pink Morsel" in header_text, f"Expected 'Pink Morsel' in header, got: {header_text}"
        
        print("✅ Test 1 PASSED: Header is present with correct content")
    
    def test_visualization_present(self, dash_duo):
        """Test 2: Verify the visualization (chart) is present"""
        # Import the app
        app = import_app("dash_app")
        
        # Start the app
        dash_duo.start_server(app)
        
        # Wait for the chart to load
        dash_duo.wait_for_element("#sales-chart", timeout=15)
        
        # Check if the chart component exists
        chart_element = dash_duo.find_element("#sales-chart")
        
        # Verify chart is visible
        assert chart_element.is_displayed(), "Chart should be visible"
        
        # Check if it contains plotly graph
        plotly_graph = dash_duo.find_element("#sales-chart .plotly")
        assert plotly_graph is not None, "Chart should contain Plotly visualization"
        
        print("✅ Test 2 PASSED: Visualization is present and visible")
    
    def test_region_picker_present(self, dash_duo):
        """Test 3: Verify the region picker (radio buttons) is present"""
        # Import the app  
        app = import_app("dash_app")
        
        # Start the app
        dash_duo.start_server(app)
        
        # Wait for the region filter to load
        dash_duo.wait_for_element("#region-filter", timeout=10)
        
        # Check if region filter exists
        region_filter = dash_duo.find_element("#region-filter")
        assert region_filter.is_displayed(), "Region filter should be visible"
        
        # Check for radio button options
        radio_buttons = dash_duo.find_elements("input[type='radio']")
        assert len(radio_buttons) >= 5, f"Should have at least 5 radio options, found {len(radio_buttons)}"
        
        # Check for expected region values
        radio_labels = dash_duo.find_elements("#region-filter label")
        label_texts = [label.text for label in radio_labels]
        
        # Verify key regions are present
        region_found = any("All" in text for text in label_texts)
        assert region_found, f"Should contain 'All' option, found: {label_texts}"
        
        print("✅ Test 3 PASSED: Region picker is present with correct options")
    
    def test_interactive_functionality(self, dash_duo):
        """Bonus Test: Verify interactive functionality works"""
        # Import the app
        app = import_app("dash_app")
        
        # Start the app
        dash_duo.start_server(app)
        
        # Wait for components to load
        dash_duo.wait_for_element("#region-filter", timeout=10)
        dash_duo.wait_for_element("#sales-chart", timeout=10)
        
        # Find radio buttons
        radio_buttons = dash_duo.find_elements("input[type='radio']")
        
        if len(radio_buttons) > 1:
            # Click on a different region (second radio button)
            radio_buttons[1].click()
            
            # Wait a moment for the callback to execute
            time.sleep(2)
            
            # Verify the chart still exists after interaction
            chart_element = dash_duo.find_element("#sales-chart")
            assert chart_element.is_displayed(), "Chart should remain visible after region change"
            
            print("✅ Bonus Test PASSED: Interactive functionality works")
        else:
            print("⚠️ Bonus Test SKIPPED: Not enough radio buttons found")

if __name__ == "__main__":
    print("🧪 Soul Foods Dashboard Test Suite")
    print("Run with: pytest test_dash_app.py -v")
