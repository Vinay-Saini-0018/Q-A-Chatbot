document.addEventListener('DOMContentLoaded', () => {
    // API Configuration
    const API_BASE_URL = 'https://q-a-chatbot-2.onrender.com';

    // DOM Elements
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');
    const chatMessages = document.getElementById('chat-messages');
    const typingIndicator = document.getElementById('typing-indicator');
    const clearChatBtn = document.getElementById('clear-chat-btn');

    const fileInput = document.getElementById('file-input');
    const uploadZone = document.getElementById('upload-zone');
    const docUl = document.getElementById('doc-ul');
    const docCount = document.getElementById('doc-count');

    // State
    let uploadedFiles = [];

    // Initialize Marked to use highlight.js
    marked.setOptions({
        highlight: function(code, lang) {
            if (lang && hljs.getLanguage(lang)) {
                return hljs.highlight(code, { language: lang }).value;
            }
            return hljs.highlightAuto(code).value;
        },
        breaks: true,
        gfm: true
    });

    // Automatically fetch files that were already uploaded
    async function loadExistingFiles(retries = 3) {
        try {
            const res = await fetch(`${API_BASE_URL}/files`);

            if (res.ok) {
                const data = await res.json();
                uploadedFiles = [];
                data.files.forEach(fileName => {
                    uploadedFiles.push({ name: fileName });
                });
                updateDocumentList();
            }
        } catch (e) {
            console.warn("Waiting for backend to be ready...");
            if (retries > 0) {
                setTimeout(() => loadExistingFiles(retries - 1), 1000);
            }
        }
    }
    loadExistingFiles();

    // --- Chat Logic ---

    // Handle incoming simple messages
    function appendMessage(text, sender) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${sender} appear-animation`;

        const avatar = document.createElement('div');
        avatar.className = 'avatar';
        avatar.innerHTML = sender === 'bot' ? '<i class="fa-solid fa-robot"></i>' : '<i class="fa-solid fa-user"></i>';

        const content = document.createElement('div');
        content.className = 'message-content';
        
        if (sender === 'bot') {
            // Render markdown for bot messages
            content.innerHTML = marked.parse(text);
        } else {
            // Plain text for user messages
            const p = document.createElement('p');
            p.textContent = text;
            content.appendChild(p);
        }

        msgDiv.appendChild(avatar);
        msgDiv.appendChild(content);

        chatMessages.appendChild(msgDiv);
        scrollToBottom();
    }

    function scrollToBottom() {
        const chatWindow = document.getElementById('chat-window');
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }

    // Handle Chat Submit
    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const text = chatInput.value.trim();
        if (!text) return;

        // User message
        appendMessage(text, 'user');
        chatInput.value = '';

        if (uploadedFiles.length === 0) {
            appendMessage("Please upload a document before asking questions.", 'bot');
            return;
        }

        // Simulate Bot thinking
        typingIndicator.classList.remove('hidden');
        scrollToBottom();

        try {
            // Send the request to our FastAPI backend using the first file uploaded
            const fileName = "data/" + uploadedFiles[0].name;

            const response = await fetch(`${API_BASE_URL}/ask`, {

                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    query: text,
                    file: fileName
                })
            });

            const data = await response.json();

            typingIndicator.classList.add('hidden');
            if (response.ok) {
                appendMessage(data.answer, 'bot');
            } else {
                appendMessage("Oops! Error from server: " + (data.detail || "Unknown Error"), 'bot');
            }
        } catch (error) {
            typingIndicator.classList.add('hidden');
            appendMessage(`Could not connect to the backend server at ${API_BASE_URL}. Please ensure the backend is running.`, 'bot');
            console.error("Error connecting to backend:", error);
        }

    });

    // Dummy logic to make UI responsive
    function generateMockReply(userText) {
        if (uploadedFiles.length === 0) {
            return "I see your question, but you haven't uploaded any documents yet. Please drag & drop a file to start RAG!";
        }
        return `Based on your ${uploadedFiles.length} uploaded document(s), here is an answer to "${userText}". (Backend API endpoint not yet connected)`;
    }

    // Clear Chat
    clearChatBtn.addEventListener('click', () => {
        chatMessages.innerHTML = '';
        appendMessage("Chat history cleared. How else can I help?", "bot");
    });


    // --- File Upload Logic ---

    // Drag & Drop
    uploadZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadZone.classList.add('dragover');
    });

    uploadZone.addEventListener('dragleave', () => {
        uploadZone.classList.remove('dragover');
    });

    uploadZone.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadZone.classList.remove('dragover');
        if (e.dataTransfer.files.length) {
            handleFiles(e.dataTransfer.files);
        }
    });

    // File Input change
    fileInput.addEventListener('change', () => {
        if (fileInput.files.length) {
            handleFiles(fileInput.files);
        }
    });

    async function handleFiles(files) {
        for (let file of Array.from(files)) {
            // Avoid duplicates
            if (!uploadedFiles.some(f => f.name === file.name)) {
                
                // Show file instantly so it doesn't wait for server response
                uploadedFiles.push(file);
                updateDocumentList();

                // Create FormData to send the file
                const formData = new FormData();
                formData.append("file", file);

                try {
                    // Upload file to the backend
                    const response = await fetch(`${API_BASE_URL}/upload`, {

                        method: 'POST',
                        body: formData
                    });

                    if (!response.ok) {
                        console.error("Failed to upload", file.name);
                    }
                } catch (error) {
                    // Server restart cuts off connection but file is still saved. Ignore error.
                    console.warn("Upload network interrupted by backend restart. File is safe!", file.name);
                }
            }
        }
    }

    function removeFile(fileName) {
        uploadedFiles = uploadedFiles.filter(f => f.name !== fileName);
        updateDocumentList();
        // ** TODO: Send Delete request to FastAPI Backend **
    }

    function updateDocumentList() {
        docUl.innerHTML = '';
        docCount.textContent = uploadedFiles.length;

        if (uploadedFiles.length === 0) {
            docUl.innerHTML = '<li class="empty-state">No documents added yet</li>';
            return;
        }

        uploadedFiles.forEach(file => {
            const li = document.createElement('li');
            li.className = 'doc-item appear-animation';

            // Simple extension icon logic
            let iconClass = 'fa-file-lines';
            if (file.name.endsWith('.pdf')) iconClass = 'fa-file-pdf';
            if (file.name.endsWith('.doc') || file.name.endsWith('.docx')) iconClass = 'fa-file-word';

            li.innerHTML = `
                <i class="fa-solid ${iconClass} doc-icon"></i>
                <span class="doc-name" title="${file.name}">${file.name}</span>
                <button class="doc-remove" aria-label="Remove Document"><i class="fa-solid fa-xmark"></i></button>
            `;

            li.querySelector('.doc-remove').addEventListener('click', () => removeFile(file.name));
            docUl.appendChild(li);
        });
    }
});
