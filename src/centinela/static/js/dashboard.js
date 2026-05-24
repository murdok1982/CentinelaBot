async function fetchAPI(url) {
    const headers = {'Accept': 'application/json'};
    const token = localStorage.getItem('token');
    if (token) headers['Authorization'] = `Bearer ${token}`;
    const res = await fetch(url, {headers});
    return res.ok ? res.json() : null;
}

async function loadDashboard() {
    const data = await fetchAPI('/api/dashboard');
    if (!data) return;
    document.getElementById('statThreats').textContent = data.statistics?.threats_detected_today ?? '-';
    document.getElementById('statAlerts').textContent = data.statistics?.alerts_active ?? '-';
    document.getElementById('statEvents').textContent = data.statistics?.events_processed ?? '-';
    const score = data.statistics?.security_score ?? 0;
    const el = document.getElementById('statScore');
    el.textContent = score + '/100';
    el.className = 'stat-value' + (score < 40 ? ' danger' : score < 70 ? ' warning' : '');

    const badge = document.getElementById('statusBadge');
    if (data.system_status === 'operational') {
        badge.textContent = 'Sistema Operativo';
        badge.style.background = '#22c55e';
    } else {
        badge.textContent = 'Incidente';
        badge.style.background = '#ef4444';
    }

    const types = data.threat_distribution || {};
    new Chart(document.getElementById('threatChart'), {
        type: 'doughnut',
        data: {
            labels: Object.keys(types),
            datasets: [{
                data: Object.values(types),
                backgroundColor: ['#ef4444', '#f97316', '#f59e0b', '#22d3ee', '#22c55e'],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { labels: { color: '#94a3b8' } } }
        }
    });

    const sev = data.severity_breakdown || {};
    new Chart(document.getElementById('severityChart'), {
        type: 'bar',
        data: {
            labels: Object.keys(sev),
            datasets: [{
                label: 'Alertas',
                data: Object.values(sev),
                backgroundColor: ['#ef4444', '#f97316', '#f59e0b', '#22c55e'],
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { display: false } },
            scales: {
                y: { beginAtZero: true, ticks: { color: '#94a3b8' }, grid: { color: '#1e293b' } },
                x: { ticks: { color: '#94a3b8' }, grid: { display: false } }
            }
        }
    });
}

async function loadHealth() {
    const data = await fetchAPI('/api/health');
    if (!data) return;
    document.querySelectorAll('.module-item').forEach(el => el.remove());
    const grid = document.getElementById('moduleGrid');
    if (data.modules) {
        for (const [name, healthy] of Object.entries(data.modules)) {
            const div = document.createElement('div');
            div.className = 'module-item';
            div.innerHTML = `<span>${name}</span><span class="status-dot ${healthy ? 'online' : 'offline'}"></span>`;
            grid.appendChild(div);
        }
    }
}

async function loadAlerts() {
    const data = await fetchAPI('/api/alerts');
    const tbody = document.getElementById('alertsBody');
    if (!data || !data.alerts || data.alerts.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6">No hay alertas activas</td></tr>';
        return;
    }
    tbody.innerHTML = data.alerts.map(a => `
        <tr class="alert-row" data-severity="${a.severity}">
            <td>${a.id}</td>
            <td>${a.title}</td>
            <td class="severity-${a.severity}">${a.severity.toUpperCase()}</td>
            <td>${a.status}</td>
            <td>${a.source || '-'}</td>
            <td>${new Date(a.created_at).toLocaleString()}</td>
        </tr>
    `).join('');
}

function filterAlerts() {
    const q = (document.getElementById('filterSearch')?.value || '').toLowerCase();
    const s = document.getElementById('filterSeverity')?.value || '';
    document.querySelectorAll('.alert-row').forEach(row => {
        const text = row.textContent.toLowerCase();
        const sev = row.dataset.severity;
        const matchText = !q || text.includes(q);
        const matchSev = !s || sev === s;
        row.style.display = matchText && matchSev ? '' : 'none';
    });
}

if (document.getElementById('statThreats')) loadDashboard();
if (document.getElementById('moduleGrid')) loadHealth();
if (document.getElementById('alertsBody')) loadAlerts();
