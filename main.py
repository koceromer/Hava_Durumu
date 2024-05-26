import pyarrow.parquet as parquet
import pandas

# Load the Parquet file
table = parquet.read_table('data/daily_weather.parquet')

# Read the data into a Pandas DataFrame
df = table.to_pandas()

# Print the schema of the table
print(df.head())
print(df.columns.tolist())