/* London Job Finder — frontend logic */

const PAGE_SIZE = 24;
let allJobs = [];
let displayedCount = 0;

// ── DOM refs ──
const searchBtn     = document.getElementById('search-btn');
const keywordInput  = document.getElementById('keyword-input');
const sourceFilter  = document.getElementById('source-filter');
const sortFilter    = document.getElementById('sort-filter');
const jobGrid       = document.getElementById('job-grid');
const loadingEl     = document.getElementById('loading');
const emptyEl       = document.getElementById('empty-state');
const errorBanner   = document.getElementById('error-banner');
const resultCount   = document.getElementById('result-count');
const loadMoreWrap  = document.getElementById('load-more-wrap');
const loadMoreBtn   = document.getElementById('load-more-btn');
const sourceStats   = document.getElementById('source-stats');
const template      = document.getElementById('job-card-template');

// ── Tag colours ──
const TAG_CLASSES = {
  'Graduate':       'tag-graduate',
  'Data & Analytics': 'tag-data',
  'Finance':        'tag-finance',
  'Banking':        'tag-banking',
  'Consulting':     'tag-consulting',
  'Quantitative':   'tag-quant',
};

// ── Fetch source metadata on load ──
async function loadSourceStats() {
  try {
    const res = await fetch('/api/sources');
    const data = await res.json();
    sourceStats.innerHTML = `
      Searching <strong>${data.total_companies}</strong> company career pages<br>
      🟦 Greenhouse: ${data.greenhouse_count} companies<br>
      🟣 Lever: ${data.lever_count} companies<br>
      🟠 Ashby: ${data.ashby_count} companies<br>
      🟩 Workday: ${data.workday_count} companies<br>
      ${data.adzuna_enabled ? '🟡 Adzuna: ✅ enabled' : '⚪ Adzuna: add API key'}
    `;
  } catch (e) { /* silent */ }
}

// ── Search ──
async function doSearch() {
  const keywords = keywordInput.value.trim()
    ? keywordInput.value.trim().split(/\s+/)
    : [];

  const checkedTags = [...document.querySelectorAll('.tag-filter:checked')]
    .map(el => el.value);

  const filters = {
    tags:   checkedTags.length < 6 ? checkedTags : [],  // empty = no tag filter
    source: sourceFilter.value || null,
  };

  // Show loading
  jobGrid.innerHTML = '';
  loadMoreWrap.classList.add('hidden');
  errorBanner.classList.add('hidden');
  emptyEl.classList.add('hidden');
  loadingEl.classList.remove('hidden');
  resultCount.textContent = '';
  searchBtn.disabled = true;
  searchBtn.textContent = 'Searching…';

  try {
    const res = await fetch('/api/search', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({ keywords, filters }),
    });

    const data = await res.json();
    allJobs = sortJobs(data.jobs || []);
    displayedCount = 0;

    loadingEl.classList.add('hidden');

    if (data.errors && data.errors.length) {
      errorBanner.textContent = `Note: some sources had errors — ${data.errors.join('; ')}`;
      errorBanner.classList.remove('hidden');
    }

    if (allJobs.length === 0) {
      emptyEl.classList.remove('hidden');
      resultCount.textContent = '0 results';
    } else {
      resultCount.textContent = `${allJobs.length} result${allJobs.length !== 1 ? 's' : ''}`;
      renderPage();
    }
  } catch (err) {
    loadingEl.classList.add('hidden');
    errorBanner.textContent = `Search failed: ${err.message}`;
    errorBanner.classList.remove('hidden');
  } finally {
    searchBtn.disabled = false;
    searchBtn.innerHTML = '<span class="btn-icon">&#x1F50D;</span> Search Jobs';
  }
}

// ── Sort ──
function sortJobs(jobs) {
  const mode = sortFilter.value;
  return [...jobs].sort((a, b) => {
    if (mode === 'company') return a.company.localeCompare(b.company);
    if (mode === 'title')   return a.title.localeCompare(b.title);
    // newest (default)
    return (a.days_ago ?? 999) - (b.days_ago ?? 999);
  });
}

