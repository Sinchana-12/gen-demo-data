# Reference for Generating `patient_histories` Data

This document summarizes all enums, value ranges, and field notes inferred for generating realistic and valid `patient_histories` documents for dialysis patients.

**Note: This document reflects the ACTUAL prescription parameters found in the database as of the latest analysis.**

---

## 1. Vascular Access (`vascular_access.value`)
- **Options:**
  - AV Fistula
  - AV Graft
  - Internal Jugular Vein (IJV)
  - Perm Catheter
  - Femoral Catheter

---

## 2. Dry Weight Units (`dry_weight.units.unit`)
- **Unit:**
  - kg

---

## 3. Prescription Parameters (`prescription_params`)

**ACTUAL PARAMETERS IN DATABASE (6 total):**

| Code         | Name                        | Unit    | Value/Range         | Enum/Dropdown Options |
|--------------|-----------------------------|---------|---------------------|----------------------|
| QBLD         | Quantum of blood            | ml/hr   | 300–500             |                      |
| QDLST        | Quantum of dialysate        | ml/hr   | 500–800             |                      |
| DLSTTEMP     | Dialysate temperature       | ˚c      | 35–37.5             |                      |
| BICON        | Dialysate Bicarbonate (DBIC)| mmol/l  | 32–40               |                      |
| DLZRUSE      | Dialyzer Use                |         |                     | Single, Multi        |
| HEPTYPE      | Heparin Type                |         |                     | Free, Rigid, Regular (Systemic) |

- **Dropdown/Enum Options:**
  - DLZRUSE: Single, Multi
  - HEPTYPE: Free, Rigid, Regular (Systemic)

**PARAMETERS NOT FOUND IN DATABASE:**
The following parameters were previously documented but are NOT present in the actual database:
- DIALYSIS_DURATION (Dialysis Duration)
- UFGOAL (UF Goal)
- UFACHVD (UF Achieved)  
- POSTWT (Post HD Weight)
- PREWT (Pre HD Weight)
- DRYWT (Dry Weight)
- IDWG (Interdialytic Weight Gain)
- WTDIFF (Weight Diff)

---

## 4. Diagnosis, Vaccination, and Shots
- **diagnosis:** Free text (e.g., "Diabetic Nephropathy", "Hypertensive Nephrosclerosis")
- **vaccination.infection:** Free text (e.g., "Hepatitis B", "Influenza", "COVID-19")
- **vaccination.shots.kind:** Free text (e.g., "dose1", "dose2", "booster")

---

## 5. Other Field Notes
- **audit:** Use a valid user from the org as created_by/updated_by, with current timestamps.
- **All values should be realistic and internally consistent for a dialysis patient profile.**
- **dialysis_runtime:** Contains hours and minutes fields (numeric values)

---

*This file reflects actual database content as verified through database analysis. Last updated based on jano_core.patient_histories collection analysis.* 