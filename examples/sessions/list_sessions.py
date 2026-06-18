"""Example: list active sessions."""
from itdpy import ITDClient

with ITDClient(refresh_token="YOUR_REFRESH_TOKEN") as client:
    sessions = client.sessions.list()
    print(f"Active sessions: {len(sessions)}")
    for s in sessions:
        current = " (current)" if s.is_current else ""
        print(f"  [{s.id[:8]}...]{current} — {s.location or 'Unknown'} — {s.device_type or '?'}")
