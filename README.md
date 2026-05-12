# Nurse Communication and Federal Hospital Quality Performance
## A Cross-Dataset Analysis of CMS Quality Programs and Hospital Performance

> A Python and SQL analysis joining CMS HCAHPS patient experience data with CMS Value-Based Purchasing, Hospital Readmissions Reduction Program, and Hospital-Acquired Condition data across 2,400+ U.S. hospitals, finding that nurse communication quality strongly aligns with broader federal quality performance while different penalty programs capture distinct operational dimensions.

---

## Project Overview

The previous project in this portfolio found that nurse communication quality was consistently associated with lower-than-expected hospital readmission rates across all six CMS-tracked conditions.

This project extends that analysis by asking a broader operational question:

> **Does nurse communication quality align with overall federal hospital quality performance beyond readmissions alone?**

To answer this, I joined CMS HCAHPS patient experience data with three major CMS reimbursement and quality programs: Hospital Value-Based Purchasing (VBP), Hospital Readmissions Reduction Program (HRRP), and Hospital-Acquired Condition Reduction Program (HACRP).

The analysis finds that nurse communication ratings strongly align with CMS Value-Based Purchasing performance scores (r = 0.541, p < 0.001), with each additional star in nurse communication associated with approximately +6.2 points in VBP Total Performance Score. Hospitals with high nurse communication ratings averaged VBP scores nearly 59% higher than those with low ratings.

At the same time, nurse communication showed little relationship with HAC penalties tied to hospital-acquired infections and procedural safety failures, suggesting communication quality connects most strongly to patient-facing and care coordination dimensions of hospital performance rather than protocol-driven safety events.

A secondary analysis found that 93.2% of hospitals in the dataset were exposed to at least one CMS penalty or reimbursement adjustment program during FY 2026.

---

## Business Context

CMS reimbursement programs increasingly tie hospital revenue to measurable operational and quality outcomes. Hospitals are evaluated across multiple dimensions simultaneously:

| Program | Focus |
|---------|-------|
| HRRP | Excess patient readmissions |
| HACRP | Hospital-acquired infections and safety events |
| VBP | Clinical outcomes, efficiency, safety, and patient experience |

These programs directly influence Medicare reimbursement levels and are closely monitored by hospital finance, quality, and operations leadership.

Patient experience metrics are often treated as soft measures. If nurse communication quality consistently aligns with broader federal performance systems, it may function as a practical leading indicator of operational quality rather than simply a satisfaction metric.

---

## Datasets

**Dataset 1: CMS HCAHPS Patient Survey (2024 Reporting Year)**
- Source: data.cms.gov
- Used for: nurse communication star ratings (1 to 5) per facility
- Reused from prior project in this portfolio

**Dataset 2: CMS Hospital Value-Based Purchasing Total Performance Score (FY 2026)**
- Source: data.cms.gov
- Used for: composite VBP performance score per facility

**Dataset 3: CMS Hospital Readmissions Reduction Program (FY 2026)**
- Source: data.cms.gov
- Used for: excess readmission ratio per facility per condition

**Dataset 4: CMS Hospital-Acquired Condition Reduction Program (FY 2026)**
- Source: data.cms.gov
- Used for: total HAC score and payment reduction flag per facility

All datasets were joined using the CMS facility identifier.

---

## Methodology

### 1. Data Cleaning and Standardization (Python, pandas)
- Removed hospitals with missing or unavailable metrics
- Standardized facility identifiers across all CMS datasets
- Converted performance measures to numeric formats with coercion to handle footnote values
- Pivoted HRRP from long format (one row per condition) to wide format (one row per hospital)

### 2. Cross-Dataset Joining
- Joined HCAHPS, VBP, HRRP, and HACRP datasets on CMS facility ID using inner joins
- Produced a unified hospital-level performance table across all programs
- Final merged dataset: 2,422 hospitals with complete records

### 3. Statistical Analysis
- Computed Pearson correlations between nurse communication ratings and VBP Total Performance Score, excess readmission ratios, and HAC penalty rates
- Built simple linear regression to estimate effect size of nurse communication on VBP performance
- Calculated grouped averages by nurse communication star rating (Low: 1-2, Medium: 3, High: 4-5)

### 4. Exposure Tier Construction
Hospitals were flagged as at risk or not at risk under each program:
- HRRP risk: any condition with excess readmission ratio above 1.0
- HACRP risk: payment reduction applied (Yes/No)
- VBP risk: total performance score below national median

Flags were summed into a composite exposure score ranging from 0 (no exposure) to 3 (exposure across all three programs).

---

## Results

### 1. Nurse Communication Aligns with Broader Federal Quality Performance

Across 2,400+ hospitals, nurse communication ratings showed a statistically significant moderate positive correlation with CMS Value-Based Purchasing performance.

| Metric | Result |
|--------|--------|
| Pearson correlation | r = 0.541 |
| Statistical significance | p < 0.001 |
| Effect size | +6.2 VBP points per star |

Hospitals with high nurse communication ratings (4-5 stars) averaged VBP scores nearly 59% higher than those with low ratings (1-2 stars).

| Nurse Communication Group | Avg VBP Score |
|---------------------------|---------------|
| Low (1-2 stars) | 23.5 |
| Medium (3 stars) | 28.3 |
| High (4-5 stars) | 37.3 |

VBP extends beyond patient satisfaction alone. It incorporates clinical outcomes, efficiency, safety, and patient experience. This suggests nurse communication quality aligns with broader operational and care coordination performance, not simply perception metrics in isolation.

### 2. Relationship with Readmissions Remains Consistent

