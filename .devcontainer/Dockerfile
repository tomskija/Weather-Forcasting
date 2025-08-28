# Use Python 3.11 slim base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    wget \
    vim \
    sudo \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create workspace directory
WORKDIR /workspace

# Create a non-root user for development
RUN groupadd --gid 1000 developer \
    && useradd --uid 1000 --gid developer --shell /bin/bash --create-home developer \
    && echo "developer:developer" | chpasswd \
    && adduser developer sudo \
    && echo "developer ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Give developer ownership of workspace
RUN chown -R developer:developer /workspace

# Switch to developer user
USER developer

# Set the default shell
SHELL ["/bin/bash", "-c"]

# Install common Python development tools
RUN pip install --user --upgrade pip setuptools wheel

# Set Python path
ENV PYTHONPATH=/workspace
ENV PATH="/home/developer/.local/bin:${PATH}"

# Set the working directory
WORKDIR /workspace