/**
 * Career & Education Advisor - College Finder JavaScript
 * Handles college search, filtering, sorting, and interactive features
 */

class CollegeFinder {
    constructor() {
        this.colleges = [];
        this.filteredColleges = [];
        this.currentFilters = {
            search: '',
            state: '',
            type: '',
            fees: '',
            facilities: []
        };
        this.sortBy = 'name';
        this.sortOrder = 'asc';
        this.savedColleges = [];
        this.currentPage = 1;
        this.collegesPerPage = 10;

        this.init();
    }

    init() {
        this.loadSavedColleges();
        this.bindEvents();
        this.initializeSearch();
        this.setupInfiniteScroll();
        this.addAdvancedFilters();
        this.initializeComparisonMode();
    }

    bindEvents() {
        // Search input with debounce
        const searchInput = document.getElementById('search');
        if (searchInput) {
            let searchTimeout;
            searchInput.addEventListener('input', (e) => {
                clearTimeout(searchTimeout);
                searchTimeout = setTimeout(() => {
                    this.handleSearch(e.target.value);
                }, 300);
            });

            // Clear search button
            this.addClearSearchButton(searchInput);
        }

        // Filter dropdowns
        const stateSelect = document.getElementById('state');
        const typeSelect = document.getElementById('type');

        if (stateSelect) {
            stateSelect.addEventListener('change', (e) => {
                this.handleFilterChange('state', e.target.value);
            });
        }

        if (typeSelect) {
            typeSelect.addEventListener('change', (e) => {
                this.handleFilterChange('type', e.target.value);
            });
        }

        // Sort functionality
        this.addSortControls();

        // College card interactions
        document.addEventListener('click', (e) => {
            if (e.target.closest('[data-action="save"]')) {
                this.handleSaveCollege(e.target.closest('[data-action="save"]'));
            }
            if (e.target.closest('[data-action="compare"]')) {
                this.handleCompareCollege(e.target.closest('[data-action="compare"]'));
            }
            if (e.target.closest('[data-action="share"]')) {
                this.handleShareCollege(e.target.closest('[data-action="share"]'));
            }
            if (e.target.closest('[data-action="view-details"]')) {
                this.handleViewDetails(e.target.closest('[data-action="view-details"]'));
            }
        });

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            this.handleKeyboardShortcuts(e);
        });

        // Advanced filter toggles
        document.addEventListener('change', (e) => {
            if (e.target.classList.contains('facility-filter')) {
                this.handleFacilityFilter(e.target);
            }
            if (e.target.classList.contains('fees-filter')) {
                this.handleFeesFilter(e.target);
            }
        });
    }

    handleSearch(query) {
        this.currentFilters.search = query;
        this.applyFilters();
        this.updateURL();
        
        // Show search suggestions
        if (query.length > 2) {
            this.showSearchSuggestions(query);
        } else {
            this.hideSearchSuggestions();
        }
    }

    handleFilterChange(filterType, value) {
        this.currentFilters[filterType] = value;
        this.applyFilters();
        this.updateURL();
        this.showFilterFeedback(filterType, value);
    }

    applyFilters() {
        const cards = document.querySelectorAll('.college-card');
        let visibleCount = 0;

        cards.forEach(card => {
            const shouldShow = this.shouldShowCollege(card);
            
            if (shouldShow) {
                card.closest('.col-lg-6').style.display = 'block';
                visibleCount++;
            } else {
                card.closest('.col-lg-6').style.display = 'none';
            }
        });

        this.updateResultsCount(visibleCount);
        this.toggleNoResultsMessage(visibleCount === 0);
        
        // Animate visible cards
        this.animateVisibleCards();
    }

    shouldShowCollege(card) {
        const collegeName = card.querySelector('h5')?.textContent?.toLowerCase() || '';
        const collegeState = card.querySelector('[data-state]')?.getAttribute('data-state')?.toLowerCase() || '';
        const collegeType = card.querySelector('[data-type]')?.getAttribute('data-type')?.toLowerCase() || '';
        
        // Search filter
        if (this.currentFilters.search) {
            const searchTerm = this.currentFilters.search.toLowerCase();
            if (!collegeName.includes(searchTerm) && 
                !collegeState.includes(searchTerm) &&
                !collegeType.includes(searchTerm)) {
                return false;
            }
        }

        // State filter
        if (this.currentFilters.state && 
            collegeState !== this.currentFilters.state.toLowerCase()) {
            return false;
        }

        // Type filter
        if (this.currentFilters.type && 
            collegeType !== this.currentFilters.type.toLowerCase()) {
            return false;
        }

        return true;
    }

    addClearSearchButton(searchInput) {
        const clearBtn = document.createElement('button');
        clearBtn.type = 'button';
        clearBtn.className = 'btn-close position-absolute top-50 end-0 translate-middle-y me-3';
        clearBtn.style.display = 'none';
        clearBtn.addEventListener('click', () => {
            searchInput.value = '';
            this.handleSearch('');
            clearBtn.style.display = 'none';
        });

        searchInput.parentElement.style.position = 'relative';
        searchInput.parentElement.appendChild(clearBtn);

        searchInput.addEventListener('input', () => {
            clearBtn.style.display = searchInput.value ? 'block' : 'none';
        });
    }

    addSortControls() {
        const sortContainer = document.createElement('div');
        sortContainer.className = 'col-md-3';
        sortContainer.innerHTML = `
            <label class="form-label fw-semibold">Sort By</label>
            <select class="form-select" id="sortBy">
                <option value="name">College Name</option>
                <option value="state">State</option>
                <option value="type">Type</option>
                <option value="fees">Fees</option>
                <option value="seats">Available Seats</option>
            </select>
        `;

        const filterRow = document.querySelector('.filter-card .row');
        if (filterRow) {
            // Adjust existing columns
            const searchCol = filterRow.querySelector('.col-md-4');
            const stateCol = filterRow.querySelector('.col-md-3:first-of-type');
            const typeCol = filterRow.querySelector('.col-md-3:last-of-type');
            const buttonCol = filterRow.querySelector('.col-md-2');

            if (searchCol) searchCol.className = 'col-md-3';
            if (stateCol) stateCol.className = 'col-md-2';
            if (typeCol) typeCol.className = 'col-md-2';
            if (buttonCol) buttonCol.className = 'col-md-2';

            filterRow.insertBefore(sortContainer, buttonCol);

            // Bind sort functionality
            const sortSelect = document.getElementById('sortBy');
            if (sortSelect) {
                sortSelect.addEventListener('change', (e) => {
                    this.handleSort(e.target.value);
                });
            }
        }
    }

    handleSort(sortBy) {
        this.sortBy = sortBy;
        const cards = Array.from(document.querySelectorAll('.col-lg-6'));
        const parent = cards[0]?.parentElement;

        if (!parent) return;

        cards.sort((a, b) => {
            const cardA = a.querySelector('.college-card');
            const cardB = b.querySelector('.college-card');

            let valueA, valueB;

            switch (sortBy) {
                case 'name':
                    valueA = cardA.querySelector('h5')?.textContent || '';
                    valueB = cardB.querySelector('h5')?.textContent || '';
                    break;
                case 'state':
                    valueA = cardA.querySelector('[data-state]')?.getAttribute('data-state') || '';
                    valueB = cardB.querySelector('[data-state]')?.getAttribute('data-state') || '';
                    break;
                case 'type':
                    valueA = cardA.querySelector('[data-type]')?.getAttribute('data-type') || '';
                    valueB = cardB.querySelector('[data-type]')?.getAttribute('data-type') || '';
                    break;
                case 'fees':
                    valueA = this.extractNumericValue(cardA.querySelector('[data-fees]')?.getAttribute('data-fees') || '0');
                    valueB = this.extractNumericValue(cardB.querySelector('[data-fees]')?.getAttribute('data-fees') || '0');
                    break;
                case 'seats':
                    valueA = parseInt(cardA.querySelector('[data-seats]')?.getAttribute('data-seats') || '0');
                    valueB = parseInt(cardB.querySelector('[data-seats]')?.getAttribute('data-seats') || '0');
                    break;
                default:
                    return 0;
            }

            if (typeof valueA === 'string') {
                return valueA.localeCompare(valueB);
            }
            return valueA - valueB;
        });

        // Re-append sorted cards
        cards.forEach(card => parent.appendChild(card));
        this.animateVisibleCards();
    }

    extractNumericValue(feeString) {
        const matches = feeString.match(/[\d,]+/g);
        if (matches) {
            return parseInt(matches[0].replace(/,/g, ''));
        }
        return 0;
    }

    showSearchSuggestions(query) {
        const suggestions = this.generateSuggestions(query);
        if (suggestions.length === 0) return;

        let suggestionContainer = document.getElementById('searchSuggestions');
        if (!suggestionContainer) {
            suggestionContainer = document.createElement('div');
            suggestionContainer.id = 'searchSuggestions';
            suggestionContainer.className = 'dropdown-menu show position-absolute w-100 mt-1';
            suggestionContainer.style.zIndex = '1050';
            
            const searchInput = document.getElementById('search');
            searchInput.parentElement.appendChild(suggestionContainer);
        }

        suggestionContainer.innerHTML = suggestions.map(suggestion => `
            <button class="dropdown-item" type="button" data-suggestion="${suggestion}">
                <i data-feather="search" class="me-2" style="width: 16px; height: 16px;"></i>
                ${suggestion}
            </button>
        `).join('');

        if (window.feather) feather.replace();

        // Bind suggestion clicks
        suggestionContainer.addEventListener('click', (e) => {
            if (e.target.classList.contains('dropdown-item')) {
                const suggestion = e.target.getAttribute('data-suggestion');
                document.getElementById('search').value = suggestion;
                this.handleSearch(suggestion);
                this.hideSearchSuggestions();
            }
        });
    }

    generateSuggestions(query) {
        const suggestions = new Set();
        const cards = document.querySelectorAll('.college-card');

        cards.forEach(card => {
            const name = card.querySelector('h5')?.textContent || '';
            const state = card.querySelector('[data-state]')?.getAttribute('data-state') || '';
            const type = card.querySelector('[data-type]')?.getAttribute('data-type') || '';

            [name, state, type].forEach(text => {
                if (text.toLowerCase().includes(query.toLowerCase()) && text !== query) {
                    suggestions.add(text);
                }
            });
        });

        return Array.from(suggestions).slice(0, 5);
    }

    hideSearchSuggestions() {
        const suggestionContainer = document.getElementById('searchSuggestions');
        if (suggestionContainer) {
            suggestionContainer.remove();
        }
    }

    handleSaveCollege(button) {
        const collegeId = button.getAttribute('data-college-id');
        if (!collegeId) return;

        let saved = this.savedColleges.includes(collegeId);
        
        if (saved) {
            // Remove from saved
            this.savedColleges = this.savedColleges.filter(id => id !== collegeId);
            button.innerHTML = '<i data-feather="bookmark" class="me-1" style="width: 14px; height: 14px;"></i>Save';
            button.classList.remove('btn-success');
            button.classList.add('btn-outline-secondary');
        } else {
            // Add to saved
            this.savedColleges.push(collegeId);
            button.innerHTML = '<i data-feather="check" class="me-1" style="width: 14px; height: 14px;"></i>Saved';
            button.classList.remove('btn-outline-secondary');
            button.classList.add('btn-success');
        }

        this.updateSavedColleges();
        if (window.feather) feather.replace();

        // Show feedback
        this.showToast(saved ? 'College removed from saved list' : 'College saved successfully', 'success');
    }

    loadSavedColleges() {
        try {
            const saved = localStorage.getItem('savedColleges');
            this.savedColleges = saved ? JSON.parse(saved) : [];
            
            // Update UI for saved colleges
            this.savedColleges.forEach(collegeId => {
                const button = document.querySelector(`[data-college-id="${collegeId}"]`);
                if (button && button.getAttribute('data-action') === 'save') {
                    button.innerHTML = '<i data-feather="check" class="me-1" style="width: 14px; height: 14px;"></i>Saved';
                    button.classList.remove('btn-outline-secondary');
                    button.classList.add('btn-success');
                }
            });
        } catch (e) {
            console.warn('Failed to load saved colleges:', e);
        }
    }

    updateSavedColleges() {
        try {
            localStorage.setItem('savedColleges', JSON.stringify(this.savedColleges));
            this.updateSavedCounter();
        } catch (e) {
            console.warn('Failed to save colleges list:', e);
        }
    }

    updateSavedCounter() {
        let counter = document.getElementById('savedCounter');
        if (!counter && this.savedColleges.length > 0) {
            counter = document.createElement('span');
            counter.id = 'savedCounter';
            counter.className = 'badge bg-success ms-2';
            
            const navLink = document.querySelector('a[href*="saved"]');
            if (navLink) {
                navLink.appendChild(counter);
            }
        }
        
        if (counter) {
            counter.textContent = this.savedColleges.length;
            counter.style.display = this.savedColleges.length > 0 ? 'inline' : 'none';
        }
    }

    handleShareCollege(button) {
        const collegeName = button.closest('.college-card').querySelector('h5')?.textContent;
        const collegeUrl = window.location.href;

        if (navigator.share) {
            navigator.share({
                title: collegeName,
                text: `Check out ${collegeName} - found on Career & Education Advisor`,
                url: collegeUrl
            }).catch(err => console.log('Error sharing:', err));
        } else {
            // Fallback: copy to clipboard
            const shareText = `${collegeName} - ${collegeUrl}`;
            navigator.clipboard.writeText(shareText).then(() => {
                this.showToast('College information copied to clipboard!', 'success');
            }).catch(() => {
                // Manual copy fallback
                this.showShareModal(collegeName, collegeUrl);
            });
        }
    }

    showShareModal(collegeName, collegeUrl) {
        const modal = document.createElement('div');
        modal.className = 'modal fade';
        modal.innerHTML = `
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Share ${collegeName}</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <p>Copy this link to share:</p>
                        <div class="input-group">
                            <input type="text" class="form-control" value="${collegeUrl}" readonly>
                            <button class="btn btn-outline-secondary" type="button" onclick="this.previousElementSibling.select(); document.execCommand('copy');">Copy</button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        new bootstrap.Modal(modal).show();
        
        modal.addEventListener('hidden.bs.modal', () => {
            modal.remove();
        });
    }

    handleViewDetails(button) {
        const card = button.closest('.college-card');
        const details = this.extractCollegeDetails(card);
        this.showDetailsModal(details);
    }

    extractCollegeDetails(card) {
        return {
            name: card.querySelector('h5')?.textContent || '',
            state: card.querySelector('[data-state]')?.getAttribute('data-state') || '',
            type: card.querySelector('[data-type]')?.getAttribute('data-type') || '',
            courses: Array.from(card.querySelectorAll('.badge')).map(badge => badge.textContent),
            facilities: Array.from(card.querySelectorAll('.facility-icon + small')).map(item => item.textContent),
            website: card.querySelector('a[href*="http"]')?.href || ''
        };
    }

    showDetailsModal(details) {
        const modal = document.createElement('div');
        modal.className = 'modal fade';
        modal.innerHTML = `
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">${details.name}</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="row g-4">
                            <div class="col-md-6">
                                <h6>Location</h6>
                                <p>${details.state}</p>
                                
                                <h6>Type</h6>
                                <p>${details.type}</p>
                            </div>
                            <div class="col-md-6">
                                <h6>Available Courses</h6>
                                <div class="d-flex flex-wrap gap-2">
                                    ${details.courses.map(course => `<span class="badge bg-primary">${course}</span>`).join('')}
                                </div>
                            </div>
                            <div class="col-12">
                                <h6>Facilities</h6>
                                <div class="row">
                                    ${details.facilities.map(facility => `
                                        <div class="col-md-6">
                                            <div class="d-flex align-items-center mb-2">
                                                <i data-feather="check-circle" class="text-success me-2" style="width: 16px; height: 16px;"></i>
                                                <small>${facility}</small>
                                            </div>
                                        </div>
                                    `).join('')}
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        ${details.website ? `<a href="${details.website}" target="_blank" class="btn btn-primary">Visit Website</a>` : ''}
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        const bootstrapModal = new bootstrap.Modal(modal);
        bootstrapModal.show();
        
        if (window.feather) feather.replace();
        
        modal.addEventListener('hidden.bs.modal', () => {
            modal.remove();
        });
    }

    updateResultsCount(count) {
        let resultsElement = document.querySelector('.results-count');
        if (!resultsElement) {
            resultsElement = document.querySelector('h5[class*="mb-0"]');
        }
        
        if (resultsElement) {
            resultsElement.textContent = `Found ${count} college${count !== 1 ? 's' : ''}`;
        }
    }

    toggleNoResultsMessage(show) {
        let noResults = document.getElementById('noResults');
        
        if (show && !noResults) {
            noResults = document.createElement('div');
            noResults.id = 'noResults';
            noResults.className = 'no-results text-center py-5';
            noResults.innerHTML = `
                <i data-feather="search" class="text-muted mb-3" style="width: 64px; height: 64px;"></i>
                <h4 class="text-muted">No colleges found</h4>
                <p class="text-muted">Try adjusting your search criteria or filters.</p>
                <button class="btn btn-primary" onclick="collegeFinder.clearAllFilters()">
                    <i data-feather="refresh-cw" class="me-2"></i>
                    Clear All Filters
                </button>
            `;
            
            const resultsContainer = document.querySelector('.row.g-4');
            if (resultsContainer) {
                resultsContainer.parentElement.appendChild(noResults);
            }
            
            if (window.feather) feather.replace();
        }
        
        if (noResults) {
            noResults.style.display = show ? 'block' : 'none';
        }
    }

    animateVisibleCards() {
        const visibleCards = document.querySelectorAll('.col-lg-6[style*="block"] .college-card');
        visibleCards.forEach((card, index) => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            
            setTimeout(() => {
                card.style.transition = 'all 0.4s ease';
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, index * 100);
        });
    }

    clearAllFilters() {
        // Reset form inputs
        const searchInput = document.getElementById('search');
        const stateSelect = document.getElementById('state');
        const typeSelect = document.getElementById('type');
        
        if (searchInput) searchInput.value = '';
        if (stateSelect) stateSelect.value = '';
        if (typeSelect) typeSelect.value = '';
        
        // Reset internal filters
        this.currentFilters = {
            search: '',
            state: '',
            type: '',
            fees: '',
            facilities: []
        };
        
        // Apply cleared filters
        this.applyFilters();
        this.updateURL();
        
        this.showToast('All filters cleared', 'info');
    }

    updateURL() {
        const params = new URLSearchParams();
        
        if (this.currentFilters.search) params.set('search', this.currentFilters.search);
        if (this.currentFilters.state) params.set('state', this.currentFilters.state);
        if (this.currentFilters.type) params.set('type', this.currentFilters.type);
        
        const newUrl = window.location.pathname + (params.toString() ? '?' + params.toString() : '');
        window.history.replaceState(null, '', newUrl);
    }

    handleKeyboardShortcuts(e) {
        if (e.ctrlKey || e.metaKey) {
            switch (e.key) {
                case 'f':
                    e.preventDefault();
                    document.getElementById('search')?.focus();
                    break;
                case 'k':
                    e.preventDefault();
                    this.clearAllFilters();
                    break;
            }
        }
    }

    showToast(message, type = 'info') {
        const colors = {
            info: '#2563eb',
            success: '#16a34a',
            warning: '#f59e0b',
            error: '#dc2626'
        };

        const toast = document.createElement('div');
        toast.className = 'toast-notification';
        toast.innerHTML = `
            <div class="d-flex align-items-center">
                <i data-feather="${type === 'success' ? 'check-circle' : type === 'error' ? 'x-circle' : 'info'}" class="me-2"></i>
                <span>${message}</span>
            </div>
        `;
        toast.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${colors[type] || colors.info};
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            z-index: 1050;
            opacity: 0;
            transform: translateX(100%);
            transition: all 0.3s ease;
            max-width: 300px;
        `;

        document.body.appendChild(toast);
        if (window.feather) feather.replace();

        setTimeout(() => {
            toast.style.opacity = '1';
            toast.style.transform = 'translateX(0)';
        }, 100);

        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateX(100%)';
            setTimeout(() => {
                if (toast.parentNode) {
                    toast.remove();
                }
            }, 300);
        }, 3000);
    }

    // Initialize comparison mode
    initializeComparisonMode() {
        this.comparisonList = [];
        this.addComparisonUI();
    }

    addComparisonUI() {
        const comparisonContainer = document.createElement('div');
        comparisonContainer.id = 'comparisonContainer';
        comparisonContainer.className = 'comparison-container';
        comparisonContainer.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: white;
            border-radius: 12px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
            padding: 1rem;
            z-index: 1040;
            display: none;
            max-width: 300px;
        `;
        
        document.body.appendChild(comparisonContainer);
    }
}

