#!/usr/bin/env python3

print("Testing requests import...")

try:
    import requests
    print("Requests imported successfully!")
    print("Requests version:", requests.__version__)
except Exception as e:
    print("Error importing requests:", e)
    import traceback
    traceback.print_exc()

print("Test completed.")