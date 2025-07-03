# SMF PatientData Mapping Script

This script generates `patientdata` records for SMF patients by mapping existing data between MongoDB clusters.

## How it works

1. **Reverse Mapping**: Finds SMF patients' reports in Demo Cluster → Gets originalnames → Backtracks to old report IDs
2. **Data Filtering**: Fetches existing patientdata records from Original MongoDB that reference those old report IDs
3. **Transformation**: Updates patientId, source.report ID, and audit timestamps for Demo Cluster insertion
4. **Output**: Generates JSON ready for MongoDB insertion

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create `.env` file in the project root with:
   ```bash
   # Original MongoDB (source of patientdata)
   ORIGINAL_MONGODB_URL=mongodb+srv://username:password@original-cluster.mongodb.net/
   
   # Demo Cluster MongoDB (target for transformed data)  
   DEMO_MONGODB_URL=mongodb+srv://username:password@demo-cluster.mongodb.net/
   ```

## Usage

```bash
cd smf/scripts
python generate_patientdata_mapping.py
```

## Output

- File: `smf/data/generated_smf_patientdata.json`
- Contains: Transformed patientdata records ready for Demo Cluster insertion
- Format: MongoDB-compatible JSON with proper ObjectId references

## Process Flow

```
SMF Patients (Demo Cluster)
    ↓ (get pathology reports)
Report originalnames
    ↓ (backtrack via reports_in_use.json)
Old Report IDs (Original MongoDB)
    ↓ (filter patientdata)
Existing PatientData Records
    ↓ (transform)
New PatientData Records (for Demo Cluster)
```

## Key Features

- **Intelligent Mapping**: Uses originalname as the bridge between old and new report IDs
- **Timestamp Sync**: Sets audit.created_on to report upload_time + 30 minutes
- **SMF Staff Assignment**: Randomly assigns SMF staff as created_by users
- **Duplicate Handling**: Creates separate records if multiple reports with same originalname exist 