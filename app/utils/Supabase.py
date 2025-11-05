import os
import tempfile

from typing import Any
from datetime import datetime


def upload_images_to_bucket(
    supabase_client,
    images,
    book_id,
    bucket_name,
    upload_type="add",
    all_book_order=[],
    existing_book_image_urls=[],
) -> list[dict[str, Any]]:
    uploaded_urls = []

    for index, book_image in enumerate(images, start=1):
        # Create a path inside the bucket

        file_path = (
            create_file_path_for_edit(
                index, book_image, book_id, existing_book_image_urls, all_book_order
            )
            if upload_type == "edit"
            else f"{book_id}-{index}"
        )

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


def create_file_path_for_edit(
    index, book_image, book_id, existing_book_image_urls=[], all_book_order=[]
):
    if len(all_book_order) == 0:
        file_path = f"{book_id}-{len(existing_book_image_urls) + index}"
    else:
        file_path = f"{book_id}-{all_book_order.index(book_image.filename) + 1}"

    return file_path
