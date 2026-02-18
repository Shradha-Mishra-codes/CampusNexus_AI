// CampusNexus AI - Main Application Logic

// API Base URL
const API_BASE = window.location.origin;

// State
const state = {
    currentTab: 'chat',
    currentLanguage: 'en',
    isOllamaConnected: false
};

// Translations dictionary
const translations = {
    en: {
        welcomeTitle: "Welcome to CampusNexus AI!",
        welcomeSubtitle: "Ask questions about your uploaded documents and I'll provide accurate answers with sources.",
        chatPlaceholder: "Ask anything about your documents...",
        sendButton: "Send",
        uploadTitle: "Drag & Drop Documents",
        uploadSubtitle: "or click to browse",
        uploadHint: "Supported: PDF, DOCX, PPTX",
        analyticsTitle: "Previous Year Questions Analytics",
        totalQuestions: "Total Questions",
        topicsCovered: "Topics Covered",
        yearRange: "Year Range",
        graphTitle: "Knowledge Graph Visualization",
        graphPlaceholder: "Knowledge graph will appear here",
        graphHint: "Upload documents to generate the graph",
        governanceTitle: "Governance Panel",
        pendingApprovals: "Pending Approvals",
        noPending: "No pending documents",
        approve: "Approve",
        reject: "Reject",
        statusConnected: "Connected",
        statusDegraded: "Degraded",
        statusOffline: "Offline",
        checkingStatus: "Checking...",
        keyPatterns: "Key Patterns",
        uploadFirst: "Upload PYQ documents to see analytics",
        nodes: "Nodes",
        edges: "Edges",
        density: "Density",
        totalDocs: "Total Documents",
        pending: "Pending",
        approved: "Approved",
        rejected: "Rejected",
        totalQueries: "Total Queries",
        frequency: "Frequency",
        importance: "Importance",
        confidence: "Confidence",
        sources: "Sources",
        languageChanged: "Language changed to English"
    },
    hi: {
        welcomeTitle: "CampusNexus AI में आपका स्वागत है!",
        welcomeSubtitle: "अपने अपलोड किए गए दस्तावेज़ों के बारे में प्रश्न पूछें और मैं सटीक उत्तर स्रोतों के साथ प्रदान करूंगा।",
        chatPlaceholder: "अपने दस्तावेज़ों के बारे में कुछ भी पूछें...",
        sendButton: "भेजें",
        uploadTitle: "दस्तावेज़ खींचें और छोड़ें",
        uploadSubtitle: "या ब्राउज़ करने के लिए क्लिक करें",
        uploadHint: "समर्थित: PDF, DOCX, PPTX",
        analyticsTitle: "पिछले वर्ष के प्रश्न विश्लेषण",
        totalQuestions: "कुल प्रश्न",
        topicsCovered: "विषय शामिल",
        yearRange: "वर्ष सीमा",
        graphTitle: "ज्ञान ग्राफ विज़ुअलाइज़ेशन",
        graphPlaceholder: "ज्ञान ग्राफ यहां दिखाई देगा",
        graphHint: "ग्राफ बनाने के लिए दस्तावेज़ अपलोड करें",
        governanceTitle: "शासन पैनल",
        pendingApprovals: "लंबित अनुमोदन",
        noPending: "कोई लंबित दस्तावेज़ नहीं",
        approve: "अनुमोदित करें",
        reject: "अस्वीकार करें",
        statusConnected: "कनेक्टेड",
        statusDegraded: "खराब",
        statusOffline: "ऑफ़लाइन",
        checkingStatus: "जांच हो रही है...",
        keyPatterns: "मुख्य पैटर्न",
        uploadFirst: "विश्लेषण देखने के लिए PYQ दस्तावेज़ अपलोड करें",
        nodes: "नोड्स",
        edges: "किनारे",
        density: "घनत्व",
        totalDocs: "कुल दस्तावेज़",
        pending: "लंबित",
        approved: "अनुमोदित",
        rejected: "अस्वीकृत",
        totalQueries: "कुल प्रश्न",
        frequency: "आवृत्ति",
        importance: "महत्व",
        confidence: "विश्वास",
        sources: "स्रोत",
        languageChanged: "भाषा हिंदी में बदल गई"
    },
    mr: {
        welcomeTitle: "CampusNexus AI मध्ये आपले स्वागत आहे!",
        welcomeSubtitle: "तुमच्या अपलोड केलेल्या कागदपत्रांबद्दल प्रश्न विचारा आणि मी स्रोतांसह अचूक उत्तरे देईन.",
        chatPlaceholder: "तुमच्या कागदपत्रांबद्दल काहीही विचारा...",
        sendButton: "पाठवा",
        uploadTitle: "कागदपत्रे येथे ड्रॅग आणि ड्रॉप करा",
        uploadSubtitle: "किंवा ब्राउझ करण्यासाठी क्लिक करा",
        uploadHint: "समर्थित: PDF, DOCX, PPTX",
        analyticsTitle: "मागील वर्षाच्या प्रश्नांचे विश्लेषण",
        totalQuestions: "एकूण प्रश्न",
        topicsCovered: "कव्हर केलेले विषय",
        yearRange: "वर्ष श्रेणी",
        graphTitle: "ज्ञान ग्राफ व्हिज्युअलायझेशन",
        graphPlaceholder: "ज्ञान ग्राफ येथे दिसेल",
        graphHint: "ग्राफ तयार करण्यासाठी कागदपत्रे अपलोड करा",
        governanceTitle: "प्रशासन पॅनेल",
        pendingApprovals: "प्रलंबित मंजूरी",
        noPending: "कोणतीही प्रलंबित कागदपत्रे नाहीत",
        approve: "मंजूर करा",
        reject: "नाकारा",
        statusConnected: "कनेक्ट केलेले",
        statusDegraded: "खालावलेले",
        statusOffline: "ऑफलाईन",
        checkingStatus: "तपासत आहे...",
        keyPatterns: "मुख्य नमुने",
        uploadFirst: "विश्लेषण पाहण्यासाठी PYQ कागदपत्रे अपलोड करा",
        nodes: "नोड्स",
        edges: "कडा",
        density: "घनता",
        totalDocs: "एकूण कागदपत्रे",
        pending: "प्रलंबित",
        approved: "मंजूर",
        rejected: "नाकारलेले",
        totalQueries: "एकूण प्रश्न",
        frequency: "वारंवारता",
        importance: "महत्व",
        confidence: "विश्वास",
        sources: "स्रोत",
        languageChanged: "भाषा मराठीत बदलली आहे"
    },
    es: {
        welcomeTitle: "¡Bienvenido a CampusNexus AI!",
        welcomeSubtitle: "Haz preguntas sobre tus documentos subidos y te proporcionaré respuestas precisas con fuentes.",
        chatPlaceholder: "Pregunta cualquier cosa sobre tus documentos...",
        sendButton: "Enviar",
        uploadTitle: "Arrastrar y soltar documentos",
        uploadSubtitle: "o haz clic para explorar",
        uploadHint: "Compatible: PDF, DOCX, PPTX",
        analyticsTitle: "Análisis de preguntas de años anteriores",
        totalQuestions: "Total de preguntas",
        topicsCovered: "Temas cubiertos",
        yearRange: "Rango de años",
        graphTitle: "Visualización del grafo de conocimiento",
        graphPlaceholder: "El grafo de conocimiento aparecerá aquí",
        graphHint: "Sube documentos para generar el grafo",
        governanceTitle: "Panel de gobernanza",
        pendingApprovals: "Aprobaciones pendientes",
        noPending: "No hay documentos pendientes",
        approve: "Aprobar",
        reject: "Rechazar",
        statusConnected: "Conectado",
        statusDegraded: "Degradado",
        statusOffline: "Sin conexión",
        checkingStatus: "Verificando...",
        keyPatterns: "Patrones clave",
        uploadFirst: "Sube documentos PYQ para ver análisis",
        nodes: "Nodos",
        edges: "Aristas",
        density: "Densidad",
        totalDocs: "Total de documentos",
        pending: "Pendiente",
        approved: "Aprobado",
        rejected: "Rechazado",
        totalQueries: "Consultas totales",
        frequency: "Frecuencia",
        importance: "Importancia",
        confidence: "Confianza",
        sources: "Fuentes",
        languageChanged: "Idioma cambiado a Español"
    },
    fr: {
        welcomeTitle: "Bienvenue sur CampusNexus AI !",
        welcomeSubtitle: "Posez des questions sur vos documents téléchargés et je vous fournirai des réponses précises avec des sources.",
        chatPlaceholder: "Posez des questions sur vos documents...",
        sendButton: "Envoyer",
        uploadTitle: "Glisser-déposer des documents",
        uploadSubtitle: "ou cliquez pour parcourir",
        uploadHint: "Pris en charge : PDF, DOCX, PPTX",
        analyticsTitle: "Analyse des questions des années précédentes",
        totalQuestions: "Nombre total de questions",
        topicsCovered: "Sujets couverts",
        yearRange: "Période",
        graphTitle: "Visualisation du graphe de connaissances",
        graphPlaceholder: "Le graphe de connaissances apparaîtra ici",
        graphHint: "Téléchargez des documents pour générer le graphe",
        governanceTitle: "Panneau de gouvernance",
        pendingApprovals: "Approbations en attente",
        noPending: "Aucun document en attente",
        approve: "Approuver",
        reject: "Rejeter",
        statusConnected: "Connecté",
        statusDegraded: "Dégradé",
        statusOffline: "Hors ligne",
        checkingStatus: "Vérification...",
        keyPatterns: "Schémas clés",
        uploadFirst: "Téléchargez des documents PYQ pour voir l'analyse",
        nodes: "Nœuds",
        edges: "Arêtes",
        density: "Densité",
        totalDocs: "Total des documents",
        pending: "En attente",
        approved: "Approuvé",
        rejected: "Rejeté",
        totalQueries: "Requêtes totales",
        frequency: "Fréquence",
        importance: "Importance",
        confidence: "Confiance",
        sources: "Sources",
        languageChanged: "Langue changée en Français"
    },
    de: {
        welcomeTitle: "Willkommen bei CampusNexus AI!",
        welcomeSubtitle: "Stellen Sie Fragen zu Ihren hochgeladenen Dokumenten und ich liefere Ihnen genaue Antworten mit Quellen.",
        chatPlaceholder: "Fragen Sie alles über Ihre Dokumente...",
        sendButton: "Senden",
        uploadTitle: "Dokumente per Drag & Drop ablegen",
        uploadSubtitle: "oder klicken Sie zum Durchsuchen",
        uploadHint: "Unterstützt: PDF, DOCX, PPTX",
        analyticsTitle: "Analyse früherer Jahresfragen",
        totalQuestions: "Gesamtzahl der Fragen",
        topicsCovered: "Abgedeckte Themen",
        yearRange: "Jahresbereich",
        graphTitle: "Wissensgraph-Visualisierung",
        graphPlaceholder: "Der Wissensgraph wird hier angezeigt",
        graphHint: "Dokumente hochladen, um den Graphen zu erstellen",
        governanceTitle: "Governance-Panel",
        pendingApprovals: "Ausstehende Genehmigungen",
        noPending: "Keine ausstehenden Dokumente",
        approve: "Genehmigen",
        reject: "Ablehnen",
        statusConnected: "Verbunden",
        statusDegraded: "Beeinträchtigt",
        statusOffline: "Offline",
        checkingStatus: "Überprüfen...",
        keyPatterns: "Wichtige Muster",
        uploadFirst: "PYQ-Dokumente hochladen, um Analysen zu sehen",
        nodes: "Knoten",
        edges: "Kanten",
        density: "Dichte",
        totalDocs: "Gesamtdokumente",
        pending: "Ausstehend",
        approved: "Genehmigt",
        rejected: "Abgelehnt",
        totalQueries: "Gesamtanfragen",
        frequency: "Häufigkeit",
        importance: "Wichtigkeit",
        confidence: "Vertrauen",
        sources: "Quellen",
        languageChanged: "Sprache auf Deutsch geändert"
    }
};

