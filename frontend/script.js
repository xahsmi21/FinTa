// ============================================
// CONFIGURATION
// ============================================
const API_BASE = 'http://localhost:8000/api';

// ============================================
// STATE VARIABLES
// ============================================
let currentZoom = 100;
let userLevel = '';
let currentUser = null;

// ============================================
// AUTHENTICATION
// ============================================
async function handleAuth() {
  const isLogin = document.getElementById('tab-login').classList.contains('active');
  const email = document.getElementById(isLogin ? 'login-email' : 'signup-email').value;
  const password = document.getElementById(isLogin ? 'login-password' : 'signup-password').value;
  const name = document.getElementById('signup-name')?.value;

  const endpoint = isLogin ? `${API_BASE}/auth/login` : `${API_BASE}/auth/register`;
  const body = isLogin ? { email, password } : { email, password, name };

  try {
    const res = await fetch(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    });
    const data = await res.json();

    if (res.ok) {
      localStorage.setItem('token', data.access_token);
      localStorage.setItem('user', JSON.stringify(data.user));
      currentUser = data.user;
      navigate('level-view');
    } else {
      alert(data.detail || 'Authentication failed.');
    }
  } catch (err) {
    alert('❌ Server error. Is the backend running on port 8000?');
    console.error(err);
  }
}

function logout() {
  localStorage.removeItem('token');
  localStorage.removeItem('user');
  currentUser = null;
  document.getElementById('app-shell').style.display = 'none';
  navigate('auth-view');
}

// ============================================
// LEVEL SELECTION
// ============================================
function selectLevel(lvl) {
  document.querySelectorAll('.level-card').forEach(c => c.classList.remove('selected'));
  document.getElementById(`level-${lvl}`).classList.add('selected');
  userLevel = lvl;
  document.getElementById('level-continue').removeAttribute('disabled');
}

async function confirmLevel() {
  const token = localStorage.getItem('token');
  if (!token) {
    alert('Please login first.');
    return;
  }

  try {
    const res = await fetch(`${API_BASE}/user/level`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({ level: userLevel })
    });

    if (res.ok) {
      const user = await res.json();
      currentUser = user;
      localStorage.setItem('user', JSON.stringify(user));
      document.getElementById('app-shell').style.display = 'flex';
      document.getElementById('level-view').classList.remove('active');
      const levelText = userLevel.charAt(0).toUpperCase() + userLevel.slice(1);
      document.getElementById('sidebar-level-name').innerText = ` ${levelText}`;
      document.getElementById('report-level').innerText = levelText;
      navigate('dashboard-view');
    } else {
      const err = await res.json();
      alert(err.detail || 'Failed to save level.');
    }
  } catch (err) {
    alert('❌ Server error. Is the backend running?');
    console.error(err);
  }
}

// ============================================
// NAVIGATION
// ============================================
function navigate(viewId) {
  document.querySelectorAll('.view').forEach(el => el.classList.remove('active'));
  document.getElementById(viewId).classList.add('active');
  if(viewId === 'dashboard-view') renderCases();
  if(viewId === 'report-view') loadReport();
  document.querySelectorAll('.sidebar-nav button').forEach(btn => btn.classList.remove('active'));
  if(viewId === 'dashboard-view') document.getElementById('nav-dashboard').classList.add('active');
  else if (viewId === 'report-view') document.getElementById('nav-report').classList.add('active');
}

function switchAuthTab(tab) {
  document.querySelectorAll('.tab-switch button').forEach(b => b.classList.remove('active'));
  document.querySelectorAll('.auth-form-panel').forEach(p => p.classList.remove('active'));
  document.getElementById(`tab-${tab}`).classList.add('active');
  document.getElementById(`${tab}-panel`).classList.add('active');
}

// ============================================
// DASHBOARD (Cases)
// ============================================
async function renderCases() {
  const token = localStorage.getItem('token');
  if (!token) {
    alert('Please login first.');
    return;
  }

  try {
    const res = await fetch(`${API_BASE}/cases`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });

    if (res.ok) {
      const cases = await res.json();
      renderCasesUI(cases);
    } else {
      const err = await res.json();
      alert(err.detail || 'Failed to load cases.');
    }
  } catch (err) {
    alert('❌ Server error. Is the backend running?');
    console.error(err);
  }
}

