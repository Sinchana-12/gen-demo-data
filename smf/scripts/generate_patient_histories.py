#!/usr/bin/env python3

import json
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any

# Patient IDs for SMF org
PATIENT_IDS = [
    "685cf29e04a6c318938015f1", "685cf29f04a6c31893801620", "685cf2a004a6c3189380164f",
    "685cf2a104a6c3189380167e", "685cf2a104a6c318938016ad", "685cf2a304a6c318938016dc",
    "685cf2a304a6c3189380170b", "685cf2a504a6c31893801743", "685cf2a604a6c31893801772",
    "685cf2a604a6c318938017a1", "685cf2a704a6c318938017d0", "685cf2a804a6c318938017ff",
    "685cf2a904a6c3189380182e", "685cf2aa04a6c3189380185d", "685cf2aa04a6c3189380188c",
    "685cf2ab04a6c318938018bb", "685cf2ac04a6c318938018ea", "685cf2ad04a6c31893801919",
    "685cf2e704a6c31893801948"
]

# Valid users for audit (Dr. Rajesh Kumar and SMF staff)
USERS = [
    "685c1c7504a6c31893801435",  # Dr. Rajesh Kumar
    "685c1f9e04a6c318938014a4",  # Anitha Kumari (staff)
    "685c1f0704a6c31893801457",  # Arjun Menon (staff)
    "685c1f4704a6c31893801478",  # Deepika Singh (staff)
    "685c1f1c04a6c31893801462",  # Kavitha Rao (staff)
    "685c1f7404a6c3189380148e",  # Lakshmi Devi (staff)
    "685c1fbe04a6c318938014af",  # Manoj Kumar T (staff)
    "685c1ef404a6c3189380144c",  # Priya Nair (staff)
    "685c1f8904a6c31893801499",  # Ravi Shankar (staff)
    "685c1f3104a6c3189380146d"   # Suresh Babu K (staff)
]

# Patient demographics (sample from actual data)
PATIENT_DEMOGRAPHICS = {
    "685cf29e04a6c318938015f1": {"name": "Priya Krishnan", "gender": "female", "age": 45, "blood_group": "B+"},
    "685cf29f04a6c31893801620": {"name": "Suresh Reddy", "gender": "male", "age": 55, "blood_group": "O+"},
    "685cf2a004a6c3189380164f": {"name": "Lakshmi Nair", "gender": "female", "age": 47, "blood_group": "AB+"},
    "685cf2a104a6c3189380167e": {"name": "Arun Kumar", "gender": "male", "age": 40, "blood_group": "A-"},
    "685cf2a104a6c318938016ad": {"name": "Deepika Patel", "gender": "female", "age": 35, "blood_group": "O-"},
    "685cf2a304a6c318938016dc": {"name": "Venkatesh Iyer", "gender": "male", "age": 60, "blood_group": "B-"},
    "685cf2a304a6c3189380170b": {"name": "Kavitha Menon", "gender": "female", "age": 43, "blood_group": "A+"},
    "685cf2a504a6c31893801743": {"name": "Anitha Kumari", "gender": "female", "age": 30, "blood_group": "AB-"},
    "685cf2a604a6c31893801772": {"name": "Manoj Kumar", "gender": "male", "age": 37, "blood_group": "B+"},
    "685cf2a604a6c318938017a1": {"name": "Sita Devi", "gender": "female", "age": 53, "blood_group": "A+"},
    "685cf2a704a6c318938017d0": {"name": "Rajesh Gupta", "gender": "male", "age": 62, "blood_group": "O-"},
    "685cf2a804a6c318938017ff": {"name": "Pooja Singh", "gender": "female", "age": 33, "blood_group": "B-"},
    "685cf2a904a6c3189380182e": {"name": "Kiran Rao", "gender": "male", "age": 38, "blood_group": "A-"},
    "685cf2aa04a6c3189380185d": {"name": "Meera Sharma", "gender": "female", "age": 57, "blood_group": "AB+"},
    "685cf2aa04a6c3189380188c": {"name": "Ashok Pillai", "gender": "male", "age": 49, "blood_group": "O+"},
    "685cf2ab04a6c318938018bb": {"name": "Divya Bhat", "gender": "female", "age": 36, "blood_group": "B+"},
    "685cf2ac04a6c318938018ea": {"name": "Santosh Kumar", "gender": "male", "age": 67, "blood_group": "A+"},
    "685cf2ad04a6c31893801919": {"name": "Radha Krishnan", "gender": "female", "age": 42, "blood_group": "O-"},
    "685cf2e704a6c31893801948": {"name": "Ramesh Sharma", "gender": "male", "age": 50, "blood_group": "A+"}
}

