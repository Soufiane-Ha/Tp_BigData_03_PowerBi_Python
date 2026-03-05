import pandas as pd
import time
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

file_path = "/kaggle/input/ecommerce-behavior-data-from-multi-category-store/2019-Oct.csv"

start_time = time.time()

chunk_size = 100_000
chunks = []  

for chunk in pd.read_csv(file_path, chunksize=chunk_size):
    chunk.dropna(inplace=True)
    chunk.drop_duplicates(inplace=True)
    chunk['date'] = pd.to_datetime(chunk['event_time'])
    
    chunks.append(chunk)  

data = pd.concat(chunks, ignore_index=True)

end_time = time.time()
print(f"Execution time: {end_time - start_time} seconds")

corr = data.select_dtypes(include='number').corr()
sns.heatmap(corr, annot=True, cmap="coolwarm")
plt.show()

purchases = data[data['event_type'] == 'purchase']
daily_sales = purchases.groupby('date')['price'].sum()
daily_sales.plot(kind='line')
plt.title("Sales Over Time")
plt.xlabel("Date")
plt.ylabel("Sales")
plt.show()

top_products = purchases.groupby('product_id').size().nlargest(10)
top_products.plot(kind='bar')
plt.title("Top 10 Products by Purchase Count")
plt.show()

X = purchases[['price']]
kmeans = KMeans(n_clusters=3, random_state=42)
purchases['Cluster'] = kmeans.fit_predict(X)
print(purchases.head())