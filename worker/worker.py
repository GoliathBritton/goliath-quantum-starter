import os, time, json, logging
from sqlalchemy import create_engine, text
from redis import Redis
from rq import Worker, Queue, Connection
from dotenv import load_dotenv
import openai
from tenacity import retry, wait_exponential, stop_after_attempt
from twilio.rest import Client as TwilioClient
import requests

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
REDIS_URL = os.getenv("REDIS_URL")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
DYNEX_KEY = os.getenv("DYNEX_API_KEY")
TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_FROM = os.getenv("TWILIO_FROM")
MAX_OUTBOUND_PER_MIN = int(os.getenv("MAX_OUTBOUND_PER_MIN", "30"))

engine = create_engine(DATABASE_URL)
redis_conn = Redis.from_url(REDIS_URL)
q = Queue('dialer', connection=redis_conn)
openai.api_key = OPENAI_KEY
twilio = TwilioClient(TWILIO_SID, TWILIO_TOKEN)

logging.basicConfig(level=logging.INFO)
last_min_window = []

def consent_ok(contact):
    """Check consent and DNC flags in DB"""
    with engine.connect() as conn:
        r = conn.execute(text("SELECT consent_status FROM contacts WHERE id=:id"), {"id": contact})
        row = r.fetchone()
        return (row and row[0] in ("opt-in","explicit"))


def rate_limit_ok():
    global last_min_window
    now = time.time()
    # Remove older than 60s
    last_min_window = [t for t in last_min_window if now - t < 60]
    if len(last_min_window) >= MAX_OUTBOUND_PER_MIN:
        return False
    last_min_window.append(now)
    return True

@retry(wait=wait_exponential(min=1, max=10), stop=stop_after_attempt(4))
def call_provider_place_call(to_number, audio_url, contact_id):
    """
    Place call using Twilio or other SIP gateway. Here we use Twilio's REST to create a call that plays an audio file.
    For more advanced IVR, use TwiML with webhook endpoints.
    """
    call = twilio.calls.create(
        to=to_number,
        from_=TWILIO_FROM,
        url=audio_url, # This could be a TwiML URL that plays the audio
        timeout=60
    )
    return call.sid

def generate_call_script(contact_info, purpose="sales_outreach"):
    # Use OpenAI to generate a personalized short script
    prompt = f"""
    You are a high-performing sales agent. Produce a short phone script (60-90 seconds, conversational) to reach {contact_info['contact_name']} at {contact_info['company_name']}.
    Company: {contact_info['company_name']}
    Role: {contact_info.get('title')}
    Pain points: {contact_info.get('pain_points','')}
    Keep the script: Intro, value prop, qualifying question, CTA to schedule a demo.
    Include fallback sentences if they ask to speak with procurement or legal.
    """
    resp = openai.ChatCompletion.create(
      model="gpt-4o-mini",
      messages=[{"role":"system","content":"You are an expert B2B SDR."},{"role":"user","content":prompt}],
      max_tokens=350,
      temperature=0.2
    )
    return resp.choices[0].message.content.strip()

def dynex_priority_score(contact_info):
    # Placeholder: call Dynex QUBO service to prioritize leads (mock returning float)
    # In production, build QUBO formulation and submit via DynexSDK.
    try:
        payload = {"features": contact_info}
        # r = requests.post("https://api.dynex.example/qubo/score", headers={"Authorization": f"Bearer {DYNEX_KEY}"}, json=payload, timeout=10)
        # return r.json().get("score", 0.5)
        return 0.5 + (hash(contact_info.get('phone') or "") % 100) / 200.0
    except Exception as e:
        logging.warning("Dynex priority error: %s", e)
        return 0.5

def synthesize_audio_nvidia(text, out_path="/tmp/out.mp3"):
    """Placeholder for NVIDIA TTS/Audio pipeline. Replace with your TTS invocation (e.g., NeMo, Triton, or cloud TTS)."""
    # For demo use OpenAI TTS or ElevenLabs; for production use NVIDIA runtime for avatars.
    # Here: return a hosted TwiML URL or S3 URL for audio content
    s3_url = f"https://my-cdn.example.com/audio/{hash(text)}.mp3"
    return s3_url

def record_call_log(contact_id, call_sid, status, duration=None, transcript=None):
    with engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO call_logs (contact_id, call_sid, status, duration, transcript)
            VALUES (:contact_id, :call_sid, :status, :duration, :transcript)
        """), {"contact_id": contact_id, "call_sid": call_sid, "status": status, "duration": duration, "transcript": transcript})

def fetch_contact(contact_id):
    with engine.connect() as conn:
        r = conn.execute(text("SELECT * FROM contacts WHERE id=:id"), {"id": contact_id})
        row = r.fetchone()
        if not row:
            return None
        cols = r.keys()
        return dict(zip(cols, row))

def dial_contact(contact_id):
    contact = fetch_contact(contact_id)
    if not contact:
        logging.info("Contact missing / deleted: %s", contact_id)
        return

    if not consent_ok(contact_id):
        logging.info("Contact %s has no consent", contact_id)
        return

    if not rate_limit_ok():
        logging.info("Rate limit reached: sleeping 20s")
        time.sleep(20)
        q.enqueue('worker.dial_contact', contact_id, job_timeout=600)
        return

    # Priority scoring
    priority = dynex_priority_score(contact)
    contact['priority'] = float(priority)

    # Generate script
    try:
        script = generate_call_script(contact)
    except Exception as e:
        logging.exception("script generation failed: %s", e)
        script = "Hi, this is from Flyfox AI. Are you available for a quick conversation?"

    # Synthesize audio via NVIDIA or a TTS fallback
    audio_url = synthesize_audio_nvidia(script)

    try:
        call_sid = call_provider_place_call(contact['phone'], audio_url, contact_id)
        logging.info("Placed call %s -> %s sid=%s", contact_id, contact['phone'], call_sid)
        record_call_log(contact_id, call_sid, "initiated", None, None)
    except Exception as e:
        logging.exception("Call placement failed: %s", e)
        record_call_log(contact_id, None, "failed", None, None)

if __name__ == '__main__':
    with Connection(redis_conn):
        worker = Worker([q])
        worker.work()