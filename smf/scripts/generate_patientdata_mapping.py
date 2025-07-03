#!/usr/bin/env python3

import json
import os
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# SMF Patient IDs (from generate_patient_reports.py)
SMF_PATIENT_IDS = [
    "685cf29e04a6c318938015f1", "685cf29f04a6c31893801620", "685cf2a004a6c3189380164f",
    "685cf2a104a6c3189380167e", "685cf2a104a6c318938016ad", "685cf2a304a6c318938016dc",
    "685cf2a304a6c3189380170b", "685cf2a504a6c31893801743", "685cf2a604a6c31893801772",
    "685cf2a604a6c318938017a1", "685cf2a704a6c318938017d0", "685cf2a804a6c318938017ff",
    "685cf2a904a6c3189380182e", "685cf2aa04a6c3189380185d", "685cf2aa04a6c3189380188c",
    "685cf2ab04a6c318938018bb", "685cf2ac04a6c318938018ea", "685cf2ad04a6c31893801919",
    "685cf2e704a6c31893801948"
]

# Valid SMF users for audit (from other scripts)
SMF_USERS = [
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

def load_reports_in_use() -> List[str]:
    """Load the 10 report IDs from reports_in_use.json"""
    reports_file = "smf/data/pathology/reports_in_use.json" 
    with open(reports_file, 'r') as f:
        return json.load(f)

def connect_to_mongodb(connection_string: str, db_name: str):
    """Connect to MongoDB and return database"""
    try:
        client = MongoClient(connection_string)
        db = client[db_name]
        # Test connection
        db.command('ping')
        print(f"✓ Connected to MongoDB: {db_name}")
        return db
    except Exception as e:
        print(f"✗ Failed to connect to MongoDB: {e}")
        return None

def get_smf_patient_reports(demo_db) -> Dict[str, List[Dict[str, Any]]]:
    """Get all reports for SMF patients from Demo Cluster"""
    print("\nFetching SMF patient reports from Demo Cluster...")
    
    smf_patient_reports = {}
    
    for patient_id in SMF_PATIENT_IDS:
        # Find all reports for this patient
        reports = list(demo_db.reports.find({
            "patient.$oid": patient_id
        }))
        
        if reports:
            smf_patient_reports[patient_id] = reports
            print(f"  Patient {patient_id}: {len(reports)} pathology reports")
    
    total_reports = sum(len(reports) for reports in smf_patient_reports.values())
    print(f"\nTotal SMF pathology reports found: {total_reports}")
    return smf_patient_reports

def create_originalname_to_old_report_mapping(original_db, reports_in_use: List[str]) -> Dict[str, str]:
    """Create mapping from originalname to old report ID"""
    print("\nCreating originalname → old report ID mapping...")
    
    # Convert string IDs to ObjectId format for query
    from bson import ObjectId
    object_ids = [ObjectId(report_id) for report_id in reports_in_use]
    
    # Get the 10 reports from original MongoDB
    old_reports = list(original_db.reports.find({
        "_id": {"$in": object_ids}
    }))
    
    originalname_to_old_id = {}
    for report in old_reports:
        originalname = report["metadata"]["originalname"]
        old_id = str(report["_id"])
        originalname_to_old_id[originalname] = old_id
        print(f"  {originalname} → {old_id}")
    
    print(f"\nMapped {len(originalname_to_old_id)} originalnames to old report IDs")
    return originalname_to_old_id

def backtrack_smf_reports_to_old_ids(smf_patient_reports: Dict[str, List[Dict[str, Any]]], 
                                   originalname_to_old_id: Dict[str, str]) -> Dict[str, List[str]]:
    """Backtrack SMF patient reports to old report IDs"""
    print("\nBacktracking SMF reports to old report IDs...")
    
    patient_to_old_report_ids = {}
    
    for patient_id, reports in smf_patient_reports.items():
        old_report_ids = []
        
        for report in reports:
            originalname = report["metadata"]["originalname"]
            
            # Find matching old report ID
            if originalname in originalname_to_old_id:
                old_report_id = originalname_to_old_id[originalname]
                old_report_ids.append(old_report_id)
                print(f"  Patient {patient_id}: {originalname} → {old_report_id}")
        
        if old_report_ids:
            patient_to_old_report_ids[patient_id] = old_report_ids
    
    return patient_to_old_report_ids

def fetch_relevant_patientdata(original_db, patient_to_old_report_ids: Dict[str, List[str]]) -> List[Dict[str, Any]]:
    """Fetch patientdata records that reference the relevant old report IDs"""
    print("\nFetching relevant patientdata records from Original MongoDB...")
    
    # Collect all old report IDs
    all_old_report_ids = []
    for old_ids in patient_to_old_report_ids.values():
        all_old_report_ids.extend(old_ids)
    
    # Remove duplicates
    unique_old_report_ids = list(set(all_old_report_ids))
    print(f"  Looking for patientdata records referencing {len(unique_old_report_ids)} old report IDs")
    
    # Convert to ObjectId format for query
    from bson import ObjectId
    old_report_object_ids = [ObjectId(report_id) for report_id in unique_old_report_ids]
    
    # Query patientdata collection
    patientdata_records = list(original_db.patientdata.find({
        "source.report.$oid": {"$in": unique_old_report_ids}
    }))
    
    print(f"  Found {len(patientdata_records)} relevant patientdata records")
    return patientdata_records

def create_old_to_new_report_mapping(smf_patient_reports: Dict[str, List[Dict[str, Any]]], 
                                   originalname_to_old_id: Dict[str, str]) -> Dict[str, str]:
    """Create mapping from old report ID to new report ID"""
    print("\nCreating old report ID → new report ID mapping...")
    
    old_to_new_report_id = {}
    
    for patient_id, reports in smf_patient_reports.items():
        for report in reports:
            originalname = report["metadata"]["originalname"]
            new_report_id = str(report["_id"])
            
            if originalname in originalname_to_old_id:
                old_report_id = originalname_to_old_id[originalname]
                old_to_new_report_id[old_report_id] = new_report_id
                print(f"  {old_report_id} → {new_report_id} ({originalname})")
    
    return old_to_new_report_id

def get_report_upload_time(demo_db, new_report_id: str) -> Optional[datetime]:
    """Get upload time for a report from Demo Cluster"""
    from bson import ObjectId
    
    report = demo_db.reports.find_one({"_id": ObjectId(new_report_id)})
    if report and "metadata" in report and "upload_time" in report["metadata"]:
        upload_time_str = report["metadata"]["upload_time"]
        if isinstance(upload_time_str, dict) and "$date" in upload_time_str:
            # MongoDB $date format
            return datetime.fromisoformat(upload_time_str["$date"].replace("Z", "+00:00"))
        elif isinstance(upload_time_str, str):
            # ISO string format
            return datetime.fromisoformat(upload_time_str.replace("Z", "+00:00"))
    
    return None

def transform_patientdata_records(patientdata_records: List[Dict[str, Any]],
                                patient_to_old_report_ids: Dict[str, List[str]],
                                old_to_new_report_id: Dict[str, str],
                                demo_db) -> List[Dict[str, Any]]:
    """Transform patientdata records for Demo Cluster insertion"""
    print("\nTransforming patientdata records...")
    
    transformed_records = []
    
    # Create reverse mapping: old_report_id → list of patients
    old_report_to_patients = {}
    for patient_id, old_report_ids in patient_to_old_report_ids.items():
        for old_report_id in old_report_ids:
            if old_report_id not in old_report_to_patients:
                old_report_to_patients[old_report_id] = []
            old_report_to_patients[old_report_id].append(patient_id)
    
    for record in patientdata_records:
        old_report_id = record["source"]["report"]["$oid"]
        
        # Find which SMF patients should get this record
        if old_report_id in old_report_to_patients:
            target_patients = old_report_to_patients[old_report_id]
            
            for patient_id in target_patients:
                # Get new report ID
                if old_report_id in old_to_new_report_id:
                    new_report_id = old_to_new_report_id[old_report_id]
                    
                    # Create transformed record
                    transformed_record = record.copy()
                    
                    # Update patient ID
                    transformed_record["patient"] = {"$oid": patient_id}
                    
                    # Update report ID
                    transformed_record["source"]["report"] = {"$oid": new_report_id}
                    
                    # Update audit timestamp (report upload_time + 30 minutes)
                    upload_time = get_report_upload_time(demo_db, new_report_id)
                    if upload_time:
                        audit_time = upload_time + timedelta(minutes=30)
                        audit_timestamp = audit_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
                        
                        transformed_record["audit"] = {
                            "created_on": {"$date": audit_timestamp},
                            "created_by": random.choice(SMF_USERS)
                        }
                    
                    # Remove MongoDB internal _id to let it auto-generate
                    if "_id" in transformed_record:
                        del transformed_record["_id"]
                    
                    transformed_records.append(transformed_record)
                    print(f"  Transformed record for patient {patient_id}, report {new_report_id}")
    
    print(f"\nTotal transformed records: {len(transformed_records)}")
    return transformed_records

def main():
    """Main function to generate mapped patientdata records"""
    print("SMF PatientData Mapping Generator")
    print("=" * 50)
    
    # Load environment variables
    original_mongodb_url = os.getenv('ORIGINAL_MONGODB_URL')
    demo_mongodb_url = os.getenv('DEMO_MONGODB_URL')
    
    if not original_mongodb_url or not demo_mongodb_url:
        print("ERROR: Missing MongoDB connection URLs in .env file")
        print("Required: ORIGINAL_MONGODB_URL, DEMO_MONGODB_URL")
        return
    
    # Load reports in use
    reports_in_use = load_reports_in_use()
    print(f"Loaded {len(reports_in_use)} report IDs from reports_in_use.json")
    
    # Connect to both MongoDB instances
    original_db = connect_to_mongodb(original_mongodb_url, "beta_test")
    demo_db = connect_to_mongodb(demo_mongodb_url, "jano_core")
    
    if original_db is None or demo_db is None:
        print("ERROR: Failed to connect to MongoDB instances")
        return
    
    # Step 1: Get SMF patient reports from Demo Cluster
    smf_patient_reports = get_smf_patient_reports(demo_db)
    
    if not smf_patient_reports:
        print("ERROR: No SMF patient reports found in Demo Cluster")
        return
    
    # Step 2: Create originalname → old report ID mapping
    originalname_to_old_id = create_originalname_to_old_report_mapping(original_db, reports_in_use)
    
    # Step 3: Backtrack SMF reports to old report IDs
    patient_to_old_report_ids = backtrack_smf_reports_to_old_ids(smf_patient_reports, originalname_to_old_id)
    
    if not patient_to_old_report_ids:
        print("ERROR: No matching reports found for backtracking")
        return
    
    # Step 4: Fetch relevant patientdata records
    patientdata_records = fetch_relevant_patientdata(original_db, patient_to_old_report_ids)
    
    if not patientdata_records:
        print("ERROR: No relevant patientdata records found")
        return
    
    # Step 5: Create old → new report ID mapping
    old_to_new_report_id = create_old_to_new_report_mapping(smf_patient_reports, originalname_to_old_id)
    
    # Step 6: Transform records
    transformed_records = transform_patientdata_records(
        patientdata_records, 
        patient_to_old_report_ids, 
        old_to_new_report_id, 
        demo_db
    )
    
    # Step 7: Save output
    output_file = "../data/generated_smf_patientdata.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(transformed_records, f, indent=2, default=str)
    
    print(f"\n{'='*50}")
    print("GENERATION COMPLETE")
    print(f"{'='*50}")
    print(f"Generated {len(transformed_records)} patientdata records")
    print(f"Data saved to: {output_file}")
    
    # Statistics
    patients_with_data = len(set(record["patient"]["$oid"] for record in transformed_records))
    reports_referenced = len(set(record["source"]["report"]["$oid"] for record in transformed_records))
    
    print(f"\nStatistics:")
    print(f"  - SMF patients with patientdata: {patients_with_data}")
    print(f"  - Unique reports referenced: {reports_referenced}")
    print(f"  - Average records per patient: {len(transformed_records) / patients_with_data:.1f}")
    
    # Show sample record
    if transformed_records:
        print(f"\nSample transformed record:")
        print(json.dumps(transformed_records[0], indent=2, default=str)[:500] + "...")
    
    return transformed_records

if __name__ == "__main__":
    main() 