// Function to apply translations
function applyTranslations(language) {
    const t = translations[language] || translations.en;
    
    // Update welcome message
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (t[key]) {
            el.textContent = t[key];
            }
    });
    //const welcomeTitle = document.querySelector('.welcome-message h3');
    //const welcomeSubtitle = document.querySelector('.welcome-message p');
    //if (welcomeTitle) welcomeTitle.textContent = t.welcomeTitle;
   // if (welcomeSubtitle) welcomeSubtitle.textContent = t.welcomeSubtitle;
    
    // Update chat input placeholder
    const chatInput = document.getElementById('chatInput');
    if (chatInput) chatInput.placeholder = t.chatPlaceholder;
    
    // 3. Update the state for future dynamic loads
    state.currentLanguage = language;
    // Update upload section
    const uploadTitle = document.querySelector('.upload-zone h3');
    const uploadSubtitle = document.querySelector('.upload-zone p');
    const uploadHint = document.querySelector('.upload-hint');
    if (uploadTitle) uploadTitle.textContent = t.uploadTitle;
    if (uploadSubtitle) uploadSubtitle.textContent = t.uploadSubtitle;
    if (uploadHint) uploadHint.textContent = t.uploadHint;
    
    // Update analytics section
    const analyticsTitle = document.querySelector('#analyticsPanel .section-title');
    if (analyticsTitle) analyticsTitle.textContent = t.analyticsTitle;
    
    // Update analytics labels
    const analyticsLabels = document.querySelectorAll('.analytics-label');
    if (analyticsLabels.length >= 3) {
        analyticsLabels[0].textContent = t.totalQuestions;
        analyticsLabels[1].textContent = t.topicsCovered;
        analyticsLabels[2].textContent = t.yearRange;
    }
    
    // Update graph section
    const graphTitle = document.querySelector('#graphPanel .section-title');
    if (graphTitle) graphTitle.textContent = t.graphTitle;
    
    // Update graph placeholder
    const graphPlaceholder = document.querySelector('.graph-placeholder p');
    const graphHint = document.querySelector('.graph-hint');
    if (graphPlaceholder) graphPlaceholder.textContent = t.graphPlaceholder;
    if (graphHint) graphHint.textContent = t.graphHint;
    
    // Update governance section
    const governanceTitle = document.querySelector('#governancePanel .section-title');
    if (governanceTitle) governanceTitle.textContent = t.governanceTitle;
    
    const governanceHeader = document.querySelector('#governanceDocuments h4');
    if (governanceHeader) governanceHeader.textContent = t.pendingApprovals;
}

