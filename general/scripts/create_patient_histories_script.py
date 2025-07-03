import json
import random
from datetime import datetime, timedelta

# Patient IDs from SMF
patient_ids = [
    "685cf29e04a6c318938015f1",  # Priya Krishnan
    "685cf29f04a6c31893801620",  # Suresh Reddy
    "685cf2a004a6c31893801650",  # Lakshmi Nair
    "685cf2a104a6c3189380167e",  # Arun Kumar
    "685cf2a104a6c318938016ad",  # Deepika Patel
    "685cf2a304a6c318938016dc",  # Venkatesh Iyer
    "685cf2a304a6c3189380170b",  # Kavitha Menon
    "685cf2a504a6c31893801743",  # Anitha Kumari
    "685cf2a604a6c31893801772",  # Manoj Kumar
    "685cf2a604a6c318938017a1",  # Sita Devi
    "685cf2a704a6c318938017d0",  # Rajesh Gupta
    "685cf2a804a6c318938017ff",  # Pooja Singh
    "685cf2a904a6c3189380182e",  # Kiran Rao
    "685cf2aa04a6c3189380185d",  # Meera Sharma
    "685cf2aa04a6c3189380188c",  # Ashok Pillai
    "685cf2ab04a6c318938018bb",  # Divya Bhat
    "685cf2ac04a6c318938018ea",  # Santosh Kumar
    "685cf2ad04a6c3189380191c",  # Radha Krishnan
    "685cf2e704a6c31893801948"   # Ramesh Sharma
]

# Options provided by user
vascular_access_types = [
    'AV Fistula',
    'AV Graft',
    'Internal Jugular Vein (IJV)',
    'Perm Catheter',
    'Femoral Catheter'
]

dialyzer_use_options = ['Single', 'Multi']
heparin_type_options = ['Free', 'Rigid', 'Regular (Systemic)']

# Medical diagnosis templates
diagnoses = [
    "Chronic kidney disease Stage 5, secondary to diabetic nephropathy. Patient has been on hemodialysis for {} years with {} compliance and {} vascular access.",
    "End-stage renal disease due to hypertensive nephrosclerosis. {} history of cardiovascular complications, currently stable on dialysis.",
    "Chronic kidney disease Stage 5, etiology unclear. Patient initiated on dialysis {} months ago with {} adaptation to treatment.",
    "Polycystic kidney disease with progression to end-stage renal disease. {} on dialysis with {} overall clinical status.",
    "Glomerulonephritis leading to chronic kidney disease. Patient has {} response to dialysis therapy over the past {} years.",
    "Chronic kidney disease secondary to chronic glomerulonephritis. {} course with {} vascular access complications.",
    "End-stage renal disease, likely secondary to diabetes mellitus. Patient shows {} compliance with dialysis regimen."
]

