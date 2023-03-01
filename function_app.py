import azure.functions as func
import logging

from api import app as fast_app

func_app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# Learn more at aka.ms/pythonprogrammingmodel

@func_app.function_name(name="FastAPITrigger")
@func_app.route(route="{*route}", methods=["get","post"])
async def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    """Each request is redirected to the ASGI handler."""
    return await func.AsgiMiddleware(fast_app).handle_async(req, context)