// Show notification function
function showNotification(message) {
    // Remove existing notification if any
    const existingNotification = document.querySelector('.language-notification');
    if (existingNotification) {
        existingNotification.remove();
    }
    
    const notification = document.createElement('div');
    notification.className = 'language-notification';
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 80px;
        right: 20px;
        background: var(--success, #10b981);
        color: white;
        padding: 12px 24px;
        border-radius: 8px;
        font-size: 14px;
        font-weight: 500;
        z-index: 1000;
        animation: slideIn 0.3s ease-out;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    `;
    
    document.body.appendChild(notification);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
}

// Add notification animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    initializeTabs();
    initializeChat();
    initializeUpload();
    initializeLanguage();
    checkHealth();
    
    // Check health every 30 seconds
    setInterval(checkHealth, 30000);
});

// Tab Management
function initializeTabs() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabPanels = document.querySelectorAll('.tab-panel');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const targetTab = button.getAttribute('data-tab');
            
            // Update buttons
            tabButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            
            // Update panels
            tabPanels.forEach(panel => panel.classList.remove('active'));
            document.getElementById(`${targetTab}Panel`).classList.add('active');
            
            state.currentTab = targetTab;
            
            // Load data for specific tabs
            if (targetTab === 'analytics') {
                loadAnalytics();
            } else if (targetTab === 'graph') {
                loadKnowledgeGraph();
            } else if (targetTab === 'governance') {
                loadGovernance();
            }
        });
    });
}

// Chat Functionality
function initializeChat() {
    const chatInput = document.getElementById('chatInput');
    const sendButton = document.getElementById('sendButton');
    
    sendButton.addEventListener('click', sendMessage);
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
}

async function sendMessage() {
    const input = document.getElementById('chatInput');
    const messagesContainer = document.getElementById('chatMessages');
    const query = input.value.trim();
    
    if (!query) return;
    
    // Clear input
    input.value = '';
    
    // Remove welcome message if exists
    const welcomeMsg = messagesContainer.querySelector('.welcome-message');
    if (welcomeMsg) {
        welcomeMsg.remove();
    }
    
    // Add user message
    addMessage(query, 'user');
    
    // Show typing indicator
    const typingId = addTypingIndicator();
    
    try {
        const response = await fetch(`${API_BASE}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                query: query,
                language: state.currentLanguage,
                top_k: 5,
                include_sources: true
            })
        });
        
        if (!response.ok) {
            throw new Error('Failed to get response');
        }
        
        const data = await response.json();
        
        // Remove typing indicator
        removeTypingIndicator(typingId);
        
        // Add assistant message
        addMessage(data.answer, 'assistant', {
            sources: data.sources,
            confidence: data.confidence_score,
            processingTime: data.processing_time
        });
        
    } catch (error) {
        removeTypingIndicator(typingId);
        addMessage('Sorry, I encountered an error. Please make sure Ollama is running and try again.', 'assistant');
        console.error('Chat error:', error);
    }
}

