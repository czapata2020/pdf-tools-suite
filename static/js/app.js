// Tab switching
function switchTab(tabName, event) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    document.querySelectorAll('.tab-button').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Show selected tab
    document.getElementById(`${tabName}-tab`).classList.add('active');
    if (event && event.target) {
        event.target.closest('.tab-button').classList.add('active');
    }
    
    // Hide error if visible
    hideError();
}

// Convert Tab Functions
const convertFileInput = document.getElementById('convert-file-input');
const convertUploadArea = document.getElementById('convert-upload-area');

convertUploadArea.addEventListener('click', (e) => {
    // Ignore clicks from the button to prevent double-trigger
    if (e.target.closest('button')) return;
    
    // Ignore clicks on the file input itself (from programmatic click())
    if (e.target === convertFileInput) {
        console.log('[CONVERT] File input clicked (programmatic), skipping');
        return;
    }
    
    console.log('[CONVERT] Upload area clicked', {
        target: e.target,
        currentTarget: e.currentTarget,
        timestamp: new Date().toISOString()
    });
    e.preventDefault();
    e.stopPropagation();
    convertFileInput.click();
});

convertUploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    e.stopPropagation();
    convertUploadArea.classList.add('dragover');
});

convertUploadArea.addEventListener('dragleave', (e) => {
    e.preventDefault();
    e.stopPropagation();
    convertUploadArea.classList.remove('dragover');
});

convertUploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    e.stopPropagation();
    convertUploadArea.classList.remove('dragover');
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleConvertFile(files[0]);
    }
});

convertFileInput.addEventListener('change', (e) => {
    console.log('[CONVERT] File input change event', {
        filesLength: e.target.files.length,
        fileName: e.target.files[0]?.name,
        timestamp: new Date().toISOString()
    });
    if (e.target.files.length > 0) {
        const file = e.target.files[0];
        console.log('[CONVERT] Processing file:', file.name, 'Size:', file.size);
        // Reset the input value immediately to prevent re-triggering
        e.target.value = '';
        console.log('[CONVERT] Input value reset');
        handleConvertFile(file);
    }
});

function handleConvertFile(file) {
    console.log('[CONVERT] handleConvertFile called', {
        fileName: file.name,
        fileSize: file.size,
        fileType: file.type
    });
    
    if (!file.name.toLowerCase().endsWith('.pdf')) {
        console.log('[CONVERT] ERROR: Not a PDF file');
        showError('Please select a PDF file');
        // Reset file input
        convertFileInput.value = '';
        return;
    }
    
    if (file.size > 100 * 1024 * 1024) {
        console.log('[CONVERT] ERROR: File too large');
        showError('File size must be less than 100MB');
        // Reset file input
        convertFileInput.value = '';
        return;
    }
    
    console.log('[CONVERT] File validation passed, starting conversion');
    convertPDF(file);
}

function convertPDF(file) {
    const formData = new FormData();
    formData.append('file', file);
    
    // Show progress
    document.getElementById('convert-upload-area').style.display = 'none';
    document.getElementById('convert-progress').style.display = 'block';
    
    // Animate progress bar
    let progress = 0;
    const progressFill = document.getElementById('convert-progress-fill');
    const progressInterval = setInterval(() => {
        progress += 1;
        if (progress <= 90) {
            progressFill.style.width = progress + '%';
        }
    }, 100);
    
    fetch('/api/convert', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        clearInterval(progressInterval);
        progressFill.style.width = '100%';
        
        setTimeout(() => {
            if (data.success) {
                showConvertResult(data);
            } else {
                showError(data.error || 'Conversion failed');
            }
        }, 500);
    })
    .catch(error => {
        clearInterval(progressInterval);
        showError('Network error: ' + error.message);
    });
}

