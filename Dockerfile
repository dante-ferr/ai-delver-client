FROM tensorflow/tensorflow:2.15.0-gpu

# Set timezone
RUN ln -fs /usr/share/zoneinfo/America/New_York /etc/localtime

# System configuration
ENV DISPLAY=:99
ENV QT_X11_NO_MITSHM=1
ENV XAUTHORITY=/tmp/.docker.xauth
ENV TEMP_DIR=/tmp/app_temp
ENV PATH="/home/appuser/.local/bin:${PATH}"

# Create user and workspace
RUN adduser -u 5678 --disabled-password --gecos "" appuser
WORKDIR /app
RUN mkdir -p /app && chown -R appuser:appuser /app

# System dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-tk \
    tk-dev \
    x11-utils \
    x11-apps \
    xfonts-100dpi \
    xfonts-75dpi \
    xfonts-base \
    xfonts-scalable \
    libx11-6 \
    libxext6 \
    libxext-dev \
    libxrender-dev \
    libxtst6 \
    libxinerama-dev \
    libxi-dev \
    libxrandr-dev \
    libxcursor-dev \
    libxtst-dev \
    libgl1-mesa-glx \
    libxft-dev \
    libfontconfig1-dev \
    xvfb \
    libgl1 \
    libcairo2-dev \
    libgdk-pixbuf2.0-dev \
    libffi-dev \
    dos2unix \
    libxss1 \
    libgconf-2-4 \
    libnss3 \
    libasound2 \
    libgbm1 \
    libgtk-3-0 \
    libdrm2 \
    mesa-utils \
    && python3 -m pip install --upgrade pip \
    && rm -rf /var/lib/apt/lists/*

# X11 configuration
RUN mkdir -p /tmp/.X11-unix && chmod 1777 /tmp/.X11-unix
RUN mkdir -p /tmp/app_temp && chmod 777 /tmp/app_temp

# Python environment setup
COPY Pipfile Pipfile.lock ./
RUN chown -R appuser:appuser /app

# Install Python dependencies system-wide
USER root
RUN pip install --no-cache-dir --ignore-installed blinker==1.4 && \
    pip install --no-cache-dir pipenv && \
    pipenv install --system --dev --deploy
USER appuser

# Local packages
COPY --chown=appuser:appuser . .
RUN pip install --user --no-cache-dir ./pytiling && \
    pip install --user --no-cache-dir ./pyglet_dragonbones

# Entrypoint setup
COPY --chown=appuser:appuser entrypoint.sh .
RUN dos2unix entrypoint.sh && \
    chmod 755 entrypoint.sh && \
    chmod +x entrypoint.sh

# Explicitly set the shell format
SHELL ["/bin/bash", "-c"]

CMD ["./entrypoint.sh"]