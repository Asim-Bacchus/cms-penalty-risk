import pandas as pd
from scipy import stats
hrrp_raw = pd.read_csv(r"C:\Users\asim0\Documents\Data\cms-penalty-risk\data\raw\FY_2026_Hospital_Readmissions_Reduction_Program_Hospital.csv")
hac = pd.read_csv(r"C:\Users\asim0\Documents\Data\cms-penalty-risk\data\raw\FY_2026_HAC_Reduction_Program_Hospital.csv")
vbp = pd.read_csv(r"C:\Users\asim0\Documents\Data\cms-penalty-risk\data\raw\hvbp_tps.csv")

hrrp_raw['Excess Readmission Ratio'] = pd.to_numeric(hrrp_raw['Excess Readmission Ratio'], errors='coerce')

hrrp = hrrp_raw.pivot_table(
    index='Facility ID',
    columns='Measure Name',
    values='Excess Readmission Ratio'
).reset_index()
hrrp.columns.name = None

hac_clean = hac[['Facility ID', 'Total HAC Score', 'Payment Reduction']].copy()
hac_clean['Total HAC Score'] = pd.to_numeric(hac_clean['Total HAC Score'], errors='coerce')

vbp_clean = vbp[['Facility ID', 'Facility Name', 'State', 'Total Performance Score']].copy()
vbp_clean['Total Performance Score'] = pd.to_numeric(vbp_clean['Total Performance Score'], errors='coerce')

merged = vbp_clean.merge(hac_clean, on='Facility ID', how='inner')
merged = merged.merge(hrrp, on='Facility ID', how='inner')

# Flag HRRP risk: any condition with excess ratio above 1.0
readmission_cols = [c for c in merged.columns if 'READM' in c]
merged['hrrp_risk'] = (merged[readmission_cols] > 1.0).any(axis=1).astype(int)

# Flag HAC risk: payment reduction yes/no
merged['hac_risk'] = (merged['Payment Reduction'] == 'Yes').astype(int)

# Flag VBP risk: below median total performance score
vbp_median = merged['Total Performance Score'].median()
merged['vbp_risk'] = (merged['Total Performance Score'] < vbp_median).astype(int)

# Composite risk score 0-3
merged['composite_risk'] = merged['hrrp_risk'] + merged['hac_risk'] + merged['vbp_risk']

print("=== Composite Risk Distribution ===")
print(merged['composite_risk'].value_counts().sort_index())

print(f"\nHospitals exposed to all three programs: {(merged['composite_risk'] == 3).sum()}")
print(f"Hospitals exposed to two programs: {(merged['composite_risk'] == 2).sum()}")
print(f"Hospitals exposed to one program: {(merged['composite_risk'] == 1).sum()}")
print(f"Hospitals exposed to none: {(merged['composite_risk'] == 0).sum()}")

merged.to_csv(r"C:\Users\asim0\Documents\Data\cms-penalty-risk\data\processed\hospital_risk_profile.csv", index=False)
print("Saved to processed folder.")

# NY specific breakdown
ny = merged[merged['State'] == 'NY']
print(f"Total NY hospitals in dataset: {len(ny)}")
print(f"NY hospitals with dual or triple exposure: {(ny['composite_risk'] >= 2).sum()}")
print(f"NY percentage dual or triple: {(ny['composite_risk'] >= 2).mean() * 100:.1f}%")
print(f"NY triple exposure: {(ny['composite_risk'] == 3).sum()}")



# NY breakdown
ny = merged[merged['State'] == 'NY']
print(f"Total NY hospitals: {len(ny)}")
print(f"NY dual or triple exposure: {(ny['composite_risk'] >= 2).sum()}")
print(f"NY dual or triple %: {(ny['composite_risk'] >= 2).mean() * 100:.1f}%")
print(f"NY triple exposure: {(ny['composite_risk'] == 3).sum()}")

