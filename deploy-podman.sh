#!/bin/bash
# Deployment script for Podman

echo "🚀 PDF Converter & Compressor - Podman Deployment"
echo "=================================================="

# Check if Podman is installed
if ! command -v podman &> /dev/null; then
    echo "❌ Podman is not installed. Please install Podman first."
    exit 1
fi

echo "✅ Podman found: $(podman --version)"

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p uploads outputs

# Build the image
echo "🔨 Building container image..."
podman build -t pdf-converter:latest .

if [ $? -ne 0 ]; then
    echo "❌ Build failed!"
    exit 1
fi

echo "✅ Image built successfully!"

# Stop and remove existing container if it exists
echo "🧹 Cleaning up existing container..."
podman stop pdf-converter-app 2>/dev/null
podman rm pdf-converter-app 2>/dev/null

# Run the container
echo "🚀 Starting container..."
podman run -d \
    --name pdf-converter-app \
    -p 8080:5000 \
    -v $(pwd)/uploads:/app/uploads:Z \
    -v $(pwd)/outputs:/app/outputs:Z \
    -e SECRET_KEY=change-this-in-production \
    --restart unless-stopped \
    pdf-converter:latest

if [ $? -ne 0 ]; then
    echo "❌ Failed to start container!"
    exit 1
fi

echo ""
echo "✅ Container started successfully!"
echo ""
echo "📊 Container Status:"
podman ps | grep pdf-converter-app

echo ""
echo "🌐 Application is running at: http://localhost:8080"
echo ""
echo "📝 Useful commands:"
echo "  - View logs:    podman logs -f pdf-converter-app"
echo "  - Stop:         podman stop pdf-converter-app"
echo "  - Start:        podman start pdf-converter-app"
echo "  - Restart:      podman restart pdf-converter-app"
echo "  - Remove:       podman rm -f pdf-converter-app"
echo ""

# Made with Bob