function addMessage(text, sender, metadata = {}) {
    const messagesContainer = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = sender === 'user' ? '👤' : '🤖';
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    const textDiv = document.createElement('div');
    textDiv.className = 'message-text';
    textDiv.textContent = text;
    
    contentDiv.appendChild(textDiv);
    
    // Add confidence score for assistant messages
    if (sender === 'assistant' && metadata.confidence !== undefined) {
        const confidenceDiv = document.createElement('div');
        confidenceDiv.className = 'confidence-score';
        confidenceDiv.innerHTML = `
            <span>📊</span>
            <span>Confidence: ${(metadata.confidence * 100).toFixed(0)}%</span>
        `;
        contentDiv.appendChild(confidenceDiv);
    }
    
    // Add sources for assistant messages
    if (sender === 'assistant' && metadata.sources && metadata.sources.length > 0) {
        const sourcesDiv = document.createElement('div');
        sourcesDiv.className = 'message-sources';
        sourcesDiv.innerHTML = '<h4>📚 Sources:</h4>';
        
        metadata.sources.forEach((source, index) => {
            const sourceDiv = document.createElement('div');
            sourceDiv.className = 'source';
            sourceDiv.innerHTML = `
                <strong>${index + 1}. ${source.filename}</strong>
                ${source.page ? ` (Page ${source.page})` : ''}
                <br>
                <small>${source.chunk_text}</small>
            `;
            sourcesDiv.appendChild(sourceDiv);
        });
        
        contentDiv.appendChild(sourcesDiv);
    }
    
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(contentDiv);
    messagesContainer.appendChild(messageDiv);
    
    // Scroll to bottom
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function addTypingIndicator() {
    const messagesContainer = document.getElementById('chatMessages');
    const typingDiv = document.createElement('div');
    const id = 'typing-' + Date.now();
    typingDiv.id = id;
    typingDiv.className = 'message assistant';
    typingDiv.innerHTML = `
        <div class="message-avatar">🤖</div>
        <div class="message-content">
            <div class="message-text">
                <div class="spinner"></div>
                Thinking...
            </div>
        </div>
    `;
    messagesContainer.appendChild(typingDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    return id;
}

function removeTypingIndicator(id) {
    const typingDiv = document.getElementById(id);
    if (typingDiv) {
        typingDiv.remove();
    }
}

// Upload Functionality
function initializeUpload() {
    const uploadZone = document.getElementById('uploadZone');
    const fileInput = document.getElementById('fileInput');
    
    uploadZone.addEventListener('click', () => {
        fileInput.click();
    });
    
    fileInput.addEventListener('change', (e) => {
        handleFiles(e.target.files);
    });
    
    // Drag and drop
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
        handleFiles(e.dataTransfer.files);
    });
}

