import json
import pandas as pd

def process_certification_data(file_path):
    """
    Process certification data from JSON file to CSV format.
    
    This function reads a JSON file containing certification data, converts it
    into a pandas DataFrame, and saves it as a CSV file. It handles nested JSON
    structures by extracting the relevant 'documents' array.
    
    Parameters:
        file_path (str): Path to the JSON file containing certification data
        
    Returns:
        pandas.DataFrame: The processed certification data
    """
    try:
        # Read and parse the JSON file
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # Convert the documents list to a DataFrame
        df = pd.DataFrame(data['documents'])
        
        # Save to CSV in the same directory as the input file
        output_path = file_path.replace('.txt', '.csv')
        df.to_csv(output_path, index=False)
        
        print(f"Data successfully saved to: {output_path}")
        print("\nDataset Overview:")
        print(f"Number of records: {len(df)}")
        print("\nColumns in the dataset:")
        print(df.columns.tolist())
        print("\nFirst few rows of the data:")
        print(df.head())
        
        return df
        
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

# Process the certification data
file_path = '~path'
df = process_certification_data(file_path)