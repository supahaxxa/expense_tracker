const types = ["Beverages", "B&L", "Entertainment", "Household", "Others", "Restaurant", "Services", "Food", "Stationery", "Transport", "Utility"];
let appTheme = 'Light';

// Pagination Variables
let currentPage = 1;
const rowsPerPage = 50;

document.addEventListener('DOMContentLoaded', () => {
    loadConfig();
    populateTypesDropdown();
    setupNavigation();
    
    document.getElementById('btn-record').addEventListener('click', onRecordClick);
    
    // Logs Import/Export Listeners
    document.getElementById('btn-export-logs').addEventListener('click', exportLogsToCSV);
    document.getElementById('btn-import-logs').addEventListener('click', () => {
        document.getElementById('import-file').click();
    });
    document.getElementById('import-file').addEventListener('change', importLogsFromCSV);
    
    // Pagination Listeners
    document.getElementById('btn-prev-page').addEventListener('click', prevPage);
    document.getElementById('btn-next-page').addEventListener('click', nextPage);
});

function loadConfig() {
    const savedConfig = JSON.parse(localStorage.getItem('expenseConfig')) || {};
    if (savedConfig.theme) {
        appTheme = savedConfig.theme;
    }
    applyTheme();
}

function applyTheme() {
    if (appTheme === 'Dark') {
        document.documentElement.setAttribute('data-theme', 'dark');
    } else {
        document.documentElement.removeAttribute('data-theme');
    }
    const themeSubtitle = document.getElementById('set-theme');
    if (themeSubtitle) themeSubtitle.innerText = appTheme;
}

function toggleTheme() {
    appTheme = (appTheme === 'Light') ? 'Dark' : 'Light';
    
    const currentConfig = JSON.parse(localStorage.getItem('expenseConfig')) || {};
    currentConfig.theme = appTheme;
    localStorage.setItem('expenseConfig', JSON.stringify(currentConfig));
    
    applyTheme();
}

function populateTypesDropdown() {
    const select = document.getElementById('input-type');
    types.forEach((type, index) => {
        const option = document.createElement('option');
        option.value = index; 
        option.text = type;
        select.appendChild(option);
    });
}

function setupNavigation() {
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => {
        item.addEventListener('click', (e) => {
            document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
            document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
            
            const target = item.closest('.nav-item').getAttribute('data-target');
            item.closest('.nav-item').classList.add('active');
            document.getElementById(target).classList.add('active');

            if(target === 'page-logs') renderLogsTable();
            if(target === 'page-query') renderQueryPage();
        });
    });
}

function onRecordClick() {
    const amount = document.getElementById('input-amount').value;
    const typeIdx = document.getElementById('input-type').value;
    const detail = document.getElementById('input-detail').value;

    document.getElementById('error-amount').innerText = !amount ? "ERROR: enter an integer" : "";
    document.getElementById('error-type').innerText = typeIdx === "" ? "ERROR: please select a category" : "";
    document.getElementById('error-detail').innerText = !detail ? "ERROR: please enter the detail of your expenditure" : "";

    if (!amount || typeIdx === "" || !detail) return;

    // Directly save and alert the user without asking for confirmation
    saveRecord(amount, typeIdx, detail);
    
    document.getElementById('input-amount').value = "";
    document.getElementById('input-type').value = "";
    document.getElementById('input-detail').value = "";
    
    alert("Entry successfully recorded.");
}

function saveRecord(amount, typeIdx, detail) {
    let logs = JSON.parse(localStorage.getItem('expenseLogs')) || [];
    const date = new Date();
    const today = `${date.getFullYear()}${String(date.getMonth()+1).padStart(2,'0')}${String(date.getDate()).padStart(2,'0')}T${String(date.getHours()).padStart(2,'0')}${String(date.getMinutes()).padStart(2,'0')}`;
    
    // Automatically determine next ID based on highest existing ID
    const nextId = logs.length > 0 ? Math.max(...logs.map(l => l.id)) + 1 : 0;
    
    logs.push({
        id: nextId,
        time: today,
        amount: parseInt(amount),
        type: parseInt(typeIdx),
        detail: detail
    });
    localStorage.setItem('expenseLogs', JSON.stringify(logs));
}

