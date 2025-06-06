import io
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_file_upload(client: AsyncClient):
    test_file = io.BytesIO(b"test file content")
    test_filename = "test_file.png"

    files = {'file': (test_filename, test_file, 'text/plain')}

    response = await client.post(
        "/api/medias",
        headers={"api-key": "test"},
        files=files
    )

    assert response.status_code == 201
    assert response.json() == {
        "result": True,
        "media_id": 1
    }
