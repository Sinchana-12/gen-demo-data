#!/usr/bin/env python3

import json
import os
from pymongo import MongoClient
from dotenv import load_dotenv
from bson import ObjectId

# Load environment variables
load_dotenv()

# SMF Patient IDs
SMF_PATIENT_IDS = [
    "685cf29e04a6c318938015f1", "685cf29f04a6c31893801620", "685cf2a004a6c3189380164f",
    "685cf2a104a6c3189380167e", "685cf2a104a6c318938016ad", "685cf2a304a6c318938016dc",
    "685cf2a304a6c3189380170b", "685cf2a504a6c31893801743", "685cf2a604a6c31893801772",
    "685cf2a604a6c318938017a1", "685cf2a704a6c318938017d0", "685cf2a804a6c318938017ff",
    "685cf2a904a6c3189380182e", "685cf2aa04a6c3189380185d", "685cf2aa04a6c3189380188c",
    "685cf2ab04a6c318938018bb", "685cf2ac04a6c318938018ea", "685cf2ad04a6c31893801919",
    "685cf2e704a6c31893801948"
]

def main():
    print("Debug: Checking SMF Patient Reports in Demo Cluster")
    print("=" * 60)
    
    # Connect to Demo Cluster
    demo_mongodb_url = os.getenv('DEMO_MONGODB_URL')
    client = MongoClient(demo_mongodb_url)
    db = client['jano_core']
    
    print(f"Connected to Demo Cluster: jano_core")
    
    # Check total reports count
    total_reports = db.reports.count_documents({})
    print(f"Total reports in collection: {total_reports}")
    
    # Check pathology reports count
    pathology_reports = db.reports.count_documents({"content_type": "pathology"})
    print(f"Total pathology reports: {pathology_reports}")
    
    print("\nChecking reports for each SMF patient...")
    
    found_any = False
    for i, patient_id in enumerate(SMF_PATIENT_IDS[:5]):  # Check first 5 patients
        print(f"\nPatient {i+1}: {patient_id}")
        
        # Try different query formats
        queries = [
            {"patient.$oid": patient_id},
            {"patient": {"$oid": patient_id}},
            {"patient": ObjectId(patient_id)},
        ]
        
        for j, query in enumerate(queries):
            try:
                count = db.reports.count_documents(query)
                if count > 0:
                    print(f"  Query format {j+1} found {count} reports")
                    found_any = True
                    
                    # Get a sample report
                    sample = db.reports.find_one(query)
                    if sample:
                        print(f"  Sample report structure:")
                        print(f"    _id: {sample.get('_id')}")
                        print(f"    patient: {sample.get('patient')}")
                        print(f"    content_type: {sample.get('content_type')}")
                        if 'metadata' in sample:
                            print(f"    originalname: {sample['metadata'].get('originalname')}")
                    break
                else:
                    print(f"  Query format {j+1}: No reports found")
            except Exception as e:
                print(f"  Query format {j+1}: Error - {e}")
    
    if not found_any:
        print("\n" + "="*60)
        print("No reports found for SMF patients!")
        print("Let's check what patients exist in reports collection...")
        
        # Sample some reports to see patient ID format
        sample_reports = list(db.reports.find({}).limit(3))
        for i, report in enumerate(sample_reports):
            print(f"\nSample report {i+1}:")
            print(f"  _id: {report.get('_id')}")
            print(f"  patient: {report.get('patient')}")
            print(f"  content_type: {report.get('content_type')}")
    
    client.close()

if __name__ == "__main__":
    main() 