# Reference data from the patient_histories_generation_reference.md
VASCULAR_ACCESS_OPTIONS = [
    "AV Fistula", "AV Graft", "Internal Jugular Vein (IJV)", 
    "Perm Catheter", "Femoral Catheter"
]

# Age and gender-appropriate diagnoses with detailed clinical information
DIAGNOSIS_OPTIONS = {
    "young_male": [
        "IgA Nephropathy with progressive chronic kidney disease, currently Stage 4 (eGFR 15-29 ml/min/1.73m²), with proteinuria and hypertension",
        "Focal Segmental Glomerulosclerosis (FSGS), primary variant, with nephrotic syndrome and progressive decline in renal function over 3 years",
        "Chronic Glomerulonephritis, post-infectious type, with chronic kidney disease Stage 5 (eGFR <15 ml/min/1.73m²) requiring renal replacement therapy",
        "Hereditary Nephritis (Alport Syndrome) with sensorineural hearing loss and progressive chronic kidney disease, currently on hemodialysis"
    ],
    "young_female": [
        "IgA Nephropathy with chronic kidney disease Stage 4, presenting with episodic gross hematuria and proteinuria (2+ protein)",
        "Focal Segmental Glomerulosclerosis (FSGS), secondary to obesity, with nephrotic syndrome and steroid resistance",
        "Autosomal Dominant Polycystic Kidney Disease (ADPKD), early onset variant, with bilateral enlarged kidneys and declining eGFR",
        "Systemic Lupus Erythematosus with Class IV Lupus Nephritis, chronic kidney disease Stage 5, requiring immunosuppressive therapy"
    ],
    "middle_aged_male": [
        "Diabetic Nephropathy secondary to Type 2 Diabetes Mellitus (15-year duration), with chronic kidney disease Stage 5, diabetic retinopathy, and peripheral neuropathy",
        "Hypertensive Nephrosclerosis with chronic kidney disease Stage 5, long-standing hypertension (20+ years), left ventricular hypertrophy",
        "Chronic Kidney Disease Stage 5 of unknown etiology, likely chronic glomerulonephritis, with anemia and secondary hyperparathyroidism",
        "Polycystic Kidney Disease (ADPKD) with multiple bilateral renal cysts, chronic kidney disease Stage 5, and family history of PKD"
    ],
    "middle_aged_female": [
        "Diabetic Nephropathy secondary to Type 2 Diabetes Mellitus (12-year duration), with chronic kidney disease Stage 5 and diabetic gastroparesis",
        "Hypertensive Nephrosclerosis with chronic kidney disease Stage 5, resistant hypertension on multiple antihypertensive medications",
        "Autosomal Dominant Polycystic Kidney Disease (ADPKD) with massive bilateral kidney enlargement, chronic pain, and recurrent UTIs",
        "Chronic Interstitial Nephritis, likely analgesic-induced, with chronic kidney disease Stage 5 and history of chronic pain syndrome"
    ],
    "older_male": [
        "Diabetic Nephropathy secondary to Type 2 Diabetes Mellitus (20+ year duration), with chronic kidney disease Stage 5, coronary artery disease, and diabetic foot ulcers",
        "Hypertensive Nephrosclerosis with chronic kidney disease Stage 5, congestive heart failure (EF 35%), and cerebrovascular disease",
        "Chronic Kidney Disease Stage 5, multifactorial etiology (diabetes + hypertension + aging), with anemia, bone disease, and cardiovascular complications",
        "Ischemic Nephropathy secondary to renovascular disease, with chronic kidney disease Stage 5, peripheral arterial disease, and history of myocardial infarction"
    ],
    "older_female": [
        "Diabetic Nephropathy secondary to Type 2 Diabetes Mellitus (18-year duration), with chronic kidney disease Stage 5, diabetic retinopathy, and osteoporosis",
        "Hypertensive Nephrosclerosis with chronic kidney disease Stage 5, diastolic heart failure, and history of stroke",
        "Chronic Kidney Disease Stage 5, likely hypertensive nephrosclerosis, with secondary hyperparathyroidism, anemia, and chronic fatigue",
        "Chronic Glomerulonephritis with chronic kidney disease Stage 5, possible membranous nephropathy, with history of nephrotic syndrome in past"
    ]
}

