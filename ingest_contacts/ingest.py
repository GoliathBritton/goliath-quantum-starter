"""
Contact ingestion:
- Validates CSV
- Normalizes phone numbers to E.164
- Checks consent / DNC list (simple demonstration)
- Inserts records into Postgres and enqueues jobs into Redis (RQ)
"""

import csv, os, phonenumbers, logging
from sqlalchemy import create_engine, text
import pandas as pd
from redis import Redis
from rq import Queue
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
REDIS_URL = os.getenv("REDIS_URL")
DNC_TABLE = "dnc_list"

engine = create_engine(DATABASE_URL)
redis_conn = Redis.from_url(REDIS_URL)
q = Queue('dialer', connection=redis_conn)

logging.basicConfig(level=logging.INFO)

def normalize_phone(num, default_region="US"):
    try:
        pn = phonenumbers.parse(str(num), default_region)
        if phonenumbers.is_valid_number(pn):
            return phonenumbers.format_number(pn, phonenumbers.PhoneNumberFormat.E164)
    except Exception as e:
        return None

def load_dnc():
    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT phone FROM {DNC_TABLE}"))
        return set([r[0] for r in result.fetchall()])

def ingest_csv(path, chunk_size=5000):
    dnc = load_dnc()
    reader = pd.read_csv(path)
    total = 0
    for i in range(0, len(reader), chunk_size):
        batch = reader.iloc[i:i+chunk_size]
        rows = []
        for _, r in batch.iterrows():
            phone = normalize_phone(r.get('phone') or r.get('phone_number') or r.get('Phone'))
            if not phone:
                continue
            if phone in dnc:
                logging.info(f"Skipped DNC: {phone}")
                continue
            contact = {
                "company_name": r.get('company_name'),
                "contact_name": r.get('contact_name') or r.get('name'),
                "title": r.get('title'),
                "phone": phone,
                "email": r.get('email'),
                "industry": r.get('industry'),
                "company_size": r.get('company_size'),
                "annual_revenue": r.get('annual_revenue'),
                "timezone": r.get('timezone', 'US/Eastern'),
                "best_contact_time": r.get('best_contact_time', '09:00-17:00'),
                "consent_status": r.get('consent_status', 'unknown'),
            }
            rows.append(contact)

        with engine.begin() as conn:
            for c in rows:
                res = conn.execute(text("""
                  INSERT INTO contacts (company_name, contact_name, title, phone, email, industry, company_size, annual_revenue, timezone, best_contact_time, consent_status)
                  VALUES (:company_name,:contact_name,:title,:phone,:email,:industry,:company_size,:annual_revenue,:timezone,:best_contact_time,:consent_status)
                  RETURNING id
                """), **c)
                contact_id = res.fetchone()[0]
                q.enqueue('worker.dial_contact', contact_id, job_timeout=600)
                total += 1
        logging.info(f"Ingested batch starting at {i}: {len(rows)} contacts queued")
    logging.info(f"Total queued contacts: {total}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python ingest.py contacts.csv")
        sys.exit(1)
    ingest_csv(sys.argv[1])

# DB table schema (Postgres) — run directly once:
# CREATE TABLE contacts (
#   id SERIAL PRIMARY KEY,
#   company_name TEXT,
#   contact_name TEXT,
#   title TEXT,
#   phone TEXT UNIQUE,
#   email TEXT,
#   industry TEXT,
#   company_size TEXT,
#   annual_revenue TEXT,
#   timezone TEXT,
#   best_contact_time TEXT,
#   consent_status TEXT,
#   created_at TIMESTAMP DEFAULT now()
# );
#
# CREATE TABLE dnc_list (
#   id SERIAL PRIMARY KEY,
#   phone TEXT UNIQUE,
#   reason TEXT,
#   added_at TIMESTAMP DEFAULT now()
# );
#
# CREATE TABLE call_logs (
#   id SERIAL PRIMARY KEY,
#   contact_id INT REFERENCES contacts(id),
#   call_sid TEXT,
#   status TEXT,
#   duration INT,
#   transcript TEXT,
#   created_at TIMESTAMP DEFAULT now()
# );