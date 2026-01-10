// @ts-check

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
const CONFIG = {
    limits: {
        subject: 100,
        message: 1000
    },
    api: {
        sendEmail: '/api/send-email'
    },
    animations: {
        slideIn: 500
    }
};

// @ts-ignore
window.AMailerConfig = CONFIG;