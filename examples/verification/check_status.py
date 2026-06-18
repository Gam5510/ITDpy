"""Example: check verification status."""
from itdpy import ITDClient

with ITDClient(refresh_token="YOUR_REFRESH_TOKEN") as client:
    status = client.verification.get_status()
    print(f"Verified: {status.is_verified}")
    if status.request:
        print(f"Pending request: {status.request.status}")
