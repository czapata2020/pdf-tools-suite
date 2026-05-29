# Deployment Guide - PDF Converter & Compressor

## Web Application Deployment with Podman

This guide will help you deploy the PDF Converter & Compressor as a containerized web application using Podman.

## Prerequisites

- Podman installed on your system
- Port 5000 available
- At least 2GB of free disk space

## Quick Start

### Option 1: Automated Deployment (Recommended)

Simply run the deployment script:

```bash
./deploy-podman.sh
```

This script will:
1. Check if Podman is installed
2. Create necessary directories
3. Build the container image
4. Stop any existing container
5. Start the new container
6. Display the application URL

### Option 2: Manual Deployment

#### Step 1: Build the Image

```bash
podman build -t pdf-converter:latest .
```

#### Step 2: Create Directories

```bash
mkdir -p uploads outputs
```

#### Step 3: Run the Container

```bash
podman run -d \
    --name pdf-converter-app \
    -p 5000:5000 \
    -v $(pwd)/uploads:/app/uploads:Z \
    -v $(pwd)/outputs:/app/outputs:Z \
    -e SECRET_KEY=your-secret-key-here \
    --restart unless-stopped \
    pdf-converter:latest
```

### Option 3: Using Podman Compose

If you have podman-compose installed:

```bash
podman-compose up -d
```

## Accessing the Application

Once deployed, open your browser and navigate to:

```
http://localhost:5000
```

You should see the modern web interface with two tabs:
- **Convert to Word**: Upload PDFs to convert to Word documents
- **Compress PDF**: Upload PDFs to compress with various quality levels

## Container Management

### View Logs

```bash
podman logs -f pdf-converter-app
```

### Stop the Container

```bash
podman stop pdf-converter-app
```

### Start the Container

```bash
podman start pdf-converter-app
```

### Restart the Container

```bash
podman restart pdf-converter-app
```

### Remove the Container

```bash
podman rm -f pdf-converter-app
```

### View Container Status

```bash
podman ps | grep pdf-converter
```

### Check Health

```bash
curl http://localhost:5000/health
```

## Configuration

### Environment Variables

You can customize the application using environment variables:

- `SECRET_KEY`: Flask secret key (change in production)
- `FLASK_APP`: Application entry point (default: app.py)

Example with custom environment:

```bash
podman run -d \
    --name pdf-converter-app \
    -p 5000:5000 \
    -v $(pwd)/uploads:/app/uploads:Z \
    -v $(pwd)/outputs:/app/outputs:Z \
    -e SECRET_KEY=my-super-secret-key \
    -e FLASK_APP=app.py \
    pdf-converter:latest
```

### Port Configuration

To use a different port (e.g., 8080):

```bash
podman run -d \
    --name pdf-converter-app \
    -p 8080:5000 \
    -v $(pwd)/uploads:/app/uploads:Z \
    -v $(pwd)/outputs:/app/outputs:Z \
    pdf-converter:latest
```

Then access at: `http://localhost:8080`

## Features

### PDF to Word Conversion
- Upload PDF files (up to 100MB)
- Automatic conversion to .docx format
- Preserves formatting and layout
- Download converted files

### PDF Compression
- **Low Quality**: 70-83% compression (maximum size reduction)
- **Medium Quality**: 40-60% compression (balanced)
- **High Quality**: 20-40% compression (minimal loss)
- **Maximum Quality**: 5-20% compression (preserve quality)
- Uses Ghostscript for superior compression
- Automatic fallback to PyPDF2 if Ghostscript unavailable

## Troubleshooting

### Container Won't Start

Check if port 5000 is already in use:

```bash
lsof -i :5000
```

Use a different port if needed.

### Permission Issues

If you encounter permission issues with volumes, try:

```bash
podman run -d \
    --name pdf-converter-app \
    -p 5000:5000 \
    -v $(pwd)/uploads:/app/uploads:Z \
    -v $(pwd)/outputs:/app/outputs:Z \
    --userns=keep-id \
    pdf-converter:latest
```

### Ghostscript Not Working

The container includes Ghostscript by default. To verify:

```bash
podman exec pdf-converter-app gs --version
```

### View Application Logs

```bash
podman logs pdf-converter-app
```

### Container Keeps Restarting

Check logs for errors:

```bash
podman logs pdf-converter-app --tail 50
```

## Production Deployment

### Security Recommendations

1. **Change the SECRET_KEY**:
   ```bash
   -e SECRET_KEY=$(openssl rand -hex 32)
   ```

2. **Use HTTPS**: Deploy behind a reverse proxy (nginx, traefik)

3. **Limit File Size**: Already set to 100MB, adjust if needed

4. **Regular Updates**: Rebuild image periodically
   ```bash
   podman pull python:3.11-slim
   podman build -t pdf-converter:latest .
   ```

### Reverse Proxy Example (nginx)

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Increase timeouts for large files
        proxy_read_timeout 300;
        proxy_connect_timeout 300;
        proxy_send_timeout 300;
        
        # Increase max body size
        client_max_body_size 100M;
    }
}
```

### Systemd Service (Optional)

Create `/etc/systemd/system/pdf-converter.service`:

```ini
[Unit]
Description=PDF Converter & Compressor
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/PDF_to_Word_Converter
ExecStart=/usr/bin/podman start -a pdf-converter-app
ExecStop=/usr/bin/podman stop pdf-converter-app
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl enable pdf-converter
sudo systemctl start pdf-converter
```

## Monitoring

### Resource Usage

```bash
podman stats pdf-converter-app
```

### Disk Usage

```bash
du -sh uploads outputs
```

### Clean Old Files

The application automatically cleans files older than 1 hour. To manually clean:

```bash
find uploads -type f -mtime +1 -delete
find outputs -type f -mtime +1 -delete
```

## Backup

### Backup Container Image

```bash
podman save pdf-converter:latest | gzip > pdf-converter-backup.tar.gz
```

### Restore Container Image

```bash
gunzip -c pdf-converter-backup.tar.gz | podman load
```

## Updating

To update the application:

1. Pull latest code
2. Rebuild image:
   ```bash
   podman build -t pdf-converter:latest .
   ```
3. Restart container:
   ```bash
   podman stop pdf-converter-app
   podman rm pdf-converter-app
   ./deploy-podman.sh
   ```

## Support

For issues or questions:
- Check logs: `podman logs pdf-converter-app`
- Verify health: `curl http://localhost:5000/health`
- Review this guide for common solutions

---

**Happy Deploying! 🚀**