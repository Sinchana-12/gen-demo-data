#!/usr/bin/env python3

import json
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any

# SMF Organization and Patient Data
SMF_ORG_ID = "685c18f504a6c31893801427"

# Patient IDs for SMF org (using the same ones from patient histories)
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

# Patient demographics (same as in patient histories)
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

# SEROLOGY TAGS: Based on infectious disease screening for dialysis patients
SEROLOGY_OPTIONS = {
    # Core serology screening (required for all dialysis patients)
    "core": [
        "HIV - Non Reactive",
        "HBsAg - Non Reactive", 
        "Anti-HCV - Non Reactive",
        "HBeAg - Non Reactive",
        "Anti-HBc - Non Reactive"
    ],
    # Additional serology tests for immunocompromised patients
    "additional": [
        "CMV IgM - Non Reactive",
        "CMV IgG - Positive",
        "EBV IgM - Non Reactive", 
        "EBV IgG - Positive",
        "Hepatitis A IgM - Non Reactive",
        "Hepatitis A IgG - Positive",
        "VDRL - Non Reactive",
        "Toxoplasma IgM - Non Reactive",
        "Toxoplasma IgG - Positive"
    ],
    # Positive results (less common but realistic)
    "positive_results": [
        "Anti-HCV - Positive",
        "HBsAg - Positive", 
        "Anti-HBc - Positive",
        "CMV IgG - Positive",
        "EBV IgG - Positive",
        "Hepatitis A IgG - Positive"
    ]
}

# ALLERGY TAGS: Common allergens for CKD/dialysis patients
ALLERGY_OPTIONS = {
    # Environmental allergens
    "environmental": [
        "Dust Mites", "Pollen", "Mold", "Pet Dander", "Smoke"
    ],
    # Food allergens
    "food": [
        "Nuts", "Shellfish", "Eggs", "Dairy", "Soy", "Wheat"
    ],
    # Drug allergens (important for dialysis patients)
    "drug": [
        "Penicillin", "Sulfa Drugs", "Contrast Dye", "Heparin", "Iron Supplements", "ACE Inhibitors"
    ],
    # Contact allergens
    "contact": [
        "Latex", "Nickel", "Adhesives", "Cleaning Products"
    ]
}

# MEDICAL CONDITIONS: Common comorbidities in CKD/dialysis patients
CONDITION_OPTIONS = {
    # Primary conditions leading to CKD
    "primary": [
        "Diabetes Mellitus Type 2", "Hypertension", "Diabetic Nephropathy", 
        "Hypertensive Nephrosclerosis", "Polycystic Kidney Disease", 
        "Glomerulonephritis", "IgA Nephropathy"
    ],
    # Cardiovascular comorbidities (very common in CKD)
    "cardiovascular": [
        "Coronary Artery Disease", "Congestive Heart Failure", "Atrial Fibrillation",
        "Peripheral Artery Disease", "Cerebrovascular Disease", "Left Ventricular Hypertrophy"
    ],
    # CKD-related complications
    "ckd_complications": [
        "Secondary Hyperparathyroidism", "Anemia of CKD", "Bone Disease (CKD-MBD)",
        "Metabolic Acidosis", "Mineral Bone Disorder", "Chronic Fatigue"
    ],
    # Other common conditions
    "other": [
        "Osteoporosis", "Depression", "Sleep Apnea", "Gout", "Thyroid Disease",
        "Chronic Pain", "Neuropathy", "Retinopathy"
    ]
}

def get_patient_demographics(patient_id: str) -> Dict[str, Any]:
    """Get patient demographics"""
    return PATIENT_DEMOGRAPHICS[patient_id]

