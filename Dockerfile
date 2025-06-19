FROM python:3.10.12-slim

WORKDIR /Bible-Gui

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "-m", "src.main" ]