#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const { formatTable, printProgress, printGantt } = require('./formatters');

const TASKS_FILE = path.join(__dirname, 'tasks.json');

function loadTasks() {
    if (!fs.existsSync(TASKS_FILE)) return [];
    return JSON.parse(fs.readFileSync(TASKS_FILE, 'utf8'));
}

function saveTasks(tasks) {
    fs.writeFileSync(TASKS_FILE, JSON.stringify(tasks, null, 2));
}

function addTask(description, priority, due) {
    const tasks = loadTasks();
    const newTask = {
        id: Date.now(),
        description,
        priority: priority || 'medium',
        due: due ? new Date(due).toISOString() : null,
        status: 'pending',
        created: new Date().toISOString(),
        completed: null,
    };
    tasks.push(newTask);
    saveTasks(tasks);
    console.log('Task added.');
}

function listTasks(filter = {}) {
    const tasks = loadTasks();
    let filtered = tasks;
    if (filter.status) filtered = filtered.filter(t => t.status === filter.status);
    if (filter.priority) filtered = filtered.filter(t => t.priority === filter.priority);
    formatTable(filtered);
    printProgress(filtered);
    printGantt(filtered);
}

function completeTask(id) {
    const tasks = loadTasks();
    const idx = tasks.findIndex(t => t.id === id);
    if (idx >= 0) {
        tasks[idx].status = 'completed';
        tasks[idx].completed = new Date().toISOString();
        saveTasks(tasks);
        console.log('Task marked as completed.');
    } else {
        console.log('Task not found.');
    }
}

function deleteTask(id) {
    let tasks = loadTasks();
    const len = tasks.length;
    tasks = tasks.filter(t => t.id !== id);
    saveTasks(tasks);
    console.log(len === tasks.length ? 'Task not found.' : 'Task deleted.');
}

function stats() {
    const tasks = loadTasks();
    const completed = tasks.filter(t => t.status === 'completed');
    const pending = tasks.filter(t => t.status === 'pending');
    const total = tasks.length;
    const overdue = pending.filter(t => t.due && new Date(t.due) < new Date());
    const byPriority = tasks.reduce((acc, t) => {
        acc[t.priority] = (acc[t.priority] || 0) + 1;
        return acc;
    }, {});
    console.log(`Total tasks: ${total}`);
    console.log(`Completed: ${completed.length}`);
    console.log(`Pending: ${pending.length}`);
    console.log(`Completion rate: ${total ? ((completed.length / total) * 100).toFixed(1) : 0}%`);
    console.log(`Overdue: ${overdue.length}`);
    console.log('By priority:', byPriority);
}

function usage() {
    console.log(`Task Manager CLI
Usage:
  add "desc" [priority] [due:YYYY-MM-DD]
  list [status] [priority]
  complete <id>
  delete <id>
  stats
`);
}

const [,,cmd,...args] = process.argv;

switch (cmd) {
    case 'add':
        addTask(args[0], args[1], args[2]);
        break;
    case 'list': {
        const filter = {};
        if (args[0] && args[0] !== '-') filter.status = args[0];
        if (args[1] && args[1] !== '-') filter.priority = args[1];
        listTasks(filter);
        break;
    }
    case 'complete':
        completeTask(Number(args[0]));
        break;
    case 'delete':
        deleteTask(Number(args[0]));
        break;
    case 'stats':
        stats();
        break;
    default:
        usage();
}