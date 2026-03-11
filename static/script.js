// Tab switching
document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const tabName = btn.dataset.tab;
        
        // Hide all tabs
        document.querySelectorAll('.tab-content').forEach(tab => {
            tab.classList.remove('active');
        });
        
        // Remove active from all buttons
        document.querySelectorAll('.tab-btn').forEach(b => {
            b.classList.remove('active');
        });
        
        // Show selected tab
        document.getElementById(tabName).classList.add('active');
        btn.classList.add('active');
    });
});

// Password visibility toggle
const passwordInput = document.getElementById('password');
const toggleBtn = document.getElementById('toggleBtn');

toggleBtn.addEventListener('click', () => {
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        toggleBtn.textContent = '👁️‍🗨️';
    } else {
        passwordInput.type = 'password';
        toggleBtn.textContent = '👁️';
    }
});

// Real-time password analysis
passwordInput.addEventListener('input', async () => {
    const password = passwordInput.value;
    
    if (password.length === 0) {
        document.getElementById('results').style.display = 'none';
        return;
    }
    
    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ password: password })
        });
        
        const data = await response.json();
        displayResults(data);
    } catch (error) {
        console.error('Error:', error);
    }
});

function displayResults(data) {
    const resultsDiv = document.getElementById('results');
    
    // Update strength
    document.getElementById('strengthBadge').textContent = data.strength;
    document.getElementById('scoreText').textContent = data.score;
    document.getElementById('entropyText').textContent = data.entropy;
    document.getElementById('crackTimeText').textContent = data.crack_time;
    
    // Update strength bar
    const bar = document.getElementById('strengthBar');
    bar.style.width = data.score + '%';
    
    // Update metrics
    updateMetric('uppercase', data.metrics.has_uppercase, data.metrics.uppercase_count);
    updateMetric('lowercase', data.metrics.has_lowercase, data.metrics.lowercase_count);
    updateMetric('digits', data.metrics.has_digits, data.metrics.digit_count);
    updateMetric('special', data.metrics.has_special, data.metrics.special_count);
    
    // Update vulnerabilities
    const vulnSection = document.getElementById('vulnSection');
    const vulnList = document.getElementById('vulnList');
    
    if (data.vulnerabilities.length > 0) {
        vulnList.innerHTML = '';
        data.vulnerabilities.forEach(vuln => {
            const li = document.createElement('li');
            li.textContent = vuln;
            vulnList.appendChild(li);
        });
        vulnSection.style.display = 'block';
    } else {
        vulnSection.style.display = 'none';
    }
    
    // Update feedback
    const feedbackList = document.getElementById('feedbackList');
    feedbackList.innerHTML = '';
    data.feedback.forEach(fb => {
        const li = document.createElement('li');
        li.textContent = fb;
        feedbackList.appendChild(li);
    });
    
    resultsDiv.style.display = 'block';
}

function updateMetric(id, hasIt, count) {
    const element = document.getElementById(id + 'Value');
    const card = document.getElementById(id + 'Card');
    
    element.textContent = hasIt ? `✓ (${count})` : '✗';
    card.classList.remove('active', 'inactive');
    card.classList.add(hasIt ? 'active' : 'inactive');
}

// Password Generator
const lengthSlider = document.getElementById('lengthSlider');
const lengthValue = document.getElementById('lengthValue');

lengthSlider.addEventListener('input', () => {
    lengthValue.textContent = lengthSlider.value;
});

document.getElementById('generateBtn').addEventListener('click', async () => {
    const data = {
        length: parseInt(lengthSlider.value),
        use_upper: document.getElementById('genUpper').checked,
        use_lower: document.getElementById('genLower').checked,
        use_digits: document.getElementById('genDigits').checked,
        use_special: document.getElementById('genSpecial').checked
    };
    
    try {
        const response = await fetch('/api/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        document.getElementById('generatedPasswordText').value = result.generated_password;
        
        const analysisDiv = document.getElementById('generatedAnalysis');
        analysisDiv.innerHTML = `
            <h4>Generated Password Analysis:</h4>
            <p><strong>Strength:</strong> ${result.strength}</p>
            <p><strong>Score:</strong> ${result.score}/100</p>
            <p><strong>Entropy:</strong> ${result.entropy} bits</p>
            <p><strong>Crack Time:</strong> ${result.crack_time}</p>
        `;
        
        document.getElementById('generatedResult').style.display = 'block';
    } catch (error) {
        console.error('Error:', error);
    }
});

document.getElementById('copyGenBtn').addEventListener('click', () => {
    const passwordText = document.getElementById('generatedPasswordText');
    passwordText.select();
    document.execCommand('copy');
    
    const originalText = document.getElementById('copyGenBtn').textContent;
    document.getElementById('copyGenBtn').textContent = '✅ Copied!';
    setTimeout(() => {
        document.getElementById('copyGenBtn').textContent = originalText;
    }, 2000);
});
