import pandas as pd
from sqlalchemy import create_engine

# ====== CONFIG ======
file_path = r"E:/VSCode/Python/Python385/Code Space/Retail Project/dataset.xlsx"

db_user = "root"
db_password = "123456"
db_host = "localhost"
db_name = "retail_data"

# ====================

# 1. Đọc file Excel
df = pd.read_excel(file_path)

# 2. Chuẩn hóa dữ liệu (QUAN TRỌNG)
df.columns = df.columns.str.strip().str.lower()

# đảm bảo sku + barcode là text
if 'sku' in df.columns:
    df['sku'] = df['sku'].astype(str)

if 'barcode' in df.columns:
    df['barcode'] = df['barcode'].astype(str)

# 3. Kết nối MySQL
engine = create_engine(
    f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}"
)

# 4. Push data (ghi đè mỗi lần chạy)
df.to_sql('dataset', con=engine, if_exists='replace', index=False)

print("✅ Done: Data pushed to MySQL")