# Comprehensive vaccination schedule for CKD/dialysis patients (immunocompromised)
VACCINATION_INFECTIONS = [
    # Core vaccines for all adults
    "Hepatitis B", "Influenza", "COVID-19", "Pneumococcal", "Tetanus/Tdap",
    
    # Additional vaccines for immunocompromised patients (CKD/dialysis)
    "Meningococcal ACWY", "Meningococcal B", "RSV", "Shingles/Zoster",
    
    # Age-appropriate vaccines
    "HPV", "MMR", "Varicella",
    
    # Travel/occupational vaccines (less common but realistic)
    "Hepatitis A", "Japanese Encephalitis", "Typhoid"
]

# Vaccination schedule patterns based on CDC guidelines
VACCINATION_SCHEDULES = {
    "Hepatitis B": {
        "shots": 3,
        "kinds": ["Primary", "Primary", "Primary"],
        "intervals": [0, 30, 180],  # days between shots
        "age_groups": "all",
        "priority": "high"
    },
    "Influenza": {
        "shots": 3,  # Multiple annual shots
        "kinds": ["Annual", "Annual", "Annual"],
        "intervals": [365, 365],  # yearly
        "age_groups": "all",
        "priority": "high"
    },
    "COVID-19": {
        "shots": 4,
        "kinds": ["Primary", "Primary", "Booster", "Booster"],
        "intervals": [0, 21, 180, 365],
        "age_groups": "all",
        "priority": "high"
    },
    "Pneumococcal": {
        "shots": 2,
        "kinds": ["Primary", "Booster"],
        "intervals": [0, 365],  # 1 year apart
        "age_groups": "all",
        "priority": "high"
    },
    "Tetanus/Tdap": {
        "shots": 2,
        "kinds": ["Primary", "Booster"],
        "intervals": [0, 3650],  # 10 years apart
        "age_groups": "all",
        "priority": "high"
    },
    "Meningococcal ACWY": {
        "shots": 2,
        "kinds": ["Primary", "Booster"],
        "intervals": [0, 1825],  # 5 years apart for high-risk
        "age_groups": "all",
        "priority": "medium"
    },
    "Meningococcal B": {
        "shots": 2,
        "kinds": ["Primary", "Primary"],
        "intervals": [0, 30],
        "age_groups": "young",  # <25 years
        "priority": "medium"
    },
    "RSV": {
        "shots": 1,
        "kinds": ["Primary"],
        "intervals": [0],
        "age_groups": "elderly",  # 60+ years
        "priority": "medium"
    },
    "Shingles/Zoster": {
        "shots": 2,
        "kinds": ["Primary", "Primary"],
        "intervals": [0, 60],  # 2-6 months apart
        "age_groups": "elderly",  # 50+ years
        "priority": "medium"
    },
    "HPV": {
        "shots": 3,
        "kinds": ["Primary", "Primary", "Primary"],
        "intervals": [0, 60, 180],
        "age_groups": "young",  # <45 years
        "priority": "low"
    },
    "MMR": {
        "shots": 2,
        "kinds": ["Primary", "Primary"],
        "intervals": [0, 28],
        "age_groups": "young_middle",  # <60 years
        "priority": "low"
    },
    "Varicella": {
        "shots": 2,
        "kinds": ["Primary", "Primary"],
        "intervals": [0, 28],
        "age_groups": "young_middle",  # <60 years
        "priority": "low"
    },
    "Hepatitis A": {
        "shots": 2,
        "kinds": ["Primary", "Primary"],
        "intervals": [0, 180],
        "age_groups": "all",
        "priority": "low"
    },
    "Japanese Encephalitis": {
        "shots": 2,
        "kinds": ["Primary", "Primary"],
        "intervals": [0, 28],
        "age_groups": "all",
        "priority": "very_low"
    },
    "Typhoid": {
        "shots": 1,
        "kinds": ["Primary"],
        "intervals": [0],
        "age_groups": "all",
        "priority": "very_low"
    }
}

