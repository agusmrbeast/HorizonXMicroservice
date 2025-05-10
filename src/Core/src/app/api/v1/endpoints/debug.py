from datetime import datetime

from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/")
async def debug_info(request: Request):
    """Return debug information about the request."""
    return {
        "client": request.client.host,
        "method": request.method,
        "url": str(request.url),
        "headers": dict(request.headers),
        "query_params": dict(request.query_params),
        "path_params": request.path_params,
        "server_port": request.url.port,
        "timestamp": str(datetime.now()),
    }