def generate_patient_history(patient_id, index):
    # Generate varied but realistic values
    vascular_access = random.choice(vascular_access_types)
    
    # Create date for vascular access (1-3 years ago)
    access_date = datetime.now() - timedelta(days=random.randint(365, 1095))
    access_date_str = access_date.strftime("%d-%m-%Y")
    
    # Dry weight based on typical ranges (45-75 kg)
    dry_weight = str(random.randint(45, 75))
    
    # Dialysis runtime (3-4 hours typical)
    runtime_hours = random.choice([3, 4])
    
    # Prescription parameters with realistic ranges
    qbld_value = str(random.randint(300, 450))
    qdlst_value = str(random.randint(500, 750))
    temp_value = str(round(random.uniform(35.5, 37.0), 1))
    bicon_value = str(random.randint(25, 32))
    
    dialyzer_use = random.choice(dialyzer_use_options)
    heparin_type = random.choice(heparin_type_options)
    
    # Generate diagnosis
    diagnosis_template = random.choice(diagnoses)
    if "{}" in diagnosis_template:
        # Fill in template variables
        years = random.randint(1, 5)
        compliance_options = ["excellent", "good", "fair"]
        access_status = ["stable", "well-functioning", "patent"]
        history_options = ["No", "Minimal", "Significant"]
        adaptation_options = ["good", "excellent", "satisfactory"]
        months = random.randint(6, 24)
        status_options = ["stable", "improving", "good"]
        response_options = ["excellent", "good", "satisfactory"]
        course_options = ["Uncomplicated", "Smooth", "Generally stable"]
        complications = ["minimal", "no significant", "occasional"]
        
        # Replace placeholders based on template
        if "years with" in diagnosis_template:
            diagnosis = diagnosis_template.format(
                years, 
                random.choice(compliance_options), 
                random.choice(access_status)
            )
        elif "history of" in diagnosis_template:
            diagnosis = diagnosis_template.format(random.choice(history_options))
        elif "months ago" in diagnosis_template:
            diagnosis = diagnosis_template.format(
                months, 
                random.choice(adaptation_options)
            )
        elif "on dialysis with" in diagnosis_template:
            diagnosis = diagnosis_template.format(
                random.choice(status_options).capitalize(),
                random.choice(status_options)
            )
        elif "response to" in diagnosis_template:
            diagnosis = diagnosis_template.format(
                random.choice(response_options).capitalize(),
                years
            )
        elif "course with" in diagnosis_template:
            diagnosis = diagnosis_template.format(
                random.choice(course_options),
                random.choice(complications)
            )
        else:
            diagnosis = diagnosis_template.format(random.choice(compliance_options).capitalize())
    else:
        diagnosis = diagnosis_template
    
    # Generate vaccination records (some patients may have different vaccines)
    vaccinations = []
    
    # COVID-19 vaccination (most patients)
    if random.random() > 0.1:  # 90% have COVID vaccination
        covid_shots = []
        first_shot_date = datetime.now() - timedelta(days=random.randint(300, 600))
        covid_shots.append({
            "date": first_shot_date.strftime("%d-%m-%Y"),
            "count": 1,
            "kind": "Primary",
            "user_id": None,
            "org_id": None
        })
        
        # Second shot
        if random.random() > 0.2:  # 80% have second shot
            second_shot_date = first_shot_date + timedelta(days=random.randint(21, 42))
            covid_shots.append({
                "date": second_shot_date.strftime("%d-%m-%Y"),
                "count": 2,
                "kind": "Primary",
                "user_id": None,
                "org_id": None
            })
        
        vaccinations.append({
            "id": None,
            "version": None,
            "patientId": patient_id,
            "infection": "COVID-19",
            "shots": covid_shots
        })
    
    # Hepatitis B vaccination (important for dialysis patients)
    if random.random() > 0.3:  # 70% have Hepatitis B vaccination
        hep_date = datetime.now() - timedelta(days=random.randint(100, 400))
        vaccinations.append({
            "id": None,
            "version": None,
            "patientId": patient_id,
            "infection": "Hepatitis B",
            "shots": [{
                "date": hep_date.strftime("%d-%m-%Y"),
                "count": 1,
                "kind": "Primary",
                "user_id": None,
                "org_id": None
            }]
        })
    
    # Flu vaccination
    if random.random() > 0.4:  # 60% have flu vaccination
        flu_date = datetime.now() - timedelta(days=random.randint(30, 365))
        vaccinations.append({
            "id": None,
            "version": None,
            "patientId": patient_id,
            "infection": "Influenza",
            "shots": [{
                "date": flu_date.strftime("%d-%m-%Y"),
                "count": 1,
                "kind": "Annual",
                "user_id": None,
                "org_id": None
            }]
        })
    
    # Create the patient history object
    patient_history = {
        "patient_id": patient_id,
        "vascular_access": {
            "value": vascular_access,
            "created": access_date_str
        },
        "dry_weight": {
            "code": "DRYWT",
            "name": "Dry Weight",
            "units": {
                "unit": "Kg",
                "ucum_code": None,
                "is_default": None,
                "ref_value": None,
                "ref_range": None,
                "format": None
            },
            "value": dry_weight
        },
        "dialysis_runtime": {
            "hours": runtime_hours,
            "minutes": 0
        },
        "prescription_params": [
            {
                "code": "QBLD",
                "name": "Quantum of blood",
                "units": {
                    "unit": "ml/hr",
                    "ucum_code": None,
                    "is_default": None,
                    "ref_value": None,
                    "ref_range": {
                        "min": 300,
                        "max": 500,
                        "systolic": None,
                        "diastolic": None
                    },
                    "format": None
                },
                "value": qbld_value
            },
            {
                "code": "QDLST",
                "name": "Quantum of dialysate",
                "units": {
                    "unit": "ml/hr",
                    "ucum_code": None,
                    "is_default": None,
                    "ref_value": None,
                    "ref_range": {
                        "min": 500,
                        "max": 800,
                        "systolic": None,
                        "diastolic": None
                    },
                    "format": None
                },
                "value": qdlst_value
            },
            {
                "code": "DLSTTEMP",
                "name": "Dialysate temperature",
                "units": {
                    "unit": "˚c",
                    "ucum_code": None,
                    "is_default": None,
                    "ref_value": None,
                    "ref_range": {
                        "min": 35,
                        "max": 37.5,
                        "systolic": None,
                        "diastolic": None
                    },
                    "format": None
                },
                "value": temp_value
            },
            {
                "code": "BICON",
                "name": "Bicarb Concentration",
                "units": {
                    "unit": "mmol/l",
                    "ucum_code": None,
                    "is_default": None,
                    "ref_value": None,
                    "ref_range": {
                        "min": 24,
                        "max": 35,
                        "systolic": None,
                        "diastolic": None
                    },
                    "format": None
                },
                "value": bicon_value
            },
            {
                "code": "DLZRUSE",
                "name": "Dialyzer Use",
                "units": {
                    "unit": "",
                    "ucum_code": None,
                    "is_default": None,
                    "ref_value": None,
                    "ref_range": {
                        "min": None,
                        "max": None,
                        "systolic": None,
                        "diastolic": None
                    },
                    "format": None
                },
                "value": dialyzer_use
            },
            {
                "code": "HEPTYPE",
                "name": "Heparin Type",
                "units": {
                    "unit": "",
                    "ucum_code": None,
                    "is_default": None,
                    "ref_value": None,
                    "ref_range": {
                        "min": None,
                        "max": None,
                        "systolic": None,
                        "diastolic": None
                    },
                    "format": None
                },
                "value": heparin_type
            }
        ],
        "diagnosis": diagnosis,
        "vaccination": vaccinations,
        "audit": {
            "created_on": datetime.now().isoformat() + "Z",
            "updated_on": datetime.now().isoformat() + "Z",
            "created_by": "685c1ef404a6c3189380144c",
            "updated_by": "685c1ef404a6c3189380144c"
        }
    }
    
    return patient_history

# Generate all patient histories
patient_histories = []
for i, patient_id in enumerate(patient_ids):
    history = generate_patient_history(patient_id, i)
    patient_histories.append(history)

# Save to JSON file
with open('create_patient_histories.json', 'w') as f:
    json.dump(patient_histories, f, indent=2)

print(f"Generated {len(patient_histories)} patient histories")
print("File saved as: create_patient_histories.json") 