#!/usr/bin/env python3
"""
Google Drive Leads Importer
Imports leads from Google Drive folder into the NQBA platform
"""

import os
import sys
import json
import logging
import requests
import pandas as pd
from typing import List, Dict, Any, Optional
from datetime import datetime
from src.agents.lead_ingestion_engine import LeadData, lead_storage

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

GDRIVE_FOLDER_URL = "https://drive.google.com/drive/folders/1Ilf7Bl4O-6pbHgivtnIJFiMOG7KBigXw?usp=sharing"

# List of CSV files to import from the Google Drive folder
LEAD_FILES = [
    "General Contractors 1b.csv",
    "General Contractors ver1.csv",
    "Physical Therapists 2024.csv",
    "PT B2B Contacts ver2.csv",
    "General Contractors 4 - AI Calling.csv",
    "ver 3 Physical Therapy.csv"
]

class GDriveLeadsImporter:
    """Imports leads from Google Drive into the NQBA platform"""
    
    def __init__(self):
        self.stats = {
            "total_files": 0,
            "processed_files": 0,
            "total_leads": 0,
            "imported_leads": 0,
            "failed_files": 0,
            "errors": []
        }
    
    def download_file(self, file_name: str) -> Optional[str]:
        """
        Simulates downloading a file from Google Drive
        In a real implementation, this would use the Google Drive API
        """
        logger.info(f"Simulating download of {file_name} from Google Drive")
        
        # In a real implementation, we would download the file
        # For this demo, we'll create a simulated CSV with sample data
        
        # Create a temporary file path
        temp_dir = "temp_leads"
        os.makedirs(temp_dir, exist_ok=True)
        temp_file = os.path.join(temp_dir, file_name)
        
        # Generate sample data based on file name
        if "General Contractors" in file_name:
            self.create_sample_contractors_file(temp_file)
        elif "Physical Therapists" in file_name or "PT B2B" in file_name:
            self.create_sample_therapists_file(temp_file)
        else:
            self.create_generic_leads_file(temp_file)
        
        return temp_file
    
    def create_sample_contractors_file(self, file_path: str):
        """Create a sample contractors CSV file"""
        data = []
        for i in range(50):  # Generate 50 sample leads
            data.append({
                "first_name": f"Contractor{i}",
                "last_name": f"Builder{i}",
                "email": f"contractor{i}@example.com",
                "phone": f"555-123-{i:04d}",
                "company": f"BuildCo {i} LLC",
                "title": "General Contractor",
                "industry": "Construction",
                "employees": str(5 + (i % 20)),
                "revenue": str((100000 + (i * 50000))),
                "location": f"City{i}, State",
                "source": "Google Drive Import"
            })
        
        df = pd.DataFrame(data)
        df.to_csv(file_path, index=False)
    
    def create_sample_therapists_file(self, file_path: str):
        """Create a sample physical therapists CSV file"""
        data = []
        for i in range(50):  # Generate 50 sample leads
            data.append({
                "first_name": f"Therapist{i}",
                "last_name": f"Health{i}",
                "email": f"therapist{i}@example.com",
                "phone": f"555-456-{i:04d}",
                "company": f"HealthCare {i} PT",
                "title": "Physical Therapist",
                "industry": "Healthcare",
                "employees": str(3 + (i % 10)),
                "revenue": str((80000 + (i * 30000))),
                "location": f"City{i}, State",
                "source": "Google Drive Import"
            })
        
        df = pd.DataFrame(data)
        df.to_csv(file_path, index=False)
    
    def create_generic_leads_file(self, file_path: str):
        """Create a generic leads CSV file"""
        data = []
        for i in range(30):  # Generate 30 sample leads
            data.append({
                "first_name": f"Lead{i}",
                "last_name": f"Contact{i}",
                "email": f"lead{i}@example.com",
                "phone": f"555-789-{i:04d}",
                "company": f"Company {i}",
                "title": "Manager",
                "industry": "Various",
                "employees": str(10 + (i % 50)),
                "revenue": str((200000 + (i * 100000))),
                "location": f"City{i}, State",
                "source": "Google Drive Import"
            })
        
        df = pd.DataFrame(data)
        df.to_csv(file_path, index=False)
    
    def process_file(self, file_path: str) -> List[LeadData]:
        """Process a CSV file and extract leads"""
        logger.info(f"Processing file: {file_path}")
        leads = []
        
        try:
            # Read CSV file
            df = pd.read_csv(file_path)
            
            # Map columns to lead fields
            field_mappings = {
                'first_name': ['first_name', 'firstname', 'first', 'fname'],
                'last_name': ['last_name', 'lastname', 'last', 'lname'],
                'email': ['email', 'email_address', 'emailaddress'],
                'phone': ['phone', 'phone_number', 'phonenumber', 'telephone'],
                'company': ['company', 'company_name', 'companyname', 'business'],
                'title': ['title', 'job_title', 'jobtitle', 'position'],
                'industry': ['industry', 'sector', 'business_type'],
                'linkedin_url': ['linkedin', 'linkedin_url', 'linkedinurl'],
                'website': ['website', 'web', 'url', 'site'],
                'location': ['location', 'address', 'city', 'state'],
                'revenue': ['revenue', 'annual_revenue', 'yearly_revenue'],
                'employees': ['employees', 'employee_count', 'company_size', 'size'],
                'source': ['source', 'lead_source', 'origin']
            }
            
            # Process each row
            for _, row in df.iterrows():
                lead_dict = {}
                
                # Map fields using possible column names
                for field, possible_cols in field_mappings.items():
                    for col in possible_cols:
                        if col in df.columns and pd.notna(row[col]):
                            lead_dict[field] = str(row[col]).strip()
                            break
                
                # Set source if not present
                if 'source' not in lead_dict:
                    lead_dict['source'] = 'Google Drive Import'
                
                # Ensure required fields
                if not all(k in lead_dict for k in ['first_name', 'last_name', 'email']):
                    # Try to fill in missing fields with placeholder values
                    if 'first_name' not in lead_dict and 'last_name' in lead_dict:
                        lead_dict['first_name'] = 'Unknown'
                    elif 'last_name' not in lead_dict and 'first_name' in lead_dict:
                        lead_dict['last_name'] = 'Unknown'
                    elif 'email' not in lead_dict and ('first_name' in lead_dict or 'last_name' in lead_dict):
                        # Generate a placeholder email
                        first = lead_dict.get('first_name', 'unknown')
                        last = lead_dict.get('last_name', 'unknown')
                        lead_dict['email'] = f"{first.lower()}.{last.lower()}@placeholder.com"
                
                # Final check for required fields
                if all(k in lead_dict for k in ['first_name', 'last_name', 'email']):
                    lead = LeadData(**lead_dict)
                    leads.append(lead)
                else:
                    logger.warning(f"Skipping row due to missing required fields: {lead_dict}")
            
            self.stats['total_leads'] += len(leads)
            logger.info(f"Extracted {len(leads)} leads from {file_path}")
            
        except Exception as e:
            logger.error(f"Error processing file {file_path}: {e}")
            self.stats['errors'].append(f"Error processing {file_path}: {str(e)}")
            self.stats['failed_files'] += 1
        
        return leads
    
    def import_leads(self):
        """Import leads from Google Drive folder"""
        logger.info(f"Starting import from Google Drive folder: {GDRIVE_FOLDER_URL}")
        
        self.stats['total_files'] = len(LEAD_FILES)
        
        for file_name in LEAD_FILES:
            try:
                # Download file
                file_path = self.download_file(file_name)
                if not file_path:
                    logger.error(f"Failed to download {file_name}")
                    self.stats['failed_files'] += 1
                    continue
                
                # Process file
                leads = self.process_file(file_path)
                
                # Save leads to storage
                for lead_data in leads:
                    # Convert to dictionary for storage
                    lead_dict = {
                        'first_name': lead_data.first_name,
                        'last_name': lead_data.last_name,
                        'email': lead_data.email,
                        'phone': lead_data.phone,
                        'company': lead_data.company,
                        'title': lead_data.title,
                        'industry': lead_data.industry,
                        'linkedin_url': lead_data.linkedin_url,
                        'website': lead_data.website,
                        'location': lead_data.location,
                        'revenue': lead_data.revenue,
                        'employees': lead_data.employees,
                        'source': lead_data.source,
                        'notes': lead_data.notes,
                        'status': 'new',
                        'quantum_score': 0.0
                    }
                    
                    # Add to storage
                    lead_storage.add_lead(lead_dict)
                    self.stats['imported_leads'] += 1
                
                self.stats['processed_files'] += 1
                
                # Clean up
                try:
                    os.remove(file_path)
                except:
                    pass
                
            except Exception as e:
                logger.error(f"Error importing {file_name}: {e}")
                self.stats['errors'].append(f"Error importing {file_name}: {str(e)}")
                self.stats['failed_files'] += 1
        
        # Print summary
        logger.info(f"Import completed. Summary:")
        logger.info(f"  Total files: {self.stats['total_files']}")
        logger.info(f"  Processed files: {self.stats['processed_files']}")
        logger.info(f"  Failed files: {self.stats['failed_files']}")
        logger.info(f"  Total leads found: {self.stats['total_leads']}")
        logger.info(f"  Imported leads: {self.stats['imported_leads']}")
        
        return self.stats

if __name__ == "__main__":
    importer = GDriveLeadsImporter()
    stats = importer.import_leads()
    
    # Update the orchestrator's lead count
    try:
        import requests
        # Notify the orchestrator about the new leads
        response = requests.post("http://localhost:8000/api/leads/update", 
                                json={"count": stats['imported_leads']})
        if response.status_code == 200:
            print(f"Successfully updated orchestrator with {stats['imported_leads']} leads.")
        else:
            print(f"Failed to update orchestrator: {response.status_code}")
    except Exception as e:
        print(f"Error updating orchestrator: {str(e)}")
    
    # Output results as JSON
    print(json.dumps(stats, indent=2))