#!/usr/bin/env python3
"""
extract_pathology_data.py
-------------------------
Extract pathology parameters from PDF reports and format them for MongoDB patientdata collection.

Usage:
    python smf/scripts/extract_pathology_data.py --input "smf/data/pathology/Report Tue, Feb 18 - 2025.pdf"
"""

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
import sys

try:
    import fitz  # PyMuPDF
except ImportError:
    print("PyMuPDF not found. Install with: pip install PyMuPDF")
    sys.exit(1)

def extract_text_from_pdf(pdf_path: Path) -> str:
    """Extract all text content from PDF."""
    doc = fitz.open(pdf_path)
    full_text = ""
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()
        full_text += f"\n--- PAGE {page_num + 1} ---\n{text}"
    
    doc.close()
    return full_text

def clean_parameter_name(name: str) -> str:
    """Clean parameter name by removing method info and normalizing."""
    # Remove parenthetical method descriptions
    name = re.sub(r'\([^)]+\)', '', name)
    # Remove extra whitespace and newlines
    name = ' '.join(name.split())
    return name.strip()

def parse_pathology_data(text: str, report_date: str) -> list:
    """Parse pathology parameters from extracted text."""
    
    parameters = []
    
    # Split text into lines for easier processing
    lines = text.split('\n')
    
    # Track which page we're on
    current_page = 1
    
    # State machine variables
    current_param = {}
    state = 'looking_for_param'  # 'looking_for_param', 'found_param', 'found_method', 'found_value', 'found_units'
    
    # Known parameter names (more comprehensive list)
    known_params = [
        'Hemoglobin', 'RBC Count', 'Hematocrit', 'MCV', 'MCH', 'MCHC', 'RDW', 
        'Total Leukocyte Count', 'Neutrophils', 'Lymphocytes', 'Monocytes', 
        'Eosinophils', 'Basophils', 'Absolute Neutrophil Count', 
        'Absolute Lymphocyte Count', 'Absolute Monocyte Count', 
        'Absolute Eosinophil Count', 'Absolute Basophil Count', 'Platelet Count',
        'MPV', 'Glycated Hemoglobin', 'Random Blood Sugar', 'Creatinine',
        'Blood Urea Nitrogen', 'Uric Acid', 'Total Cholesterol', 'HDL Cholesterol',
        'LDL Cholesterol', 'Triglycerides', 'SGOT', 'SGPT', 'Alkaline Phosphatase',
        'Total Bilirubin', 'Direct Bilirubin', 'Indirect Bilirubin'
    ]
    
    for i, line in enumerate(lines):
        line = line.strip()
        
        # Track page changes
        if line.startswith('--- PAGE'):
            page_match = re.search(r'PAGE (\d+)', line)
            if page_match:
                current_page = int(page_match.group(1))
            continue
        
        # Skip empty lines and major headers
        if not line or line in ['HAEMATOLOGY', 'Complete Blood Counts', 'Differential count % (VCSn Technology & light microscopy)', 'Differential Counts, Absolute(calculated)']:
            continue
        
        # State machine logic
        if state == 'looking_for_param':
            # Look for parameter names
            param_name = None
            
            # Check for exact matches first
            if line in known_params:
                param_name = line
            # Check for parameters with additional info in parentheses
            elif any(line.startswith(param) for param in known_params):
                for param in known_params:
                    if line.startswith(param):
                        param_name = param
                        break
            # Handle parameters with full names like "MCV(Mean Corpuscular Volume)"
            elif '(' in line:
                base_name = line.split('(')[0].strip()
                if base_name in known_params:
                    param_name = base_name
            
            if param_name:
                current_param = {
                    'name': param_name,
                    'method': '',
                    'page': current_page,
                    'value': '',
                    'units': '',
                    'reference': ''
                }
                state = 'found_param'
        
        elif state == 'found_param':
            # Look for method in parentheses or value
            if line.startswith('(') and line.endswith(')'):
                current_param['method'] = line[1:-1]
                state = 'found_method'
            elif re.match(r'^\d+\.?\d*$', line):
                # Direct value without method
                current_param['value'] = line
                state = 'found_value'
        
        elif state == 'found_method':
            # Look for value
            if re.match(r'^\d+\.?\d*$', line):
                current_param['value'] = line
                state = 'found_value'
        
        elif state == 'found_value':
            # Look for units
            if re.match(r'^[A-Za-z/%^µ³⁶/]+$', line):
                current_param['units'] = line
                state = 'found_units'
            elif re.match(r'^\d+\.?\d*\s*-\s*\d+\.?\d*$', line):
                # Reference range without units
                current_param['reference'] = line
                state = 'complete'
        
        elif state == 'found_units':
            # Look for reference range
            if re.match(r'^\d+\.?\d*\s*-\s*\d+\.?\d*$', line) or re.match(r'^\d+-\d+$', line):
                current_param['reference'] = line
                state = 'complete'
        
        # Complete parameter
        if state == 'complete':
            parameter_doc = {
                "_id": {"$oid": ""},  # Would be generated by MongoDB
                "patient": {"$oid": ""},  # Would need to be provided
                "parameter_id": {"$oid": ""},  # Would need parameter collection lookup
                "parameter_name": current_param['name'],
                "date": {"$date": f"{report_date}T00:42:00.000Z"},
                "value": current_param['value'],
                "units": current_param['units'],
                "reference_interval": current_param['reference'],
                "method": current_param['method'],
                "source": {
                    "page_index": current_param['page'],
                    "report": {"$oid": ""}  # Would be the report document ID
                },
                "audit": {
                    "created_on": {"$date": datetime.now().isoformat() + "Z"}
                },
                "schema_version": "2.0"
            }
            
            parameters.append(parameter_doc)
            current_param = {}
            state = 'looking_for_param'
    
    return parameters

