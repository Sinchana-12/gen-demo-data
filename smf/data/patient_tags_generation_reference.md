# Patient Tags Generation Reference

## Overview
This document describes the `generate_patient_tags.py` script that creates realistic patient tag data for SMF (Sundaram Medical Foundation) dialysis patients. The script generates medically accurate data based on CKD/dialysis patient profiles and follows established medical guidelines.

## Script Purpose
- Generate comprehensive patient tags across three categories: serology, allergies, and conditions
- Create age and gender-appropriate medical data
- Follow medical best practices for CKD/dialysis patient care
- Match existing database schema for immediate import

## Database Schema
The patient_tags collection follows this structure:
```json
{
  "_id": "ObjectId (auto-generated)",
  "patientId": "ObjectId (references patients collection)",
  "category": "String (serology|allergies|conditions)", 
  "tags": [
    {
      "name": "String (tag name)",
      "since": "Date (when condition/result was first noted)"
    }
  ],
  "audit": {
    "created_on": "Date",
    "updated_on": "Date", 
    "created_by": "String (user ID)",
    "updated_by": "String (user ID)"
  },
  "version": "String (typically '1')",
  "organizationId": "ObjectId (SMF org ID)"
}
```

## Categories Generated

### 1. Serology Tags (`category: "serology"`)
**Purpose**: Infectious disease screening results for dialysis patients

**Core Tests** (Required for all dialysis patients):
- HIV - Non Reactive
- HBsAg - Non Reactive  
- Anti-HCV - Non Reactive
- HBeAg - Non Reactive
- Anti-HBc - Non Reactive

**Additional Tests** (Age-based, more common in older patients):
- CMV IgM/IgG
- EBV IgM/IgG  
- Hepatitis A IgM/IgG
- VDRL - Non Reactive
- Toxoplasma IgM/IgG

**Positive Results** (15% probability for realistic prevalence):
- Anti-HCV - Positive
- HBsAg - Positive
- CMV IgG - Positive (common)
- Hepatitis A IgG - Positive (immunity)

**Medical Logic**:
- All dialysis patients require infectious disease screening
- Older patients (>50) get more comprehensive testing
- Positive HCV/HBV results include viral load monitoring
- Test dates within last 1-3 years for active patients

### 2. Allergy Tags (`category: "allergies"`)
**Purpose**: Document patient allergies for safe medical care

**Categories**:
- **Environmental**: Dust Mites, Pollen, Mold, Pet Dander, Smoke
- **Food**: Nuts, Shellfish, Eggs, Dairy, Soy, Wheat  
- **Drug**: Penicillin, Sulfa Drugs, Contrast Dye, Heparin, Iron Supplements, ACE Inhibitors
- **Contact**: Latex, Nickel, Adhesives, Cleaning Products

**Medical Logic**:
- 60% of patients have no documented allergies (realistic prevalence)
- Drug allergies more important for dialysis patients
- Environmental allergies most common (60% probability)
- Latex allergies significant due to healthcare exposure
- Allergy onset dates span patient's lifetime

### 3. Condition Tags (`category: "conditions"`)
**Purpose**: Document medical conditions and comorbidities

**Primary Conditions** (Leading to CKD):
- Diabetes Mellitus Type 2
- Hypertension  
- Diabetic Nephropathy
- Hypertensive Nephrosclerosis
- Polycystic Kidney Disease
- Glomerulonephritis
- IgA Nephropathy

**Cardiovascular Comorbidities** (Age-dependent):
- Coronary Artery Disease
- Congestive Heart Failure
- Atrial Fibrillation
- Peripheral Artery Disease
- Cerebrovascular Disease
- Left Ventricular Hypertrophy

**CKD Complications** (70% of dialysis patients):
- Secondary Hyperparathyroidism
- Anemia of CKD
- Bone Disease (CKD-MBD)
- Metabolic Acidosis
- Mineral Bone Disorder
- Chronic Fatigue

**Other Conditions** (Age/gender-specific):
- Osteoporosis (more common in elderly females)
- Depression, Sleep Apnea
- Gout, Thyroid Disease
- Chronic Pain, Neuropathy

**Medical Logic**:
- All CKD patients have 1-2 primary conditions
- Cardiovascular comorbidities increase with age (60+ years get 2-4)
- CKD complications develop as kidney function declines
- Condition onset dates reflect realistic disease progression

## Age and Gender Considerations

### Age-Based Patterns:
- **Young (<35)**: Fewer comorbidities, basic serology
- **Middle-aged (35-55)**: Increasing cardiovascular risk
- **Elderly (55+)**: Multiple comorbidities, comprehensive testing

### Gender-Specific:
- **Female >50**: Higher osteoporosis risk
- **Males**: Slightly higher cardiovascular disease prevalence
- **Both**: Equal CKD complication rates

## Data Generation Statistics

### Generated for 19 SMF Patients:
- **Total Records**: 42 patient_tags records
- **Serology Records**: 19 (100% of patients)
- **Allergy Records**: 4 (21% of patients - realistic prevalence)
- **Condition Records**: 19 (100% of patients)
- **Total Individual Tags**: 199 tags across all categories

### Realistic Distributions:
- **Serology**: 3-9 tests per patient (avg 5.2)
- **Allergies**: 1-5 allergies when present (avg 2.8)
- **Conditions**: 1-10 conditions per patient (avg 5.0)

## Medical Validation

### Clinical Accuracy:
- Based on CDC guidelines for immunocompromised patients
- Follows nephrology best practices for CKD care
- Realistic prevalence rates for each condition type
- Age-appropriate disease progression timelines

### Database Compliance:
- Matches existing patient_tags schema exactly
- Uses correct MongoDB ObjectId references
- Includes proper audit trails with valid SMF user IDs
- Compatible for direct database import

## Usage
```bash
cd smf/scripts
python3 generate_patient_tags.py
```

**Output**: `../data/generated_patient_tags.json`

## Integration Notes
- Patient IDs match existing SMF patient records
- Organization ID references SMF (685c18f504a6c31893801427)
- User IDs reference actual SMF staff for audit trails
- Date formats compatible with MongoDB import processes
- Ready for direct insertion into patient_tags collection 