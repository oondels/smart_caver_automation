FROM pytorch/pytorch:2.5.1-cuda12.4-cudnn9-runtime

WORKDIR /app
COPY requirements-minimal.txt ./
RUN pip install --no-cache-dir -r requirements-minimal.txt
COPY . .
CMD ["python", "./dataset/train.py"]