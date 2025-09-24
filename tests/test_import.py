try:
    from api.src.main import app
    print("Success")
except Exception as e:
    print(f"Error: {e}")