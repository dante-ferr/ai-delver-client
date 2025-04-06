FROM tensorflow/tensorflow:2.15.0-gpu

# Set timezone
RUN ln -fs /usr/share/zoneinfo/America/New_York /etc/localtime

# System configuration
ENV DISPLAY=:99
ENV QT_X11_NO_MITSHM=1
ENV XAUTHORITY=/tmp/.docker.xauth
ENV TEMP_DIR=/tmp/app_temp
ENV PATH="/home/appuser/.local/bin:${PATH}"
ENV XLIB_SKIP_ARGB_VISUALS=1
ENV FREETYPE_PROPERTIES="truetype:interpreter-version=35"
ENV FONTCONFIG_PATH=/etc/fonts

# Create user and workspace
RUN adduser -u 5678 --disabled-password --gecos "" appuser
# RUN mkdir -p /app && chown -R appuser:appuser /src

# System dependencies
RUN apt-get update && apt-get install -y \
    # Core Python and Tools
    python3 \
    python3-pip \
    python3-tk \
    tk-dev \
    dos2unix \
    \
    # X11 Utilities and Fonts
    x11-utils \
    x11-apps \
    xfonts-100dpi \
    xfonts-75dpi \
    xfonts-base \
    xfonts-scalable \
    xvfb \
    # fonts-dejavu \
    # fonts-liberation \
    # fonts-freefont-ttf \
    # fontconfig \
    # libfreetype6 \
    # libxft2 \
    \
    # X11 Libraries and Extensions
    libx11-6 \
    libxext6 \
    libxext-dev \
    libxtst6 \
    libxtst-dev \
    libxinerama-dev \
    libxi-dev \
    libxrandr-dev \
    libxcursor-dev \
    libgl1-mesa-dev \
    \
    # Rendering and Graphics
    libglx-mesa0 \
    libgl1-mesa-glx \
    libgl1 \
    libglu1-mesa \
    libxrender-dev \
    libxft-dev \
    libfontconfig1-dev \
    libcairo2-dev \
    libgdk-pixbuf2.0-dev \
    mesa-utils \
    libdrm2 \
    \
    # Font and anti-aliasing specific
    libfreetype6-dev \
    libpng-dev \
    \
    # GTK and UI
    libgtk-3-0 \
    libasound2 \
    libgbm1 \
    \
    # Misc UI Dependencies (Electron/Chromium related)
    libxss1 \
    libgconf-2-4 \
    libnss3 \
    \
    # FFI and Compatibility
    libffi-dev \
    \
    && python3 -m pip install --upgrade pip \
    && rm -rf /var/lib/apt/lists/*

# X11 configuration
RUN mkdir -p /tmp/.X11-unix && chmod 1777 /tmp/.X11-unix
RUN mkdir -p /tmp/app_temp && chmod 777 /tmp/app_temp
# RUN Xvfb :99 -screen 0 1280x1024x24 -ac +extension GLX +render -noreset &> /tmp/xvfb.log &

# Python environment setup
COPY Pipfile Pipfile.lock ./
# RUN chown -R appuser:appuser /app

# Install Python dependencies system-wide
USER root
RUN pip install --no-cache-dir --ignore-installed blinker==1.4 && \
pip install --no-cache-dir pipenv && \
pipenv install --system --dev --deploy

# Local packages
WORKDIR /app
COPY --chown=appuser:appuser . .

# RUN pip install --dev --deploy && \
#     pipenv install -e ./pytiling && \
#     pipenv install -e ./pyglet_dragonbones

RUN pip install --no-cache-dir ./pytiling && \
    pip install --no-cache-dir ./pyglet_dragonbones