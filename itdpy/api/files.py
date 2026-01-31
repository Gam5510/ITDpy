from ..models import Attachment

def upload_file(client, file_path: str):
    with open(file_path, "rb") as f:
        r = client.post(
            "/api/files/upload",
            files={"file": f}
        )

    r.raise_for_status()
    return Attachment(r.json())