async function handleFiles(files) {
    const uploadList = document.getElementById('uploadList');
    
    for (const file of files) {
        const itemDiv = createUploadItem(file);
        uploadList.appendChild(itemDiv);
        
        try {
            await uploadFile(file, itemDiv);
        } catch (error) {
            updateUploadItemStatus(itemDiv, 'error', error.message);
        }
    }
}

function createUploadItem(file) {
    const itemDiv = document.createElement('div');
    itemDiv.className = 'upload-item';
    itemDiv.innerHTML = `
        <div class="upload-item-info">
            <div class="upload-item-icon">📄</div>
            <div>
                <div><strong>${file.name}</strong></div>
                <div class="upload-hint">${formatFileSize(file.size)}</div>
            </div>
        </div>
        <div class="upload-progress">
            <div class="upload-progress-bar" style="width: 0%"></div>
        </div>
        <div class="upload-status">⏳ Uploading...</div>
    `;
    return itemDiv;
}

async function uploadFile(file, itemDiv) {
    const formData = new FormData();
    formData.append('file', file);
    
    const progressBar = itemDiv.querySelector('.upload-progress-bar');
    
    // Simulate progress (real progress tracking would require additional setup)
    let progress = 0;
    const progressInterval = setInterval(() => {
        progress += 10;
        if (progress <= 90) {
            progressBar.style.width = progress + '%';
        }
    }, 200);
    
    try {
        const response = await fetch(`${API_BASE}/upload`, {
            method: 'POST',
            body: formData
        });
        
        clearInterval(progressInterval);
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Upload failed');
        }
        
        const result = await response.json();
        
        progressBar.style.width = '100%';
        updateUploadItemStatus(itemDiv, 'success', `✅ Uploaded (${result.metadata.total_chunks} chunks)`);
        
    } catch (error) {
        clearInterval(progressInterval);
        throw error;
    }
}