// Helper Functions
const CollegeFinderHelpers = {
    formatFees(feesString) {
        // Convert fees to a standardized format
        const numbers = feesString.match(/[\d,]+/g);
        if (numbers && numbers.length > 0) {
            const fee = parseInt(numbers[0].replace(/,/g, ''));
            if (fee < 100000) {
                return `₹${(fee / 1000).toFixed(0)}K`;
            } else {
                return `₹${(fee / 100000).toFixed(1)}L`;
            }
        }
        return feesString;
    },

    truncateText(text, maxLength) {
        if (text.length <= maxLength) return text;
        return text.substr(0, maxLength - 3) + '...';
    },

    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
};

// Global functions for template compatibility
function clearFilters() {
    if (window.collegeFinder) {
        window.collegeFinder.clearAllFilters();
    }
}

function saveCollege(collegeId) {
    const button = document.querySelector(`[data-college-id="${collegeId}"][data-action="save"]`);
    if (button && window.collegeFinder) {
        window.collegeFinder.handleSaveCollege(button);
    }
}

function shareCollege(collegeName) {
    const button = document.querySelector(`[data-college-name="${collegeName}"][data-action="share"]`);
    if (button && window.collegeFinder) {
        window.collegeFinder.handleShareCollege(button);
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Only initialize on college finder pages
    if (document.querySelector('.college-card')) {
        window.collegeFinder = new CollegeFinder();
    }
});

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { CollegeFinder, CollegeFinderHelpers };
}
