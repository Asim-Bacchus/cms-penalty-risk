import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

df = pd.read_csv(r"C:\Users\asim0\Documents\Data\cms-penalty-risk\data\processed\hospital_risk_profile.csv")

# ── Figure 1: Composite Risk Distribution ──────────────────────────────────────
labels = ['No Exposure\n(0 programs)', 'Single Exposure\n(1 program)',
          'Dual Exposure\n(2 programs)', 'Triple Exposure\n(3 programs)']
counts = [165, 959, 961, 337]
colors = ['#2ecc71', '#f39c12', '#e67e22', '#e74c3c']

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(labels, counts, color=colors, edgecolor='white', linewidth=0.8)

for bar, count in zip(bars, counts):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 15,
            f'{count:,}', ha='center', va='bottom', fontweight='bold', fontsize=11)

ax.set_title('CMS Penalty Program Exposure Across 2,422 U.S. Hospitals\nFY 2026',
             fontsize=14, fontweight='bold', pad=15)
ax.set_ylabel('Number of Hospitals', fontsize=11)
ax.set_ylim(0, 1100)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.tick_params(axis='x', labelsize=10)

plt.tight_layout()
plt.savefig(r"C:\Users\asim0\Documents\Data\cms-penalty-risk\outputs\figures\01_composite_risk_distribution.png",
            dpi=150, bbox_inches='tight')
plt.close()
print("Figure 1 saved.")

# ── Figure 2: Triple Exposure by State ────────────────────────────────────────
triple = df[df['composite_risk'] == 3]
state_counts = triple['State'].value_counts().head(15)

fig, ax = plt.subplots(figsize=(10, 7))
bars = ax.barh(state_counts.index[::-1], state_counts.values[::-1], color='#e74c3c', edgecolor='white')

for bar, val in zip(bars, state_counts.values[::-1]):
    ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height() / 2,
            str(val), va='center', fontweight='bold', fontsize=10)

ax.set_title('States with Most Hospitals Exposed Across All Three CMS Penalty Programs\nFY 2026',
             fontsize=13, fontweight='bold', pad=15)
ax.set_xlabel('Number of Hospitals with Triple Exposure', fontsize=11)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig(r"C:\Users\asim0\Documents\Data\cms-penalty-risk\outputs\figures\02_triple_exposure_by_state.png",
            dpi=150, bbox_inches='tight')
plt.close()
print("Figure 2 saved.")

# ── Figure 3: VBP Score by Risk Tier ──────────────────────────────────────────
risk_labels = {0: 'No Exposure', 1: 'Single', 2: 'Dual', 3: 'Triple'}
df['risk_label'] = df['composite_risk'].map(risk_labels)
order = ['No Exposure', 'Single', 'Dual', 'Triple']
colors_box = ['#2ecc71', '#f39c12', '#e67e22', '#e74c3c']

fig, ax = plt.subplots(figsize=(10, 6))
data_by_tier = [df[df['risk_label'] == label]['Total Performance Score'].dropna() for label in order]
bp = ax.boxplot(data_by_tier, labels=order, patch_artist=True, medianprops=dict(color='white', linewidth=2))

for patch, color in zip(bp['boxes'], colors_box):
    patch.set_facecolor(color)
    patch.set_alpha(0.8)

ax.set_title('VBP Total Performance Score by CMS Penalty Exposure Tier\nFY 2026',
             fontsize=13, fontweight='bold', pad=15)
ax.set_ylabel('Total Performance Score', fontsize=11)
ax.set_xlabel('Composite Risk Tier', fontsize=11)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig(r"C:\Users\asim0\Documents\Data\cms-penalty-risk\outputs\figures\03_vbp_score_by_risk_tier.png",
            dpi=150, bbox_inches='tight')
plt.close()
print("Figure 3 saved.")

# ── Figure 4: Average Excess Readmission Ratio by Risk Tier ───────────────────
readmission_cols = [c for c in df.columns if 'READM' in c]
df['avg_excess_readmission'] = df[readmission_cols].mean(axis=1)

avg_by_tier = df.groupby('risk_label')['avg_excess_readmission'].mean().reindex(order)

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(order, avg_by_tier.values, color=colors_box, edgecolor='white')

for bar, val in zip(bars, avg_by_tier.values):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.002,
            f'{val:.3f}', ha='center', va='bottom', fontweight='bold', fontsize=11)

ax.axhline(y=1.0, color='black', linestyle='--', linewidth=1.2, label='Expected Ratio = 1.0')
ax.set_title('Average Excess Readmission Ratio by CMS Penalty Exposure Tier\nFY 2026',
             fontsize=13, fontweight='bold', pad=15)
ax.set_ylabel('Average Excess Readmission Ratio', fontsize=11)
ax.set_xlabel('Composite Risk Tier', fontsize=11)
ax.legend(fontsize=10)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig(r"C:\Users\asim0\Documents\Data\cms-penalty-risk\outputs\figures\04_readmission_by_risk_tier.png",
            dpi=150, bbox_inches='tight')
