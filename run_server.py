import asyncio

import uvicorn


async def main() -> None:
    config = uvicorn.Config(
        "src.api.main:app",
        host="127.0.0.1",
        port=8000,
        access_log=False,
    )

    server = uvicorn.Server(config)

    await server.serve()


if __name__ == "__main__":
    asyncio.run(
        main(),
        loop_factory=asyncio.SelectorEventLoop,
    )