function renderPage() {
  const slice = allJobs.slice(displayedCount, displayedCount + PAGE_SIZE);
  slice.forEach(job => jobGrid.appendChild(buildCard(job)));
  displayedCount += slice.length;

  if (displayedCount < allJobs.length) {
    loadMoreWrap.classList.remove('hidden');
    loadMoreBtn.textContent = `Load More (${allJobs.length - displayedCount} remaining)`;
  } else {
    loadMoreWrap.classList.add('hidden');
  }
}

// ── Build a job card from template ──
function buildCard(job) {
  const clone = template.content.cloneNode(true);

  // Avatar initials
  const avatar = clone.querySelector('.company-avatar');
  const initials = job.company
    .split(' ')
    .slice(0, 2)
    .map(w => w[0] || '')
    .join('')
    .toUpperCase();
  avatar.textContent = initials;
  avatar.style.background = avatarGradient(job.company);

  clone.querySelector('.company-name').textContent = job.company;
  clone.querySelector('.location-text').textContent = job.location;
  clone.querySelector('.job-title').textContent = job.title;

  if (job.department) {
    clone.querySelector('.department-line').textContent = job.department;
  }

  // Days badge
  const badge = clone.querySelector('.days-badge');
  const d = job.days_ago ?? 99;
  if (d <= 7)       { badge.textContent = d === 0 ? 'Today' : `${d}d ago`; badge.classList.add('fresh'); }
  else if (d <= 30) { badge.textContent = `${d}d ago`; badge.classList.add('recent'); }
  else              { badge.textContent = job.posted_date || `${d}d ago`; badge.classList.add('older'); }

  // Tags
  const tagsEl = clone.querySelector('.card-tags');
  (job.tags || []).forEach(tag => {
    const span = document.createElement('span');
    span.className = `tag ${TAG_CLASSES[tag] || 'tag-default'}`;
    span.textContent = tag;
    tagsEl.appendChild(span);
  });

  // Source
  const sourceColor = {
    Greenhouse: '#00b4d8',
    Lever:      '#6c63ff',
    Ashby:      '#ff9800',
    Workday:    '#2e7d32',
    Adzuna:     '#ff6b35',
  };
  clone.querySelector('.source-dot').style.background =
    sourceColor[job.source_system] || '#aaa';
  clone.querySelector('.source-text').textContent = job.source_system || 'Company';

  // Apply button
  const applyBtn = clone.querySelector('.apply-btn');
  applyBtn.href = job.url || '#';
  if (!job.url) applyBtn.style.opacity = '.4';

  return clone;
}

// Deterministic gradient per company name
function avatarGradient(name) {
  const palettes = [
    ['#0a2342','#1565c0'], ['#1b5e20','#388e3c'], ['#4a148c','#7b1fa2'],
    ['#bf360c','#e64a19'], ['#006064','#00838f'], ['#e65100','#f57c00'],
    ['#880e4f','#c2185b'], ['#1a237e','#303f9f'], ['#33691e','#558b2f'],
  ];
  let hash = 0;
  for (let i = 0; i < name.length; i++) hash = name.charCodeAt(i) + (hash << 5) - hash;
  const [a, b] = palettes[Math.abs(hash) % palettes.length];
  return `linear-gradient(135deg, ${a} 0%, ${b} 100%)`;
}

// ── Event listeners ──
searchBtn.addEventListener('click', doSearch);
loadMoreBtn.addEventListener('click', renderPage);

keywordInput.addEventListener('keydown', e => {
  if (e.key === 'Enter') doSearch();
});

sortFilter.addEventListener('change', () => {
  if (allJobs.length) {
    allJobs = sortJobs(allJobs);
    jobGrid.innerHTML = '';
    displayedCount = 0;
    renderPage();
  }
});

// ── Init ──
loadSourceStats();
doSearch();  // auto-search on page load with default filters
