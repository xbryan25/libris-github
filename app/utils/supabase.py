import os
import tempfile

from typing import Any
from datetime import datetime

from uuid import uuid4


def upload_images_to_bucket_from_add_book_service(
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


def upload_images_to_bucket_from_edit_book_service(
    supabase_client,
    book_images,
    book_id,
    bucket_name,
    existing_book_image_urls,
    all_book_order,
) -> list[tuple[int, dict[str, Any]]]:
    uploaded_urls_with_order_num = []

    for book_image in book_images:
        # Create a path inside the bucket

        file_path = f"{book_id}/{uuid4()}"

        if not all_book_order:
            order_num = len(existing_book_image_urls) + 1
        else:
            order_num = all_book_order.index(book_image.filename) + 1

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
        uploaded_urls_with_order_num.append(
            (order_num, {"image_url": public_url, "uploaded_at": datetime.now()})
        )

    return uploaded_urls_with_order_num
