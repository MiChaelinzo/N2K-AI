import geopandas as gpd
import pandas as pd

# Step 1: Data Collection and Preprocessing
data = gpd.read_file('n2k_data.gpkg')

# Step 2: Feature Extraction
# Assuming you want to extract features such as vessel speed, proximity to sensitive areas, and environmental conditions

# Extract vessel speed feature
data['vessel_speed'] = data['speed']

# Extract proximity to sensitive areas feature (assuming you have a sensitive areas dataset as a GeoPackage)
sensitive_areas = gpd.read_file('sensitive_areas.gpkg')
proximity = data.distance(sensitive_areas.geometry).min(axis=1)
data['proximity_to_sensitive_areas'] = proximity

# Extract environmental conditions features (assuming you have environmental data as a GeoPackage)
environmental_data = gpd.read_file('environmental_data.gpkg')
# Assuming the environmental data has variables like temperature, salinity, and depth
environmental_features = ['temperature', 'salinity', 'depth']
env_data_extracted = gpd.sjoin(data, environmental_data, how='left', op='intersects')[environmental_features]

# Concatenate all extracted features into a single DataFrame
features = pd.concat([data['vessel_speed'], data['proximity_to_sensitive_areas'], env_data_extracted], axis=1)

# Step 3: Data Labeling
# Assuming you have labeled the data with the impacts on protected species and habitats and stored it in a column called 'impact'
# 1 represents the presence of impact, 0 represents the absence of impact
labels = data['impact']

# Further preprocessing and normalization of the features and labels can be done if required

# Save the extracted features and labels to a CSV file
extracted_features = pd.concat([features, labels], axis=1)
extracted_features.to_csv('extracted_features.csv', index=False)
