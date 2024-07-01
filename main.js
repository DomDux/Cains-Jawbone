// Function to populate the file list
function populateFileList() {
    const fs = require('fs');

    // Directory path
    const directoryPath = './data/processed';

    // Read the contents of the directory
    fs.readdir(directoryPath, (err, files) => {
        if (err) {
            console.error('Error reading directory:', err);
            return;
        }
        const fileNames = files;
        const fileListDiv = document.getElementById("fileList");
        fileListDiv.innerHTML = "";

        fileNames.forEach((fileName) => {
            const icon = document.createElement("div");
            icon.className = "fileIcon";
            icon.textContent = fileName;
            icon.onclick = () => displayFileDetails(fileName);

            fileListDiv.appendChild(icon);
        });
    });
}

// Function to display file details when an icon is clicked
function displayFileDetails(fileName) {
    const fileNameHeader = document.getElementById("fileNameHeader");
    const fileContent = document.getElementById("fileContent");

    fileNameHeader.textContent = fileName;

    // Fetch content from the file and display it in the textarea
    // You may need to use Node.js to handle file operations on the server-side
    // Example: fetchFileContent(fileName).then(content => fileContent.value = content);
}

// Function to save the current file content
function saveFile() {
    const fileNameHeader = document.getElementById("fileNameHeader");
    const fileContent = document.getElementById("fileContent");

    // Save the content to the corresponding file using Node.js backend
    // Example: saveFileContent(fileNameHeader.textContent, fileContent.value);
}

// Function to create a new file
function createNewFile() {
    const fileNameHeader = document.getElementById("fileNameHeader");
    const fileContent = document.getElementById("fileContent");

    fileNameHeader.textContent = "New File";
    fileContent.value = "";
}

// Initial setup
populateFileList();
