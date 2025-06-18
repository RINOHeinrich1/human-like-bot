FROM python:3.10-slim

# Mise à jour et installation des dépendances
RUN apt-get update && apt-get install -y \
    xvfb \
    x11-utils \
    x11vnc \
    x11-xserver-utils \
    scrot \
    wmctrl \
    libx11-6 \
    fluxbox \
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
    xclip \
    gnome-screenshot \
    unzip \
    && rm -rf /var/lib/apt/lists/*
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        fonts-liberation \
        fonts-dejavu \
        fonts-freefont-otf \
        fonts-noto-core \
        fonts-noto-cjk \
        fonts-noto-mono \
        fonts-noto-color-emoji && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

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
CMD sh -c "\
  Xvfb :99 -screen 0 1366x768x24 & \
  fluxbox & \
  x11vnc -noxdamage -xdamage -display  :99 -nopw -forever -shared & \
  python3 main.py"