function showConvertResult(data) {
    document.getElementById('convert-progress').style.display = 'none';
    document.getElementById('convert-result').style.display = 'block';
    
    document.getElementById('convert-original-size').textContent = data.original_size;
    document.getElementById('convert-converted-size').textContent = data.converted_size;
    
    const downloadBtn = document.getElementById('convert-download-btn');
    downloadBtn.onclick = () => {
        window.location.href = data.download_url;
    };
}

function resetConvert() {
    document.getElementById('convert-result').style.display = 'none';
    document.getElementById('convert-upload-area').style.display = 'block';
    document.getElementById('convert-progress-fill').style.width = '0%';
    convertFileInput.value = '';
}

// Compress Tab Functions
const compressFileInput = document.getElementById('compress-file-input');
const compressUploadArea = document.getElementById('compress-upload-area');

compressUploadArea.addEventListener('click', (e) => {
    // Ignore clicks from the button to prevent double-trigger
    if (e.target.closest('button')) return;
    
    // Ignore clicks on the file input itself (from programmatic click())
    if (e.target === compressFileInput) {
        console.log('[COMPRESS] File input clicked (programmatic), skipping');
        return;
    }
    
    console.log('[COMPRESS] Upload area clicked', {
        target: e.target,
        currentTarget: e.currentTarget,
        timestamp: new Date().toISOString()
    });
    e.preventDefault();
    e.stopPropagation();
    compressFileInput.click();
});

compressUploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    e.stopPropagation();
    compressUploadArea.classList.add('dragover');
});

compressUploadArea.addEventListener('dragleave', (e) => {
    e.preventDefault();
    e.stopPropagation();
    compressUploadArea.classList.remove('dragover');
});

compressUploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    e.stopPropagation();
    compressUploadArea.classList.remove('dragover');
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleCompressFile(files[0]);
    }
});

compressFileInput.addEventListener('change', (e) => {
    console.log('[COMPRESS] File input change event', {
        filesLength: e.target.files.length,
        fileName: e.target.files[0]?.name,
        timestamp: new Date().toISOString()
    });
    if (e.target.files.length > 0) {
        const file = e.target.files[0];
        console.log('[COMPRESS] Processing file:', file.name, 'Size:', file.size);
        // Reset the input value immediately to prevent re-triggering
        e.target.value = '';
        console.log('[COMPRESS] Input value reset');
        handleCompressFile(file);
    }
});

function handleCompressFile(file) {
    console.log('[COMPRESS] handleCompressFile called', {
        fileName: file.name,
        fileSize: file.size,
        fileType: file.type
    });
    
    if (!file.name.toLowerCase().endsWith('.pdf')) {
        console.log('[COMPRESS] ERROR: Not a PDF file');
        showError('Please select a PDF file');
        // Reset file input
        compressFileInput.value = '';
        return;
    }
    
    if (file.size > 100 * 1024 * 1024) {
        console.log('[COMPRESS] ERROR: File too large');
        showError('File size must be less than 100MB');
        // Reset file input
        compressFileInput.value = '';
        return;
    }
    
    console.log('[COMPRESS] File validation passed, starting compression');
    compressPDF(file);
}

function compressPDF(file) {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('quality', document.getElementById('quality-select').value);
    
    // Show progress
    document.getElementById('compress-upload-area').style.display = 'none';
    document.getElementById('compress-progress').style.display = 'block';
    
    // Animate progress bar
    let progress = 0;
    const progressFill = document.getElementById('compress-progress-fill');
    const progressInterval = setInterval(() => {
        progress += 1;
        if (progress <= 90) {
            progressFill.style.width = progress + '%';
        }
    }, 100);
    
    fetch('/api/compress', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        clearInterval(progressInterval);
        progressFill.style.width = '100%';
        
        setTimeout(() => {
            if (data.success) {
                showCompressResult(data);
            } else {
                showError(data.error || 'Compression failed');
            }
        }, 500);
    })
    .catch(error => {
        clearInterval(progressInterval);
        showError('Network error: ' + error.message);
    });
}

