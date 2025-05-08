const dropArea = document.getElementById('drop-area');
const fileInput = document.getElementById('file-input');
const fileList = document.getElementById('file-list');

function preventDefaults(e) {
  e.preventDefault();
  e.stopPropagation();
}

function highlight(e) {
  dropArea.classList.add('highlight');
}

function unhighlight(e) {
  dropArea.classList.remove('highlight');
}

function handleDrop(e) {
  unhighlight(e);
  const files = e.dataTransfer.files;
  handleFiles(files);
}

function handleFiles(files) {
  for (let i = 0; i < files.length; i++) {
    const file = files[i];
    const listItem = document.createElement('p');
    let fileType = 'File';
        if (file.type.startsWith('image')) {
            fileType = 'Image';
        } else if (file.type.startsWith('video')) {
            fileType = 'Video';
        } else if (file.type.startsWith('audio')) {
            fileType = 'Audio';
        }
    listItem.textContent = `${fileType}: ${file.name} (${(file.size / 1024).toFixed(2)} KB)`;  // Show file name and size
    fileList.appendChild(listItem);
  }
  // Clear the input so you can drop same files again
  fileInput.value = '';
}

function handleInputChange(e) {
  const files = e.target.files;
  handleFiles(files);
}

// Add event listeners
dropArea.addEventListener('dragenter', preventDefaults, false);
dropArea.addEventListener('dragover', preventDefaults, false);
dropArea.addEventListener('dragleave', unhighlight, false);
dropArea.addEventListener('drop', handleDrop, false);
fileInput.addEventListener('change', handleInputChange, false);