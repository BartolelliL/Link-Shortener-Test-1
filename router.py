from sqlite3 import IntegrityError

import fastapi
from fastapi.responses import RedirectResponse

from database import db_create_link, db_fifty_latest_links, db_link_out, db_delete_link, db_add_click, \
    db_get_link_by_code
from link_generator import generate_random_slug as slug
from schemas import LinkCreate

router = fastapi.APIRouter()

@router.post("/api/links", status_code=201)
def post_create_link(link: LinkCreate, request: fastapi.Request):
    url = str(link.url)
    for _ in range(10):
        try:
            code = slug()
            row = db_create_link(url, code)
            return db_link_out(row, request)
        except IntegrityError:
            continue
    raise fastapi.HTTPException(
        status_code=500,
        detail="Could not generate a unique short URL after 10 attempts."
    )

@router.get("/api/links")
def get_fifty_latest_links(request: fastapi.Request):
    rows = db_fifty_latest_links()
    return [db_link_out(row, request) for row in rows]

@router.delete("/api/links/{code}", status_code=204)
def delete_link(code: str):
    delete_operation_successful = db_delete_link(code)
    if not delete_operation_successful:
        raise fastapi.HTTPException(
            status_code=404,
            detail=f"Link '{code}' not found."
        )

    return f"Link '{code}' deleted successfully."

@router.get("/{code}", status_code=307)
def redirect_to_url(code: str):
    click_operation_successful = db_add_click(code)
    if not click_operation_successful:
        raise fastapi.HTTPException(
            status_code=404,
            detail=f"Link '{code}' not found."
        )
    row = db_get_link_by_code(code)
    return RedirectResponse(url=row["url"])