function showCompressResult(data) {
    document.getElementById('compress-progress').style.display = 'none';
    document.getElementById('compress-result').style.display = 'block';
    
    document.getElementById('compress-original-size').textContent = data.original_size;
    document.getElementById('compress-compressed-size').textContent = data.compressed_size;
    document.getElementById('compress-reduction').textContent = data.reduction_percent;
    document.getElementById('compress-saved').textContent = data.reduction_mb;
    document.getElementById('compress-method').textContent = data.method === 'ghostscript' ? 'Ghostscript (High Quality)' : 'PyPDF2 (Basic)';
    
    const downloadBtn = document.getElementById('compress-download-btn');
    downloadBtn.onclick = () => {
        window.location.href = data.download_url;
    };
}

function resetCompress() {
    document.getElementById('compress-result').style.display = 'none';
    document.getElementById('compress-upload-area').style.display = 'block';
    document.getElementById('compress-progress-fill').style.width = '0%';
    compressFileInput.value = '';
}

// Metadata Cleaning Tab Functions
const metadataFileInput = document.getElementById('metadata-file-input');
const metadataUploadArea = document.getElementById('metadata-upload-area');

console.log('[METADATA] File input element:', metadataFileInput);
console.log('[METADATA] Upload area element:', metadataUploadArea);

// Add direct button click handler
const metadataButton = metadataUploadArea.querySelector('button.btn-primary');
if (metadataButton) {
    console.log('[METADATA] Button found, adding click handler');
    metadataButton.addEventListener('click', (e) => {
        console.log('[METADATA] Button click handler triggered');
        e.preventDefault();
        e.stopPropagation();
        
        if (metadataFileInput) {
            console.log('[METADATA] Triggering file input click');
            metadataFileInput.click();
        } else {
            console.error('[METADATA] File input not found!');
        }
    });
} else {
    console.error('[METADATA] Button not found!');
}

metadataUploadArea.addEventListener('click', (e) => {
    // Ignore clicks from the button to prevent double-trigger
    if (e.target.closest('button')) {
        console.log('[METADATA] Button clicked, skipping upload area handler');
        return;
    }
    
    // Ignore clicks on the file input itself (from programmatic click())
    if (e.target === metadataFileInput) {
        console.log('[METADATA] File input clicked (programmatic), skipping');
        return;
    }
    
    console.log('[METADATA] Upload area clicked', {
        target: e.target,
        currentTarget: e.currentTarget,
        timestamp: new Date().toISOString()
    });
    e.preventDefault();
    e.stopPropagation();
    
    if (metadataFileInput) {
        metadataFileInput.click();
    }
});

metadataUploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    e.stopPropagation();
    metadataUploadArea.classList.add('dragover');
});

metadataUploadArea.addEventListener('dragleave', (e) => {
    e.preventDefault();
    e.stopPropagation();
    metadataUploadArea.classList.remove('dragover');
});

metadataUploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    e.stopPropagation();
    metadataUploadArea.classList.remove('dragover');
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleMetadataFile(files[0]);
    }
});

metadataFileInput.addEventListener('change', (e) => {
    console.log('[METADATA] File input change event', {
        filesLength: e.target.files.length,
        fileName: e.target.files[0]?.name,
        timestamp: new Date().toISOString()
    });
    if (e.target.files.length > 0) {
        const file = e.target.files[0];
        console.log('[METADATA] Processing file:', file.name, 'Size:', file.size);
        // Reset the input value immediately to prevent re-triggering
        e.target.value = '';
        console.log('[METADATA] Input value reset');
        handleMetadataFile(file);
    }
});

