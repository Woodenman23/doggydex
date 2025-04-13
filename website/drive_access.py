import io
import base64
from PIL import Image

from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload, MediaIoBaseDownload
from google.oauth2 import service_account

from website import PROJECT_ROOT

MODEL_PATH = "/tmp/dognet-convnext_large.pth"
MODEL_ID = "1oW40saWGECdPi4mZ0hewJ0T9_nuyModx"

SERVICE_ACCOUNT_FILE = PROJECT_ROOT / "secrets/doggydex-456203-e6ca832dbc3c.json"

IMAGE_FOLDER_ID = "1hUgN1BnLdaLzmelLM3ZJMQ1Sklt0FYrZ"

credentials = service_account.Credentials.from_service_account_file(
    str(SERVICE_ACCOUNT_FILE),
    scopes=["https://www.googleapis.com/auth/drive"],
)

drive_service = build("drive", "v3", credentials=credentials)


# upload dog image
def upload_to_drive(file_stream, filename, mimetype):
    id = file_exists(filename)
    if id:
        return id

    file_metadata = {
        "name": filename,
        "parents": [IMAGE_FOLDER_ID],
    }
    media = MediaIoBaseUpload(file_stream, mimetype=mimetype, resumable=True)
    uploaded_file = (
        drive_service.files()
        .create(body=file_metadata, media_body=media, fields="id")
        .execute()
    )

    return uploaded_file.get("id")


# get dog image
def download_from_drive(file_id):
    request = drive_service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)

    done = False
    while not done:
        status, done = downloader.next_chunk()

    fh.seek(0)
    pil_image = Image.open(fh)
    jpeg_io = io.BytesIO()
    pil_image.convert("RGB").save(jpeg_io, format="JPEG")
    jpeg_io.seek(0)
    jpeg_b64 = base64.b64encode(jpeg_io.read()).decode("utf-8")

    return pil_image, jpeg_b64


def file_exists(filename):
    query = (
        f"name = '{filename}' and '{IMAGE_FOLDER_ID}' in parents and trashed = false"
    )
    results = drive_service.files().list(q=query, fields="files(id)").execute()
    files = results.get("files", [])
    return files[0].get("id") if files else None
