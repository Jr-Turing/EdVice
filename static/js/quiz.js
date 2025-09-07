/**
 * Career & Education Advisor - Quiz JavaScript
 * Handles quiz interactions, progress tracking, and user experience enhancements
 */

class QuizManager {
    constructor() {
        this.currentQuestion = 1;
        this.totalQuestions = 20;
        this.selectedAnswer = null;
        this.timeSpent = 0;
        this.startTime = Date.now();
        this.answers = {};
        
        this.init();
    }

    init() {
        this.bindEvents();
        this.loadProgress();
        this.startTimer();
        this.initializeAccessibility();
    }

    bindEvents() {
        // Option selection events
        document.addEventListener('click', (e) => {
            if (e.target.closest('.option-btn')) {
                this.selectOption(e.target.closest('.option-btn'));
            }
        });

        // Yes/No button events
        document.addEventListener('click', (e) => {
            if (e.target.closest('.yes-no-btn')) {
                this.selectYesNo(e.target.closest('.yes-no-btn'));
            }
        });

        // Likert scale events
        document.addEventListener('change', (e) => {
            if (e.target.type === 'radio' && e.target.name === 'answer') {
                this.selectLikert(e.target);
            }
        });

        // Keyboard navigation
        document.addEventListener('keydown', (e) => {
            this.handleKeyboardNavigation(e);
        });

        // Form submission
        const quizForm = document.getElementById('quizForm');
        if (quizForm) {
            quizForm.addEventListener('submit', (e) => {
                this.handleSubmit(e);
            });
        }

        // Auto-save functionality
        setInterval(() => {
            this.autoSave();
        }, 30000); // Auto-save every 30 seconds
    }

    selectOption(button) {
        // Remove selected state from all options
        document.querySelectorAll('.option-btn').forEach(btn => {
            btn.classList.remove('selected');
            const icon = btn.querySelector('.option-icon');
            if (icon) {
                icon.setAttribute('data-feather', 'circle');
            }
        });

        // Add selected state to clicked option
        button.classList.add('selected');
        const icon = button.querySelector('.option-icon');
        if (icon) {
            icon.setAttribute('data-feather', 'check-circle');
        }

        // Get the answer value
        const answerValue = button.getAttribute('data-value') || 
                           button.querySelector('[data-value]')?.getAttribute('data-value');
        
        if (answerValue) {
            this.selectedAnswer = answerValue;
            this.updateHiddenInput('selectedAnswer', answerValue);
            this.enableNextButton();
        }

        // Re-render feather icons
        if (window.feather) {
            feather.replace();
        }

        // Add visual feedback
        this.addFeedback(button);
    }

    selectYesNo(button) {
        // Remove active state from both buttons
        document.querySelectorAll('.yes-no-btn').forEach(btn => {
            btn.classList.remove('btn-success', 'btn-danger', 'selected');
            if (btn.textContent.trim().toLowerCase() === 'yes') {
                btn.classList.add('btn-outline-success');
                btn.classList.remove('btn-outline-danger');
            } else {
                btn.classList.add('btn-outline-danger');
                btn.classList.remove('btn-outline-success');
            }
        });

        // Add active state to selected button
        const isYes = button.textContent.trim().toLowerCase() === 'yes';
        const answer = isYes ? 'yes' : 'no';
        
        button.classList.add('selected');
        if (isYes) {
            button.classList.remove('btn-outline-success');
            button.classList.add('btn-success');
        } else {
            button.classList.remove('btn-outline-danger');
            button.classList.add('btn-danger');
        }

        this.selectedAnswer = answer;
        this.updateHiddenInput('yesNoAnswer', answer);
        this.enableNextButton();

        // Add visual feedback
        this.addFeedback(button);
    }

    selectLikert(radio) {
        this.selectedAnswer = radio.value;
        this.enableNextButton();

        // Add visual feedback to the label
        const label = document.querySelector(`label[for="${radio.id}"]`);
        if (label) {
            this.addFeedback(label);
        }
    }

    updateHiddenInput(inputId, value) {
        const input = document.getElementById(inputId);
        if (input) {
            input.value = value;
        }
    }

    enableNextButton() {
        const nextBtn = document.getElementById('nextBtn');
        if (nextBtn) {
            nextBtn.disabled = false;
            nextBtn.classList.add('animate-pulse');
            setTimeout(() => {
                nextBtn.classList.remove('animate-pulse');
            }, 1000);
        }
    }

    addFeedback(element) {
        element.classList.add('animate-pulse');
        setTimeout(() => {
            element.classList.remove('animate-pulse');
        }, 300);
    }