function handleMetadataFile(file) {
    console.log('[METADATA] handleMetadataFile called', {
        fileName: file.name,
        fileSize: file.size,
        fileType: file.type
    });
    
    if (!file.name.toLowerCase().endsWith('.pdf')) {
        console.log('[METADATA] ERROR: Not a PDF file');
        showError('Please select a PDF file');
        // Reset file input
        metadataFileInput.value = '';
        return;
    }
    
    if (file.size > 100 * 1024 * 1024) {
        console.log('[METADATA] ERROR: File too large');
        showError('File size must be less than 100MB');
        // Reset file input
        metadataFileInput.value = '';
        return;
    }
    
    console.log('[METADATA] File validation passed, starting metadata cleaning');
    cleanMetadata(file);
}

function cleanMetadata(file) {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('keep_basic_info', document.getElementById('keep-basic-info').checked);
    
    // Show progress
    document.getElementById('metadata-upload-area').style.display = 'none';
    document.getElementById('metadata-progress').style.display = 'block';
    
    // Animate progress bar
    let progress = 0;
    const progressFill = document.getElementById('metadata-progress-fill');
    const progressInterval = setInterval(() => {
        progress += 1;
        if (progress <= 90) {
            progressFill.style.width = progress + '%';
        }
    }, 100);
    
    fetch('/api/clean-metadata', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        clearInterval(progressInterval);
        progressFill.style.width = '100%';
        
        setTimeout(() => {
            if (data.success) {
                showMetadataResult(data);
            } else {
                showError(data.error || 'Metadata cleaning failed');
            }
        }, 500);
    })
    .catch(error => {
        clearInterval(progressInterval);
        showError('Network error: ' + error.message);
    });
}

function showMetadataResult(data) {
    document.getElementById('metadata-progress').style.display = 'none';
    document.getElementById('metadata-result').style.display = 'block';
    
    document.getElementById('metadata-original-size').textContent = data.original_size;
    document.getElementById('metadata-cleaned-size').textContent = data.cleaned_size;
    document.getElementById('metadata-removed-count').textContent = data.metadata_removed;
    
    // Display original metadata
    const originalMetadataList = document.getElementById('original-metadata-list');
    originalMetadataList.innerHTML = '';
    for (const [key, value] of Object.entries(data.original_metadata)) {
        if (value !== 'N/A' && key !== 'error') {
            const p = document.createElement('p');
            p.innerHTML = `<strong>${key}:</strong> ${value}`;
            originalMetadataList.appendChild(p);
        }
    }
    
    // Display cleaned metadata
    const cleanedMetadataList = document.getElementById('cleaned-metadata-list');
    cleanedMetadataList.innerHTML = '';
    const cleanedMeta = data.cleaned_metadata;
    if (cleanedMeta.message) {
        const p = document.createElement('p');
        p.innerHTML = `<em>${cleanedMeta.message}</em>`;
        p.style.color = '#28a745';
        cleanedMetadataList.appendChild(p);
    } else {
        for (const [key, value] of Object.entries(cleanedMeta)) {
            if (value !== 'N/A' && key !== 'error') {
                const p = document.createElement('p');
                p.innerHTML = `<strong>${key}:</strong> ${value}`;
                p.classList.add('kept');
                cleanedMetadataList.appendChild(p);
            }
        }
    }
    
    const downloadBtn = document.getElementById('metadata-download-btn');
    downloadBtn.onclick = () => {
        window.location.href = data.download_url;
    };
}

function resetMetadata() {
    document.getElementById('metadata-result').style.display = 'none';
    document.getElementById('metadata-upload-area').style.display = 'block';
    document.getElementById('metadata-progress-fill').style.width = '0%';
    metadataFileInput.value = '';
}

// Merge Tab Functions
const mergeFileInput = document.getElementById('merge-file-input');
const mergeUploadArea = document.getElementById('merge-upload-area');
const mergeChooseBtn = document.getElementById('merge-choose-btn');
let mergeFiles = [];

if (mergeChooseBtn) {
    mergeChooseBtn.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        console.log('[MERGE] Choose button clicked');
        mergeFileInput.click();
    });
}

