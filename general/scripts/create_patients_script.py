import json
import requests
import time

# Configuration
API_BASE_URL = "https://api-stg2.janohealth.com/ops"
ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2ODVjMWVmNDA0YTZjMzE4OTM4MDE0NGMiLCJ1c2VyIjoie1wibmFtZVwiOlwiUHJpeWEgTmFpclwiLFwiZ2VuZGVyXCI6XCJmZW1hbGVcIixcInVzZXJfdHlwZVwiOlwic3RhZmZcIixcInNwZWNpYWxpemF0aW9uXCI6XCJnZW5lcmFsXCIsXCJwaG9uZVwiOlwiKzkxOTc2NTQzMjEwOVwiLFwiZW1haWxcIjpcInByaXlhLm5haXJAc21mLm9yZ1wiLFwib3JnYW5pemF0aW9uc1wiOltdLFwiaHBpblwiOlwiJDJiJDEwJFlvQ1dNeFdBZnV2Q0RkMDh5cU42a2U0S3R6WHUwREVwd1VnR0hYVmRNMmhTalg2dVZrUHFDXCIsXCJ0ZWFtc1wiOlt7XCJvcmdfaWRcIjpcIjY4NWMxOGY1MDRhNmMzMTg5MzgwMTQyN1wiLFwib3JnX25hbWVcIjpcIlN1bmRhcmFtIE1lZGljYWwgRm91bmRhdGlvblwiLFwiZGVwdF9jb2RlXCI6XCJORVBIUk9cIixcInRlYW1faWRcIjpcIjY4NWMxOGY1MDRhNmMzMTg5MzgwMTQzMFwiLFwidGVhbV9uYW1lXCI6XCJSZW5hbCBDYXJlIFVuaXRcIixcInJvbGVcIjpcImRjX2luY2hhcmdlXCIsXCJkZXNpZ25hdGlvblwiOlwiSW5jaGFyZ2VcIixcInRlYW1fcGhvbmVcIjpcIis5MTk4NzY1NDMyMTBcIn1dLFwiaWRcIjpcIjY4NWMxZWY0MDRhNmMzMTg5MzgwMTQ0Y1wifSIsImF1dGhfaWQiOiJyZW5hbGNhcmVAamFuby5oZWFsdGgiLCJvcmdfaWRzIjpbIjY4NWMxOGY1MDRhNmMzMTg5MzgwMTQyNyJdLCJ0ZWFtX2lkcyI6WyI2ODVjMThmNTA0YTZjMzE4OTM4MDE0MzAiXSwiaWF0IjoxNzUwOTE3MzEwLCJleHAiOjE3NTEwMDA0MDB9.wDRcPPRlUe30WDolCYkhwKMLoiyJjMonBxw_W0KUCBw"
TEAM_ID = "685c18f504a6c31893801430"
ORG_ID = "685c18f504a6c31893801427"

# Headers
headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

def create_patient(patient_data):
    """Create a single patient using the API"""
    url = f"{API_BASE_URL}/patients"
    params = {
        "team_id": TEAM_ID,
        "org_id": ORG_ID
    }
    
    try:
        response = requests.post(url, json=patient_data, headers=headers, params=params)
        return response
    except Exception as e:
        print(f"Error creating patient {patient_data.get('name', 'Unknown')}: {str(e)}")
        return None

def main():
    # Load patient data
    try:
        with open('create_patients.json', 'r') as f:
            patients = json.load(f)
    except FileNotFoundError:
        print("Error: create_patients.json file not found!")
        return
    except json.JSONDecodeError:
        print("Error: Invalid JSON in create_patients.json!")
        return
    
    print(f"Found {len(patients)} patients to create...")
    print(f"API Endpoint: {API_BASE_URL}/patients")
    print(f"Team ID: {TEAM_ID}")
    print(f"Org ID: {ORG_ID}")
    print("-" * 50)
    
    created_patients = []
    failed_patients = []
    
    for i, patient in enumerate(patients, 1):
        print(f"Creating patient {i}/{len(patients)}: {patient['name']}")
        
        response = create_patient(patient)
        
        if response and response.status_code == 200:
            try:
                patient_response = response.json()
                created_patients.append({
                    "name": patient['name'],
                    "patient_id": patient_response.get('_id'),
                    "response": patient_response
                })
                print(f"✅ SUCCESS: Created {patient['name']} (ID: {patient_response.get('_id', 'Unknown')})")
            except json.JSONDecodeError:
                print(f"✅ SUCCESS: Created {patient['name']} (Response not JSON)")
                created_patients.append({
                    "name": patient['name'],
                    "patient_id": "unknown",
                    "response": response.text
                })
        else:
            error_msg = "Unknown error"
            if response:
                error_msg = f"HTTP {response.status_code}"
                try:
                    error_detail = response.json()
                    error_msg += f": {error_detail}"
                except:
                    error_msg += f": {response.text}"
            
            failed_patients.append({
                "name": patient['name'],
                "error": error_msg
            })
            print(f"❌ FAILED: {patient['name']} - {error_msg}")
        
        # Small delay to avoid overwhelming the API
        time.sleep(0.5)
    
    # Summary
    print("\n" + "=" * 50)
    print("CREATION SUMMARY")
    print("=" * 50)
    print(f"Total patients: {len(patients)}")
    print(f"Successfully created: {len(created_patients)}")
    print(f"Failed: {len(failed_patients)}")
    
    if created_patients:
        print(f"\n✅ SUCCESSFULLY CREATED PATIENTS:")
        for patient in created_patients:
            print(f"  - {patient['name']} (ID: {patient['patient_id']})")
    
    if failed_patients:
        print(f"\n❌ FAILED PATIENTS:")
        for patient in failed_patients:
            print(f"  - {patient['name']}: {patient['error']}")
    
    # Save results to file
    results = {
        "summary": {
            "total": len(patients),
            "created": len(created_patients),
            "failed": len(failed_patients)
        },
        "created_patients": created_patients,
        "failed_patients": failed_patients
    }
    
    with open('patient_creation_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📄 Results saved to: patient_creation_results.json")

if __name__ == "__main__":
    main() 