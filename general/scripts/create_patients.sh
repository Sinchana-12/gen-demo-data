#!/bin/bash

# Configuration
API_BASE_URL="https://api-stg2.janohealth.com/ops"
ACCESS_TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2ODVjMWVmNDA0YTZjMzE4OTM4MDE0NGMiLCJ1c2VyIjoie1wibmFtZVwiOlwiUHJpeWEgTmFpclwiLFwiZ2VuZGVyXCI6XCJmZW1hbGVcIixcInVzZXJfdHlwZVwiOlwic3RhZmZcIixcInNwZWNpYWxpemF0aW9uXCI6XCJnZW5lcmFsXCIsXCJwaG9uZVwiOlwiKzkxOTc2NTQzMjEwOVwiLFwiZW1haWxcIjpcInByaXlhLm5haXJAc21mLm9yZ1wiLFwib3JnYW5pemF0aW9uc1wiOltdLFwiaHBpblwiOlwiJDJiJDEwJFlvQ1dNeFdBZnV2Q0RkMDh5cU42a2U0S3R6WHUwREVwd1VnR0hYVmRNMmhTalg2dVZrUHFDXCIsXCJ0ZWFtc1wiOlt7XCJvcmdfaWRcIjpcIjY4NWMxOGY1MDRhNmMzMTg5MzgwMTQyN1wiLFwib3JnX25hbWVcIjpcIlN1bmRhcmFtIE1lZGljYWwgRm91bmRhdGlvblwiLFwiZGVwdF9jb2RlXCI6XCJORVBIUk9cIixcInRlYW1faWRcIjpcIjY4NWMxOGY1MDRhNmMzMTg5MzgwMTQzMFwiLFwidGVhbV9uYW1lXCI6XCJSZW5hbCBDYXJlIFVuaXRcIixcInJvbGVcIjpcImRjX2luY2hhcmdlXCIsXCJkZXNpZ25hdGlvblwiOlwiSW5jaGFyZ2VcIixcInRlYW1fcGhvbmVcIjpcIis5MTk4NzY1NDMyMTBcIn1dLFwiaWRcIjpcIjY4NWMxZWY0MDRhNmMzMTg5MzgwMTQ0Y1wifSIsImF1dGhfaWQiOiJyZW5hbGNhcmVAamFuby5oZWFsdGgiLCJvcmdfaWRzIjpbIjY4NWMxOGY1MDRhNmMzMTg5MzgwMTQyNyJdLCJ0ZWFtX2lkcyI6WyI2ODVjMThmNTA0YTZjMzE4OTM4MDE0MzAiXSwiaWF0IjoxNzUwOTE3MzEwLCJleHAiOjE3NTEwMDA0MDB9.wDRcPPRlUe30WDolCYkhwKMLoiyJjMonBxw_W0KUCBw"
TEAM_ID="685c18f504a6c31893801430"
ORG_ID="685c18f504a6c31893801427"

# Function to create a patient
create_patient() {
    local patient_data="$1"
    local patient_name="$2"
    
    echo "Creating patient: $patient_name"
    
    response=$(curl -s -w "HTTPSTATUS:%{http_code}" \
        -X POST \
        -H "Authorization: Bearer $ACCESS_TOKEN" \
        -H "Content-Type: application/json" \
        -d "$patient_data" \
        "$API_BASE_URL/patients?team_id=$TEAM_ID&org_id=$ORG_ID")
    
    # Extract HTTP status code
    http_code=$(echo "$response" | grep -o "HTTPSTATUS:[0-9]*" | cut -d: -f2)
    
    # Extract response body
    response_body=$(echo "$response" | sed -E 's/HTTPSTATUS:[0-9]*$//')
    
    if [ "$http_code" -eq 200 ] || [ "$http_code" -eq 201 ]; then
        echo "✅ SUCCESS: Created $patient_name"
        patient_id=$(echo "$response_body" | grep -o '"_id":"[^"]*"' | cut -d'"' -f4)
        echo "   Patient ID: $patient_id"
        echo "$patient_name,$patient_id" >> created_patients.csv
    else
        echo "❌ FAILED: $patient_name (HTTP $http_code)"
        echo "   Error: $response_body"
        echo "$patient_name,ERROR: HTTP $http_code" >> failed_patients.csv
    fi
    
    echo "---"
    sleep 0.5
}

# Initialize result files
echo "Patient Name,Patient ID" > created_patients.csv
echo "Patient Name,Error" > failed_patients.csv

echo "Starting patient creation..."
echo "API Endpoint: $API_BASE_URL/patients"
echo "Team ID: $TEAM_ID"
echo "Org ID: $ORG_ID"
echo "=================================================="

# Read patients from JSON and create them one by one
patients=$(cat create_patients.json)

# Extract each patient and create them
echo "$patients" | jq -c '.[]' | while read -r patient; do
    patient_name=$(echo "$patient" | jq -r '.name')
    create_patient "$patient" "$patient_name"
done

echo "=================================================="
echo "Patient creation completed!"
echo ""
echo "Results:"
echo "✅ Successfully created patients: $(tail -n +2 created_patients.csv | wc -l)"
echo "❌ Failed patients: $(tail -n +2 failed_patients.csv | wc -l)"
echo ""
echo "Check created_patients.csv and failed_patients.csv for details." 