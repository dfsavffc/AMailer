// @ts-check

document.addEventListener('DOMContentLoaded', () => {
    /**
     * @typedef {Object} Config
     * @property {Object} limits
     * @property {number} limits.subject
     * @property {number} limits.message
     * @property {Object} api
     * @property {string} api.sendEmail
     * @property {Object} animations
     * @property {number} animations.slideIn
     */

    /** @type {Config} */
    // @ts-ignore
    const config = window.AMailerConfig;

    /** @type {HTMLFormElement} */
    const form = /** @type {HTMLFormElement} */ (document.getElementById('emailForm'));
    /** @type {HTMLInputElement} */
    const recipientInput = /** @type {HTMLInputElement} */ (document.getElementById('recipient'));
    /** @type {HTMLInputElement} */
    const subjectInput = /** @type {HTMLInputElement} */ (document.getElementById('subject'));
    /** @type {HTMLTextAreaElement} */
    const messageInput = /** @type {HTMLTextAreaElement} */ (document.getElementById('message'));
    /** @type {HTMLButtonElement} */
    const submitBtn = /** @type {HTMLButtonElement} */ (document.getElementById('submitBtn'));
    /** @type {HTMLElement} */
    const successMsg = /** @type {HTMLElement} */ (document.getElementById('successMessage'));
    /** @type {HTMLElement} */
    const errorMsg = /** @type {HTMLElement} */ (document.getElementById('errorMessage'));
    /** @type {HTMLElement} */
    const emailErrorMsg = /** @type {HTMLElement} */ (document.getElementById('emailError'));

    function initInputs() {
        subjectInput.setAttribute('maxlength', String(config.limits.subject));
        messageInput.setAttribute('maxlength', String(config.limits.message));

        updateCounter('subjectCharCount', 0, config.limits.subject);
        updateCounter('messageCharCount', 0, config.limits.message);

        setupAutoResize(subjectInput, 'subjectCharCount', config.limits.subject);
        setupAutoResize(messageInput, 'messageCharCount', config.limits.message);

        recipientInput.addEventListener('input', validateEmail);
        recipientInput.addEventListener('blur', validateEmail);
    }

    /**
     * @param {string} elementId
     * @param {number} current
     * @param {number} max
     */
    function updateCounter(elementId, current, max) {
        const element = document.getElementById(elementId);
        if (element) {
            element.textContent = `${current}/${max}`;
        }
    }

    /**
     * @param {HTMLInputElement|HTMLTextAreaElement} input
     * @param {string} counterId
     * @param {number} maxLength
     */
    function setupAutoResize(input, counterId, maxLength) {
        const resize = () => {
            input.style.height = 'auto';
            input.style.height = (input.scrollHeight) + 'px';
            updateCounter(counterId, input.value.length, maxLength);
        };

        input.addEventListener('input', resize);
        resize();
    }

    /**
     * @returns {boolean}
     */
    function validateEmail() {
        const email = recipientInput.value;
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        if (email && !emailRegex.test(email)) {
            emailErrorMsg.classList.add('visible');
            recipientInput.setAttribute('aria-invalid', 'true');
            return false;
        } else {
            emailErrorMsg.classList.remove('visible');
            recipientInput.removeAttribute('aria-invalid');
            return true;
        }
    }

    let isSubmitting = false;

    /**
     * @param {Event} e
     */
    async function handleSubmit(e) {
        e.preventDefault();

        submitBtn.blur();

        if (isSubmitting) return;

        if (!validateEmail()) {
            return;
        }

        isSubmitting = true;

        successMsg.style.display = 'none';
        errorMsg.style.display = 'none';

        submitBtn.style.opacity = '0.7';
        submitBtn.style.cursor = 'not-allowed';

        const formData = {
            recipient: recipientInput.value,
            subject: subjectInput.value,
            message: messageInput.value
        };

        try {
            const response = await fetch(config.api.sendEmail, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            const result = await response.json();

            if (response.ok) {
                successMsg.style.display = 'block';
                form.reset();
                setTimeout(() => {
                    updateCounter('subjectCharCount', 0, config.limits.subject);
                    updateCounter('messageCharCount', 0, config.limits.message);
                    subjectInput.style.height = 'auto';
                    messageInput.style.height = 'auto';
                    recipientInput.removeAttribute('aria-invalid');
                    emailErrorMsg.classList.remove('visible');
                }, 0);
            } else {
                throw new Error('Failed to send');
            }
        } catch (error) {
            console.error('Error:', error);
            errorMsg.style.display = 'block';
            // Always show generic error message
            errorMsg.textContent = 'Failed to send message. Please try again.';
        } finally {
            isSubmitting = false;
            submitBtn.style.opacity = '1';
            submitBtn.style.cursor = 'pointer';
        }
    }

    initInputs();
    form.addEventListener('submit', handleSubmit);
});