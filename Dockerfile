# 1. Utilisation de Python 3.10
FROM python:3.10-slim

# 2. Mise à jour des paquets système pour OpenCV
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

# 3. Dossier de travail
WORKDIR /app

# 4. Installation des dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copie du code
COPY . .

# 6. Lancement
CMD ["python", "app.py"]