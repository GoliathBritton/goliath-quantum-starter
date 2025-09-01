def automate_follow_up(deal_id: str) -> dict:
    return {"deal_id": deal_id, "status": "scheduled", "channel": "email+sms+voice"}