// ----------------- Deletion Logic -----------------

function deleteLog(logId) {
    if (confirm("Are you sure you want to delete this entry?")) {
        let logs = JSON.parse(localStorage.getItem('expenseLogs')) || [];
        logs = logs.filter(l => l.id !== logId);
        localStorage.setItem('expenseLogs', JSON.stringify(logs));
        
        // Adjust pagination if the current page becomes empty
        const totalPages = Math.ceil(logs.length / rowsPerPage) || 1;
        if (currentPage > totalPages) currentPage = totalPages;
        
        renderLogsTable();
    }
}

// ----------------- Pagination & Table Render Logic -----------------

function makeEditable(cell, logId, field) {
    cell.addEventListener('click', () => {
        if (cell.querySelector('.edit-input')) return;

        const currentValue = cell.innerText;
        cell.innerHTML = '';
        
        let input;
        if (field === 'type') {
            input = document.createElement('select');
            input.className = 'edit-input';
            types.forEach((t, idx) => {
                const opt = document.createElement('option');
                opt.value = idx;
                opt.text = t;
                if (t === currentValue) opt.selected = true;
                input.appendChild(opt);
            });
        } else {
            input = document.createElement('input');
            input.type = field === 'amount' ? 'number' : 'text';
            input.value = currentValue;
            input.className = 'edit-input';
        }
        
        let isSaved = false;
        const saveEdit = () => {
            if (isSaved) return; 
            isSaved = true;
            
            let logs = JSON.parse(localStorage.getItem('expenseLogs')) || [];
            const logIndex = logs.findIndex(l => l.id === logId);
            
            if (logIndex > -1) {
                if (field === 'type') {
                    logs[logIndex][field] = parseInt(input.value);
                } else if (field === 'amount') {
                    logs[logIndex][field] = parseInt(input.value) || 0;
                } else {
                    logs[logIndex][field] = input.value;
                }
                localStorage.setItem('expenseLogs', JSON.stringify(logs));
            }
            renderLogsTable();
        };

        input.addEventListener('blur', saveEdit);
        input.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                input.blur(); 
            }
        });

        cell.appendChild(input);
        input.focus();
    });
}

function renderLogsTable() {
    const logs = JSON.parse(localStorage.getItem('expenseLogs')) || [];
    const tbody = document.querySelector('#table-logs tbody');
    tbody.innerHTML = "";
    
    const totalPages = Math.ceil(logs.length / rowsPerPage) || 1;
    if (currentPage > totalPages) currentPage = totalPages;
    
    const startIndex = (currentPage - 1) * rowsPerPage;
    const endIndex = Math.min(startIndex + rowsPerPage, logs.length);
    const paginatedLogs = logs.slice(startIndex, endIndex);

    paginatedLogs.forEach(log => {
        const tr = document.createElement('tr');
        
        const tdId = document.createElement('td');
        tdId.innerText = log.id;
        
        const tdTime = document.createElement('td');
        tdTime.innerText = log.time;
        makeEditable(tdTime, log.id, 'time');
        
        const tdAmount = document.createElement('td');
        tdAmount.innerText = log.amount;
        makeEditable(tdAmount, log.id, 'amount');
        
        const tdType = document.createElement('td');
        tdType.innerText = types[log.type];
        makeEditable(tdType, log.id, 'type');
        
        const tdDetail = document.createElement('td');
        tdDetail.innerText = log.detail;
        makeEditable(tdDetail, log.id, 'detail');

        const tdAction = document.createElement('td');
        const deleteBtn = document.createElement('button');
        deleteBtn.innerHTML = '<span class="material-icons">delete</span>';
        deleteBtn.className = 'icon-btn delete-btn';
        deleteBtn.onclick = () => deleteLog(log.id);
        tdAction.appendChild(deleteBtn);
        
        tr.appendChild(tdId);
        tr.appendChild(tdTime);
        tr.appendChild(tdAmount);
        tr.appendChild(tdType);
        tr.appendChild(tdDetail);
        tr.appendChild(tdAction);
        
        tbody.appendChild(tr);
    });
    
    // Update Pagination UI
    document.getElementById('page-indicator').innerText = `Page ${currentPage} of ${totalPages}`;
    document.getElementById('btn-prev-page').disabled = currentPage === 1;
    document.getElementById('btn-next-page').disabled = currentPage === totalPages;
}

