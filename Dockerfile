FROM python:3.10-slim

# Mise à jour et installation des dépendances
RUN apt-get update && apt-get install -y \
    xvfb \
    x11-utils \
    x11-xserver-utils \
    scrot \
    wmctrl \
    libx11-6 \
    libx11-dev \
    libxcomposite-dev \
    libxcursor-dev \
    libxdamage-dev \
    libxext-dev \
    libxi-dev \
    libxtst-dev \
    libnss3 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libasound2 \
    python3-tk \
    python3-dev \
    fonts-liberation \
    wget \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Installer Google Chrome
RUN curl -sSL https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o chrome.deb && \
    apt-get update && apt-get install -y ./chrome.deb && \
    rm chrome.deb

# Installer les packages Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code dans le conteneur
COPY . /app
WORKDIR /app

# Exposer l'affichage virtuel
ENV DISPLAY=:99

# Commande d’entrée
CMD ["sh", "-c", "Xvfb :99 -screen 0 1920x1080x24 & python3 main.py"]