    handleKeyboardNavigation(e) {
        const nextBtn = document.getElementById('nextBtn');
        
        switch(e.key) {
            case 'Enter':
                if (nextBtn && !nextBtn.disabled) {
                    e.preventDefault();
                    nextBtn.click();
                }
                break;
            case '1':
            case '2':
            case '3':
            case '4':
                // Quick selection for MCQ options
                const optionIndex = parseInt(e.key) - 1;
                const options = document.querySelectorAll('.option-btn');
                if (options[optionIndex]) {
                    e.preventDefault();
                    this.selectOption(options[optionIndex]);
                }
                break;
            case 'y':
            case 'Y':
                // Quick yes selection
                const yesBtn = document.querySelector('.yes-no-btn:contains("Yes")') || 
                              Array.from(document.querySelectorAll('.yes-no-btn'))
                                   .find(btn => btn.textContent.trim().toLowerCase() === 'yes');
                if (yesBtn) {
                    e.preventDefault();
                    this.selectYesNo(yesBtn);
                }
                break;
            case 'n':
            case 'N':
                // Quick no selection
                const noBtn = document.querySelector('.yes-no-btn:contains("No")') || 
                             Array.from(document.querySelectorAll('.yes-no-btn'))
                                  .find(btn => btn.textContent.trim().toLowerCase() === 'no');
                if (noBtn) {
                    e.preventDefault();
                    this.selectYesNo(noBtn);
                }
                break;
        }
    }

    handleSubmit(e) {
        if (!this.selectedAnswer) {
            e.preventDefault();
            this.showValidationMessage();
            return;
        }

        // Store answer locally for auto-save
        const questionId = document.querySelector('input[name="question_id"]')?.value;
        if (questionId) {
            this.answers[questionId] = this.selectedAnswer;
            this.saveToLocalStorage();
        }

        // Show loading state
        this.showLoadingState();
    }

    showValidationMessage() {
        // Create or update validation message
        let message = document.getElementById('validationMessage');
        if (!message) {
            message = document.createElement('div');
            message.id = 'validationMessage';
            message.className = 'alert alert-warning mt-3';
            message.innerHTML = '<i data-feather="alert-triangle" class="me-2"></i>Please select an answer before continuing.';
            
            const form = document.getElementById('quizForm');
            if (form) {
                form.appendChild(message);
                if (window.feather) feather.replace();
            }
        }

        // Animate the message
        message.style.opacity = '0';
        message.style.display = 'block';
        setTimeout(() => {
            message.style.opacity = '1';
        }, 100);

        // Remove message after 5 seconds
        setTimeout(() => {
            if (message && message.parentNode) {
                message.style.opacity = '0';
                setTimeout(() => {
                    if (message.parentNode) {
                        message.remove();
                    }
                }, 300);
            }
        }, 5000);
    }

    showLoadingState() {
        const nextBtn = document.getElementById('nextBtn');
        if (nextBtn) {
            const originalText = nextBtn.innerHTML;
            nextBtn.innerHTML = '<span class="spinner me-2"></span>Loading...';
            nextBtn.disabled = true;
            
            // Restore after 3 seconds if form hasn't submitted
            setTimeout(() => {
                if (nextBtn) {
                    nextBtn.innerHTML = originalText;
                    nextBtn.disabled = false;
                    if (window.feather) feather.replace();
                }
            }, 3000);
        }
    }

    loadProgress() {
        // Load any saved progress from localStorage
        const saved = localStorage.getItem('quizProgress');
        if (saved) {
            try {
                const progress = JSON.parse(saved);
                this.answers = progress.answers || {};
                this.timeSpent = progress.timeSpent || 0;
            } catch (e) {
                console.warn('Failed to load quiz progress:', e);
            }
        }
    }

    saveToLocalStorage() {
        const progress = {
            answers: this.answers,
            timeSpent: this.timeSpent,
            lastSaved: Date.now()
        };
        
        try {
            localStorage.setItem('quizProgress', JSON.stringify(progress));
        } catch (e) {
            console.warn('Failed to save quiz progress:', e);
        }
    }

    autoSave() {
        if (Object.keys(this.answers).length > 0) {
            this.saveToLocalStorage();
        }
    }

    startTimer() {
        setInterval(() => {
            this.timeSpent = Math.floor((Date.now() - this.startTime) / 1000);
            this.updateTimeDisplay();
        }, 1000);
    }

    updateTimeDisplay() {
        const timeDisplay = document.getElementById('timeDisplay');
        if (timeDisplay) {
            const minutes = Math.floor(this.timeSpent / 60);
            const seconds = this.timeSpent % 60;
            timeDisplay.textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;
        }
    }