if (mergeUploadArea) {
    mergeUploadArea.addEventListener('click', (e) => {
        if (e.target.closest('button')) {
            console.log('[MERGE] Button clicked, skipping upload area handler');
            return;
        }
        
        if (e.target === mergeFileInput) {
            console.log('[MERGE] File input clicked (programmatic), skipping');
            return;
        }
        
        console.log('[MERGE] Upload area clicked');
        e.preventDefault();
        e.stopPropagation();
        
        if (mergeFileInput) {
            mergeFileInput.click();
        }
    });

    mergeUploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        e.stopPropagation();
        mergeUploadArea.classList.add('dragover');
    });

    mergeUploadArea.addEventListener('dragleave', (e) => {
        e.preventDefault();
        e.stopPropagation();
        mergeUploadArea.classList.remove('dragover');
    });

    mergeUploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        e.stopPropagation();
        mergeUploadArea.classList.remove('dragover');
        const files = Array.from(e.dataTransfer.files).filter(f => f.type === 'application/pdf');
        if (files.length > 0) {
            addMergeFiles(files);
        }
    });
}

if (mergeFileInput) {
    mergeFileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            const files = Array.from(e.target.files);
            addMergeFiles(files);
        }
    });
}

function addMergeFiles(files) {
    mergeFiles = mergeFiles.concat(files);
    displayMergeFiles();
    
    document.getElementById('merge-upload-area').style.display = 'none';
    document.getElementById('merge-file-list').style.display = 'block';
}

function displayMergeFiles() {
    const container = document.getElementById('merge-files-container');
    container.innerHTML = '';
    
    mergeFiles.forEach((file, index) => {
        const fileItem = document.createElement('div');
        fileItem.className = 'merge-file-item';
        fileItem.draggable = true;
        fileItem.dataset.index = index;
        
        fileItem.innerHTML = `
            <div class="file-info">
                <span class="file-number">${index + 1}</span>
                <span class="file-name">📄 ${file.name}</span>
                <span class="file-size">${(file.size / 1024 / 1024).toFixed(2)} MB</span>
            </div>
            <div class="file-actions">
                <button class="btn-icon" onclick="moveMergeFile(${index}, -1)" ${index === 0 ? 'disabled' : ''}>↑</button>
                <button class="btn-icon" onclick="moveMergeFile(${index}, 1)" ${index === mergeFiles.length - 1 ? 'disabled' : ''}>↓</button>
                <button class="btn-icon btn-remove" onclick="removeMergeFile(${index})">🗑️</button>
            </div>
        `;
        
        // Drag and drop for reordering
        fileItem.addEventListener('dragstart', (e) => {
            e.dataTransfer.effectAllowed = 'move';
            e.dataTransfer.setData('text/plain', index);
            fileItem.classList.add('dragging');
        });
        
        fileItem.addEventListener('dragend', () => {
            fileItem.classList.remove('dragging');
        });
        
        fileItem.addEventListener('dragover', (e) => {
            e.preventDefault();
            e.dataTransfer.dropEffect = 'move';
        });
        
        fileItem.addEventListener('drop', (e) => {
            e.preventDefault();
            const fromIndex = parseInt(e.dataTransfer.getData('text/plain'));
            const toIndex = index;
            
            if (fromIndex !== toIndex) {
                const [movedFile] = mergeFiles.splice(fromIndex, 1);
                mergeFiles.splice(toIndex, 0, movedFile);
                displayMergeFiles();
            }
        });
        
        container.appendChild(fileItem);
    });
}

function moveMergeFile(index, direction) {
    const newIndex = index + direction;
    if (newIndex >= 0 && newIndex < mergeFiles.length) {
        [mergeFiles[index], mergeFiles[newIndex]] = [mergeFiles[newIndex], mergeFiles[index]];
        displayMergeFiles();
    }
}

function removeMergeFile(index) {
    mergeFiles.splice(index, 1);
    if (mergeFiles.length === 0) {
        clearMergeFiles();
    } else {
        displayMergeFiles();
    }
}

