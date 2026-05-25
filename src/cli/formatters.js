const ANSI = {
    reset: '\x1b[0m',
    bold: '\x1b[1m',
    red: '\x1b[31m',
    green: '\x1b[32m',
    yellow: '\x1b[33m',
    blue: '\x1b[34m',
    magenta: '\x1b[35m',
    cyan: '\x1b[36m',
};

function color(str, color) {
    return color ? ANSI[color] + str + ANSI.reset : str;
}

function pad(str, len) {
    return String(str).padEnd(len);
}

function formatTable(tasks) {
    if (!tasks.length) return console.log('No tasks.');
    const headers = ['ID','Description','Priority','Status','Due','Created','Completed'];
    const colWidths = [14, 24, 10, 10, 14, 21, 21];
    let out = headers.map((h,i) => pad(h,colWidths[i])).join(' | ');
    out = color(out, 'bold');
    console.log(out);
    console.log('-'.repeat(out.length));
    for (const t of tasks) {
        const cols = [
            t.id,
            pad((t.description||'').slice(0,22),22),
            pad(t.priority,8),
            t.status==='completed'?color('✔','green'):color(t.status,'yellow'),
            t.due ? t.due.slice(0,10) : '-',
            t.created.slice(0,19),
            t.completed ? t.completed.slice(0,19) : '-',
        ];
        console.log(cols.map((v,i) => pad(v,colWidths[i])).join(' | '));
    }
}

function printProgress(tasks) {
    const total = tasks.length;
    const done = tasks.filter(t => t.status === 'completed').length;
    const bar = Math.round((done / (total||1)) * 30);
    console.log(
        'Progress: [' + color('■'.repeat(bar),'green') + color('■'.repeat(30-bar),'red') + `] ${done}/${total}`
    );
}

function printGantt(tasks) {
    const withDue = tasks.filter(t => t.due);
    if (!withDue.length) return;
    console.log('Timeline:');
    for (const t of withDue) {
        const due = new Date(t.due), now = new Date();
        const daysDiff = Math.round((due-now)/(1000*60*60*24));
        let bar = '';
        if (daysDiff < 0) bar = color('⏰ Overdue','red');
        else bar = color('▉'.repeat(Math.max(1,10-daysDiff)),'blue');
        console.log(`  [${due.toISOString().slice(0,10)}] ${bar} ${t.description}`);
    }
}

module.exports = { formatTable, printProgress, printGantt, color };
