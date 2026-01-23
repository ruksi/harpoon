import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("ship")


async def app(scope, receive, send):
    """Uvicorn-compatible ASGI hello world application."""
    logger.debug(f"Received scope: {scope}")

    if scope["type"] == "lifespan":
        while True:
            message = await receive()
            logger.info(f"Lifespan message: {message}")
            if message["type"] == "lifespan.startup":
                logger.info("Application startup")
                await send({"type": "lifespan.startup.complete"})
            elif message["type"] == "lifespan.shutdown":
                logger.info("Application shutdown")
                await send({"type": "lifespan.shutdown.complete"})
                return

    if scope["type"] == "http":
        method = scope.get("method", "UNKNOWN")
        path = scope.get("path", "/")
        logger.info(f"HTTP request: {method} {path}")

        request_body = b""
        while True:
            message = await receive()
            logger.debug(f"Received message: {message}")
            request_body += message.get("body", b"")
            if not message.get("more_body", False):
                break

        if request_body:
            logger.debug(f"Request body: {request_body}")

        response_body = b"Hello, World!"
        logger.info(f"Sending response: 200 OK, body={response_body}")

        await send(
            {
                "type": "http.response.start",
                "status": 200,
                "headers": [[b"content-type", b"text/plain"]],
            }
        )
        await send(
            {
                "type": "http.response.body",
                "body": response_body,
            }
        )
        logger.debug("Response sent")
