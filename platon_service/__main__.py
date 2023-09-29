import uvicorn

from platon_service.server import Server

if __name__ == "__main__":
    app = Server().get_app()
    uvicorn.run(app, host="0.0.0.0", port=8000)
