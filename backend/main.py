from fastapi import FastAPI, WebSocket
import cv2
import base64
import numpy as np
from ai_engine import analyze_frame

app = FastAPI()
teacher_clients = []

@app.websocket("/ws/student")
async def student_ws(ws: WebSocket):
    await ws.accept()

    while True:
        try:
            data = await ws.receive_text()

            if not data:
                continue  

           
            img_bytes = base64.b64decode(data, validate=True)

            if len(img_bytes) == 0:
                continue

            img_np = np.frombuffer(img_bytes, dtype=np.uint8)

            frame = cv2.imdecode(img_np, cv2.IMREAD_COLOR)

            if frame is None:
                continue  

            result = analyze_frame(frame)

            for t in teacher_clients:
                await t.send_json(result)

        except Exception as e:
            print("Student WS error:", e)
            break

@app.websocket("/ws/teacher")
async def teacher_ws(ws: WebSocket):
    await ws.accept()
    teacher_clients.append(ws)
    try:
        while True:
            await ws.receive_text()
    except:
        teacher_clients.remove(ws)
