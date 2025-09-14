#!/usr/bin/env python3
"""
Quantum AI Lead Ingestion Engine
Processes contact lists and prepares them for NQBA quantum lead scoring
"""

import json
from datetime import datetime
import logging
from typing import List, Dict, Optional, Union
from dataclasses import dataclass
import os
from dotenv import load_dotenv
import csv
import requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Simple in-memory storage for testing
class LeadStorage:
    def __init__(self):
        self.leads = []
        self.next_id = 1
    
    def add_lead(self, lead_data):
        lead_data['id'] = self.next_id
        lead_data['created_at'] = datetime.utcnow().isoformat()
        lead_data['updated_at'] = datetime.utcnow().isoformat()
        self.leads.append(lead_data)
        self.next_id += 1
        return lead_data
    
    def get_all_leads(self):
        return self.leads
    
    def get_lead_count(self):
        return len(self.leads)

# Global storage instance
lead_storage = LeadStorage()

@dataclass
class LeadData:
    """Lead data structure for ingestion"""
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    company: Optional[str] = None
    title: Optional[str] = None
    industry: Optional[str] = None
    linkedin_url: Optional[str] = None
    website: Optional[str] = None
    location: Optional[str] = None
    revenue: Optional[str] = None
    employees: Optional[str] = None
    source: Optional[str] = None
    notes: Optional[str] = None

