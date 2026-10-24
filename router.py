from sqlite3 import IntegrityError

import fastapi
from schemas import LinkCreate
from link_generator import generate_random_slug as slug
from database import link_out, create_link, db_fifty_latest_links

router = fastapi.APIRouter()

@router.post("/api/links", status_code=201)
def post_create_link(link: LinkCreate, request: fastapi.Request):
    url = str(link.url)
    for _ in range(10):
        try:
            code = slug()
            row = create_link(url, code)
            return link_out(row, request)
        except IntegrityError:
            continue
    raise fastapi.HTTPException(
        status_code=500,
        detail="Could not generate a unique short URL after 10 attempts."
    )

@router.get("/api/links")
def get_fifty_latest_links(request: fastapi.Request):
    rows = db_fifty_latest_links()
    return [link_out(row, request) for row in rows]