    initializeAccessibility() {
        // Add ARIA labels and descriptions
        const progressBar = document.querySelector('.quiz-progress-bar');
        if (progressBar) {
            progressBar.setAttribute('role', 'progressbar');
            progressBar.setAttribute('aria-label', 'Quiz progress');
        }

        // Add focus management
        const firstOption = document.querySelector('.option-btn, .yes-no-btn, input[type="radio"]');
        if (firstOption) {
            firstOption.focus();
        }

        // Add skip link for screen readers
        this.addSkipLink();
    }

    addSkipLink() {
        const skipLink = document.createElement('a');
        skipLink.href = '#nextBtn';
        skipLink.textContent = 'Skip to next button';
        skipLink.className = 'sr-only sr-only-focusable';
        skipLink.style.cssText = `
            position: absolute;
            left: -10000px;
            top: auto;
            width: 1px;
            height: 1px;
            overflow: hidden;
        `;
        
        skipLink.addEventListener('focus', () => {
            skipLink.style.cssText = `
                position: static;
                width: auto;
                height: auto;
                background: #2563eb;
                color: white;
                padding: 8px;
                text-decoration: none;
                border-radius: 4px;
            `;
        });

        document.body.insertBefore(skipLink, document.body.firstChild);
    }

    // Public methods for external access
    getCurrentProgress() {
        return {
            currentQuestion: this.currentQuestion,
            totalQuestions: this.totalQuestions,
            timeSpent: this.timeSpent,
            answers: this.answers
        };
    }

    resetQuiz() {
        localStorage.removeItem('quizProgress');
        this.answers = {};
        this.selectedAnswer = null;
        this.timeSpent = 0;
        this.startTime = Date.now();
    }
}

// Quiz Helper Functions
const QuizHelpers = {
    // Smooth scroll to top after question change
    scrollToTop() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    },

    // Add visual feedback to progress bar
    animateProgress(percentage) {
        const progressBar = document.querySelector('.quiz-progress-bar');
        if (progressBar) {
            progressBar.style.width = percentage + '%';
            progressBar.classList.add('animate-progress');
            setTimeout(() => {
                progressBar.classList.remove('animate-progress');
            }, 500);
        }
    },

    // Show encouragement messages
    showEncouragement(questionNumber, total) {
        const messages = [
            "Great start! Keep going!",
            "You're doing well!",
            "Halfway there!",
            "Almost done!",
            "Final stretch!"
        ];
        
        const milestone = Math.floor(questionNumber / (total / messages.length));
        const message = messages[Math.min(milestone, messages.length - 1)];
        
        if (questionNumber % 5 === 0 && questionNumber > 0) {
            this.showToast(message, 'success');
        }
    },

    // Toast notification system
    showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast-notification toast-${type}`;
        toast.innerHTML = `
            <div class="d-flex align-items-center">
                <i data-feather="check-circle" class="me-2"></i>
                <span>${message}</span>
            </div>
        `;
        toast.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${type === 'success' ? '#16a34a' : '#2563eb'};
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            z-index: 1050;
            opacity: 0;
            transform: translateX(100%);
            transition: all 0.3s ease;
        `;

        document.body.appendChild(toast);
        if (window.feather) feather.replace();

        // Animate in
        setTimeout(() => {
            toast.style.opacity = '1';
            toast.style.transform = 'translateX(0)';
        }, 100);

        // Remove after 3 seconds
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
};

// Initialize quiz manager when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Only initialize on quiz pages
    if (document.getElementById('quizForm') || document.querySelector('.quiz-progress')) {
        window.quizManager = new QuizManager();
    }

    // Add smooth scrolling to top after page transitions
    if (document.querySelector('.question-card')) {
        QuizHelpers.scrollToTop();
    }
});

// Global functions for template compatibility
function selectOption(value) {
    if (window.quizManager) {
        const button = Array.from(document.querySelectorAll('.option-btn'))
                           .find(btn => btn.getAttribute('data-value') === value ||
                                       btn.textContent.includes(value));
        if (button) {
            window.quizManager.selectOption(button);
        }
    }
}

function selectYesNo(value) {
    if (window.quizManager) {
        const button = Array.from(document.querySelectorAll('.yes-no-btn'))
                           .find(btn => btn.textContent.trim().toLowerCase() === value.toLowerCase());
        if (button) {
            window.quizManager.selectYesNo(button);
        }
    }
}

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { QuizManager, QuizHelpers };
}
