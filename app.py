#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ADVANCED PASSWORD ANALYZER - WEB VERSION
Professional Password Security Analysis Application
Developed for Pinnacle Labs Cybersecurity Internship
"""

from flask import Flask, render_template, request, jsonify
import re
import string
import math
import json
from datetime import datetime

app = Flask(__name__)

class AdvancedPasswordAnalyzer:
    """Enterprise-grade password analysis engine."""
    
    def __init__(self):
        self.vulnerability_patterns = self.init_patterns()
        self.common_passwords = self.load_common_passwords()
    
    def init_patterns(self):
        """Initialize vulnerability detection patterns."""
        return {
            'keyboard_sequential': [
                'qwerty', 'asdfgh', 'zxcvbn', '123456', '098765',
                'qwertyuiop', 'asdfghjkl', 'zxcvbnm'
            ],
            'common_words': [
                'password', 'admin', 'user', 'root', 'test', 'demo',
                'welcome', 'login', 'default', 'letmein', 'monkey',
                'dragon', 'master', 'sunshine', 'princess'
            ]
        }
    
    def load_common_passwords(self):
        """Load common passwords."""
        return set([
            'password', '123456', '12345678', 'qwerty', 'abc123', 'monkey',
            'letmein', 'trustno1', 'dragon', 'baseball', 'iloveyou', 'master',
            'sunshine', 'ashley', 'bailey', 'passw0rd', 'shadow', 'superman',
            '123123', '654321', '111111', 'starwars', '666666', '123321'
        ])
    
    def analyze(self, password: str) -> dict:
        """Complete advanced analysis."""
        if not password:
            return self._empty_result()
        
        metrics = self._analyze_characters(password)
        entropy = self._calculate_entropy(password)
        crack_time = self._estimate_crack_time(entropy)
        vulnerabilities = self._detect_vulnerabilities(password)
        score = self._calculate_score(metrics, entropy, vulnerabilities)
        strength = self._determine_strength(score)
        feedback = self._generate_feedback(metrics, vulnerabilities, password)
        
        return {
            'password_length': len(password),
            'strength': strength,
            'score': min(score, 100),
            'entropy': round(entropy, 2),
            'crack_time': crack_time,
            'feedback': feedback,
            'metrics': metrics,
            'vulnerabilities': vulnerabilities,
            'vulnerability_count': len(vulnerabilities),
            'is_common': password.lower() in self.common_passwords,
            'recommendations': self._get_recommendations(metrics, vulnerabilities),
            'analysis_time': datetime.now().isoformat(),
        }
    
    def _analyze_characters(self, pwd: str) -> dict:
        """Analyze character composition."""
        return {
            'has_uppercase': bool(re.search(r'[A-Z]', pwd)),
            'has_lowercase': bool(re.search(r'[a-z]', pwd)),
            'has_digits': bool(re.search(r'\d', pwd)),
            'has_special': bool(re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|`~]', pwd)),
            'uppercase_count': sum(1 for c in pwd if c.isupper()),
            'lowercase_count': sum(1 for c in pwd if c.islower()),
            'digit_count': sum(1 for c in pwd if c.isdigit()),
            'special_count': sum(1 for c in pwd if c in string.punctuation),
            'unique_chars': len(set(pwd)),
            'repeated_chars': max((pwd.count(c) for c in pwd), default=0),
            'has_spaces': ' ' in pwd,
            'char_types': sum([
                bool(re.search(r'[A-Z]', pwd)),
                bool(re.search(r'[a-z]', pwd)),
                bool(re.search(r'\d', pwd)),
                bool(re.search(r'[^a-zA-Z0-9]', pwd))
            ])
        }
    
    def _calculate_entropy(self, pwd: str) -> float:
        """Calculate Shannon entropy."""
        if not pwd:
            return 0.0
        
        charset_size = 0
        if re.search(r'[a-z]', pwd): charset_size += 26
        if re.search(r'[A-Z]', pwd): charset_size += 26
        if re.search(r'\d', pwd): charset_size += 10
        if re.search(r'[^a-zA-Z0-9]', pwd): charset_size += 32
        
        if charset_size == 0:
            return 0.0
        
        return len(pwd) * math.log2(charset_size)
    
    def _estimate_crack_time(self, entropy: float) -> str:
        """Estimate brute force time."""
        if entropy == 0:
            return "< 1ms"
        
        seconds = (2 ** entropy) / (10**12 * 2)
        
        if seconds < 0.001: return "< 1ms"
        if seconds < 1: return f"{int(seconds*1000)}ms"
        if seconds < 60: return f"{int(seconds)}s"
        if seconds < 3600: return f"{int(seconds/60)}m"
        if seconds < 86400: return f"{int(seconds/3600)}h"
        if seconds < 31536000: return f"{int(seconds/86400)}d"
        if seconds < 31536000*100: return f"{int(seconds/31536000)}y"
        return "Impossible"
    
    def _detect_vulnerabilities(self, pwd: str) -> list:
        """Detect security vulnerabilities."""
        vulns = []
        pwd_lower = pwd.lower()
        
        for pattern in self.vulnerability_patterns['keyboard_sequential']:
            if pattern in pwd_lower:
                vulns.append(f"Keyboard pattern: {pattern}")
        
        for word in self.vulnerability_patterns['common_words']:
            if word in pwd_lower:
                vulns.append(f"Common word: {word}")
        
        if re.search(r'\b(19|20)\d{2}\b', pwd):
            vulns.append("Year pattern detected")
        
        if re.search(r'(.)\1{2,}', pwd):
            vulns.append("Character repetition")
        
        if re.search(r'(012|123|234|345|456|567|678|789|890)', pwd):
            vulns.append("Sequential numbers")
        
        if pwd.lower() in self.common_passwords:
            vulns.append("COMMONLY USED PASSWORD!")
        
        return vulns
    
    def _calculate_score(self, metrics: dict, entropy: float, vulns: list) -> int:
        """Calculate security score (0-100)."""
        score = 0
        
        # Length (30 points)
        length = len(metrics.get('password', ''))
        if length >= 8: score += 10
        if length >= 12: score += 10
        if length >= 16: score += 10
        
        # Character variety (40 points)
        if metrics['has_uppercase']: score += 10
        if metrics['has_lowercase']: score += 10
        if metrics['has_digits']: score += 10
        if metrics['has_special']: score += 10
        
        # Entropy (20 points)
        if entropy >= 50: score += 10
        if entropy >= 80: score += 10
        
        # Penalty for vulnerabilities
        score -= len(vulns) * 5
        
        return max(0, min(100, score))
    
    def _determine_strength(self, score: int) -> str:
        """Determine strength level."""
        if score >= 90: return "🟢 EXCELLENT"
        if score >= 75: return "🟢 VERY STRONG"
        if score >= 60: return "🟢 STRONG"
        if score >= 45: return "🟡 MEDIUM"
        if score >= 30: return "🟠 WEAK"
        return "🔴 VERY WEAK"
    
    def _generate_feedback(self, metrics: dict, vulns: list, pwd: str) -> list:
        """Generate detailed feedback."""
        feedback = []
        
        if len(pwd) < 8:
            feedback.append("Password is too short (8+ chars minimum)")
        elif len(pwd) < 12:
            feedback.append("Consider 12+ characters for better security")
        
        if not metrics['has_uppercase']:
            feedback.append("Add uppercase letters (A-Z)")
        if not metrics['has_lowercase']:
            feedback.append("Add lowercase letters (a-z)")
        if not metrics['has_digits']:
            feedback.append("Add numbers (0-9)")
        if not metrics['has_special']:
            feedback.append("Add special characters (!@#$%^&*)")
        
        for vuln in vulns:
            feedback.append(f"Avoid: {vuln}")
        
        if not feedback:
            feedback.append("Excellent! Password meets all security criteria")
        
        return feedback
    
    def _get_recommendations(self, metrics: dict, vulns: list) -> list:
        """Get recommendations."""
        recs = []
        
        if metrics['repeated_chars'] > 2:
            recs.append("Reduce character repetition")
        
        if metrics['unique_chars'] < 6:
            recs.append("Use more unique characters")
        
        if vulns:
            recs.append("Avoid patterns and common words")
        
        if metrics['char_types'] < 4:
            recs.append("Mix all character types")
        
        return recs
    
    def _empty_result(self) -> dict:
        """Return empty result."""
        return {
            'password_length': 0,
            'strength': 'NONE',
            'score': 0,
            'entropy': 0,
            'crack_time': 'N/A',
            'feedback': ['Enter a password'],
            'metrics': {},
            'vulnerabilities': [],
            'vulnerability_count': 0,
            'is_common': False,
            'recommendations': [],
            'analysis_time': datetime.now().isoformat(),
        }


analyzer = AdvancedPasswordAnalyzer()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    data = request.get_json()
    password = data.get('password', '')
    
    result = analyzer.analyze(password)
    return jsonify(result)

@app.route('/api/generate', methods=['POST'])
def api_generate():
    import secrets
    
    data = request.get_json()
    length = min(int(data.get('length', 16)), 64)
    use_upper = data.get('use_upper', True)
    use_lower = data.get('use_lower', True)
    use_digits = data.get('use_digits', True)
    use_special = data.get('use_special', True)
    
    chars = ''
    if use_upper: chars += string.ascii_uppercase
    if use_lower: chars += string.ascii_lowercase
    if use_digits: chars += string.digits
    if use_special: chars += '!@#$%^&*()_+-=[]{}|;:,.<>?'
    
    if not chars:
        chars = string.ascii_letters + string.digits
    
    password = ''.join(secrets.choice(chars) for _ in range(length))
    
    # Analyze generated password
    result = analyzer.analyze(password)
    result['generated_password'] = password
    
    return jsonify(result)

@app.route('/health')
def health():
    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
