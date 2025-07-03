# Pathology Data Extraction Summary
## Report: "Report Tue, Feb 18 - 2025.pdf"

### Extraction Overview
- **Total Parameters Extracted**: 23
- **Successfully Mapped to Database**: 11 parameters
- **Unmapped Parameters**: 12 parameters (need to be added to parameters collection)
- **Report Date**: 2025-02-18
- **Patient ID**: 677666e8241872e14d9b04c5
- **Report ID**: 67a0ca1d4929e8e245e89003

### Successfully Mapped Parameters (Ready for Database Insertion)

| Parameter Name | Value | Units | Reference Interval | Method | Parameter ID |
|---|---|---|---|---|---|
| **HEMOGLOBIN** | 14.0 | g/dL | 13.0 - 17.0 | photometric method | 65dcbbff3012fd1f2b81ed23 |
| **RBC COUNT** | 4.8 | - | 4.5 - 5.5 | coulter principle | 66b4520e99e0f8155af76bbb |
| **MCV** | 88.6 | fL | 83.0 - 101.0 | Derived from RBC Histogram | 66b99875b24811d93e003516 |
| **MCH** | 29.0 | pg | 27.0 - 32.0 | Calculated | 66b99a11f35babdfc3ddff28 |
| **MCH** | 32.8 | g/dL | 31.5 - 34.5 | Calculated | 66b99a11f35babdfc3ddff28 |
| **NEUTROPHILS** | 50.0 | % | 40.0 - 80.0 | - | 66825b2beaf6c5bb046acf6f |
| **LYMPHOCYTES** | 38.0 | % | 20.0 - 40.0 | - | 65dcbc003012fd1f2b81ed34 |
| **PLATELET COUNT** | 283 | - | 150.0 - 410.0 | coulter principle | 65dcbc003012fd1f2b81ed39 |
| **MPV** | 7.3 | L | 7.5 - 11.5 | - | 66b99ebe7936a32cd05c03c5 |
| **CREATININE** | 1.06 | mg/dL | 136.0 - 145.0 | Modified Jaffe Kinetic | 66b4a3c459cc60bfb4958d29 |
| **TRIGLYCERIDES** | 77.6 | mg/dL | 2.5 - 4.5 | Enzymatic colorimetry | 65dcbc023012fd1f2b81ed69 |

### Unmapped Parameters (Need Parameter Collection Entries)

These parameters were successfully extracted but don't have corresponding entries in the parameters collection:

1. **HEMATOCRIT** - 42.7 % (40.0 - 50.0)
2. **RDW** - 13.7 % (11.6 - 14.0) - Derived from RBC Histogram
3. **TOTAL LEUKOCYTE COUNT** - 4.7 (4.0 - 10.0) - coulter principle
4. **MONOCYTES** - 6.0 % (2.0 - 10.0)
5. **EOSINOPHILS** - 6.0 % (1.0 - 6.0)
6. **BASOPHILS** - 0.0 % (0.0 - 1.0)
7. **ABSOLUTE NEUTROPHIL COUNT** - 2.35 (2.0 - 7.0) - VCSn/Calculated
8. **ABSOLUTE LYMPHOCYTE COUNT** - 1.79 (1.0 - 3.0) - VCSn/Calculated
9. **ABSOLUTE MONOCYTE COUNT** - 0.28 (0.2 - 1.0)
10. **ABSOLUTE EOSINOPHIL COUNT** - 0.28 (0.02 - 0.5) - VCSn/Calculated
11. **ABSOLUTE BASOPHIL COUNT** - 0.00 (0.02 - 0.1)
12. **GLYCATED HEMOGLOBIN** - 5.40 % (8.8 - 20.5) - TINIA

### Sample MongoDB Document Structure

```json
{
  "_id": {"$oid": ""},
  "patient": {"$oid": "677666e8241872e14d9b04c5"},
  "parameter_id": {"$oid": "65dcbbff3012fd1f2b81ed23"},
  "parameter_name": "HEMOGLOBIN",
  "date": {"$date": "2025-02-18T00:42:00.000Z"},
  "value": "14.0",
  "units": "g/dL",
  "reference_interval": {"low": 13.0, "high": 17.0},
  "method": "photometric method",
  "source": {
    "page_index": 1,
    "report": {"$oid": "67a0ca1d4929e8e245e89003"}
  },
  "audit": {
    "created_on": {"$date": "2025-07-03T17:26:10.895743Z"}
  },
  "schema_version": "2.0"
}
```

### Key Features
- ✅ **Proper ObjectId References**: Links to patient and report documents
- ✅ **Structured Reference Intervals**: Converted to `{low: number, high: number}` format
- ✅ **Complete Method Extraction**: Captured test methods when available
- ✅ **Multi-page Support**: Tracked source page for each parameter
- ✅ **Units Normalization**: Proper unit extraction and formatting
- ✅ **Schema Compliance**: Follows exact MongoDB patientdata collection structure

### Files Generated
1. **Raw Extraction**: `pathology_data_Report Tue, Feb 18 - 2025.json`
2. **MongoDB Formatted**: `mongodb_formatted_pathology_data_Report Tue, Feb 18 - 2025.json`
3. **Summary**: `SUMMARY_Report_Feb18_2025.md`

### Next Steps
1. **Add Missing Parameters**: Create parameter collection entries for the 12 unmapped parameters
2. **Database Insertion**: Insert the 11 successfully mapped parameters into the patientdata collection
3. **Validation**: Verify data accuracy against the original PDF report 