function clearMergeFiles() {
    mergeFiles = [];
    mergeFileInput.value = '';
    document.getElementById('merge-file-list').style.display = 'none';
    document.getElementById('merge-upload-area').style.display = 'block';
}

function startMerge() {
    if (mergeFiles.length < 2) {
        showError('Please select at least 2 PDF files to merge');
        return;
    }
    
    const formData = new FormData();
    mergeFiles.forEach(file => {
        formData.append('files[]', file);
    });
    
    document.getElementById('merge-file-list').style.display = 'none';
    document.getElementById('merge-progress').style.display = 'block';
    
    let progress = 0;
    const progressFill = document.getElementById('merge-progress-fill');
    const progressText = document.getElementById('merge-progress-text');
    const progressInterval = setInterval(() => {
        progress += 1;
        if (progress <= 90) {
            progressFill.style.width = progress + '%';
            progressText.textContent = `Merging ${mergeFiles.length} PDFs...`;
        }
    }, 100);
    
    fetch('/api/merge', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        clearInterval(progressInterval);
        progressFill.style.width = '100%';
        
        setTimeout(() => {
            if (data.success) {
                showMergeResult(data);
            } else {
                showError(data.error || 'PDF merge failed');
            }
        }, 500);
    })
    .catch(error => {
        clearInterval(progressInterval);
        showError('Network error: ' + error.message);
    });
}

function showMergeResult(data) {
    document.getElementById('merge-progress').style.display = 'none';
    document.getElementById('merge-result').style.display = 'block';
    
    document.getElementById('merge-file-count').textContent = data.file_count;
    document.getElementById('merge-total-pages').textContent = data.total_pages;
    document.getElementById('merge-output-size').textContent = data.output_size;
    
    const downloadBtn = document.getElementById('merge-download-btn');
    downloadBtn.onclick = () => {
        window.location.href = data.download_url;
    };
}

function resetMerge() {
    document.getElementById('merge-result').style.display = 'none';
    document.getElementById('merge-progress-fill').style.width = '0%';
    clearMergeFiles();
}

// Error handling
function showError(message) {
    // Hide all other sections
    document.getElementById('convert-upload-area').style.display = 'none';
    document.getElementById('convert-progress').style.display = 'none';
    document.getElementById('convert-result').style.display = 'none';
    document.getElementById('compress-upload-area').style.display = 'none';
    document.getElementById('compress-progress').style.display = 'none';
    document.getElementById('compress-result').style.display = 'none';
    document.getElementById('metadata-upload-area').style.display = 'none';
    document.getElementById('metadata-progress').style.display = 'none';
    document.getElementById('metadata-result').style.display = 'none';
    document.getElementById('merge-upload-area').style.display = 'none';
    document.getElementById('merge-file-list').style.display = 'none';
    document.getElementById('merge-progress').style.display = 'none';
    document.getElementById('merge-result').style.display = 'none';
    
    // Show error
    document.getElementById('error-message').style.display = 'block';
    document.getElementById('error-text').textContent = message;
}

function hideError() {
    document.getElementById('error-message').style.display = 'none';
    
    // Show appropriate upload area based on active tab
    if (document.getElementById('convert-tab').classList.contains('active')) {
        document.getElementById('convert-upload-area').style.display = 'block';
    } else if (document.getElementById('compress-tab').classList.contains('active')) {
        document.getElementById('compress-upload-area').style.display = 'block';
    } else if (document.getElementById('metadata-tab').classList.contains('active')) {
        document.getElementById('metadata-upload-area').style.display = 'block';
    } else if (document.getElementById('merge-tab').classList.contains('active')) {
        if (mergeFiles.length > 0) {
            document.getElementById('merge-file-list').style.display = 'block';
        } else {
            document.getElementById('merge-upload-area').style.display = 'block';
        }
    }
}

// Made with Bob