def generate_serology_tags(demographics: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Generate realistic serology tags based on medical guidelines"""
    tags = []
    age = demographics["age"]
    
    # All dialysis patients must have core serology screening
    core_tests = random.sample(SEROLOGY_OPTIONS["core"], random.randint(3, 5))
    
    # Older patients more likely to have additional tests
    if age > 50:
        additional_tests = random.sample(SEROLOGY_OPTIONS["additional"], random.randint(2, 4))
        core_tests.extend(additional_tests)
    elif age > 35:
        additional_tests = random.sample(SEROLOGY_OPTIONS["additional"], random.randint(1, 3))
        core_tests.extend(additional_tests)
    
    # Small chance of positive results (realistic prevalence)
    if random.random() < 0.15:  # 15% chance of having at least one positive result
        positive_test = random.choice(SEROLOGY_OPTIONS["positive_results"])
        core_tests.append(positive_test)
        
        # If HCV or HBV positive, likely to have additional monitoring
        if "HCV" in positive_test or "HBsAg" in positive_test:
            core_tests.append("Viral Load - Undetectable" if random.random() < 0.7 else "Viral Load - Detectable")
    
    # Generate dates for each test (within last 1-3 years for active patients)
    for test in core_tests:
        test_date = datetime.now() - timedelta(days=random.randint(30, 1095))
        # Format as MongoDB $date format
        iso_timestamp = test_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        tags.append({
            "name": test,
            "since": {"$date": iso_timestamp}
        })
    
    return tags

def generate_allergy_tags(demographics: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Generate realistic allergy tags"""
    tags = []
    age = demographics["age"]
    gender = demographics["gender"]
    
    # About 40% of patients have documented allergies
    if random.random() > 0.4:
        return tags
    
    allergy_categories = []
    
    # Environmental allergies more common
    if random.random() < 0.6:
        allergy_categories.extend(random.sample(ALLERGY_OPTIONS["environmental"], random.randint(1, 3)))
    
    # Drug allergies important for dialysis patients
    if random.random() < 0.3:
        allergy_categories.extend(random.sample(ALLERGY_OPTIONS["drug"], random.randint(1, 2)))
    
    # Food allergies
    if random.random() < 0.2:
        allergy_categories.extend(random.sample(ALLERGY_OPTIONS["food"], random.randint(1, 2)))
    
    # Contact allergies (especially latex for healthcare exposure)
    if random.random() < 0.25:
        allergy_categories.extend(random.sample(ALLERGY_OPTIONS["contact"], random.randint(1, 2)))
    
    # Generate dates (allergies often discovered years ago)
    for allergy in allergy_categories:
        # Allergies typically discovered throughout life, more recent for drug allergies
        if "drug" in [cat for cat, allergens in ALLERGY_OPTIONS.items() if allergy in allergens]:
            allergy_date = datetime.now() - timedelta(days=random.randint(30, 1825))  # Last 5 years
        else:
            allergy_date = datetime.now() - timedelta(days=random.randint(365, age * 365 // 2))  # Could be from childhood
        
        # Format as MongoDB $date format
        iso_timestamp = allergy_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        tags.append({
            "name": allergy,
            "since": {"$date": iso_timestamp}
        })
    
    return tags

def generate_condition_tags(demographics: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Generate realistic medical condition tags based on CKD patient profiles"""
    tags = []
    age = demographics["age"]
    gender = demographics["gender"]
    
    # All CKD patients have at least one primary condition
    primary_conditions = random.sample(CONDITION_OPTIONS["primary"], random.randint(1, 2))
    
    # Age-based condition probabilities
    cardiovascular_conditions = []
    if age > 60:
        # High probability of cardiovascular comorbidities in elderly
        cardiovascular_conditions = random.sample(CONDITION_OPTIONS["cardiovascular"], random.randint(2, 4))
    elif age > 45:
        cardiovascular_conditions = random.sample(CONDITION_OPTIONS["cardiovascular"], random.randint(1, 2))
    elif age > 35:
        if random.random() < 0.4:  # 40% chance
            cardiovascular_conditions = random.sample(CONDITION_OPTIONS["cardiovascular"], 1)
    
    # CKD complications (more common in longer-term patients)
    ckd_complications = []
    if random.random() < 0.7:  # 70% of dialysis patients have CKD complications
        ckd_complications = random.sample(CONDITION_OPTIONS["ckd_complications"], random.randint(1, 3))
    
    # Other conditions based on age and gender
    other_conditions = []
    if age > 55:
        if random.random() < 0.5:
            other_conditions = random.sample(CONDITION_OPTIONS["other"], random.randint(1, 2))
    
    # Gender-specific considerations
    if gender == "female" and age > 50:
        if random.random() < 0.3:
            other_conditions.append("Osteoporosis")
    
    # Combine all conditions
    all_conditions = primary_conditions + cardiovascular_conditions + ckd_complications + other_conditions
    
    # Generate realistic onset dates for conditions
    for condition in all_conditions:
        if condition in CONDITION_OPTIONS["primary"]:
            # Primary conditions typically diagnosed years before dialysis
            condition_date = datetime.now() - timedelta(days=random.randint(1095, 7300))  # 3-20 years ago
        elif condition in CONDITION_OPTIONS["cardiovascular"]:
            # Cardiovascular conditions often develop after primary condition
            condition_date = datetime.now() - timedelta(days=random.randint(365, 5475))  # 1-15 years ago
        elif condition in CONDITION_OPTIONS["ckd_complications"]:
            # CKD complications develop as kidney function declines
            condition_date = datetime.now() - timedelta(days=random.randint(180, 2190))  # 6 months - 6 years ago
        else:
            # Other conditions - variable timing
            condition_date = datetime.now() - timedelta(days=random.randint(365, age * 365 // 3))
        
        # Format as MongoDB $date format
        iso_timestamp = condition_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        tags.append({
            "name": condition,
            "since": {"$date": iso_timestamp}
        })
    
    return tags

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

def generate_patient_tags(patient_id: str) -> List[Dict[str, Any]]:
    """Generate comprehensive patient tags for a patient across all categories"""
    demographics = get_patient_demographics(patient_id)
    patient_tags = []
    
    print(f"  Generating tags for {demographics['name']} (age {demographics['age']}, {demographics['gender']})...")
    
    # Generate serology tags
    serology_tags = generate_serology_tags(demographics)
    if serology_tags:
        patient_tags.append({
            "patientId": {"$oid": patient_id},
            "category": "serology", 
            "tags": serology_tags,
            "audit": generate_audit(),
            "version": "1",
            "organizationId": {"$oid": SMF_ORG_ID}
        })
        print(f"    - {len(serology_tags)} serology results")
    
    # Generate allergy tags
    allergy_tags = generate_allergy_tags(demographics)
    if allergy_tags:
        patient_tags.append({
            "patientId": {"$oid": patient_id},
            "category": "allergies",
            "tags": allergy_tags,
            "audit": generate_audit(),
            "version": "1", 
            "organizationId": {"$oid": SMF_ORG_ID}
        })
        print(f"    - {len(allergy_tags)} allergies")
    
    # Generate condition tags  
    condition_tags = generate_condition_tags(demographics)
    if condition_tags:
        patient_tags.append({
            "patientId": {"$oid": patient_id},
            "category": "conditions",
            "tags": condition_tags,
            "audit": generate_audit(),
            "version": "1",
            "organizationId": {"$oid": SMF_ORG_ID}
        })
        print(f"    - {len(condition_tags)} medical conditions")
    
    return patient_tags

def main():
    """Generate patient tags for all SMF patients"""
    all_patient_tags = []
    
    print(f"Generating patient_tags for {len(PATIENT_IDS)} SMF patients...")
    print("Categories: serology, allergies, conditions")
    print("Based on medical best practices for CKD/dialysis patients\n")
    
    for i, patient_id in enumerate(PATIENT_IDS, 1):
        demographics = get_patient_demographics(patient_id)
        print(f"Processing patient {i}/{len(PATIENT_IDS)}: {demographics['name']}")
        
        patient_tags = generate_patient_tags(patient_id)
        all_patient_tags.extend(patient_tags)
    
    # Save to JSON file
    output_file = "../data/generated_patient_tags.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_patient_tags, f, indent=2, default=str)
    
    print(f"\n{'='*60}")
    print(f"GENERATION COMPLETE")
    print(f"{'='*60}")
    print(f"Total patient_tags records generated: {len(all_patient_tags)}")
    print(f"Data saved to: {output_file}")
    
    # Statistics
    serology_count = len([tag for tag in all_patient_tags if tag['category'] == 'serology'])
    allergy_count = len([tag for tag in all_patient_tags if tag['category'] == 'allergies']) 
    condition_count = len([tag for tag in all_patient_tags if tag['category'] == 'conditions'])
    
    print(f"\nBreakdown by category:")
    print(f"  - Serology records: {serology_count}")
    print(f"  - Allergy records: {allergy_count}")
    print(f"  - Condition records: {condition_count}")
    
    total_tags = sum(len(record['tags']) for record in all_patient_tags)
    print(f"  - Total individual tags: {total_tags}")
    
    print(f"\nSample record structure:")
    if all_patient_tags:
        print(json.dumps(all_patient_tags[0], indent=2, default=str)[:800] + "...")
    
    return all_patient_tags

if __name__ == "__main__":
    main() 