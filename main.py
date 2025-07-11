import websockets
import asyncio
from ultralytics import YOLO
from PIL import ImageGrab
import pytesseract
import cv2
import numpy as np

pytesseract.pytesseract.tesseract_cmd = (
    r"/usr/bin/tesseract"
)
model = YOLO("./train_beta/weights/best.pt")
print("Starting real-time prediction...")

# async def send_message(message):
#     async with websockets.connect("ws://localhost:2399") as websocket:
#         await websocket.send(message)

async def main():
    while True:
        # Capturar a tela em tempo real
        screen = ImageGrab.grab()
        screen_np = np.array(screen)

        # Converter a imagem para o formato do OpenCV (RGB -> BGR)
        frame = cv2.cvtColor(screen_np, cv2.COLOR_RGB2BGR)

        # Fazer a predição no frame atual
        results = model.predict(source=frame, stream=False, conf=0.15)

        # Para cada resultado, desenhar a caixa delimitadora e extrair a região de interesse
        for result in results:
            for box in result.boxes.xyxy:
                x1, y1, x2, y2 = map(int, box[:4])
                
                # Desenhar a caixa delimitadora na tela capturada
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                
                roi = frame[y1:y2, x1:x2]
                
                print(f"Coordenadas da caixa: ({x1}, {y1}), ({x2}, {y2})")
                # Mostrar a região de interesse
                cv2.imshow("ROI", roi)
                # Pressionar 'q' para sair
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    cv2.destroyAllWindows()
                    return
        
        # Exibir a tela capturada completa com as detecções
        # cv2.imshow("Tela Capturada", frame)

        await asyncio.sleep(0.5)  # Pequeno delay para não sobrecarregar o sistema


asyncio.run(main())
