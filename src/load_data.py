import pandas as pd

hrrp_raw = pd.read_csv(r"C:\Users\asim0\Documents\Data\cms-penalty-risk\data\raw\FY_2026_Hospital_Readmissions_Reduction_Program_Hospital.csv")
hac = pd.read_csv(r"C:\Users\asim0\Documents\Data\cms-penalty-risk\data\raw\FY_2026_HAC_Reduction_Program_Hospital.csv")
vbp = pd.read_csv(r"C:\Users\asim0\Documents\Data\cms-penalty-risk\data\raw\hvbp_tps.csv")

# Convert Excess Readmission Ratio to numeric
hrrp_raw['Excess Readmission Ratio'] = pd.to_numeric(hrrp_raw['Excess Readmission Ratio'], errors='coerce')

# Pivot HRRP to one row per hospital
hrrp = hrrp_raw.pivot_table(
    index='Facility ID',
    columns='Measure Name',
    values='Excess Readmission Ratio'
).reset_index()

# Flatten column names
hrrp.columns.name = None

# Keep only what we need from HAC
hac_clean = hac[['Facility ID', 'Total HAC Score', 'Payment Reduction']].copy()
hac_clean['Total HAC Score'] = pd.to_numeric(hac_clean['Total HAC Score'], errors='coerce')

# Keep only what we need from VBP
vbp_clean = vbp[['Facility ID', 'Facility Name', 'State', 'Total Performance Score']].copy()
vbp_clean['Total Performance Score'] = pd.to_numeric(vbp_clean['Total Performance Score'], errors='coerce')

# Join all three
merged = vbp_clean.merge(hac_clean, on='Facility ID', how='inner')
merged = merged.merge(hrrp, on='Facility ID', how='inner')

print(f"Merged rows: {len(merged)}")
print(merged.head())
print(merged.columns.tolist())