const WORDLIST = ['www', 'mail', 'ftp', 'admin', 'test', 'blog', 'dev', 'shop', 'api', 'cdn', 'static', 'media', 'secure', 'mobile', 'app', 'support', 'help', 'news', 'forum', 'store', 'beta', 'demo', 'portal', 'login', 'dashboard', 'cpanel', 'webmail', 'mx', 'ns1', 'ns2', 'pop', 'smtp', 'imap', 'staging', 'prod'];
let scanResults = [], currentDomain = '';
function mockIP() { return `${~~(Math.random() * 256)}.${~~(Math.random() * 256)}.${~~(Math.random() * 256)}.${~~(Math.random() * 256)}`; }
function mockResult(sub, dom) { let f = Math.random() > .65; return f ? { subdomain: `${sub}.${dom}`, ip: mockIP(), status: Math.random() > .2 ? 200 : 404, found: 1 } : { subdomain: `${sub}.${dom}`, found: 0 }; }
function logMsg(msg, t) { let d = document.getElementById('scanLog'), e = document.createElement('div'); e.className = 'log-entry' + (t ? ' ' + t : ''); e.textContent = `[${new Date().toLocaleTimeString()}] ${msg}`; d.appendChild(e); d.scrollTop = d.scrollHeight; }
function updProg(c, t) { let p = Math.round(c / t * 100); document.getElementById('progressBar').style.width = p + '%'; document.getElementById('progressText').textContent = `${c}/${t} (${p}%)`; }
function updStats() { let f = scanResults.filter(r => r.found).length, n = scanResults.length - f; document.getElementById('totalScanned').textContent = scanResults.length; document.getElementById('totalFound').textContent = f; document.getElementById('totalNotFound').textContent = n; }
function showResult(r) { if (r.found) { let d = document.createElement('div'); d.className = 'subdomain-card'; d.innerHTML = `<span class="subdomain-name">${r.subdomain}</span> <span class="found-badge">✓</span><br><small>IP: ${r.ip} | Status: ${r.status}</small>`; document.getElementById('subdomainsList').appendChild(d); } }
async function startScan() {
    let domain = document.getElementById('domainInput').value.trim(), btn = document.getElementById('scanBtn');
    if (!domain) return alert('Enter a domain');
    scanResults = [];['subdomainsList', 'scanLog'].forEach(id => document.getElementById(id).innerHTML = '');
    document.getElementById('progressSection').style.display = 'block';
    document.getElementById('resultsSection').style.display = 'block';
    btn.disabled = 1; btn.textContent = 'Scanning...'; currentDomain = domain;
    logMsg(`Starting scan for: ${domain}`, 'success'); logMsg(`Total: ${WORDLIST.length}`); logMsg('='.repeat(30));
    for (let i = 0; i < WORDLIST.length; i++) {
        let sub = WORDLIST[i], full = `${sub}.${domain}`; document.getElementById('currentScan').textContent = `Checking: ${full}`;
        logMsg(`Checking ${i + 1}/${WORDLIST.length}: ${full}`);
        await new Promise(r => setTimeout(r, 80));
        let res = mockResult(sub, domain); scanResults.push(res);
        if (res.found) { logMsg(`FOUND! ${res.subdomain} (${res.ip}) - ${res.status}`, 'success'); showResult(res); }
        else logMsg(`Not found: ${res.subdomain}`, 'error');
        updProg(i + 1, WORDLIST.length); updStats();
    }
    document.getElementById('currentScan').textContent = 'Scan completed!';
    logMsg('='.repeat(30)); logMsg(`Scan completed! Found ${scanResults.filter(r => r.found).length}.`, 'success');
    btn.disabled = 0; btn.textContent = 'Start New Scan';
}
function downloadResults() {
    let found = scanResults.filter(r => r.found); if (!found.length) return alert('No results');
    let c = `Subdomain Scan Results for: ${currentDomain}\nScan Date: ${new Date().toLocaleString()}\nTotal Found: ${found.length}\n${'='.repeat(30)}\n\n`;
    found.forEach((r, i) => { c += `${i + 1}. ${r.subdomain}\n   IP: ${r.ip}\n   Status: ${r.status}\n${'-'.repeat(20)}\n`; });
    let blob = new Blob([c], { type: 'text/plain' }), url = URL.createObjectURL(blob), a = document.createElement('a');
    a.href = url; a.download = `subdomains_${currentDomain}_${Date.now()}.txt`; document.body.appendChild(a); a.click(); a.remove(); URL.revokeObjectURL(url);
}
document.getElementById('domainInput').addEventListener('keypress', e => { if (e.key === 'Enter') startScan(); });
document.getElementById('domainInput').focus();
