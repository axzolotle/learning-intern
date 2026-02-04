#  Age Group Classifier
# - Difficulty: 🟡 Medium

# - Category: Feature Engineering



# - Background :



#     Tim analitik mau mengelompokkan pelanggan berdasarkan umur supaya bisa bikin strategi marketing berbeda.
### Dataset
import pandas as pd
import numpy as np


data = {
    "name": ["A", "B", "C", "D", "E", "F"],
    "age": [15, 22, 35, 47, 63, 29]
}

df = pd.DataFrame(data)
print("Original DataFrame:")
print(df)
print()

# ============================================================
# CARA 1: Menggunakan pd.cut() dengan bins yang benar
# ============================================================
def add_age_group_v1(df):
    """
    Cara 1: Menggunakan pd.cut() dengan bins yang sudah diperbaiki.
    right=False membuat bin menjadi left-inclusive: [0, 17), [17, 35), [35, 50), [50, 100]
    """
    bins = [0, 17, 35, 50, 100]
    labels = ['Teen', 'Young Adult', 'Adult', 'Senior']
    df['age_group_v1'] = pd.cut(df['age'], bins=bins, labels=labels, right=False)
    return df

# ============================================================
# CARA 2: Menggunakan np.select() untuk kondisi logika
# ============================================================
def add_age_group_v2(df):
    """
    Cara 2: Menggunakan np.select() dengan kondisi eksplisit.
    Lebih readable dan flexible untuk kondisi kompleks.
    """
    conditions = [
        (df['age'] < 17),
        (df['age'] < 35),
        (df['age'] < 50),
        (df['age'] >= 50)
    ]
    choices = ['Teen', 'Young Adult', 'Adult', 'Senior']
    df['age_group_v2'] = np.select(conditions, choices, default='Unknown')
    return df

# ============================================================
# CARA 3: Menggunakan apply() dengan fungsi lambda
# ============================================================
def add_age_group_v3(df):
    """
    Cara 3: Menggunakan apply() dengan fungsi lambda.
    Sangat flexible untuk transformasi custom.
    """
    def categorize_age(age):
        if age < 17:
            return 'Teen'
        elif age < 35:
            return 'Young Adult'
        elif age < 50:
            return 'Adult'
        else:
            return 'Senior'
    
    df['age_group_v3'] = df['age'].apply(categorize_age)
    return df

# ============================================================
# CARA 4: Menggunakan pd.cut() dengan include_lowest=True
# ============================================================
def add_age_group_v4(df):
    """
    Cara 4: Menggunakan pd.cut() dengan include_lowest=True dan right=True.
    include_lowest=True memastikan nilai pertama (0) termasuk dalam bin pertama.
    """
    bins = [0, 17, 35, 50, 100]
    labels = ['Teen', 'Young Adult', 'Adult', 'Senior']
    df['age_group_v4'] = pd.cut(df['age'], bins=bins, labels=labels, 
                                 include_lowest=True, right=True)
    return df

# ============================================================
# CARA 5: Menggunakan map() dengan dictionary
# ============================================================
def add_age_group_v5(df):
    """
    Cara 5: Membuat bins dan menggunakan pd.cut() lalu map ke labels.
    Berguna jika ingin memisahkan pembuatan bins dan labels.
    """
    bins = [0, 17, 35, 50, 100]
    labels = ['Teen', 'Young Adult', 'Adult', 'Senior']
    
    # Assign bin indices terlebih dahulu
    df['bin_idx'] = pd.cut(df['age'], bins=bins, include_lowest=True)
    
    # Map bin indices ke labels
    df['age_group_v5'] = df['bin_idx'].cat.codes.map(dict(enumerate(labels)))
    
    # Hapus kolom temporary jika tidak diperlukan
    df.drop('bin_idx', axis=1, inplace=True)
    return df

# ============================================================
# CARA 6: Menggunakan list comprehension (paling simple)
# ============================================================
def add_age_group_v6(df):
    """
    Cara 6: Menggunakan list comprehension.
    Paling cepat dan pythonic untuk operasi sederhana.
    """
    def get_age_group(age):
        if age < 17:
            return 'Teen'
        elif age < 35:
            return 'Young Adult'
        elif age < 50:
            return 'Adult'
        else:
            return 'Senior'
    
    df['age_group_v6'] = [get_age_group(age) for age in df['age']]
    return df

# ============================================================
# Menjalankan semua cara dan menampilkan hasil
# ============================================================
print("=" * 60)
print("HASIL PERBANDINGAN SEMUA CARA:")
print("=" * 60)

# Apply semua cara
df_result = df.copy()
add_age_group_v1(df_result)
add_age_group_v2(df_result)
add_age_group_v3(df_result)
add_age_group_v4(df_result)
add_age_group_v5(df_result)
add_age_group_v6(df_result)

print(df_result.to_string(index=False))
print()

# ============================================================
# RINGKASAN:
# ============================================================
print("=" * 60)
print("RINGKASAN CARA-CARA:")
print("=" * 60)
print("""
CARA 1 (pd.cut + right=False): 
   - Paling efficient untuk operasi vectorized
   - Cocok untuk dataset besar
   
CARA 2 (np.select):
   - Sangat flexible untuk kondisi kompleks
   - Good untuk multiple conditions
   
CARA 3 (apply + function):
   - Sangat readable dan mudah dipahami
   - Flexible untuk transformasi custom
   
CARA 4 (pd.cut + include_lowest):
   - Alternatif dari cara 1
   - include_lowest=True memastikan bin pertama benar
   
CARA 5 (map + dictionary):
   - Memisahkan step creation dan mapping
   - Berguna untuk debugging
   
CARA 6 (list comprehension):
   - Paling simple dan pythonic
   - Cocok untuk operasi cepat
""")

