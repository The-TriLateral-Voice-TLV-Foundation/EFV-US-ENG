
// ============================================
// GLOBAL STATE
// ============================================
let currentWord = null;
let entryData = null;
let activeTab = 'etymology';
const API_BASE_URL = 'https://efv-us-eng.onrender.com/api/v1';

// Section mapping
const SECTIONMAP = {
    'etymology': '1. Etymology & Historical Development',
    'contemporary': '2. Contemporary Common Usage',
    'evocation': '3. Precise Evocation Intent',
    'conceptual': '4. Conceptual Explanation',
    'cultural': '5. Cultural Translation Contexts',
    'tlv': '6. TLV Protocol Application',
    'somatic': '7. Somatic Signature Documentation'
};



// ============ Initialization ============
document.addEventListener('DOMContentLoaded', init);
async function init() {
    try {
        setupTabListeners();

        const urlParams = new URLSearchParams(window.location.search);
        const word = urlParams.get('word');

        if (word) {
            await loadWord(word);
        } else {
            await loadRandomWord();
        }
    } catch (error) {
        showError(`Failed to initialize: ${error.message}`);
    }
}

function setupTabListeners() {
    document.querySelectorAll('.tab-button').forEach(button => {
        button.addEventListener('click', () => {
            const tab = button.dataset.tab;
            switchTab(tab);
        });
    });
}
function findSectionByNumber(children, n) {
const prefix = `${n}.`;
return (children || []).find(c => (c.title || '').trim().startsWith(prefix));
}
// ============ Data Loading ============
async function loadWord(wordName) {
    try {
        showLoading();
        const response = await fetch(`${API_BASE_URL}/word/${wordName.toUpperCase()}`);

        if (!response.ok) {
            throw new Error(`Word not found: ${wordName}`);
        }

        const data = await response.json();
        if (data.status !== 'success') {
            throw new Error(data.message || 'Failed to load word');
        }

        entryData = data.data;
        currentWord = wordName.toUpperCase();

        // Update URL without reload
        window.history.replaceState({}, '', `?word=${currentWord}`);

        renderEntry();
    } catch (error) {
        showError(error.message);
    }
}

async function loadRandomWord() {
    try {
        showLoading();
        const response = await fetch(`${API_BASE_URL}/word/random`);

        if (!response.ok) {
            throw new Error('Failed to load random word');
        }

        const data = await response.json();
        if (data.status !== 'success') {
            throw new Error(data.message || 'Failed to load word');
        }

        await loadWord(data.word);
    } catch (error) {
        showError(error.message);
    }
}

function goBack() {
    if (window.history.length > 1) {
        window.history.back();
    } else {
        window.location.href = 'index.html';
    }
}



// ============ Rendering ============
function renderEntry() {
    // Update header
    document.getElementById('entryTitle').textContent = entryData.word || 'UNKNOWN';
    document.getElementById('entryCategory').textContent = entryData.category;
    
    // Update metadata
    const precisionEl = document.getElementById('precisionLevel');
    precisionEl.textContent = entryData.precisionLevel;
    precisionEl.className = `meta-value ${entryData.precisionLevel?.toLowerCase()}`;
    
    const somaticEl = document.getElementById('somaticIntegration');
    somaticEl.textContent = entryData.somaticIntegration;
    somaticEl.className = `meta-value ${entryData.somaticIntegration?.toLowerCase()}`;
    
    const culturalEl = document.getElementById('culturalBridge');
    culturalEl.textContent = entryData.culturalBridge;
    culturalEl.className = `meta-value ${entryData.culturalBridge?.toLowerCase()}`;
    
    const temporalEl = document.getElementById('temporalTranslation');
    temporalEl.textContent = entryData.temporalTranslation;
    temporalEl.className = `meta-value ${entryData.temporalTranslation?.toLowerCase()}`;
    
    // Update page title
    document.title = `${entryData.word} - EFV Entry`;
    
    // DEBUG: Log the ENTIRE entryData structure
    console.log('===== FULL ENTRY DATA =====');
    console.log(JSON.stringify(entryData, null, 2));
    console.log('===== OBJECT KEYS =====');
    console.log(Object.keys(entryData));
    
    // Render all tabs
    renderAllTabs();
    
    // Show first tab
    switchTab('etymology');
}

function renderAllTabs() {
    const container = document.getElementById('tabContent');
    container.innerHTML = '';
    
    console.log('===== RENDERING ALL TABS =====');
    console.log('Full Entry Data:', entryData);
    
    const children = entryData.children || [];
    const tabIds = Object.keys(SECTIONMAP);
    
    console.log(`Found ${children.length} child sections`);
    console.log(`Expected ${tabIds.length} tabs`);
    
    // ✅ FIXED: Direct array indexing instead of searching
    tabIds.forEach((tabId, index) => {
        const tabContent = document.createElement('div');
        tabContent.className = 'tab-content';
        tabContent.id = `tab-${tabId}`;
        tabContent.dataset.tab = tabId;
        
        // Direct access to children array
        const sectionData = children[index];
        const sectionTitle = SECTIONMAP[tabId];
        
        console.log(`Tab ${index} (${tabId}):`, sectionData ? 'FOUND' : 'NOT FOUND');
        
        if (sectionData && sectionData.content) {
            // Section found and has content
            tabContent.innerHTML = renderSectionContent({
                title: sectionTitle,
                content: sectionData.content
            });
            console.log(`  ✓ Rendered with content from: "${sectionData.title}"`);
        } else {
            // Section not found - show placeholder
            tabContent.innerHTML = `
                <div class="section-card">
                    <h3>${sectionTitle}</h3>
                    <p>Content not available for this section.</p>
                </div>
            `;
            console.log(`  ✗ Content not available`);
        }
        
        container.appendChild(tabContent);
    });
    
    console.log('===== TAB RENDERING COMPLETE =====');
}