function renderCasesUI(cases) {
  const container = document.getElementById('cases-grid');
  container.innerHTML = '';
  let completed = 0;
  cases.forEach(c => {
    if(c.score !== null) completed++;
    let tagClass = c.level === 'Easy' ? 'tag-easy' : 'tag-medium';
    let lockHtml = c.status === 'locked' ? `<span class="lock">🔒 Locked</span>` : `<span class="score">${c.score !== null ? c.score + '%' : 'Start Case →'}</span>`;
    let cardHTML = `
      <div class="case-card ${c.status}" onclick="${c.status === 'unlocked' ? `loadCase(${c.id})` : ''}">
        <div class="tag-row"><span class="tag ${tagClass}">${c.level}</span></div>
        <h3>${c.title}</h3>
        <p>${c.description}</p>
        <div class="card-foot">${lockHtml}</div>
      </div>
    `;
    container.innerHTML += cardHTML;
  });
  document.getElementById('dash-count').innerText = `${completed} / ${cases.length} completed`;
  document.getElementById('dash-bar-fill').style.width = `${(completed/cases.length)*100}%`;
}

// ============================================
// WORKSPACE (Submit Case)
// ============================================
async function loadCase(id) {
  const token = localStorage.getItem('token');
  if (!token) return;

  try {
    const res = await fetch(`${API_BASE}/cases/${id}/detail`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    if (!res.ok) throw new Error('Failed to load case');
    const caseData = await res.json();

    // Store case data globally
    window.currentCase = caseData;
    window.expectedAnswers = caseData.expected;

    // Set title, description, level
    document.getElementById('ws-title').innerText = caseData.title;
    document.getElementById('ws-brief').innerText = caseData.description;
    document.getElementById('task-brief-body').innerText = caseData.description;
    const levelTag = caseData.level.toLowerCase();
    document.getElementById('ws-tags').innerHTML = `<span class="tag tag-${levelTag}">${caseData.level}</span>`;

    // Build input fields dynamically from expected keys
    const sheetBody = document.getElementById('sheet-body');
    // Remove existing input rows (keep the header rows and the first rows with revenue, cogs)
    const inputRows = sheetBody.querySelectorAll('.cell-input-wrap');
    inputRows.forEach(row => row.closest('tr').remove());

    const expectedKeys = Object.keys(caseData.expected);
    // Add a row for each expected field
    expectedKeys.forEach(key => {
      const label = key.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase());
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>${label}</td>
        <td></td>
        <td><div class="cell-input-wrap"><input type="number" id="input-${key}" data-field="${key}"></div></td>
        <td></td>
      `;
      sheetBody.appendChild(tr);
    });

    // Update checklist
    const checklist = document.getElementById('checklist-body');
    checklist.innerHTML = expectedKeys.map(key => 
      `<button><div class="check-dot"></div>Calculate ${key.replace(/([A-Z])/g, ' $1').trim()}</button>`
    ).join('');

    // Navigate to workspace
    document.getElementById('workspace-view').dataset.caseId = id;
    navigate('workspace-view');

  } catch (err) {
    alert('Failed to load case: ' + err.message);
    console.error(err);
  }
}
async function evaluateAI() {
  const token = localStorage.getItem('token');
  if (!token) {
    alert('Please login first.');
    return;
  }

  const caseId = parseInt(document.getElementById('workspace-view').dataset.caseId) || 1;
  const inputs = document.querySelectorAll('#sheet-body .cell-input-wrap input[type="number"]');
  const answers = {};
  inputs.forEach(inp => {
    const field = inp.dataset.field;
    answers[field] = parseFloat(inp.value) || 0;
  });

  try {
    const res = await fetch(`${API_BASE}/submissions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({ case_id: caseId, answers })
    });

    if (res.ok) {
      const data = await res.json();
      displayFeedback(data, answers);
    } else {
      const err = await res.json();
      alert(err.detail || 'Submission failed.');
    }
  } catch (err) {
    alert('❌ Server error. Is the backend running?');
    console.error(err);
  }
}

