import json
from datetime import datetime

# Load the current patient histories
with open('create_patient_histories.json', 'r') as f:
    histories = json.load(f)

print("=== FIXING PATIENT HISTORIES SCHEMA ===")
print("Issues to fix:")
print("1. Audit dates should be MongoDB Date objects")
print("2. Temperature unit should be '˚c' not '°c'")
print("3. Need to remove _id field (MongoDB will auto-generate)")
print("4. Ensure proper data types")
print()

# Fix each history record
fixed_histories = []
for history in histories:
    # Create fixed version
    fixed_history = {
        "patient_id": history["patient_id"],
        "vascular_access": history["vascular_access"],
        "dry_weight": history["dry_weight"],
        "dialysis_runtime": history["dialysis_runtime"],
        "prescription_params": [],
        "diagnosis": history["diagnosis"],
        "vaccination": history["vaccination"],
        "audit": {
            "created_on": {"$date": history["audit"]["created_on"]},
            "updated_on": {"$date": history["audit"]["updated_on"]},
            "created_by": history["audit"]["created_by"],
            "updated_by": history["audit"]["updated_by"]
        }
    }
    
    # Fix prescription parameters
    for param in history["prescription_params"]:
        fixed_param = param.copy()
        
        # Fix temperature unit to match existing schema
        if param["code"] == "DLSTTEMP":
            fixed_param["units"]["unit"] = "˚c"  # Use the correct degree symbol
        
        fixed_history["prescription_params"].append(fixed_param)
    
    fixed_histories.append(fixed_history)

# Save the fixed version
with open('patient_histories_fixed.json', 'w') as f:
    json.dump(fixed_histories, f, indent=2)

print(f"✅ Fixed {len(fixed_histories)} patient history records")
print("✅ Corrected audit date format to MongoDB Date objects")
print("✅ Fixed temperature unit symbol")
print("✅ Ensured proper schema structure")
print()
print("Saved to: patient_histories_fixed.json")

# Show sample of fixed data
print("\n=== SAMPLE FIXED RECORD ===")
sample = fixed_histories[0]
print(f"Patient ID: {sample['patient_id']}")
print(f"Vascular Access: {sample['vascular_access']['value']}")
print(f"Audit Created: {sample['audit']['created_on']}")
temp_param = next(p for p in sample['prescription_params'] if p['code'] == 'DLSTTEMP')
print(f"Temperature Unit: '{temp_param['units']['unit']}'")
print(f"Temperature Value: {temp_param['value']}") 