import sqlite3

import fastapi
from schemas import LinkCreate
from link_generator import generate_random_slug as slug
from database import link_out, create_link
router = fastapi.APIRouter()

@router.post("/api/links", status_code=201)
def post_create_link(link: LinkCreate, request: fastapi.Request):
    try:
        code = slug()
        url = str(link.url)
        row = create_link(url, code)
        return link_out(row, request)
    except sqlite3.IntegrityError:
        pass
        # richiamare la funzione per generare un nuovo short_url
        # può essere chiamata massimo 10 volte