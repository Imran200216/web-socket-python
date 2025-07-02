from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

clients = []


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print(f"✅ Client connected: {websocket.client.host}:{websocket.client.port}")
    clients.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"📩 Received: {data}")
            for client in clients:
                await client.send_text(data)
                print(f"📤 Sent to: {client.client.host}:{client.client.port}")
    except Exception as e:
        print(
            f"❌ Client disconnected: {websocket.client.host}:{websocket.client.port} ({e})"
        )
        clients.remove(websocket)
