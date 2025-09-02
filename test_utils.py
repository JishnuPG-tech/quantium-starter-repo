
"""
Test utilities for Soul Foods Dashboard
"""
import pandas as pd
import os

def create_test_data():
    """Create minimal test data for testing purposes"""
    test_data = pd.DataFrame({
        'date': pd.date_range('2020-01-01', periods=100),
        'sales': [1000 + i*10 for i in range(100)],
        'region': ['north', 'south', 'east', 'west'] * 25
    })
    return test_data

def ensure_test_data_exists():
    """Ensure test data file exists"""
    if not os.path.exists('processed_transaction_data.csv'):
        test_data = create_test_data()
        test_data.to_csv('processed_transaction_data.csv', index=False)
        return True
    return False

def validate_app_structure():
    """Validate the Dash app has required components"""
    try:
        with open('dash_app.py', 'r') as f:
            content = f.read()
        
        requirements = {
            'header': 'Soul Foods' in content,
            'chart': 'sales-chart' in content,
            'region_filter': 'region-filter' in content,
            'radio_items': any(term in content for term in ['RadioItems', 'dcc.RadioItems'])
        }
        
        return all(requirements.values()), requirements
    except FileNotFoundError:
        return False, {'error': 'dash_app.py not found'}

if __name__ == "__main__":
    print("🛠️ Test Utilities")
    print("Running validation...")
    
    # Check data
    data_created = ensure_test_data_exists()
    if data_created:
        print("✅ Test data created")
    else:
        print("✅ Test data already exists")
    
    # Check app structure
    valid, details = validate_app_structure()
    if valid:
        print("✅ App structure is valid")
    else:
        print(f"❌ App structure issues: {details}")