The relationship identified in the previous project remained directionally consistent here. Hospitals with stronger nurse communication ratings tended to maintain lower excess readmission ratios, particularly for chronic medical conditions where discharge comprehension and self-management matter most.

| Nurse Communication Tier | Avg Excess Readmission Ratio |
|--------------------------|------------------------------|
| Low (1-2 stars) | 1.017 |
| Medium (3 stars) | 1.002 |
| High (4-5 stars) | 0.994 |

Only high communication hospitals remained below the operationally meaningful 1.0 threshold on average.

### 3. HAC Penalties Showed Little Relationship with Communication

Unlike VBP and readmissions, HAC penalties showed minimal variation across nurse communication groups.

| Nurse Communication Tier | HAC Penalty Rate |
|--------------------------|-----------------|
| Low (1-2 stars) | 23.7% |
| Medium (3 stars) | 24.7% |
| High (4-5 stars) | 24.8% |

This distinction is operationally meaningful. Hospital-acquired infections, falls, and procedural safety failures are driven more heavily by infection control systems, staffing processes, and clinical protocol execution. The weak relationship suggests nurse communication quality primarily connects to patient-facing coordination and recovery processes rather than protocol-driven safety events.

### 4. CMS Penalty Exposure Across 2,422 U.S. Hospitals

A secondary analysis examined how many hospitals were simultaneously exposed to multiple CMS quality and reimbursement programs.

| Exposure Tier | Hospitals | Share |
|---------------|-----------|-------|
| No Exposure (0 programs) | 165 | 6.8% |
| Single Exposure (1 program) | 959 | 39.6% |
| Dual Exposure (2 programs) | 961 | 39.7% |
| Triple Exposure (3 programs) | 337 | 13.9% |

93.2% of hospitals in the dataset were exposed to at least one federal reimbursement adjustment or penalty program during FY 2026.

---

## Operational Implications

This analysis suggests nurse communication quality functions as more than a patient satisfaction metric. Hospitals with stronger nurse communication ratings consistently aligned with better Value-Based Purchasing performance, lower readmission burden, and stronger broader federal quality outcomes.

The lack of relationship with HAC penalties helps clarify where communication matters operationally and where it does not. Communication quality appears most relevant in areas involving patient comprehension, care coordination, discharge understanding, and follow-through. It appears less connected to protocol-driven procedural safety events.

For hospital systems, patient experience metrics may provide earlier operational signals than reimbursement penalties alone. Nurse communication scores are already collected nationally and may help identify broader quality performance patterns before downstream financial consequences fully emerge.

---

## Limitations

- Correlations are associational, not causal. Well-resourced hospitals may perform better across multiple dimensions simultaneously due to factors not captured here, including staffing ratios, facility type, teaching status, and patient population characteristics.
- VBP partially incorporates patient experience measures, meaning some structural overlap with nurse communication is expected. The observed relationship therefore should not be interpreted as fully independent.
- The composite exposure score uses a median split for VBP risk flagging, meaning results depend on the distribution of the dataset rather than an absolute performance threshold.
- HRRP and HACRP data reflect FY 2026 reporting periods while HCAHPS reflects 2024. Time periods are overlapping but not identical.
- HAC penalty rates are relatively flat across communication groups, which reflects that HAC captures genuinely different operational processes rather than a limitation of the analysis.

---

## Project Structure

```
cms-penalty-risk/
├── README.md
├── data/
│   ├── raw/
│   │   ├── FY_2026_Hospital_Readmissions_Reduction_Program_Hospital.csv
│   │   ├── FY_2026_HAC_Reduction_Program_Hospital.csv
│   │   ├── hvbp_tps.csv
│   │   └── hospital_kpis_2024.csv
│   └── processed/
│       └── hospital_risk_profile.csv
├── src/
│   ├── analyze.py
│   └── make_figures.py
├── outputs/
│   └── figures/
│       ├── 01_composite_risk_distribution.png
│       ├── 02_triple_exposure_by_state.png
│       ├── 05_nurse_comm_by_risk_tier.png
│       ├── 06_vbp_by_nurse_comm.png
│       └── 07_nurse_comm_vbp_scatter.png
├── requirements.txt
└── README.md
```

---

## Tools and Skills Demonstrated

- Multi-source dataset integration (Python, pandas)
- Long-to-wide data transformation (pivot_table)
- Composite risk scoring and flag engineering
- Pearson correlation and simple linear regression (scipy.stats)
- Comparative analysis across federal program types
- Healthcare reimbursement data interpretation (HRRP, HACRP, VBP, HCAHPS)
- Analytical storytelling and operational framing
- Reproducible pipeline design

---

## Portfolio Context

This project is the fourth in a healthcare operations analytics portfolio:

| Project | Focus |
|---------|-------|
| Preventable Punchlisting Analysis | Root-cause analysis of operational failure in healthcare IT deployment workflows |
| Hospital Patient Experience Analytics | Performance monitoring and insight generation from national HCAHPS data |
| Nurse Communication and Readmissions | Cross-dataset analysis connecting patient experience metrics to clinical outcome data |
| Nurse Communication and Federal Quality Performance *(this project)* | Connecting patient experience to broader federal quality and reimbursement systems |

Together these projects trace a broader analytical theme:

**Diagnose operational breakdown → Monitor performance at scale → Connect experience metrics to clinical outcomes → Test whether communication quality signals broader federal performance.**

---

## Author

Asim Bacchus
[LinkedIn](https://www.linkedin.com/in/asimbacchus/) | [GitHub](https://github.com/Asim-Bacchus)