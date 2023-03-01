# TODO: Add setup or configuration specifications for the application here

from fastapi import FastAPI, Request, Security
from fastapi.responses import RedirectResponse, JSONResponse

from .security import get_api_key

app = FastAPI(
    title="FastAPI Demo", version="1.0", description="FastAPI with azurte function key security"
)

@app.get("/", include_in_schema=False)
@app.get("/{*route}", include_in_schema=False)
def docs_redirect(request: Request):
    return RedirectResponse(f"/docs")

@app.get("/hello")
def hello(
    name: str
) -> JSONResponse:
    return JSONResponse(
        status_code=200,
        content = {
            "message": f"Hello {name}"
        }
    )

@app.get("/hello_secure")
def hello_secure(
    name: str,
    api_key: str = Security(get_api_key)
) -> JSONResponse:
    return JSONResponse(
        status_code=200,
        content = {
            "message": f"Hello {name}"
        }
    )