function renderSectionContent(section) {
    const content = parseMarkdownContent(section.content);
    return `
        <div class="section-card">
            <h3>${section.title}</h3>
            ${content}
        </div>
    `;
}

function parseMarkdownContent(text) {
    if (!text) return '<p>No content available.</p>';

    const lines = text.split('\n');
    let html = '';
    let currentList = null;
    let inBlockquote = false;

    lines.forEach(line => {
        line = line.trim();
        if (!line) {
            if (currentList) {
                html += '</ul>';
                currentList = null;
            }
            return;
        }

        // Blockquotes
        if (line.startsWith('>')) {
            if (!inBlockquote) {
                html += '<blockquote>';
                inBlockquote = true;
            }
            html += formatInlineMarkdown(line.substring(1).trim()) + ' ';
            return;
        } else if (inBlockquote) {
            html += '</blockquote>';
            inBlockquote = false;
        }

        // Cultural bridges
        if (line.includes('⇄') || line.includes('Bridge')) {
            if (currentList) {
                html += '</ul>';
                currentList = null;
            }
            html += `<div class="cultural-bridge"><div class="bridge-label">Cultural Bridge</div><div class="bridge-content">${formatInlineMarkdown(line)}</div></div>`;
            return;
        }

        // Subsection headers WITH content (- **Label**: content here)
        if (line.startsWith('- **') && line.includes('**:')) {
            if (currentList) {
                html += '</ul>';
                currentList = null;
            }
            
            // Extract label and content
            const match = line.match(/- \*\*([^*]+)\*\*:\s*(.*)/);
            if (match) {
                const label = match[1];
                const content = match[2];
                
                html += `<div class="subsection"><div class="subsection-title">${label}</div>`;
                
                // If there's content after the colon, render it
                if (content) {
                    html += `<p>${formatInlineMarkdown(content)}</p>`;
                }
                html += `</div>`;
            }
            return;
        }

        // List items
        if (line.startsWith('- ') || line.startsWith('* ')) {
            if (!currentList) {
                html += '<ul>';
                currentList = 'ul';
            }
            const listContent = line.substring(2);
            html += `<li>${formatInlineMarkdown(listContent)}</li>`;
            return;
        }

        // Regular paragraphs
        if (currentList) {
            html += '</ul>';
            currentList = null;
        }
        html += `<p>${formatInlineMarkdown(line)}</p>`;
    });

    if (currentList) html += '</ul>';
    if (inBlockquote) html += '</blockquote>';

    return html;
}

function formatInlineMarkdown(text) {
    return text
        .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
        .replace(/\*([^*]+)\*/g, '<em>$1</em>')
        .replace(/`([^`]+)`/g, '<code>$1</code>');
}

// ============ Tab Switching ============
function switchTab(tabId) {
    activeTab = tabId;

    // Update tab buttons
    document.querySelectorAll('.tab-button').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.tab === tabId);
    });

    // Update tab content
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.toggle('active', content.dataset.tab === tabId);
    });
}

// ============ UI States ============
function showLoading() {
    document.getElementById('tabContent').innerHTML = `
        <div class="loading">
            <div class="spinner"></div>
            <p>Loading entry...</p>
        </div>
    `;
}

function showError(message) {
    document.getElementById('tabContent').innerHTML = `
        <div class="error">
            <strong>Error:</strong> ${message}
        </div>
    `;
}

// ============================================
// API FUNCTIONS
// ============================================
async function performSearch() {
    const query = document.getElementById('searchInput').value.trim();
    if (!query) return;

    try {
        const response = await fetch(`${API_BASE_URL}/search?q=${encodeURIComponent(query)}`);
        if (!response.ok) throw new Error('Search failed');
        const data = await response.json();
        
        if (data.results && data.results.length > 0) {
            // Load the first result
            displayWord(data.results[0]);
        } else {
            showError('No results found for your search.');
        }
    } catch (error) {
        console.error('Error searching:', error);
        showError('Search failed. Please try again.');
    }
}

// ============================================
// DISPLAY FUNCTIONS
// ============================================
function displayWord(wordData) {
    currentWord = wordData;

    // Update header
    document.getElementById('entryTitle').textContent = wordData.word || 'Unknown';
    document.getElementById('entryCategory').textContent = wordData.category || '—';

    // Update metadata
    document.getElementById('precisionLevel').textContent = wordData.precision_level || '—';
    document.getElementById('somaticIntegration').textContent = wordData.somatic_integration || '—';
    document.getElementById('culturalBridge').textContent = wordData.cultural_bridge || '—';
    document.getElementById('temporalTranslation').textContent = wordData.temporal_translation || '—';

    // Build tab content
    buildTabContent(wordData);

    // Show entry header
    document.getElementById('entryHeader').classList.add('active');

    // Scroll to entry
    setTimeout(() => {
        document.getElementById('entryHeader').scrollIntoView({ behavior: 'smooth' });
    }, 100);
}

// ============================================
// NAVIGATION FUNCTIONS
// ============================================
function goHome() {
    window.location.hash = '#home';
    window.scrollTo(0, 0);
}

function goBack() {
    if (window.history.length > 1) {
        window.history.back();
    } else {
        window.location.href = 'index.html';
    }
}

function scrollToSection(sectionId) {
    const element = document.getElementById(sectionId);
    if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
    }
}

function filterCategory(category) {
    // Placeholder for category filtering
    document.getElementById('searchInput').value = `category:${category}`;
    performSearch();
}

// ============ Start ============
document.addEventListener('DOMContentLoaded', init);
