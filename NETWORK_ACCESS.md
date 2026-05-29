# 🌐 Local Network Access Guide

## Your PDF Tools Suite is Now Accessible on Your Local Network!

### 📍 Access URLs

#### On This Computer (Host Machine)
- **URL**: http://localhost:8080
- **Alternative**: http://127.0.0.1:8080

#### From Other Devices on Your Local Network
- **URL**: http://192.168.68.52:8080

### 📱 Devices That Can Access

Any device connected to your local network can access the application:
- ✅ Other computers (Windows, Mac, Linux)
- ✅ Smartphones (iPhone, Android)
- ✅ Tablets (iPad, Android tablets)
- ✅ Smart TVs with web browsers

### 🔧 How to Use from Other Devices

1. **Make sure the device is on the same WiFi/network** as your Mac
2. **Open a web browser** on that device
3. **Type the URL**: `http://192.168.68.52:8080`
4. **Use the application** just like on your computer!

### 🔒 Security Notes

- ⚠️ This is accessible to **anyone on your local network**
- ⚠️ Not accessible from the internet (safe by default)
- ⚠️ No authentication required (anyone on network can use it)
- ✅ Files are processed locally on your Mac
- ✅ No data leaves your local network

### 🛠️ Container Management

#### Check if Container is Running
```bash
podman ps | grep pdf-tools
```

#### Stop the Container
```bash
podman stop pdf-tools
```

#### Start the Container
```bash
podman start pdf-tools
```

#### Restart the Container
```bash
podman restart pdf-tools
```

#### View Container Logs
```bash
podman logs pdf-tools --tail 50
```

#### Remove Container (if needed)
```bash
podman stop pdf-tools
podman rm pdf-tools
```

#### Rebuild and Run (after code changes)
```bash
cd PDF_to_Word_Converter
podman build -t pdf-tools-suite:latest .
podman stop pdf-tools && podman rm pdf-tools
podman run -d --name pdf-tools -p 8080:5000 pdf-tools-suite:latest
```

### 🔄 Auto-Start on Boot (Optional)

To make the container start automatically when your Mac boots:

```bash
# Create a systemd user service (if using systemd)
podman generate systemd --new --name pdf-tools > ~/.config/systemd/user/pdf-tools.service
systemctl --user enable pdf-tools.service
```

Or use macOS launchd:
```bash
# Create a launch agent plist file
# This requires additional configuration
```

### 🌍 Making it Accessible from Internet (Advanced)

If you want to access this from outside your local network:

1. **Port Forwarding**: Configure your router to forward port 8080 to 192.168.68.52:8080
2. **Dynamic DNS**: Use a service like DuckDNS or No-IP to get a domain name
3. **Security**: Add authentication (not currently implemented)
4. **HTTPS**: Use a reverse proxy like Nginx with Let's Encrypt SSL

⚠️ **Warning**: Exposing to internet without authentication is not recommended!

### 📊 Current Configuration

- **Host IP**: 192.168.68.52
- **Container Port**: 5000 (internal)
- **Host Port**: 8080 (external)
- **Binding**: 0.0.0.0 (all interfaces)
- **Workers**: 4 Gunicorn workers
- **Timeout**: 300 seconds

### 🎯 Features Available

1. **📄 PDF to Word Conversion** - Convert PDFs to editable DOCX files
2. **🗜️ PDF Compression** - Reduce PDF file size (3 quality levels)
3. **🧹 Metadata Cleaning** - Remove sensitive metadata from PDFs
4. **🔗 PDF Merging** - Combine multiple PDFs into one document

### 🆘 Troubleshooting

#### Can't Access from Other Devices?

1. **Check Firewall**: Make sure macOS firewall allows connections on port 8080
   ```bash
   # Check firewall status
   sudo /usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate
   ```

2. **Verify Container is Running**:
   ```bash
   podman ps | grep pdf-tools
   ```

3. **Test from Host Machine First**:
   ```bash
   curl http://localhost:8080
   ```

4. **Check Network Connectivity**:
   ```bash
   # From another device, ping your Mac
   ping 192.168.68.52
   ```

#### Container Not Starting?

```bash
# Check logs for errors
podman logs pdf-tools

# Check if port is already in use
lsof -i :8080
```

### 📝 Notes

- The IP address (192.168.68.52) may change if your Mac gets a new DHCP lease
- Consider setting a static IP on your Mac for consistent access
- Container must be running for the application to be accessible
- Files uploaded are temporarily stored and automatically cleaned up

---

**Made with ❤️ by Bob**