import pandas as pd
import os

file_path = "/kaggle/input/ecommerce-behavior-data-from-multi-category-store/2019-Oct.csv"
output_file = "clean_purchases_oct_sample.csv.gz"
chunk_size = 100_000
first_chunk = True


if os.path.exists(output_file):
    os.remove(output_file)

for chunk in pd.read_csv(file_path, chunksize=chunk_size, usecols=['event_time','event_type','product_id','price']):

    chunk.dropna(inplace=True)
    chunk.drop_duplicates(inplace=True)

    purchases = chunk[chunk['event_type'] == 'purchase']
    
    if not purchases.empty:

        sample = purchases.sample(frac=0.1, random_state=42)
        
        sample.to_csv(
            output_file,
            mode='a',
            index=False,
            header=first_chunk,
            compression='gzip'
        )
        first_chunk = False

print(f"file was created : {output_file}")