# ACTUAL prescription parameters found in database (only 6 parameters)
PRESCRIPTION_PARAMS = [
    {"code": "QBLD", "name": "Quantum of blood", "unit": "ml/hr", "range": (300, 500)},
    {"code": "QDLST", "name": "Quantum of dialysate", "unit": "ml/hr", "range": (500, 800)},
    {"code": "DLSTTEMP", "name": "Dialysate temperature", "unit": "˚c", "range": (35, 37.5)},
    {"code": "BICON", "name": "Bicarb Concentration", "unit": "mmol/l", "range": (24, 35)},  # Updated name to match DB
]

DROPDOWN_OPTIONS = {
    "DLZRUSE": ["Single", "Multi"],
    "HEPTYPE": ["Free", "Rigid", "Regular (Systemic)"]
}

def get_patient_demographics(patient_id: str) -> Dict[str, Any]:
    """Get patient demographics from the complete database"""
    return PATIENT_DEMOGRAPHICS[patient_id]

def get_diagnosis_for_patient(demographics: Dict[str, Any]) -> str:
    """Get age and gender appropriate diagnosis"""
    age = demographics["age"]
    gender = demographics["gender"]
    
    if age < 35:
        key = f"young_{gender}"
    elif age < 55:
        key = f"middle_aged_{gender}"
    else:
        key = f"older_{gender}"
    
    return random.choice(DIAGNOSIS_OPTIONS[key])

def generate_vascular_access() -> Dict[str, Any]:
    """Generate vascular access data"""
    created_date = datetime.now() - timedelta(days=random.randint(30, 365))
    return {
        "value": random.choice(VASCULAR_ACCESS_OPTIONS),
        "created": created_date.strftime("%d-%m-%Y")  # DD-MM-YYYY format to match database
    }

def generate_dry_weight(demographics: Dict[str, Any]) -> Dict[str, Any]:
    """Generate realistic dry weight based on demographics"""
    # Gender and age-based weight ranges
    if demographics["gender"] == "male":
        base_weight = random.uniform(55, 85)
    else:
        base_weight = random.uniform(45, 75)
    
    # Adjust for age
    if demographics["age"] > 60:
        base_weight *= 0.95  # Slightly lower for elderly
    
    weight = round(base_weight, 1)
    
    return {
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
        "value": str(weight)
    }

def generate_dialysis_runtime(demographics: Dict[str, Any]) -> Dict[str, int]:
    """Generate dialysis runtime based on patient needs"""
    # Older or sicker patients might need longer dialysis
    base_hours = 3
    if demographics["age"] > 65:
        base_hours = random.choice([3, 4])
    elif demographics["age"] > 50:
        base_hours = random.choice([3, 3, 4])  # More likely to be 3
    
    minutes = random.choice([0, 30])
    return {
        "hours": base_hours,
        "minutes": minutes
    }

