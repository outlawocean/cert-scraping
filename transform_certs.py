import pandas as pd
import json

def parse_list_or_string(value):
    """
    Handles both string representations of lists and actual list objects.
    
    This function is necessary because our data comes in mixed formats:
    - Sometimes as string representations of lists: "[{'Species': 'Salmon'}]"
    - Sometimes as actual list objects: [{'Species': 'Salmon'}]
    """
    # If it's already a list, return it
    if isinstance(value, list):
        return value
        
    # If it's a string, try to parse it
    try:
        # Replace single quotes with double quotes for JSON compatibility
        cleaned = value.replace("'", '"')
        return json.loads(cleaned)
    except (json.JSONDecodeError, AttributeError) as e:
        print(f"Error parsing value: {value}")
        print(f"Error details: {e}")
        return value

def extract_value_from_dict(item, key='Species'):
    """
    Extracts a value from a dictionary, handling various formats.
    
    For example:
    - {'Species': 'Salmon'} becomes 'Salmon'
    - Already-string values are returned as-is
    """
    if isinstance(item, dict):
        return item.get(key, '')
    return item

def transform_certification_sites(csv_path):
    """
    Transforms certification data to create individual rows for each site-species-stage
    combination while preserving all certification information.
    """
    # Read the CSV file
    df = pd.read_csv(csv_path)
    
    # Convert the Sites column first
    df['Sites'] = df['Sites'].apply(parse_list_or_string)
    
    # Keep these certification columns
    cert_columns = ['Certificate_Number', 'Ch_ID', 'Ch_Name', 'Uoc_ID', 'Uoc_Name', 
                   'Certificate_Status', 'Valid_From', 'Valid_Until', 'Country', 
                   'Production_Model', 'Type_of_Certification']
    
    # Create initial dataframe with exploded Sites
    sites_df = df[cert_columns + ['Sites']].explode('Sites')
    
    # Convert site dictionaries to columns
    sites_info = pd.json_normalize(sites_df['Sites'])
    
    # Combine certification info with site info
    sites_df = sites_df.drop('Sites', axis=1).reset_index(drop=True)
    result_df = pd.concat([sites_df, sites_info], axis=1)
    
    # Handle Fed_Species and Growth_Stage columns
    result_df['Fed_Species'] = result_df['Fed_Species'].apply(parse_list_or_string)
    result_df['Growth_Stage'] = result_df['Growth_Stage'].apply(parse_list_or_string)
    
    # Create separate rows for species and stages
    exploded_df = result_df.explode('Fed_Species').explode('Growth_Stage')
    
    # Extract clean values from dictionaries
    exploded_df['Species'] = exploded_df['Fed_Species'].apply(
        lambda x: extract_value_from_dict(x, 'Species'))
    exploded_df['Stage'] = exploded_df['Growth_Stage'].apply(
        lambda x: extract_value_from_dict(x, 'Stage'))
    
    # Clean up and organize columns
    final_df = exploded_df.drop(['Fed_Species', 'Growth_Stage'], axis=1)
    
    # Arrange columns in a logical order
    column_order = ['Site_ID', 'Site_Name', 'Species', 'Stage', 'Latitude', 'Longitude', 
                   'Site_Status'] + cert_columns
    final_df = final_df[column_order]
    
    # Save transformed data
    output_path = csv_path.replace('.csv', 'exploded_transformed.csv')
    final_df.to_csv(output_path, index=False)
    
    return final_df

# Process the file
file_path = '~path'
transformed_df = transform_certification_sites(file_path)

# Show results
print("\nTransformation complete!")
print(f"\nOriginal shape: {pd.read_csv(file_path).shape}")
print(f"Transformed shape: {transformed_df.shape}")
print("\nFirst few rows of transformed data:")
print(transformed_df.head())

# Show some statistics about the transformation
print("\nUnique species in dataset:")
print(transformed_df['Species'].unique())
print("\nUnique stages in dataset:")
print(transformed_df['Stage'].unique())