def main():
    parser = argparse.ArgumentParser(description="Extract pathology data from PDF report")
    parser.add_argument("--input", required=True, type=Path, help="Path to PDF report")
    parser.add_argument("--output", type=Path, help="Output JSON file (optional)")
    parser.add_argument("--show-text", action="store_true", help="Show extracted text for debugging")
    args = parser.parse_args()
    
    if not args.input.exists():
        print(f"Error: Input file {args.input} does not exist")
        sys.exit(1)
    
    print(f"Extracting text from {args.input}...")
    text = extract_text_from_pdf(args.input)
    
    if args.show_text:
        print(f"\nFull extracted text:")
        print("=" * 80)
        print(text)
        print("=" * 80)
    
    # Extract date from filename (e.g., "Report Tue, Feb 18 - 2025.pdf")
    filename = args.input.name
    date_match = re.search(r'(\w+)\s+(\d+)\s*-\s*(\d+)', filename)
    if date_match:
        month = date_match.group(1)
        day = date_match.group(2)
        year = date_match.group(3)
        # Convert month name to number (basic implementation)
        month_map = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06',
                    'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
        month_num = month_map.get(month[:3], '01')
        report_date = f"{year}-{month_num}-{day.zfill(2)}"
    else:
        report_date = "2025-02-18"  # Default date
    
    print(f"Parsing pathology parameters for date: {report_date}")
    parameters = parse_pathology_data(text, report_date)
    
    print(f"\nFound {len(parameters)} pathology parameters:")
    print("-" * 80)
    for i, param in enumerate(parameters, 1):
        print(f"{i:2d}. {param['parameter_name']}")
        print(f"    Value: {param['value']} {param['units']}")
        if param['reference_interval']:
            print(f"    Reference: {param['reference_interval']}")
        if param['method']:
            print(f"    Method: {param['method']}")
        print(f"    Page: {param['source']['page_index']}")
        print()
    
    # Save to file if output path provided
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(parameters, f, indent=2)
        print(f"Parameters saved to {args.output}")
    
    # Also save a sample document for reference
    if parameters:
        sample_output = args.input.parent / f"pathology_data_{args.input.stem}.json"
        with open(sample_output, 'w') as f:
            json.dump(parameters, f, indent=2)
        print(f"Pathology data saved to: {sample_output}")

if __name__ == "__main__":
    main() 