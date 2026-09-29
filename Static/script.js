'use strict';

(function () {
  const $ = (id) => document.getElementById(id);
  const messageInput = $('messageInput');
  const urlInput = $('urlInput');
  const checkBtn = $('checkBtn');
  const btnIcon = checkBtn.querySelector('.btn-icon');
  const btnLabel = checkBtn.querySelector('.btn-label');
  const inputError = $('inputError');
  const resultCard = $('resultCard');
  const stamp = $('stamp');
  const scoreMeter = $('scoreMeter');
  const meterFill = $('meterFill');
  const meterPercent = $('meterPercent');
  const CIRCUMFERENCE = 2 * Math.PI * 52;
  const resultTitle = $('resultTitle');
  const confidenceBadge = $('confidenceBadge');
  const sourceBadge = $('sourceBadge');
  const resultSubtitle = $('resultSubtitle');
  const translationPanel = $('translationPanel');
  const originalLabel = $('originalLabel');
  const originalTextDisplay = $('originalTextDisplay');
  const translatedTextDisplay = $('translatedTextDisplay');
  const highlightedText = $('highlightedText');
  const highlightLegend = $('highlightLegend');
  const rec = $('recommendation');
  const responseTime = $('responseTime');
  const checkAnotherBtn = $('checkAnotherBtn');

  const STATES = ['is-loading', 'is-true', 'is-false', 'is-unverified', 'is-error'];
  const VERDICT_LABEL = { true: 'True', false: 'False', unverified: 'Unverified' };
  const VERDICT_CLASS = { true: 'is-true', false: 'is-false', unverified: 'is-unverified' };

  function setState(cls) {
    resultCard.classList.remove(...STATES);
    stamp.classList.remove('stamp-in');
    if (cls) resultCard.classList.add(cls);
  }

  function reset() {
    highlightedText.hidden = true; highlightedText.innerHTML = '';
    highlightLegend.hidden = true;
    sourceBadge.hidden = true; sourceBadge.textContent = ''; sourceBadge.className = 'source-badge';
    translationPanel.hidden = true;
    originalLabel.textContent = 'Original';
    originalTextDisplay.textContent = '';
    translatedTextDisplay.textContent = '';
    rec.hidden = true; rec.textContent = '';
    confidenceBadge.hidden = true; confidenceBadge.textContent = '';
    scoreMeter.hidden = true;
    responseTime.hidden = true; responseTime.textContent = '';
    checkAnotherBtn.hidden = true;
  }

  function loading() {
    setState('is-loading');
    reset();
    resultTitle.textContent = 'Checking…';
    resultSubtitle.textContent = 'Running the message through the model…';
  }

  function fail(message) {
    setState('is-error');
    reset();
    resultTitle.textContent = 'Check failed';
    resultSubtitle.textContent = (message ? message + ' ' : '') +
      'Make sure you opened the app at http://127.0.0.1:5000 and tap Check Now to try again.';
  }

  function esc(s) {
    const d = document.createElement('div');
    d.textContent = s;
    return d.innerHTML;
  }

  function escapeRegExp(str) {
    return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  }

  function extractDomain(url) {
    try {
      const withScheme = /^https?:\/\//i.test(url) ? url : 'http://' + url;
      return new URL(withScheme).hostname.replace(/^www\./i, '');
    } catch {
      return url;
    }
  }

  function classifySource(score) {
    if (score >= 70) return { cls: 'is-credible', label: 'Credible source' };
    if (score <= 30) return { cls: 'is-suspicious', label: 'Suspicious source' };
    return { cls: 'is-unknown', label: 'Unknown source' };
  }

  function buildHighlightedHTML(text, fakeWords, realWords) {
    const wordMap = new Map();
    (fakeWords || []).forEach((w) => {
      const word = Array.isArray(w) ? w[0] : w && w.word;
      if (word) wordMap.set(String(word).toLowerCase(), 'hl-fake');
    });
    (realWords || []).forEach((w) => {
      const word = Array.isArray(w) ? w[0] : w && w.word;
      if (word) wordMap.set(String(word).toLowerCase(), 'hl-real');
    });

    if (wordMap.size === 0) return esc(text);

    const pattern = new RegExp(
      '\\b(' + Array.from(wordMap.keys()).map(escapeRegExp).join('|') + ')\\b',
      'gi'
    );

    return esc(text).replace(pattern, (match) => {
      const cls = wordMap.get(match.toLowerCase());
      return cls ? `<span class="${cls}">${match}</span>` : match;
    });
  }

  function updateMeter(trustScore, verdict) {
    const percent = Math.round(trustScore * 100);
    const offset = CIRCUMFERENCE - (percent / 100) * CIRCUMFERENCE;
    const color = verdict === 'false' ? 'var(--red)' : verdict === 'true' ? 'var(--green)' : 'var(--amber)';

    scoreMeter.hidden = false;
    meterFill.style.stroke = color;
    meterPercent.textContent = percent + '%';
    meterFill.style.strokeDashoffset = CIRCUMFERENCE;
    requestAnimationFrame(() => {
      requestAnimationFrame(() => { meterFill.style.strokeDashoffset = offset; });
    });
  }

  function render(data, sourceUrl, elapsedMs) {
    const verdict = VERDICT_LABEL[data.verdict] ? data.verdict : 'unverified';

    setState(VERDICT_CLASS[verdict]);
    resultTitle.textContent = VERDICT_LABEL[verdict];
    updateMeter(data.trust_score, verdict);
    requestAnimationFrame(() => stamp.classList.add('stamp-in'));

    let summary;
    if (data.note) {
      summary = data.note;
    } else if (verdict === 'false') {
      summary = 'Our model matched this to patterns seen in false or misleading content.';
    } else if (verdict === 'true') {
      summary = 'Our model matched this to patterns seen in reliable reporting.';
    } else {
      summary = 'The signals are mixed, so we cannot call this one either way.';
    }
    if (data.detected_language && data.detected_language !== 'en') {
      summary += ` (translated from ${data.detected_language})`;
    }
    resultSubtitle.textContent = summary;

    if (data.confidence_level) {
      confidenceBadge.textContent = data.confidence_level.toLowerCase() + ' confidence';
      confidenceBadge.hidden = false;
    }

    if (data.source_score !== null && data.source_score !== undefined) {
      const domain = sourceUrl ? extractDomain(sourceUrl) : '';
      const { cls, label } = classifySource(data.source_score);
      sourceBadge.textContent = domain ? `${label} · ${domain}` : label;
      sourceBadge.className = 'source-badge ' + cls;
      sourceBadge.hidden = false;
    }

    if (data.detected_language && data.detected_language !== 'en' && data.translated_text) {
      originalLabel.textContent = '🌐 Original (' + data.detected_language.toUpperCase() + ')';
      originalTextDisplay.textContent = data.original_text;
      translatedTextDisplay.textContent = data.translated_text;
      translationPanel.hidden = false;
    }

    const sourceText = data.translated_text || data.original_text || '';
    const fakeWords = (data.highlights && data.highlights.fake_words) || [];
    const realWords = (data.highlights && data.highlights.real_words) || [];

    if (sourceText && (fakeWords.length || realWords.length)) {
      highlightedText.innerHTML = buildHighlightedHTML(sourceText, fakeWords, realWords);
      highlightedText.hidden = false;
      highlightLegend.hidden = false;
    }

    rec.textContent = verdict === 'true'
      ? 'Still worth a second source before forwarding.'
      : 'Avoid forwarding until verified by a trusted fact-checking source.';
    rec.hidden = false;

    if (typeof elapsedMs === 'number') {
      responseTime.textContent = 'Analysed in ' + (elapsedMs / 1000).toFixed(1) + 's';
      responseTime.hidden = false;
    }
    checkAnotherBtn.hidden = false;
  }

  function busy(isBusy) {
    checkBtn.disabled = isBusy;
    checkBtn.setAttribute('aria-busy', isBusy ? 'true' : 'false');
    btnLabel.textContent = isBusy ? 'Checking…' : 'Check Now';
    btnIcon.classList.toggle('spin', isBusy);
  }

  async function check() {
    const message = messageInput.value.trim();
    const url = urlInput.value.trim();
    if (!message) {
      messageInput.classList.add('is-invalid');
      inputError.hidden = false;
      messageInput.focus();
      return;
    }
    messageInput.classList.remove('is-invalid');
    inputError.hidden = true;
    busy(true);
    loading();
    const startedAt = performance.now();

    try {
      const res = await fetch('/api/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: message, source_url: url })
      });
      const data = await res.json();
      if (!res.ok || data.error) throw new Error(data.error || 'status ' + res.status);
      render(data, url, performance.now() - startedAt);
    } catch (err) {
      console.error('TruthLens check failed:', err);
      fail(err.message);
    } finally {
      busy(false);
    }
  }

  checkBtn.addEventListener('click', check);
  checkAnotherBtn.addEventListener('click', () => {
    messageInput.value = '';
    urlInput.value = '';
    messageInput.classList.remove('is-invalid');
    inputError.hidden = true;
    setState(null);
    reset();
    resultTitle.textContent = 'Ready';
    resultSubtitle.textContent = 'Paste a message above and tap Check Now.';
    messageInput.focus();
  });
  messageInput.addEventListener('input', () => {
    if (messageInput.value.trim()) {
      messageInput.classList.remove('is-invalid');
      inputError.hidden = true;
    }
  });
  messageInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) { e.preventDefault(); check(); }
  });
})();