class LeadIngestionEngine:
    """Advanced lead ingestion engine with quantum-enhanced processing"""
    
    def __init__(self):
        load_dotenv()
        
        # Use global storage
        self.storage = lead_storage
        
        # API configurations
        self.clearbit_api_key = os.getenv('CLEARBIT_API_KEY', 'demo_key')
        self.hunter_api_key = os.getenv('HUNTER_API_KEY', 'demo_key')
        self.linkedin_api_key = os.getenv('LINKEDIN_API_KEY', 'demo_key')
        
        # Quantum scoring endpoint
        self.quantum_scoring_url = os.getenv('QUANTUM_SCORING_URL', 'http://localhost:8001/score')
        
        # Statistics
        self.stats = {
            'processed': 0,
            'valid': 0,
            'enriched': 0,
            'errors': 0
        }
    
    def validate_email(self, email: str) -> bool:
        """Simple email validation"""
        if not email or '@' not in email:
            return False
        
        parts = email.split('@')
        if len(parts) != 2:
            return False
        
        local, domain = parts
        if not local or not domain or '.' not in domain:
            return False
        
        return True
    
    def validate_phone(self, phone: str, country_code: str = 'US') -> tuple[bool, str]:
        """Simple phone validation and formatting"""
        if not phone:
            return False, ''
        
        # Remove all non-digit characters
        digits = ''.join(filter(str.isdigit, phone))
        
        # Basic validation - should have 10-15 digits
        if len(digits) >= 10 and len(digits) <= 15:
            # Format as +1-XXX-XXX-XXXX for US numbers
            if len(digits) == 10:
                formatted = f"+1-{digits[:3]}-{digits[3:6]}-{digits[6:]}"
            elif len(digits) == 11 and digits.startswith('1'):
                formatted = f"+{digits[0]}-{digits[1:4]}-{digits[4:7]}-{digits[7:]}"
            else:
                formatted = f"+{digits}"
            return True, formatted
        
        return False, phone
    
    def enrich_lead_data(self, lead_data: LeadData) -> LeadData:
        """Enrich lead data using external APIs (placeholder for real enrichment)"""
        # In production, integrate with:
        # - Clearbit for company data
        # - ZoomInfo for contact enrichment
        # - LinkedIn Sales Navigator API
        # - Apollo.io or similar
        
        enriched = lead_data
        
        # Mock enrichment logic
        if lead_data.company and not lead_data.industry:
            # Simulate industry detection
            company_lower = lead_data.company.lower()
            if any(tech in company_lower for tech in ['software', 'tech', 'ai', 'saas']):
                enriched.industry = 'Technology'
            elif any(fin in company_lower for fin in ['bank', 'finance', 'capital']):
                enriched.industry = 'Financial Services'
            elif any(health in company_lower for health in ['health', 'medical', 'pharma']):
                enriched.industry = 'Healthcare'
        
        return enriched
    
    def process_csv_file(self, file_path: str, mapping: Dict[str, str] = None) -> List[LeadData]:
        """Process CSV file and extract lead data"""
        leads = []
        
        # Default column mapping
        default_mapping = {
            'first_name': ['first_name', 'firstname', 'first', 'fname'],
            'last_name': ['last_name', 'lastname', 'last', 'lname'],
            'email': ['email', 'email_address', 'mail'],
            'phone': ['phone', 'phone_number', 'mobile', 'tel'],
            'company': ['company', 'organization', 'org'],
            'title': ['title', 'job_title', 'position'],
            'industry': ['industry', 'sector'],
            'linkedin_url': ['linkedin', 'linkedin_url', 'linkedin_profile'],
            'website': ['website', 'company_website', 'url'],
            'location': ['location', 'city', 'address'],
            'revenue': ['revenue', 'annual_revenue', 'company_revenue'],
            'employees': ['employees', 'company_size', 'headcount']
        }
        
        if mapping:
            default_mapping.update(mapping)
        
        try:
            df = pd.read_csv(file_path)
            logger.info(f"Processing {len(df)} rows from {file_path}")
            
            for _, row in df.iterrows():
                lead_dict = {}
                
                # Map columns to lead fields
                for field, possible_cols in default_mapping.items():
                    for col in possible_cols:
                        if col in df.columns and pd.notna(row[col]):
                            lead_dict[field] = str(row[col]).strip()
                            break
                
                # Ensure required fields
                if 'first_name' in lead_dict and 'last_name' in lead_dict and 'email' in lead_dict:
                    lead = LeadData(**lead_dict)
                    leads.append(lead)
                else:
                    logger.warning(f"Skipping row due to missing required fields: {lead_dict}")
                    self.stats['invalid_leads'] += 1
                
                self.stats['total_processed'] += 1
        
        except Exception as e:
            logger.error(f"Error processing CSV file {file_path}: {e}")
        
        return leads
    
    def process_json_file(self, file_path: str) -> List[LeadData]:
        """Process JSON file and extract lead data"""
        leads = []
        
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            # Handle different JSON structures
            if isinstance(data, list):
                lead_list = data
            elif isinstance(data, dict) and 'leads' in data:
                lead_list = data['leads']
            elif isinstance(data, dict) and 'contacts' in data:
                lead_list = data['contacts']
            else:
                lead_list = [data]
            
            for item in lead_list:
                try:
                    lead = LeadData(**item)
                    leads.append(lead)
                    self.stats['total_processed'] += 1
                except Exception as e:
                    logger.warning(f"Skipping invalid lead data: {e}")
                    self.stats['invalid_leads'] += 1
        
        except Exception as e:
            logger.error(f"Error processing JSON file {file_path}: {e}")
        
        return leads
    
    def save_leads_to_db(self, leads: List[LeadData]) -> int:
        """Save processed leads to storage"""
        saved_count = 0
        
        try:
            for lead_data in leads:
                # Validate email
                email_valid = self.validate_email(lead_data.email)
                
                # Validate phone
                phone_valid, formatted_phone = self.validate_phone(lead_data.phone)
                
                # Check for duplicates
                existing_leads = self.storage.get_all_leads()
                duplicate_found = False
                for lead in existing_leads:
                    if lead.get('email') == lead_data.email:
                        logger.info(f"Duplicate lead found: {lead_data.email}")
                        self.stats['duplicates'] += 1
                        duplicate_found = True
                        break
                
                if duplicate_found:
                    continue
                
                # Enrich data
                enriched_data = self.enrich_lead_data(lead_data)
                
                # Create lead record
                lead_dict = {
                    'first_name': enriched_data.first_name,
                    'last_name': enriched_data.last_name,
                    'email': enriched_data.email,
                    'phone': formatted_phone if phone_valid else enriched_data.phone,
                    'company': enriched_data.company,
                    'title': enriched_data.title,
                    'industry': enriched_data.industry,
                    'linkedin_url': enriched_data.linkedin_url,
                    'website': enriched_data.website,
                    'location': enriched_data.location,
                    'revenue': enriched_data.revenue,
                    'employees': enriched_data.employees,
                    'source': enriched_data.source,
                    'notes': enriched_data.notes,
                    'email_valid': email_valid,
                    'phone_valid': phone_valid,
                    'data_enriched': True,
                    'status': 'new',
                    'quantum_score': 0.0
                }
                
                self.storage.add_lead(lead_dict)
                saved_count += 1
                
                if email_valid:
                    self.stats['valid_leads'] += 1
                else:
                    self.stats['invalid_leads'] += 1
                
                if enriched_data != lead_data:
                    self.stats['enriched'] += 1
            
            logger.info(f"Successfully saved {saved_count} leads to storage")
        
        except Exception as e:
            logger.error(f"Error saving leads to storage: {e}")
        
        return saved_count
    
    def process_file(self, file_path: str, mapping: Dict[str, str] = None) -> Dict:
        """Process a single file (CSV or JSON)"""
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        logger.info(f"Processing file: {file_path}")
        
        # Reset stats for this file
        self.stats = {key: 0 for key in self.stats}
        
        if file_path.suffix.lower() == '.csv':
            leads = self.process_csv_file(str(file_path), mapping)
        elif file_path.suffix.lower() == '.json':
            leads = self.process_json_file(str(file_path))
        else:
            raise ValueError(f"Unsupported file format: {file_path.suffix}")
        
        # Save to database
        saved_count = self.save_leads_to_db(leads)
        
        # Update stats
        self.stats['saved'] = saved_count
        
        return self.stats
    
    def batch_process_directory(self, directory_path: str, pattern: str = "*.csv") -> Dict:
        """Process all files in a directory matching the pattern"""
        directory = Path(directory_path)
        files = list(directory.glob(pattern))
        
        logger.info(f"Found {len(files)} files to process in {directory}")
        
        total_stats = {key: 0 for key in self.stats}
        
        for file_path in files:
            try:
                file_stats = self.process_file(str(file_path))
                for key, value in file_stats.items():
                    total_stats[key] += value
                
                logger.info(f"Completed processing {file_path.name}: {file_stats}")
            
            except Exception as e:
                logger.error(f"Error processing {file_path}: {e}")
        
        return total_stats
    
    def export_leads_for_quantum_scoring(self, output_file: str = "leads_for_scoring.json") -> str:
        """Export leads ready for quantum scoring"""
        session = self.SessionLocal()
        
        try:
            # Get unscored leads with valid email
            leads = session.query(Lead).filter(
                Lead.quantum_score == 0.0,
                Lead.email_valid == True,
                Lead.status == 'new'
            ).all()
            
            export_data = []
            for lead in leads:
                lead_dict = {
                    'id': str(lead.id),
                    'first_name': lead.first_name,
                    'last_name': lead.last_name,
                    'email': lead.email,
                    'phone': lead.phone,
                    'company': lead.company,
                    'title': lead.title,
                    'industry': lead.industry,
                    'location': lead.location,
                    'revenue': lead.revenue,
                    'employees': lead.employees,
                    'created_at': lead.created_at.isoformat() if lead.created_at else None
                }
                export_data.append(lead_dict)
            
            with open(output_file, 'w') as f:
                json.dump(export_data, f, indent=2)
            
            logger.info(f"Exported {len(export_data)} leads to {output_file}")
            return output_file
        
        finally:
            session.close()

# CLI Interface
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Quantum AI Lead Ingestion Engine")
    parser.add_argument("--file", "-f", help="Single file to process")
    parser.add_argument("--directory", "-d", help="Directory to batch process")
    parser.add_argument("--pattern", "-p", default="*.csv", help="File pattern for batch processing")
    parser.add_argument("--export", "-e", action="store_true", help="Export leads for quantum scoring")
    parser.add_argument("--db-url", default="postgresql://localhost/quantum_leads", help="Database URL")
    
    args = parser.parse_args()
    
    engine = LeadIngestionEngine(db_url=args.db_url)
    
    if args.export:
        output_file = engine.export_leads_for_quantum_scoring()
        print(f"Leads exported to: {output_file}")
    
    elif args.file:
        stats = engine.process_file(args.file)
        print(f"Processing complete: {stats}")
    
    elif args.directory:
        stats = engine.batch_process_directory(args.directory, args.pattern)
        print(f"Batch processing complete: {stats}")
    
    else:
        print("Please specify --file, --directory, or --export")
        parser.print_help()