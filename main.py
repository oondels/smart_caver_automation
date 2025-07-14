import websockets
import asyncio
from ultralytics import YOLO
from PIL import ImageGrab
import pytesseract
import cv2
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r"/usr/bin/tesseract"
model = YOLO("./train_beta3/weights/best.pt")
print("Starting real-time prediction...")

async def main():
    while True:
        # Capturar a tela em tempo real
        screen = ImageGrab.grab()
        screen_np = np.array(screen)

        # Converter a imagem para o formato do OpenCV (RGB -> BGR)
        frame = cv2.cvtColor(screen_np, cv2.COLOR_RGB2BGR)

        # Fazer a predição no frame atual
        results = model.predict(source=frame, stream=False, conf=0.15)

        for result in results:
            boxes = result.boxes
            if boxes is not None:
                for i, box in enumerate(boxes.xyxy):
                    x1, y1, x2, y2 = map(int, box[:4])

                    # Obter o nome da classe detectada
                    class_id = int(boxes.cls[i])
                    class_name = model.names[class_id]
                    confidence = float(boxes.conf[i])

                    # Desenhar a caixa delimitadora na tela capturada
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                    # Adicionar o texto com o nome da classe e confiança
                    label = f"{class_name}: {confidence:.2f}"
                    cv2.putText(
                        frame,
                        label,
                        (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (0, 255, 0),
                        2,
                    )

                    print(
                        f"Detectado: {class_name} - Confiança: {confidence:.2f} - Coordenadas: ({x1}, {y1}), ({x2}, {y2})"
                    )

        # Exibir apenas a tela capturada completa com as detecções
        # cv2.imshow("Smart Caver Detection", frame)

        # Pressionar 'q' para sair
        if cv2.waitKey(1) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            return

        await asyncio.sleep(0.5)  # Pequeno delay para não sobrecarregar o sistema

asyncio.run(main())