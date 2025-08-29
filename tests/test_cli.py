import subprocess
import sys
import os

def test_cli_status():
    venv_python = os.path.join(os.path.dirname(sys.executable), 'python.exe')
    result = subprocess.run([venv_python, "cli.py", "status"], capture_output=True, text=True)
    
    # Test should pass whether server is online or offline
    # If offline, it should show connection error
    # If online, it should show status
    assert result.returncode == 0  # CLI should not crash
    assert "Checking system status" in result.stdout  # Should show status check message
    
    # Should either show connection error or platform status
    assert any([
        "Cannot connect to" in result.stdout,  # Offline case
        "Platform is up and running" in result.stdout  # Online case
    ])