function updateUploadItemStatus(itemDiv, status, message) {
    const statusDiv = itemDiv.querySelector('.upload-status');
    statusDiv.textContent = message;
    
    if (status === 'error') {
        statusDiv.style.color = 'var(--danger)';
    } else if (status === 'success') {
        statusDiv.style.color = 'var(--success)';
    }
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

// Language Selection
function initializeLanguage() {
    const languageSelect = document.getElementById('languageSelect');
    languageSelect.addEventListener('change', (e) => {
        const selectedLanguage = e.target.value;
        state.currentLanguage = selectedLanguage;
        
        // Apply translations to UI
        applyTranslations(selectedLanguage);
        
        // Show notification
        const t = translations[selectedLanguage] || translations.en;
        showNotification(t.languageChanged);
    });
}

// Health Check
async function checkHealth() {
    try {
        const response = await fetch(`${API_BASE}/health`);
        const data = await response.json();
        
        const statusIndicator = document.getElementById('statusIndicator');
        const statusText = statusIndicator.querySelector('.status-text');
        const statusDot = statusIndicator.querySelector('.status-dot');
        
        if (data.status === 'healthy') {
            statusText.textContent = 'Connected';
            statusDot.style.background = 'var(--success)';
            statusIndicator.style.background = 'rgba(16, 185, 129, 0.1)';
            statusIndicator.style.borderColor = 'rgba(16, 185, 129, 0.3)';
            state.isOllamaConnected = true;
        } else {
            statusText.textContent = 'Degraded';
            statusDot.style.background = 'var(--warning)';
            statusIndicator.style.background = 'rgba(245, 158, 11, 0.1)';
            statusIndicator.style.borderColor = 'rgba(245, 158, 11, 0.3)';
            state.isOllamaConnected = false;
        }
    } catch (error) {
        const statusIndicator = document.getElementById('statusIndicator');
        const statusText = statusIndicator.querySelector('.status-text');
        const statusDot = statusIndicator.querySelector('.status-dot');
        
        statusText.textContent = 'Offline';
        statusDot.style.background = 'var(--danger)';
        statusIndicator.style.background = 'rgba(239, 68, 68, 0.1)';
        statusIndicator.style.borderColor = 'rgba(239, 68, 68, 0.3)';
        state.isOllamaConnected = false;
    }
}

// Analytics
async function loadAnalytics() {
    try {
        const response = await fetch(`${API_BASE}/analytics/pyq`);
        const data = await response.json();
        
        document.getElementById('totalQuestions').textContent = data.total_questions;
        document.getElementById('topicCount').textContent = Object.keys(data.topic_distribution).length;
        
        const years = Object.keys(data.year_wise_trends);
        if (years.length > 0) {
            const minYear = Math.min(...years.map(Number));
            const maxYear = Math.max(...years.map(Number));
            document.getElementById('yearRange').textContent = `${minYear}-${maxYear}`;
        }
        
        // Display patterns
        const detailsDiv = document.getElementById('analyticsDetails');
        detailsDiv.innerHTML = '<h4 style="margin-bottom: 1rem; color: var(--text-primary);">📌 Key Patterns</h4>';
        
        if (data.patterns && data.patterns.length > 0) {
            data.patterns.forEach(pattern => {
                const patternDiv = document.createElement('div');
                patternDiv.style.padding = 'var(--spacing-md)';
                patternDiv.style.background = 'var(--bg-tertiary)';
                patternDiv.style.borderRadius = 'var(--radius-md)';
                patternDiv.style.marginBottom = 'var(--spacing-sm)';
                patternDiv.innerHTML = `
                    <strong>${pattern.topic}</strong>
                    <br>
                    <small style="color: var(--text-muted);">
                        Frequency: ${pattern.frequency} | 
                        Importance: ${(pattern.importance_score * 100).toFixed(0)}%
                    </small>
                `;
                detailsDiv.appendChild(patternDiv);
            });
        } else {
            detailsDiv.innerHTML += '<p style="color: var(--text-muted);">Upload PYQ documents to see analytics</p>';
        }
        
    } catch (error) {
        console.error('Failed to load analytics:', error);
    }
}

// Knowledge Graph
async function loadKnowledgeGraph() {
    try {
        const response = await fetch(`${API_BASE}/knowledge-graph`);
        const data = await response.json();
        
        const graphCanvas = document.getElementById('graphCanvas');
        const graphStats = document.getElementById('graphStats');
        
        if (data.nodes.length === 0) {
            graphCanvas.innerHTML = `
                <div class="graph-placeholder">
                    <div class="graph-placeholder-icon">🕸️</div>
                    <p>Knowledge graph will appear here</p>
                    <p class="graph-hint">Upload documents to generate the graph</p>
                </div>
            `;
            return;
        }
        
        // Simple text-based graph visualization
        graphCanvas.innerHTML = '';
        const graphList = document.createElement('div');
        graphList.style.padding = 'var(--spacing-lg)';
        graphList.style.maxHeight = '600px';
        graphList.style.overflowY = 'auto';
        
        data.edges.forEach(edge => {
            const edgeDiv = document.createElement('div');
            edgeDiv.style.padding = 'var(--spacing-sm)';
            edgeDiv.style.margin = 'var(--spacing-xs) 0';
            edgeDiv.style.background = 'var(--bg-tertiary)';
            edgeDiv.style.borderRadius = 'var(--radius-sm)';
            edgeDiv.style.borderLeft = '3px solid var(--primary)';
            edgeDiv.innerHTML = `
                <strong>${edge.source}</strong> 
                <span style="color: var(--primary);">→ ${edge.relationship} →</span> 
                <strong>${edge.target}</strong>
            `;
            graphList.appendChild(edgeDiv);
        });
        
        graphCanvas.appendChild(graphList);
        
        // Display stats
        graphStats.innerHTML = `
            <div class="graph-stat">Nodes: ${data.statistics.total_nodes}</div>
            <div class="graph-stat">Edges: ${data.statistics.total_edges}</div>
            <div class="graph-stat">Density: ${(data.statistics.density * 100).toFixed(2)}%</div>
        `;
        
    } catch (error) {
        console.error('Failed to load knowledge graph:', error);
    }
}

// Refresh graph button
document.getElementById('refreshGraph')?.addEventListener('click', loadKnowledgeGraph);

// Governance
async function loadGovernance() {
    try {
        // 1. Fetch the data from your API
        const statsResponse = await fetch(`${API_BASE}/governance/stats`);
        const stats = await statsResponse.json();
        
        // 2. GET THE CURRENT TRANSLATION (PASTE THIS)
        const t = translations[state.currentLanguage] || translations.en;
        
        const statsDiv = document.getElementById('governanceStats');
        
        // 3. UPDATE THE INNERHTML (REPLACE YOUR OLD HTML BLOCK WITH THIS)
        statsDiv.innerHTML = `
            <div class="analytics-card">
                <div class="analytics-icon">📄</div>
                <div class="analytics-value">${stats.total_documents}</div>
                <div class="analytics-label">${t.totalDocs}</div>
            </div>
            <div class="analytics-card">
                <div class="analytics-icon">⏳</div>
                <div class="analytics-value">${stats.pending_approval}</div>
                <div class="analytics-label">${t.pending}</div>
            </div>
            <div class="analytics-card">
                <div class="analytics-icon">✅</div>
                <div class="analytics-value">${stats.approved_documents}</div>
                <div class="analytics-label">${t.approved}</div>
            </div>
            <div class="analytics-card">
                <div class="analytics-icon">❌</div>
                <div class="analytics-value">${stats.rejected_documents}</div>
                <div class="analytics-label">${t.rejected}</div>
            </div>
            <div class="analytics-card">
                <div class="analytics-icon">💬</div>
                <div class="analytics-value">${stats.total_queries}</div>
                <div class="analytics-label">${t.totalQueries}</div>
            </div>
        `;
    
        // ... (rest of the function remains the same)
        //statsDiv.innerHTML = `
           // <div class="analytics-card">
                //<div class="analytics-icon">📄</div>
                //<div class="analytics-value">${stats.total_documents}</div>
                //<div class="analytics-label">Total Documents</div>
           // </div>
           // <div class="analytics-card">
                //<div class="analytics-icon">⏳</div>
                //<div class="analytics-value">${stats.pending_approval}</div>
                //<div class="analytics-label">Pending</div>
            //</div>
           // <div class="analytics-card">
                //<div class="analytics-icon">✅</div>
                //<div class="analytics-value">${stats.approved_documents}</div>
                //<div class="analytics-label">Approved</div>
            //</div>
            //<div class="analytics-card">
              //  <div class="analytics-icon">❌</div>
                //<div class="analytics-value">${stats.rejected_documents}</div>
               // <div class="analytics-label">Rejected</div>
            //</div>
            //<div class="analytics-card">
               // <div class="analytics-icon">💬</div>
                //<div class="analytics-value">${stats.total_queries}</div>
                //<div class="analytics-label">Total Queries</div>
           // </div>
        //`;
        
        // Load pending documents
        const pendingResponse = await fetch(`${API_BASE}/governance/pending`);
        const pendingData = await pendingResponse.json();
        
        const pendingList = document.getElementById('pendingList');
        pendingList.innerHTML = '';
        
        if (pendingData.documents.length === 0) {
            pendingList.innerHTML = '<p style="color: var(--text-muted);">No pending documents</p>';
        } else {
            pendingData.documents.forEach(doc => {
                const itemDiv = document.createElement('div');
                itemDiv.className = 'pending-item';
                itemDiv.innerHTML = `
                    <div>
                        <strong>${doc.filename}</strong>
                        <br>
                        <small style="color: var(--text-muted);">${new Date(doc.upload_date).toLocaleString()}</small>
                    </div>
                    <div class="pending-actions">
                        <button class="approve-btn" onclick="approveDocument('${doc.document_id}')">✓ Approve</button>
                        <button class="reject-btn" onclick="rejectDocument('${doc.document_id}')">✗ Reject</button>
                    </div>
                `;
                pendingList.appendChild(itemDiv);
            });
        }
        
    } catch (error) {
        console.error('Failed to load governance:', error);
    }
}

async function approveDocument(documentId) {
    try {
        const response = await fetch(`${API_BASE}/governance/approve`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                document_id: documentId,
                action: 'approve'
            })
        });
        
        if (response.ok) {
            loadGovernance(); // Reload
        }
    } catch (error) {
        console.error('Failed to approve document:', error);
    }
}

async function rejectDocument(documentId) {
    const reason = prompt('Reason for rejection:') || 'Not suitable';
    
    try {
        const response = await fetch(`${API_BASE}/governance/approve`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                document_id: documentId,
                action: 'reject',
                reason: reason
            })
        });
        
        if (response.ok) {
            loadGovernance(); // Reload
        }
    } catch (error) {
        console.error('Failed to reject document:', error);
    }
} 

// Make functions global for HTML onclick
window.approveDocument = approveDocument;
window.rejectDocument = rejectDocument;
    