function displayFeedback(data, answers) {
  const { score, feedback } = data;
  const expected = window.expectedAnswers || {};

  let compBody = '';
  for (const [field, correct] of Object.entries(expected)) {
    const userVal = answers[field] ?? 0;
    const isCorrect = userVal === correct;
    const statusClass = isCorrect ? 'status-ok' : 'status-bad';
    const icon = isCorrect ? '✅' : '❌';
    const formattedUser = userVal.toLocaleString();
    const formattedCorrect = correct.toLocaleString();
    compBody += `
      <tr>
        <td>${field.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase())}</td>
        <td class="${statusClass}">${formattedUser}</td>
        <td>${formattedCorrect}</td>
        <td>${icon}</td>
      </tr>
    `;
  }
  document.getElementById('compare-body').innerHTML = compBody;

  document.getElementById('errors-list').innerHTML = feedback.errors.map(e => `<li><div class="dot dot-red"></div>${e}</li>`).join('');
  document.getElementById('ai-explanation-list').innerHTML = feedback.explanations.map(e => `<li><div class="dot dot-green"></div>${e}</li>`).join('');
  document.getElementById('recommendations-list').innerHTML = feedback.recommendations.map(r => `<li><div class="dot dot-gold"></div>${r}</li>`).join('');

  document.getElementById('final-score').innerText = score + '%';
  document.getElementById('score-ring').style.setProperty('--pct', score);
  if (score === 100) {
    document.getElementById('score-word').innerText = "Excellent";
  } else if (score >= 80) {
    document.getElementById('score-word').innerText = "Good";
  } else if (score >= 60) {
    document.getElementById('score-word').innerText = "Needs Review";
  } else {
    document.getElementById('score-word').innerText = "Keep Practicing";
  }

  navigate('feedback-view');
}

// ============================================
// REPORT
// ============================================
async function goToReport() {
  navigate('report-view');
}

async function loadReport() {
  const token = localStorage.getItem('token');
  if (!token) return;
  try {
    const res = await fetch(`${API_BASE}/user/report`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    if (res.ok) {
      const data = await res.json();
      document.getElementById('report-score').innerText = data.averageScore + '%';
      document.getElementById('report-level').innerText = data.level.charAt(0).toUpperCase() + data.level.slice(1);
      document.getElementById('report-completed').innerText = `${data.completedCount} / ${data.totalCases}`;
    }
  } catch (err) {
    console.error('Failed to load report:', err);
  }
}

// ============================================
// SHEET TOOLS
// ============================================
function zoomSheet(amount) {
  currentZoom += amount;
  if(currentZoom < 50) currentZoom = 50;
  if(currentZoom > 150) currentZoom = 150;
  document.getElementById('zoom-label').innerText = currentZoom + '%';
  document.documentElement.style.setProperty('--sheet-zoom', currentZoom + '%');
}
function undoLast() {
  document.getElementById('input-gp').value = '';
  document.getElementById('input-ni').value = '';
  document.getElementById('autosave-status').innerText = 'Undone';
  setTimeout(() => document.getElementById('autosave-status').innerText = 'All changes saved', 1500);
}
function searchSheet(val) { console.log('Searching for:', val); }
function exportCSV() { alert('Exporting CSV...'); }
function saveNote() { 
  document.getElementById('autosave-status').innerText = 'Saving...';
  setTimeout(() => document.getElementById('autosave-status').innerText = 'All changes saved', 1000);
}

// ============================================
// INITIALIZATION
// ============================================
window.onload = function() {
  const token = localStorage.getItem('token');
  const userData = localStorage.getItem('user');
  if (token && userData) {
    try {
      currentUser = JSON.parse(userData);
      document.getElementById('app-shell').style.display = 'flex';
      document.getElementById('auth-view').classList.remove('active');
      const levelText = currentUser.level.charAt(0).toUpperCase() + currentUser.level.slice(1);
      document.getElementById('sidebar-level-name').innerText = ` ${levelText}`;
      document.getElementById('report-level').innerText = levelText;
      navigate('dashboard-view');
    } catch (e) {
      localStorage.removeItem('user');
    }
  }
};