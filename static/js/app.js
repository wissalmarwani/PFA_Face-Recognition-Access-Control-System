/* ============================================
   FaceID — Client-Side Logic
   ============================================ */

document.addEventListener('DOMContentLoaded', () => {
    createParticles();
    initClock();
});

// --- State ---
let isScanning = false;
let progressInterval = null;
let currentProgress = 0;

// --- DOM refs ---
const getEl = (id) => document.getElementById(id);

// --- Start Scanning ---
function startScanning() {
    if (isScanning) return;
    isScanning = true;

    // Activate scanning visuals
    const viewport = document.querySelector('.scanner-viewport');
    if (viewport) viewport.classList.add('scanning-active');

    const statusEl = getEl('scanner-status');
    if (statusEl) {
        statusEl.textContent = 'Scanning...';
        statusEl.classList.add('active');
    }

    // Reset result panel
    resetResultPanel();

    // Animate progress bar then verify
    animateProgress(0, 60, 2000, () => {
        verifyAccess();
    });
}

// --- Animate Progress ---
function animateProgress(from, to, duration, callback) {
    currentProgress = from;
    const progressFill = getEl('progress-fill');
    const progressValue = getEl('progress-value');
    const startTime = performance.now();

    function update(now) {
        const elapsed = now - startTime;
        const ratio = Math.min(elapsed / duration, 1);
        // Ease out cubic
        const eased = 1 - Math.pow(1 - ratio, 3);
        currentProgress = from + (to - from) * eased;

        if (progressFill) progressFill.style.width = currentProgress + '%';
        if (progressValue) progressValue.textContent = Math.round(currentProgress) + ' %';

        if (ratio < 1) {
            requestAnimationFrame(update);
        } else {
            if (callback) callback();
        }
    }

    requestAnimationFrame(update);
}

// --- Verify Access ---
async function verifyAccess() {
    const statusEl = getEl('scanner-status');
    if (statusEl) statusEl.textContent = 'Analyzing...';

    try {
        const response = await fetch('/verify');
        const data = await response.json();

        // Complete progress to 100%
        animateProgress(currentProgress, 100, 800, () => {
            setTimeout(() => {
                showResult(data);
            }, 400);
        });

    } catch (error) {
        animateProgress(currentProgress, 100, 500, () => {
            showResult({ verified: false, error: error.message });
        });
    }
}

// --- Show Result ---
function showResult(data) {
    const statusEl = getEl('scanner-status');
    const viewport = document.querySelector('.scanner-viewport');

    if (viewport) viewport.classList.remove('scanning-active');
    if (statusEl) {
        statusEl.classList.remove('active');
        statusEl.textContent = 'Complete';
    }

    // Hide waiting state
    const waitingState = getEl('waiting-state');
    if (waitingState) waitingState.style.display = 'none';

    // Show result content
    const resultContent = getEl('result-content');
    if (resultContent) resultContent.style.display = 'flex';

    const resultIcon = getEl('result-icon');
    const resultTitle = getEl('result-title');
    const resultSubtitle = getEl('result-subtitle');
    const resultAvatar = getEl('result-avatar');
    const resultName = getEl('result-name');
    const resultDivider = getEl('result-divider');
    const resultInfo = getEl('result-info');

    if (data.verified) {
        // Success
        if (resultIcon) {
            resultIcon.innerHTML = '👍';
            resultIcon.className = 'result-icon success visible';
        }
        if (resultTitle) {
            resultTitle.textContent = 'Successful!';
            resultTitle.className = 'result-title success visible';
        }
        if (resultSubtitle) {
            resultSubtitle.textContent = 'ID Confirmed. You may Enter.';
            resultSubtitle.className = 'result-subtitle visible';
        }

        // Avatar
        if (resultAvatar) {
            const avatarImg = resultAvatar.querySelector('img');
            if (avatarImg && data.photo_url) {
                avatarImg.src = data.photo_url;
            }
            resultAvatar.classList.add('visible');
        }

        // Name
        if (resultName) {
            resultName.textContent = capitalizeWords(data.name || 'Unknown');
            resultName.classList.add('visible');
        }

        if (resultDivider) resultDivider.classList.add('visible');

        // Info
        if (resultInfo) {
            const empId = getEl('info-emp-id');
            const entryTime = getEl('info-entry');
            const designation = getEl('info-designation');
            const exitTime = getEl('info-exit');

            if (empId) empId.textContent = data.employee_id || 'N/A';
            if (entryTime) entryTime.textContent = formatTime(new Date());
            if (designation) designation.textContent = data.designation || 'Member';
            if (exitTime) exitTime.textContent = '—';

            resultInfo.classList.add('visible');
        }

    } else {
        // Denied
        if (resultIcon) {
            resultIcon.innerHTML = '⛔';
            resultIcon.className = 'result-icon denied visible';
        }
        if (resultTitle) {
            resultTitle.textContent = 'Access Denied';
            resultTitle.className = 'result-title denied visible';
        }
        if (resultSubtitle) {
            resultSubtitle.textContent = 'User not recognized. Please contact admin.';
            resultSubtitle.className = 'result-subtitle visible';
        }

        if (resultAvatar) resultAvatar.classList.remove('visible');
        if (resultName) {
            resultName.textContent = 'Unknown User';
            resultName.classList.add('visible');
        }
        if (resultDivider) resultDivider.classList.add('visible');
        if (resultInfo) resultInfo.classList.remove('visible');
    }

    isScanning = false;
}

// --- Reset Result Panel ---
function resetResultPanel() {
    const waitingState = getEl('waiting-state');
    const resultContent = getEl('result-content');

    if (waitingState) waitingState.style.display = 'flex';
    if (resultContent) resultContent.style.display = 'none';

    // Reset all animated elements
    ['result-icon', 'result-title', 'result-subtitle', 'result-avatar',
        'result-name', 'result-divider', 'result-info'].forEach(id => {
            const el = getEl(id);
            if (el) el.classList.remove('visible');
        });

    // Reset progress
    const progressFill = getEl('progress-fill');
    const progressValue = getEl('progress-value');
    if (progressFill) progressFill.style.width = '0%';
    if (progressValue) progressValue.textContent = '0 %';
}

// --- Reset Everything ---
function resetAll() {
    isScanning = false;
    resetResultPanel();

    const statusEl = getEl('scanner-status');
    if (statusEl) {
        statusEl.textContent = 'Ready';
        statusEl.classList.remove('active');
    }

    const viewport = document.querySelector('.scanner-viewport');
    if (viewport) viewport.classList.remove('scanning-active');
}

// --- Utilities ---
function capitalizeWords(str) {
    return str.replace(/\b\w/g, c => c.toUpperCase());
}

function formatTime(date) {
    return date.toLocaleTimeString('en-US', {
        hour: 'numeric',
        minute: '2-digit',
        hour12: true
    });
}

function initClock() {
    // Update the entry time placeholder periodically if needed
}

// --- Decorative Particles ---
function createParticles() {
    const count = 15;
    for (let i = 0; i < count; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.left = Math.random() * 100 + 'vw';
        particle.style.top = Math.random() * 100 + 'vh';
        particle.style.animationDelay = Math.random() * 8 + 's';
        particle.style.animationDuration = (6 + Math.random() * 6) + 's';
        document.body.appendChild(particle);
    }
}
