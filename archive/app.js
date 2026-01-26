
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

        // Tab content mapping for entry display
        const TAB_CONTENT_MAP = {
            etymology: 'etymology',
            contemporary: 'contemporary',
            somatic: 'somatic',
            cultural: 'cultural'
        };

        // ============================================
        // VIEW MANAGEMENT
        // ============================================

        function switchView(viewName) {
            // Hide all views
            document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
            
            // Remove active from all nav items
            document.querySelectorAll('nav a').forEach(a => a.classList.remove('active'));
            
            // Show selected view
            document.getElementById(viewName).classList.add('active');
            
            // Add active to nav item
            document.getElementById('nav-' + viewName).classList.add('active');

            // Load content if needed
            if (viewName === 'wotd') {
                loadWordOfDay();
            }

            // Scroll to top
            window.scrollTo(0, 0);
        }

        // ============================================
        // TAB FUNCTIONALITY
        // ============================================

        function setupTabListeners() {
            document.querySelectorAll('.tab-button').forEach(button => {
                button.addEventListener('click', () => {
                    const tabName = button.dataset.tab;
                    switchTab(tabName);
                });
            });
        }

        function switchTab(tabName) {
            // Remove active from all tabs
            document.querySelectorAll('.tab-button').forEach(btn => btn.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
            
            // Add active to selected tab
            document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
            document.getElementById(tabName).classList.add('active');
        }

        // ============================================
        // WORD OF THE DAY LOADING
        // ============================================

        async function loadWordOfDay() {
            try {
                const response = await fetch(`${API_BASE_URL}/word-of-day`);
                const data = await response.json();

                if (data.status === 'success') {
                    const word = data.word;
                    document.getElementById('wotd-word').textContent = word.word || 'Unknown';
                    document.getElementById('wotd-category').textContent = word.category || '—';
                    document.getElementById('wotd-precision').textContent = word.precisionLevel || '—';
                    document.getElementById('wotd-total').textContent = (data.totalWords || 0).toLocaleString();
                    
                    // Update tab content
                    document.getElementById('etymology-content').textContent = word.etymology || 'Explore the roots and evolution of this word across cultures and centuries.';
                    document.getElementById('contemporary-content').textContent = word.contemporary || 'How this word is understood and used in modern communication.';
                    document.getElementById('somatic-content').textContent = word.somaticIntegration || '—';
                    document.getElementById('cultural-content').textContent = word.culturalBridge || '—';

                    // Update date
                    const date = new Date(data.date).toLocaleDateString('en-US', {
                        weekday: 'long',
                        year: 'numeric',
                        month: 'long',
                        day: 'numeric'
                    });
                    document.getElementById('wotd-date').textContent = date;
                } else {
                    showError('Failed to load word of the day');
                }
            } catch (error) {
                console.error('Error loading word of day:', error);
                showError('Error loading word of the day. Please try again.');
            }
        }

        // ============================================
        // RANDOM WORD LOADING
        // ============================================

        async function loadRandomWord() {
            try {
                const response = await fetch(`${API_BASE_URL}/word/random`);
                const data = await response.json();

                if (data.status === 'success') {
                    loadWordOfDay(); // Reload to show new word
                } else {
                    showError('Failed to load random word');
                }
            } catch (error) {
                console.error('Error loading random word:', error);
                showError('Error loading random word. Please try again.');
            }
        }

        // ============================================
        // SEARCH FUNCTIONALITY
        // ============================================

        async function performSearch() {
            const query = document.getElementById('search-input').value.trim();
            
            if (!query) {
                showError('Please enter a search term');
                return;
            }

            try {
                const resultsDiv = document.getElementById('search-results');
                const resultsList = document.getElementById('results-list');
                
                resultsList.innerHTML = '<div class="loading"><div class="spinner"></div><p>Searching...</p></div>';
                resultsDiv.style.display = 'block';

                const response = await fetch(`${API_BASE_URL}/search?q=${encodeURIComponent(query)}`);
                const data = await response.json();

                if (data.status === 'success' && data.results && data.results.length > 0) {
                    const resultsHTML = data.results.map(result => `
                        <div class="result-item" onclick="loadWordFromSearch('${result.word}')">
                            <div class="result-word">${result.word}</div>
                            <span class="result-category">${result.category || 'Uncategorized'}</span>
                            <p class="result-description">${result.definition || 'No description available'}</p>
                        </div>
                    `).join('');
                    
                    resultsList.innerHTML = resultsHTML;
                } else {
                    resultsList.innerHTML = `
                        <div class="no-results">
                            <p>No words found matching "${query}"</p>
                            <p style="font-size: 0.95rem;">Try searching by category name (e.g., Joy, Fear) or word fragment.</p>
                        </div>
                    `;
                }
            } catch (error) {
                console.error('Search error:', error);
                document.getElementById('results-list').innerHTML = '<div class="error">Search unavailable. Please try again.</div>';
                document.getElementById('search-results').style.display = 'block';
            }
        }

        // ============================================
        // LOAD WORD FROM SEARCH RESULT
        // ============================================

        async function loadWordFromSearch(wordName) {
            try {
                const response = await fetch(`${API_BASE_URL}/word/${encodeURIComponent(wordName)}`);
                const data = await response.json();

                if (data.status === 'success') {
                    const word = data.word;
                    
                    // Update word of day section with searched word
                    document.getElementById('wotd-word').textContent = word.word || 'Unknown';
                    document.getElementById('wotd-category').textContent = word.category || '—';
                    document.getElementById('wotd-precision').textContent = word.precisionLevel || '—';
                    
                    // Update tab content
                    document.getElementById('etymology-content').textContent = word.etymology || 'Content not available';
                    document.getElementById('contemporary-content').textContent = word.contemporary || 'Content not available';
                    document.getElementById('somatic-content').textContent = word.somaticIntegration || '—';
                    document.getElementById('cultural-content').textContent = word.culturalBridge || '—';

                    // Switch to WOTD view to display full entry
                    switchView('wotd');
                    
                    // Scroll to top
                    window.scrollTo(0, 0);
                } else {
                    showError('Failed to load word details');
                }
            } catch (error) {
                console.error('Error loading word:', error);
                showError('Error loading word details. Please try again.');
            }
        }

        // ============================================
        // UTILITY FUNCTIONS
        // ============================================

        function showError(message) {
            console.error(message);
            alert(message);
        }

        // ============================================
        // INITIALIZATION
        // ============================================

        document.addEventListener('DOMContentLoaded', () => {
            setupTabListeners();
            
            // Add Enter key support for search
            document.getElementById('search-input').addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    performSearch();
                }
            });

            console.log('EFV Application Initialized');
            console.log('API Endpoint:', API_BASE_URL);
        });
    