function prevPage() {
    if (currentPage > 1) {
        currentPage--;
        renderLogsTable();
    }
}

function nextPage() {
    const logs = JSON.parse(localStorage.getItem('expenseLogs')) || [];
    const totalPages = Math.ceil(logs.length / rowsPerPage) || 1;
    if (currentPage < totalPages) {
        currentPage++;
        renderLogsTable();
    }
}

// ----------------- Export / Import CSV Logic -----------------

function exportLogsToCSV() {
    const logs = JSON.parse(localStorage.getItem('expenseLogs')) || [];
    if (logs.length === 0) {
        alert("No logs to export.");
        return;
    }

    const csvRows = logs.map(log => `${log.id},${log.time},${log.amount},${log.type},${log.detail}`);
    const csvString = csvRows.join('\n');
    
    const blob = new Blob([csvString], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    
    const a = document.createElement('a');
    a.href = url;
    a.download = 'logs.csv';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

function importLogsFromCSV(event) {
    const file = event.target.files[0];
    if (!file) return;

    if (confirm("Importing will overwrite your existing logs. Are you sure?")) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const text = e.target.result;
            const lines = text.split('\n');
            const newLogs = [];
            
            lines.forEach((line, index) => {
                if (!line.trim()) return; 
                const parts = line.split(',');
                if (parts.length >= 5) {
                    newLogs.push({
                        id: parseInt(parts[0]) || index,
                        time: parts[1],
                        amount: parseInt(parts[2]),
                        type: parseInt(parts[3]),
                        detail: parts.slice(4).join(',') 
                    });
                }
            });

            localStorage.setItem('expenseLogs', JSON.stringify(newLogs));
            currentPage = 1; 
            renderLogsTable();
            alert('Logs imported successfully!');
        };
        reader.readAsText(file);
    }
    event.target.value = '';
}

// -------------------------------------------------------------

function renderQueryPage() {
    const logs = JSON.parse(localStorage.getItem('expenseLogs')) || [];
    let aggregated = {};

    logs.forEach(log => {
        const monthKey = log.time.substring(0, 6);
        if (!aggregated[monthKey]) {
            aggregated[monthKey] = {};
            types.forEach(t => aggregated[monthKey][t] = 0);
        }
        aggregated[monthKey][types[log.type]] += log.amount;
    });

    const select = document.getElementById('select-month');
    select.innerHTML = "";
    Object.keys(aggregated).forEach(key => {
        const option = document.createElement('option');
        option.value = key;
        option.text = timeFormatTransform(key);
        select.appendChild(option);
    });

    if (Object.keys(aggregated).length > 0) {
        select.onchange = () => renderSummaryTable(aggregated[select.value]);
        renderSummaryTable(aggregated[Object.keys(aggregated)[0]]);
    } else {
        document.querySelector('#table-summary tbody').innerHTML = "";
    }
}

function timeFormatTransform(yyyymm) {
    const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    const year = yyyymm.substring(0, 4);
    const month = parseInt(yyyymm.substring(4, 6)) - 1;
    return `${year}, ${months[month]}`;
}

function renderSummaryTable(monthData) {
    const tbody = document.querySelector('#table-summary tbody');
    tbody.innerHTML = "";
    let total = 0;
    
    Object.entries(monthData).forEach(([category, amount]) => {
        if(amount > 0) {
            total += amount;
            const tr = document.createElement('tr');
            tr.innerHTML = `<td>${category}</td><td>${amount}</td>`;
            tbody.appendChild(tr);
        }
    });

    const trTotal = document.createElement('tr');
    trTotal.innerHTML = `<td><strong>Total</strong></td><td><strong>${total}</strong></td>`;
    tbody.appendChild(trTotal);
}