def generate_prescription_params(demographics: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Generate prescription parameters based on actual database schema"""
    params = []
    
    # Generate the 4 numeric parameters
    for param in PRESCRIPTION_PARAMS:
        if param["code"] == "DLSTTEMP":
            value = round(random.uniform(*param["range"]), 1)
        elif param["code"] == "BICON":
            # Adjust bicarbonate based on age (older patients might need higher values)
            min_val, max_val = param["range"]
            if demographics["age"] > 60:
                value = random.randint(max(min_val, 28), max_val)
            else:
                value = random.randint(min_val, max_val)
        else:
            # Adjust blood flow based on gender and age
            if param["code"] == "QBLD":
                min_val, max_val = param["range"]
                if demographics["gender"] == "female" or demographics["age"] > 65:
                    # Lower blood flow for females and elderly
                    value = random.randint(min_val, min_val + 150)
                else:
                    value = random.randint(min_val, max_val)
            else:
                value = random.randint(*param["range"])
        
        param_data = {
            "code": param["code"],
            "name": param["name"],
            "units": {
                "unit": param["unit"],
                "ucum_code": None,
                "is_default": None,
                "ref_value": None,
                "ref_range": {
                    "min": param["range"][0],
                    "max": param["range"][1],
                    "systolic": None,
                    "diastolic": None
                },
                "format": None
            },
            "value": str(value)
        }
        params.append(param_data)
    
    # Add dropdown parameters
    for code, options in DROPDOWN_OPTIONS.items():
        param_names = {
            "DLZRUSE": "Dialyzer Use",
            "HEPTYPE": "Heparin Type"
        }
        
        # Smart selection based on patient profile
        if code == "DLZRUSE":
            # Newer patients more likely to use Single use
            value = "Single" if random.random() < 0.7 else "Multi"
        elif code == "HEPTYPE":
            # Age-based heparin type selection
            if demographics["age"] > 65:
                value = random.choice(["Free", "Regular (Systemic)"])  # Safer for elderly
            else:
                value = random.choice(options)
        else:
            value = random.choice(options)
        
        param_data = {
            "code": code,
            "name": param_names[code],
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
            "value": value
        }
        params.append(param_data)
    
    return params

def is_age_appropriate(vaccine: str, age: int) -> bool:
    """Check if vaccine is age-appropriate based on CDC guidelines"""
    schedule = VACCINATION_SCHEDULES[vaccine]
    age_group = schedule["age_groups"]
    
    if age_group == "all":
        return True
    elif age_group == "young":  # <35
        return age < 35
    elif age_group == "young_middle":  # <60
        return age < 60
    elif age_group == "elderly":  # 50+ (some vaccines) or 60+ (others)
        if vaccine == "Shingles/Zoster":
            return age >= 50
        else:  # RSV
            return age >= 60
    return False

def get_vaccination_probability(vaccine: str, age: int) -> float:
    """Get probability of patient having this vaccine based on priority and demographics"""
    schedule = VACCINATION_SCHEDULES[vaccine]
    priority = schedule["priority"]
    
    # Base probabilities by priority
    base_probs = {
        "high": 0.95,      # Core vaccines - almost everyone should have
        "medium": 0.75,    # Important for immunocompromised
        "low": 0.45,       # Age-appropriate but not always given
        "very_low": 0.15   # Travel/occupational vaccines
    }
    
    prob = base_probs[priority]
    
    # Adjust based on age and vaccine type
    if vaccine in ["Shingles/Zoster", "RSV"] and age >= 60:
        prob += 0.1  # Higher probability for elderly
    elif vaccine == "HPV" and age > 30:
        prob *= 0.3  # Much lower for older adults
    elif vaccine in ["Meningococcal ACWY", "Meningococcal B"] and age < 25:
        prob += 0.15  # Higher for young adults
    
    # CKD patients are more likely to be fully vaccinated
    prob += 0.1
    
    return min(prob, 0.98)  # Cap at 98%

def generate_vaccination_dates(vaccine: str, age: int) -> List[datetime]:
    """Generate realistic vaccination dates based on medical timeline"""
    schedule = VACCINATION_SCHEDULES[vaccine]
    intervals = schedule["intervals"]
    num_shots = len(intervals)
    
    # Determine when vaccination series likely started
    if vaccine == "COVID-19":
        # COVID vaccines started in 2021
        series_start = datetime(2021, 3, 1) + timedelta(days=random.randint(0, 400))
    elif vaccine == "Influenza":
        # Recent annual flu shots (last 3 years)
        series_start = datetime.now() - timedelta(days=random.randint(30, 1095))
    elif vaccine in ["HPV", "MMR", "Varicella"]:
        # Often given in young adulthood
        years_ago = max(1, age - random.randint(18, 25))
        series_start = datetime.now() - timedelta(days=years_ago * 365)
    elif vaccine in ["Shingles/Zoster", "RSV"]:
        # Recent vaccines for elderly
        series_start = datetime.now() - timedelta(days=random.randint(30, 730))
    elif vaccine in ["Japanese Encephalitis", "Typhoid"]:
        # Travel vaccines - random timing
        series_start = datetime.now() - timedelta(days=random.randint(180, 2555))
    else:
        # Standard vaccines - historical
        series_start = datetime.now() - timedelta(days=random.randint(365, 3650))
    
    # Generate shot dates based on intervals
    dates = []
    current_date = series_start
    
    for i, interval_days in enumerate(intervals):
        if i == 0:
            dates.append(current_date)
        else:
            # Add some realistic variation to intervals (±7 days)
            actual_interval = interval_days + random.randint(-7, 7)
            current_date = dates[0] + timedelta(days=actual_interval)
            dates.append(current_date)
    
    # For influenza, generate multiple annual shots
    if vaccine == "Influenza" and num_shots > 1:
        dates = []
        for i in range(schedule["shots"]):
            shot_date = datetime.now() - timedelta(days=365 * i + random.randint(-30, 30))
            dates.insert(0, shot_date)  # Insert at beginning for chronological order
    
    return dates

def generate_vaccination(patient_id: str, demographics: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Generate comprehensive, realistic vaccination data based on CDC guidelines"""
    vaccinations = []
    age = demographics["age"]
    
    print(f"  Generating vaccinations for {demographics['name']} (age {age})...")
    
    # Go through all possible vaccines
    for vaccine in VACCINATION_INFECTIONS:
        # Check if age-appropriate
        if not is_age_appropriate(vaccine, age):
            continue
            
        # Check probability of having this vaccine
        prob = get_vaccination_probability(vaccine, age)
        if random.random() > prob:
            continue
            
        print(f"    Adding {vaccine} vaccination series")
        
        # Get vaccination schedule
        schedule = VACCINATION_SCHEDULES[vaccine]
        shot_kinds = schedule["kinds"]
        
        # Generate realistic dates
        shot_dates = generate_vaccination_dates(vaccine, age)
        
        # Determine how many shots patient actually received
        # High priority vaccines: usually complete series
        # Lower priority: might be incomplete
        if schedule["priority"] in ["high", "medium"]:
            num_shots_received = len(shot_dates)
        else:
            # Might have incomplete series for low priority vaccines
            num_shots_received = random.randint(1, len(shot_dates))
            shot_dates = shot_dates[:num_shots_received]
            
        # Create shot records
        shots = []
        for i, shot_date in enumerate(shot_dates):
            shots.append({
                "date": shot_date.strftime("%d-%m-%Y"),  # DD-MM-YYYY format to match database
                "count": i + 1,
                "kind": shot_kinds[min(i, len(shot_kinds) - 1)],
                "user_id": None,
                "org_id": None
            })
        
        vaccination = {
            "id": None,
            "version": None,
            "patientId": patient_id,
            "infection": vaccine,
            "shots": shots
        }
        vaccinations.append(vaccination)
    
    print(f"    Generated {len(vaccinations)} vaccination series with {sum(len(v['shots']) for v in vaccinations)} total shots")
    return vaccinations

def generate_audit() -> Dict[str, Any]:
    """Generate audit data with proper users and MongoDB date format"""
    user = random.choice(USERS)
    # Generate a realistic timestamp within the last 6 months
    now = datetime.now()
    created_time = now - timedelta(days=random.randint(1, 180))
    
    # Format as MongoDB $date format
    iso_timestamp = created_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    return {
        "created_on": {"$date": iso_timestamp},
        "updated_on": {"$date": iso_timestamp},
        "created_by": user,
        "updated_by": user
    }

def generate_patient_history(patient_id: str) -> Dict[str, Any]:
    """Generate complete patient history record"""
    demographics = get_patient_demographics(patient_id)
    
    return {
        "patient_id": patient_id,  # Put patient_id first to match database structure
        "vascular_access": generate_vascular_access(),
        "dry_weight": generate_dry_weight(demographics),
        "dialysis_runtime": generate_dialysis_runtime(demographics),
        "prescription_params": generate_prescription_params(demographics),
        "diagnosis": get_diagnosis_for_patient(demographics),
        "vaccination": generate_vaccination(patient_id, demographics),
        "audit": generate_audit()
    }

def main():
    """Generate patient histories for all 19 patients"""
    patient_histories = []
    
    print(f"Generating patient_histories for {len(PATIENT_IDS)} SMF patients...")
    print("Using realistic data based on patient demographics and medical best practices")
    
    for i, patient_id in enumerate(PATIENT_IDS, 1):
        demographics = get_patient_demographics(patient_id)
        print(f"Generating data for patient {i}/{len(PATIENT_IDS)}: {demographics['name']} (Age: {demographics['age']}, Gender: {demographics['gender']})")
        patient_history = generate_patient_history(patient_id)
        patient_histories.append(patient_history)
    
    # Save to JSON file
    output_file = "smf/data/generated_patient_histories.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(patient_histories, f, indent=2, default=str)
    
    print(f"\nGenerated {len(patient_histories)} patient_histories records")
    print(f"Data saved to: {output_file}")
    print("\nSample record structure:")
    print(json.dumps(patient_histories[0], indent=2, default=str)[:500] + "...")
    
    return patient_histories

if __name__ == "__main__":
    main() 