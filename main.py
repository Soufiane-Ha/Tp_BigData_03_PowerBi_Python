import pandas as pd
import os
import time
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import zscore
from sklearn.cluster import KMeans

start_time = time.time()

file_path = "/kaggle/input/ecommerce-behavior-data-from-multi-category-store/2019-Oct.csv"
output_file = "clean_purchases_oct_sample.csv.gz"

chunk_size = 100000
first_chunk = True

chunks = []

# حذف الملف القديم
if os.path.exists(output_file):
    os.remove(output_file)

for data in pd.read_csv(
        file_path,
        chunksize=chunk_size,
        usecols=['event_time','event_type','product_id','price']
    ):

    # تنظيف البيانات
    data.dropna(inplace=True)
    data.drop_duplicates(inplace=True)

    # تحويل التاريخ
    data['date'] = pd.to_datetime(data['event_time'], errors='coerce')

    # إزالة القيم الشاذة
    data = data[(abs(zscore(data['price'])) < 3)]

    # اختيار عمليات الشراء
    purchases = data[data['event_type'] == 'purchase']

    if not purchases.empty:

        # عينة 10%
        sample = purchases.sample(frac=0.1, random_state=42)

        sample.to_csv(
            output_file,
            mode='a',
            index=False,
            header=first_chunk,
            compression='gzip'
        )

        first_chunk = False
        chunks.append(sample)

# دمج البيانات
data = pd.concat(chunks, ignore_index=True)

# ------------------------------
# تحليل البيانات
# ------------------------------

# Correlation
corr = data.select_dtypes(include='number').corr()
sns.heatmap(corr, annot=True, cmap="coolwarm")
plt.show()

# المبيعات اليومية
purchases = data[data['event_type'] == 'purchase']
daily_sales = purchases.groupby('date')['price'].sum()

daily_sales.plot(kind='line')
plt.title("Sales Over Time")
plt.xlabel("Date")
plt.ylabel("Sales")
plt.show()

# أفضل المنتجات
top_products = purchases.groupby('product_id').size().nlargest(10)

top_products.plot(kind='bar')
plt.title("Top 10 Products by Purchase Count")
plt.show()

# KMeans clustering
X = purchases[['price']]
kmeans = KMeans(n_clusters=3, random_state=42)

purchases['Cluster'] = kmeans.fit_predict(X)

print(purchases.head())

end_time = time.time()
print(f"Execution time: {end_time - start_time} seconds")

print(f"تم إنشاء الملف: {output_file}")