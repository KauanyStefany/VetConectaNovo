/**
 * Sistema de gerenciamento de toasts
 * Utiliza Bootstrap 5.3 Toast component
 *
 * VetConecta - Sistema de notificações toast
 */

class ToastManager {
    constructor() {
        this.container = null;
        this.init();
    }

    init() {
        // Aguarda o DOM estar pronto
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.setupContainer());
        } else {
            this.setupContainer();
        }
    }

    setupContainer() {
        this.container = document.getElementById('toast-container');
        if (!this.container) {
            this.createContainer();
        }

        // Processa mensagens flash do backend
        this.processFlashMessages();
    }

    createContainer() {
        const container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'toast-container position-fixed bottom-0 end-0 p-3';
        container.style.zIndex = '9999';
        document.body.appendChild(container);
        this.container = container;
    }

    /**
     * Processa mensagens flash vindas do backend
     */
    processFlashMessages() {
        const messagesScript = document.getElementById('mensagens-data');
        if (messagesScript) {
            try {
                const messages = JSON.parse(messagesScript.textContent);
                if (Array.isArray(messages) && messages.length > 0) {
                    messages.forEach(msg => {
                        this.show(msg.text, msg.type);
                    });
                }
            } catch (e) {
                console.error('Erro ao processar mensagens flash:', e);
            }
        }
    }

    /**
     * Exibe um toast
     * @param {string} message - Mensagem a ser exibida
     * @param {string} type - Tipo (success, danger, warning, info)
     * @param {number} duration - Duração em ms (0 = permanente)
     */
    show(message, type = 'info', duration = 5000) {
        if (!this.container) {
            console.error('Toast container não inicializado');
            return null;
        }

        const toast = this.createToast(message, type);
        this.container.appendChild(toast);

        const bsToast = new bootstrap.Toast(toast, {
            autohide: duration > 0,
            delay: duration
        });

        toast.addEventListener('hidden.bs.toast', () => {
            toast.remove();
        });

        bsToast.show();
        return bsToast;
    }

    createToast(message, type) {
        const toastId = 'toast-' + Date.now() + '-' + Math.random().toString(36).substr(2, 9);

        const typeClasses = {
            'success': 'text-bg-success',
            'danger': 'text-bg-danger',
            'warning': 'text-bg-warning',
            'info': 'text-bg-info'
        };

        const typeIcons = {
            'success': 'bi-check-circle-fill',
            'danger': 'bi-x-circle-fill',
            'warning': 'bi-exclamation-triangle-fill',
            'info': 'bi-info-circle-fill'
        };

        const bgClass = typeClasses[type] || 'text-bg-info';
        const iconClass = typeIcons[type] || 'bi-info-circle-fill';

        const toastHtml = `
            <div class="toast ${bgClass}" role="alert" aria-live="assertive" aria-atomic="true" id="${toastId}">
                <div class="d-flex">
                    <div class="toast-body">
                        <i class="bi ${iconClass} me-2"></i>
                        ${this.escapeHtml(message)}
                    </div>
                    <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Fechar"></button>
                </div>
            </div>
        `;

        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = toastHtml.trim();
        return tempDiv.firstElementChild;
    }

    /**
     * Escapa HTML para prevenir XSS
     */
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    getTypeTitle(type) {
        const titles = {
            'success': 'Sucesso',
            'danger': 'Erro',
            'warning': 'Aviso',
            'info': 'Informação'
        };
        return titles[type] || 'Notificação';
    }

    // Métodos de conveniência
    success(message, duration = 5000) {
        return this.show(message, 'success', duration);
    }

    error(message, duration = 7000) {
        return this.show(message, 'danger', duration);
    }

    warning(message, duration = 6000) {
        return this.show(message, 'warning', duration);
    }

    info(message, duration = 5000) {
        return this.show(message, 'info', duration);
    }
}

// Instância global
window.toastManager = new ToastManager();

// Funções globais para facilitar o uso
window.showToast = function(message, type = 'info', duration = 5000) {
    return window.toastManager.show(message, type, duration);
};

window.showSuccess = function(message, duration = 5000) {
    return window.toastManager.success(message, duration);
};

window.showError = function(message, duration = 7000) {
    return window.toastManager.error(message, duration);
};

window.showWarning = function(message, duration = 6000) {
    return window.toastManager.warning(message, duration);
};

window.showInfo = function(message, duration = 5000) {
    return window.toastManager.info(message, duration);
};
