import pandas as pd
from sqlalchemy import create_engine

# ===== CONFIG =====
file_path = "E:/VSCode/Python/Python385/Code Space/Retail Project/dataset.xlsx"  
engine = create_engine("mysql+pymysql://root:123456@localhost/retail_data")

# ===== LOAD EXCEL =====
df = pd.read_excel(file_path)

# ===== PUSH TO MYSQL =====
df.to_sql('dataset', engine, if_exists='replace', index=False)

print("✅ Data pushed to MySQL")

# ===== LOAD VIEW =====
query = "SELECT * FROM final_dataset"
df = pd.read_sql(query, engine)

# ===== CLEAN =====
df = df.fillna(0)

# ===== FEATURE ENGINEERING =====
df['months_of_stock'] = df['inventory'] / (df['avg_monthly_sales'] + 1)

# ===== RECOMMENDATION =====
def classify(row):

    # 🚨 nguy hiểm 
    if row['sales_quartile'] == 1 and row['months_of_stock'] > 6:
        return "🚨 Cảnh báo hết date"

    # ⚠️ bán kém
    if row['sales_quartile'] == 1:
        return "⚠️ Bán chậm"

    # 🔥 cần nhập gấp
    if row['sales_quartile'] == 4 and row['months_of_stock'] < 1:
        return "🔥 Nhập hàng bán chạy"

    # 📈 bán tốt
    if row['sales_quartile'] == 4:
        return "📈 Bán chạy"

    # 💰 margin thấp
    if row['sales_quartile'] >= 3 and row['margin'] <= 0.25:
        return "💰 Bán chạy, tăng giá"

    return "Bình thường"

df['recommendation'] = df.apply(classify, axis=1)

# ===== ADD ORDER COLUMN =====
df['order'] = ""

# ===== FORMAT OUTPUT =====
# format tiền
money_cols = ['revenue', 'cost', 'price', 'profit']

for col in money_cols:
    df[col] = df[col].apply(lambda x: f"{int(x):,}" if pd.notnull(x) else "")

# format %
df['margin'] = df['margin'].apply(lambda x: f"{x:.2%}" if pd.notnull(x) else "")

# ===== SORT =====
df = df.sort_values(by=['sales_quartile', 'months_of_stock'])

# ===== EXPORT =====
with pd.ExcelWriter("recommendation.xlsx", engine="xlsxwriter") as writer:
    df.to_excel(writer, index=False, sheet_name="Sheet1")

    workbook  = writer.book
    worksheet = writer.sheets["Sheet1"]

    # ✅ Bật filter
    worksheet.autofilter(0, 0, len(df), len(df.columns) - 1)

    # ✅ Freeze header
    worksheet.freeze_panes(1, 0)

    # ✅ AUTO WIDTH (đặt ở đây)
    for i, col in enumerate(df.columns):
        column_len = max(df[col].astype(str).map(len).max(), len(col)) + 2
        worksheet.set_column(i, i, column_len)

print("✅ Done")