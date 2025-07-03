#!/usr/bin/env python3

import json
import random
import os
import subprocess
import uuid
import mimetypes
from datetime import datetime, timedelta
from typing import List, Dict, Any
import sys

# SMF Organization and Patient Data
SMF_ORG_ID = "685c18f504a6c31893801427"

# Patient IDs for SMF org (same as other scripts)
PATIENT_IDS = [
    "685cf29e04a6c318938015f1", "685cf29f04a6c31893801620", "685cf2a004a6c3189380164f",
    "685cf2a104a6c3189380167e", "685cf2a104a6c318938016ad", "685cf2a304a6c318938016dc",
    "685cf2a304a6c3189380170b", "685cf2a504a6c31893801743", "685cf2a604a6c31893801772",
    "685cf2a604a6c318938017a1", "685cf2a704a6c318938017d0", "685cf2a804a6c318938017ff",
    "685cf2a904a6c3189380182e", "685cf2aa04a6c3189380185d", "685cf2aa04a6c3189380188c",
    "685cf2ab04a6c318938018bb", "685cf2ac04a6c318938018ea", "685cf2ad04a6c31893801919",
    "685cf2e704a6c31893801948"
]

# Patient demographics for context
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

# S3 Configuration (based on existing reports data)
S3_BUCKET = "jano-nexus-uploads-stg2"
PATHOLOGY_DIR = "../data/pathology"

def get_available_report_files() -> List[str]:
    """Get list of available report files, excluding json and system files"""
    files = []
    for filename in os.listdir(PATHOLOGY_DIR):
        if filename.endswith(('.pdf', '.jpg', '.jpeg', '.png')) and not filename.startswith('.'):
            files.append(filename)
    return files

def get_file_info(filepath: str) -> Dict[str, Any]:
    """Get file information including size and mimetype"""
    size = os.path.getsize(filepath)
    mimetype, _ = mimetypes.guess_type(filepath)
    if not mimetype:
        # Default mimetypes for common file extensions
        if filepath.lower().endswith('.pdf'):
            mimetype = 'application/pdf'
        elif filepath.lower().endswith(('.jpg', '.jpeg')):
            mimetype = 'image/jpeg'
        elif filepath.lower().endswith('.png'):
            mimetype = 'image/png'
        else:
            mimetype = 'application/octet-stream'
    
    return {
        'size': size,
        'mimetype': mimetype
    }