plt.close()
print("Figure 4 saved.")

# ── Figure 5: Nurse Communication by Risk Tier ─────────────────────────────────
hcahps = pd.read_csv(r"C:\Users\asim0\Documents\Data\cms-penalty-risk\data\raw\hospital_kpis_2024.csv")

# Fix ID format to match merged dataset
hcahps['facility_id'] = pd.to_numeric(hcahps['facility_id'].astype(str).str.lstrip('0'), errors='coerce')
hcahps = hcahps.dropna(subset=['facility_id'])
hcahps['facility_id'] = hcahps['facility_id'].astype(int)
hcahps['nurse_comm_stars'] = pd.to_numeric(hcahps['nurse_comm_stars'], errors='coerce')

# Join to composite risk data
df_nurse = df.merge(hcahps[['facility_id', 'nurse_comm_stars']], 
                    left_on='Facility ID', right_on='facility_id', how='inner')

print(f"Joined rows: {len(df_nurse)}")

# Average nurse comm stars by risk tier
nurse_by_tier = df_nurse.groupby('risk_label')['nurse_comm_stars'].mean().reindex(order)

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(order, nurse_by_tier.values, color=colors_box, edgecolor='white')

for bar, val in zip(bars, nurse_by_tier.values):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.02,
            f'{val:.2f}', ha='center', va='bottom', fontweight='bold', fontsize=11)

ax.set_title('Average Nurse Communication Rating by CMS Penalty Exposure Tier\nFY 2026',
             fontsize=13, fontweight='bold', pad=15)
ax.set_ylabel('Average Nurse Communication Star Rating (1-5)', fontsize=11)
ax.set_xlabel('Composite Risk Tier', fontsize=11)
ax.set_ylim(0, 4)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig(r"C:\Users\asim0\Documents\Data\cms-penalty-risk\outputs\figures\05_nurse_comm_by_risk_tier.png",
            dpi=150, bbox_inches='tight')
plt.close()
print("Figure 5 saved.")

# ── Figure 6: Risk Profile by Nurse Communication Group ───────────────────────
df_nurse['comm_group'] = pd.cut(df_nurse['nurse_comm_stars'],
                                 bins=[0, 2, 3, 5],
                                 labels=['Low (1-2 stars)', 'Medium (3 stars)', 'High (4-5 stars)'])

# Composite risk distribution by communication group
risk_by_comm = df_nurse.groupby('comm_group')['composite_risk'].mean()

fig, axes = plt.subplots(1, 3, figsize=(15, 6))

# Chart A: Average composite risk score
comm_colors = ['#e74c3c', '#f39c12', '#2ecc71']
axes[0].bar(risk_by_comm.index, risk_by_comm.values, color=comm_colors, edgecolor='white')
for i, (label, val) in enumerate(risk_by_comm.items()):
    axes[0].text(i, val + 0.02, f'{val:.2f}', ha='center', fontweight='bold', fontsize=11)
axes[0].set_title('Avg Composite Risk Score', fontweight='bold')
axes[0].set_ylabel('Average Risk Score (0-3)')
axes[0].set_ylim(0, 2.5)
axes[0].spines['top'].set_visible(False)
axes[0].spines['right'].set_visible(False)

# Chart B: HAC penalty rate
hac_by_comm = df_nurse.groupby('comm_group').apply(
    lambda x: (x['Payment Reduction'] == 'Yes').mean() * 100
)
axes[1].bar(hac_by_comm.index, hac_by_comm.values, color=comm_colors, edgecolor='white')
for i, (label, val) in enumerate(hac_by_comm.items()):
    axes[1].text(i, val + 0.5, f'{val:.1f}%', ha='center', fontweight='bold', fontsize=11)
axes[1].set_title('HAC Payment Penalty Rate', fontweight='bold')
axes[1].set_ylabel('% of Hospitals Penalized')
axes[1].set_ylim(0, 50)
axes[1].spines['top'].set_visible(False)
axes[1].spines['right'].set_visible(False)

# Chart C: Average excess readmission ratio
readmission_cols = [c for c in df_nurse.columns if 'READM' in c]
df_nurse['avg_excess_readmission'] = df_nurse[readmission_cols].mean(axis=1)
readm_by_comm = df_nurse.groupby('comm_group')['avg_excess_readmission'].mean()
axes[2].bar(readm_by_comm.index, readm_by_comm.values, color=comm_colors, edgecolor='white')
axes[2].axhline(y=1.0, color='black', linestyle='--', linewidth=1.2, label='Expected = 1.0')
for i, (label, val) in enumerate(readm_by_comm.items()):
    axes[2].text(i, val + 0.002, f'{val:.3f}', ha='center', fontweight='bold', fontsize=11)
axes[2].set_title('Avg Excess Readmission Ratio', fontweight='bold')
axes[2].set_ylabel('Average Excess Readmission Ratio')
axes[2].set_ylim(0.85, 1.05)
axes[2].legend(fontsize=9)
axes[2].spines['top'].set_visible(False)
axes[2].spines['right'].set_visible(False)

