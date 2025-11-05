import os
import tempfile

from typing import Any
from datetime import datetime

from uuid import uuid4


def upload_images_to_bucket(
    supabase_client,
    book_images,
    book_id,
    bucket_name,
) -> list[dict[str, Any]]:
    uploaded_urls = []

    for book_image in book_images:
        # Create a path inside the bucket

        file_path = f"{book_id}/{uuid4()}"

        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(book_image.read())
            tmp_path = tmp.name

        # Upload directly from memory (no need to save locally)
        supabase_client.storage.from_(bucket_name).upload(
            file=tmp_path,
            path=file_path,
            file_options={
                "cache-control": "3600",
                "upsert": "true",
                "content-type": book_image.content_type,
            },
        )

        os.remove(tmp_path)

        # Get public URL
        public_url = supabase_client.storage.from_(bucket_name).get_public_url(
            file_path
        )
        uploaded_urls.append({"image_url": public_url, "uploaded_at": datetime.now()})

    return uploaded_urls