def upload_file_to_s3(local_path: str, s3_key: str) -> bool:
    """Upload file to S3 using AWS CLI"""
    try:
        s3_uri = f"s3://{S3_BUCKET}/{s3_key}"
        
        # Use AWS CLI to upload file
        cmd = [
            "aws", "s3", "cp", 
            local_path, 
            s3_uri,
            "--no-cli-pager"
        ]
        
        print(f"    Uploading {os.path.basename(local_path)} to {s3_uri}")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"    ✓ Upload successful")
            return True
        else:
            print(f"    ✗ Upload failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"    ✗ Upload error: {str(e)}")
        return False

def generate_upload_time() -> datetime:
    """Generate realistic upload time (within last 6 months)"""
    now = datetime.now()
    days_ago = random.randint(1, 180)  # Last 6 months
    upload_time = now - timedelta(days=days_ago)
    
    # Add some realistic time variation (business hours)
    hour = random.randint(8, 18)  # 8 AM to 6 PM
    minute = random.randint(0, 59)
    upload_time = upload_time.replace(hour=hour, minute=minute, second=random.randint(0, 59))
    
    return upload_time

def create_report_record(patient_id: str, filename: str, file_info: Dict[str, Any], 
                        s3_key: str, upload_time: datetime) -> Dict[str, Any]:
    """Create MongoDB report record"""
    
    # Let MongoDB generate the _id automatically
    return {
        "schema_version": "1",
        "key": s3_key,
        "bucket": S3_BUCKET,
        "patient": {"$oid": patient_id},
        "metadata": {
            "originalname": filename,
            "mimetype": file_info['mimetype'],
            "patient_id": patient_id,
            "size": file_info['size'],
            "upload_time": {"$date": upload_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")}
        },
        "__v": 0
    }

def generate_patient_reports(patient_id: str, available_files: List[str], 
                           dry_run: bool = False) -> List[Dict[str, Any]]:
    """Generate reports for a single patient"""
    demographics = PATIENT_DEMOGRAPHICS[patient_id]
    
    # Random number of reports per patient (1-10)
    num_reports = random.randint(1, 10)
    
    # Randomly select files for this patient
    selected_files = random.sample(available_files, min(num_reports, len(available_files)))
    
    print(f"  Processing {demographics['name']} - {num_reports} reports")
    
    reports = []
    
    for filename in selected_files:
        # Generate unique S3 key (UUID)
        s3_key = str(uuid.uuid4())
        
        # Get file information
        file_path = os.path.join(PATHOLOGY_DIR, filename)
        file_info = get_file_info(file_path)
        
        # Generate upload time
        upload_time = generate_upload_time()
        
        if not dry_run:
            # Upload file to S3
            upload_success = upload_file_to_s3(file_path, s3_key)
            
            if not upload_success:
                print(f"    ⚠️  Skipping {filename} due to upload failure")
                continue
        else:
            print(f"    [DRY RUN] Would upload {filename} as {s3_key}")
        
        # Create MongoDB record
        report_record = create_report_record(
            patient_id, filename, file_info, s3_key, upload_time
        )
        
        reports.append(report_record)
        
        print(f"    ✓ Created report record for {filename}")
    
    return reports

def check_aws_cli() -> bool:
    """Check if AWS CLI is available and configured"""
    try:
        result = subprocess.run(["aws", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ AWS CLI available: {result.stdout.strip()}")
            return True
        else:
            print("✗ AWS CLI not available")
            return False
    except FileNotFoundError:
        print("✗ AWS CLI not installed")
        return False

def check_aws_credentials() -> bool:
    """Check if AWS credentials are configured"""
    try:
        result = subprocess.run(["aws", "sts", "get-caller-identity"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ AWS credentials configured")
            return True
        else:
            print("✗ AWS credentials not configured or invalid")
            return False
    except Exception:
        print("✗ Unable to verify AWS credentials")
        return False

def main():
    """Generate patient reports for all SMF patients"""
    print("SMF Patient Reports Generator")
    print("=" * 50)
    
    # Check AWS CLI availability
    if not check_aws_cli():
        print("\nERROR: AWS CLI is required for uploading files to S3")
        print("Please install AWS CLI: https://aws.amazon.com/cli/")
        sys.exit(1)
    
    # Check AWS credentials
    if not check_aws_credentials():
        print("\nERROR: AWS credentials not configured")
        print("Please run: aws configure")
        sys.exit(1)
    
    # Check if pathology directory exists
    if not os.path.exists(PATHOLOGY_DIR):
        print(f"\nERROR: Pathology directory not found: {PATHOLOGY_DIR}")
        sys.exit(1)
    
    # Get available report files
    available_files = get_available_report_files()
    if not available_files:
        print(f"\nERROR: No report files found in {PATHOLOGY_DIR}")
        sys.exit(1)
    
    print(f"\nFound {len(available_files)} report files:")
    for f in available_files:
        print(f"  - {f}")
    
    # Ask for confirmation
    print(f"\nThis will generate reports for {len(PATIENT_IDS)} patients.")
    print(f"Files will be uploaded to S3 bucket: {S3_BUCKET}")
    
    dry_run = input("\nRun in dry-run mode? (y/N): ").lower().startswith('y')
    
    if not dry_run:
        confirm = input("Proceed with actual uploads? (y/N): ").lower().startswith('y')
        if not confirm:
            print("Operation cancelled.")
            sys.exit(0)
    
    print(f"\n{'='*50}")
    print("GENERATING PATIENT REPORTS")
    print(f"{'='*50}")
    
    all_reports = []
    
    for i, patient_id in enumerate(PATIENT_IDS, 1):
        demographics = PATIENT_DEMOGRAPHICS[patient_id]
        print(f"\nPatient {i}/{len(PATIENT_IDS)}: {demographics['name']} (ID: {patient_id})")
        
        patient_reports = generate_patient_reports(patient_id, available_files, dry_run)
        all_reports.extend(patient_reports)
    
    # Save to JSON file
    output_file = "../data/generated_patient_reports.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_reports, f, indent=2, default=str)
    
    print(f"\n{'='*50}")
    print("GENERATION COMPLETE")
    print(f"{'='*50}")
    print(f"Total reports generated: {len(all_reports)}")
    print(f"Data saved to: {output_file}")
    
    # Statistics
    patients_with_reports = len(set(report['patient']['$oid'] for report in all_reports))
    avg_reports_per_patient = len(all_reports) / patients_with_reports if patients_with_reports > 0 else 0
    
    print(f"\nStatistics:")
    print(f"  - Patients with reports: {patients_with_reports}")
    print(f"  - Average reports per patient: {avg_reports_per_patient:.1f}")
    print(f"  - S3 bucket used: {S3_BUCKET}")
    
    if dry_run:
        print(f"\n⚠️  DRY RUN MODE - No files were actually uploaded")
    else:
        print(f"\n✓ Files uploaded to S3 and report records created")
    
    print(f"\nSample report record:")
    if all_reports:
        print(json.dumps(all_reports[0], indent=2, default=str)[:500] + "...")
    
    return all_reports

if __name__ == "__main__":
    main() 