fig.suptitle('How Nurse Communication Quality Relates to CMS Financial Risk\nFY 2026',
             fontsize=14, fontweight='bold', y=1.02)

plt.tight_layout()
plt.savefig(r"C:\Users\asim0\Documents\Data\cms-penalty-risk\outputs\figures\06_comm_group_risk_profile.png",
            dpi=150, bbox_inches='tight')
plt.close()
print("Figure 6 saved.")

# ── Figure 7: VBP Score by Nurse Communication Group ──────────────────────────
df_nurse['comm_group'] = pd.cut(df_nurse['nurse_comm_stars'],
                                 bins=[0, 2, 3, 5],
                                 labels=['Low (1-2 stars)', 'Medium (3 stars)', 'High (4-5 stars)'])

df_nurse['Total Performance Score'] = pd.to_numeric(df_nurse['Total Performance Score'], errors='coerce')
vbp_by_comm = df_nurse.groupby('comm_group')['Total Performance Score'].mean()

comm_colors = ['#e74c3c', '#f39c12', '#2ecc71']

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(vbp_by_comm.index, vbp_by_comm.values, color=comm_colors, edgecolor='white')

for bar, val in zip(bars, vbp_by_comm.values):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3,
            f'{val:.1f}', ha='center', va='bottom', fontweight='bold', fontsize=12)

ax.set_title('VBP Total Performance Score by Nurse Communication Rating\nFY 2026',
             fontsize=13, fontweight='bold', pad=15)
ax.set_ylabel('Average VBP Total Performance Score', fontsize=11)
ax.set_xlabel('Nurse Communication Star Rating Group', fontsize=11)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig(r"C:\Users\asim0\Documents\Data\cms-penalty-risk\outputs\figures\07_vbp_by_nurse_comm.png",
            dpi=150, bbox_inches='tight')
plt.close()
print("Figure 7 saved.")

# Nurse comm vs VBP correlation
from scipy import stats

df_corr = df_nurse[['nurse_comm_stars', 'Total Performance Score']].dropna()
r, p = stats.pearsonr(df_corr['nurse_comm_stars'], df_corr['Total Performance Score'])
print(f"\nPearson r (nurse comm vs VBP): {r:.3f}")
print(f"P-value: {p:.6f}")

slope, intercept, r_value, p_value, std_err = stats.linregress(
    df_corr['nurse_comm_stars'], df_corr['Total Performance Score']
)
print(f"Slope: {slope:.2f} (each star increase = +{slope:.1f} VBP points)")

# ── Figure 7: Scatter - Nurse Comm vs VBP (styled) ────────────────────────────
fig, ax = plt.subplots(figsize=(8, 7))
fig.patch.set_facecolor('#FAFAF8')
ax.set_facecolor('#FAFAF8')

ax.scatter(df_corr['nurse_comm_stars'], df_corr['Total Performance Score'],
           alpha=0.25, color='#4A7C6F', edgecolors='none', s=45, zorder=3)

x_line = np.linspace(df_corr['nurse_comm_stars'].min(), df_corr['nurse_comm_stars'].max(), 100)
y_line = slope * x_line + intercept
ax.plot(x_line, y_line, color='#e74c3c', linewidth=1.8, zorder=4)

ax.text(0.03, 0.93, 'r = 0.541 | p < 0.001',
        transform=ax.transAxes, fontsize=10, color='#444',
        fontfamily='serif', fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                  edgecolor='#ddd', alpha=0.8))

fig.text(0.5, 0.97,
         'Higher nurse communication ratings align with stronger federal quality performance',
         ha='center', fontsize=9.5, color='#555', fontfamily='serif', fontstyle='italic')

ax.set_title('Nurse Communication vs CMS VBP Performance',
             fontsize=13, fontweight='bold', fontfamily='serif', pad=16, color='#1a1a1a')

ax.set_xlabel('Nurse Communication Star Rating', fontsize=11,
              fontfamily='serif', color='#555', labelpad=10)
ax.set_ylabel('VBP Total Performance Score', fontsize=11,
              fontfamily='serif', color='#555', labelpad=10)

ax.tick_params(colors='#555', labelsize=10)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#ddd')
ax.spines['bottom'].set_color('#ddd')
ax.yaxis.grid(True, color='#e8e8e8', linewidth=0.8, zorder=0)
ax.set_axisbelow(True)

ax.text(0.98, 0.02, 'Source: CMS Hospital Quality Data · FY 2026',
        transform=ax.transAxes, fontsize=8, color='#999',
        ha='right', va='bottom', fontfamily='serif')

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig(r"C:\Users\asim0\Documents\Data\cms-penalty-risk\outputs\figures\07_nurse_comm_vbp_scatter.png",
            dpi=180, bbox_inches='tight', facecolor='#FAFAF8')
plt.close()
print("Figure 7 saved.")
