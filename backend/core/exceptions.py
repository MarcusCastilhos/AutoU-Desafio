from fastapi import HTTPException, status

def unsupported_file():
    raise HTTPException(
        status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        detail="Only .txt and .pdf files are supported"
    )


def empty_content():
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="File content is empty"
    )
