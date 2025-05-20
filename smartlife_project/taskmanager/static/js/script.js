// Task Manager JavaScript
document.addEventListener('DOMContentLoaded', function () {
    // Initialize Font Awesome
    const script = document.createElement('script');
    script.src = 'https://kit.fontawesome.com/your-kit-code.js';
    script.crossorigin = 'anonymous';
    document.head.appendChild(script);

    // Initialize tasks
    loadTasks();
    
    // Add task button click handler
    document.querySelector('.add-task-btn').addEventListener('click', addTask);
    
    // Enter key handler
    document.getElementById('task').addEventListener('keypress', function (e) {
        if (e.key === 'Enter') addTask();
    });

    // Filter buttons event delegation
    document.querySelector('.btn-group').addEventListener('click', function(e) {
        const button = e.target.closest('button');
        if (button && button.dataset.action) {
            const action = button.dataset.action;
            switch(action) {
                case 'all':
                    showAllTasks();
                    break;
                case 'active':
                    showActiveTasks();
                    break;
                case 'completed':
                    showCompletedTasks();
                    break;
            }
        }
    });
});

// Filter functions
function showAllTasks() {
    document.querySelectorAll('.task-item').forEach(task => {
        task.style.display = 'block';
    });
    showNotification('Showing all tasks', 'info');
}

function showActiveTasks() {
    document.querySelectorAll('.task-item').forEach(task => {
        task.style.display = task.classList.contains('completed') ? 'none' : 'block';
    });
    showNotification('Showing active tasks', 'info');
}

function showCompletedTasks() {
    document.querySelectorAll('.task-item').forEach(task => {
        task.style.display = task.classList.contains('completed') ? 'block' : 'none';
    });
    showNotification('Showing completed tasks', 'info');
}

// Filter functions
function showAllTasks() {
    document.querySelectorAll('.task-item').forEach(task => {
        task.style.display = 'block';
    });
    showNotification('Showing all tasks', 'info');
}

function showActiveTasks() {
    document.querySelectorAll('.task-item').forEach(task => {
        task.style.display = task.classList.contains('completed') ? 'none' : 'block';
    });
    showNotification('Showing active tasks', 'info');
}

function showCompletedTasks() {
    document.querySelectorAll('.task-item').forEach(task => {
        task.style.display = task.classList.contains('completed') ? 'block' : 'none';
    });
    showNotification('Showing completed tasks', 'info');
}

// Add task function
function addTask() {
    const taskInput = document.getElementById('task');
    const timeInput = document.getElementById('time');
    const taskList = document.getElementById('taskList');

    const taskText = taskInput.value.trim();
    const taskTime = timeInput.value;

    if (!taskText) {
        showNotification('Silakan masukkan tugas!', 'danger');
        return;
    }

    const taskId = Date.now().toString();
    const taskItem = document.createElement('li');
    taskItem.id = taskId;
    taskItem.className = 'task-item';
    taskItem.innerHTML = `
        <div class="task-content">
            <span class="task-text">${taskText}</span>
            ${taskTime ? `<span class="task-time">${taskTime}</span>` : ''}
        </div>
        <div class="task-actions">
            <button class="complete-btn" onclick="completeTask('${taskId}')">✓</button>
            <button class="edit-btn" onclick="editTask('${taskId}')">🖉</button>
            <button class="delete-btn" onclick="deleteTask('${taskId}')">🗑</button>
        </div>
    `;
    taskList.appendChild(taskItem);
    taskInput.value = '';
    timeInput.value = '';
    showNotification('Tugas berhasil ditambahkan!', 'success');
    saveTasks();
}

function completeTask(taskId) {
    const taskItem = document.getElementById(taskId);
    taskItem.classList.toggle('completed');
    saveTasks();
}

function editTask(taskId) {
  const taskItem = document.getElementById(taskId);
  const taskText = taskItem.querySelector('.task-text').textContent;
  const taskTimeElement = taskItem.querySelector('.task-time');
  let taskTime = '';

  if (taskTimeElement) {
    const timeParts = taskTimeElement.textContent.match(/(\d+):(\d+)/);
    if (timeParts) {
      let hours = parseInt(timeParts[1]);
      const minutes = timeParts[2];

      if (taskTimeElement.textContent.toLowerCase().includes('pm') && hours < 12) {
        hours += 12;
      } else if (taskTimeElement.textContent.toLowerCase().includes('am') && hours === 12) {
        hours = 0;
      }

      taskTime = `${hours.toString().padStart(2, '0')}:${minutes}`;
    }
  }

  document.getElementById('task').value = taskText;
  document.getElementById('time').value = taskTime;

  deleteTask(taskId);
  document.getElementById('task').focus();
}

function deleteTask(taskId) {
  const taskItem = document.getElementById(taskId);
  if (taskItem) taskItem.remove();
  saveTasks();
}

function saveTasks() {
  const taskList = document.getElementById('taskList');
  const tasks = [];

  taskList.querySelectorAll('li.task-item').forEach(function (taskItem) {
    const taskText = taskItem.querySelector('.task-text').textContent;
    const taskTimeElement = taskItem.querySelector('.task-time');
    const taskTime = taskTimeElement ? taskTimeElement.textContent : '';
    const isCompleted = taskItem.classList.contains('completed');

    tasks.push({
      id: taskItem.id,
      text: taskText,
      time: taskTime,
      completed: isCompleted
    });
  });

  localStorage.setItem('tasks', JSON.stringify(tasks));
}

function loadTasks() {
  const taskList = document.getElementById('taskList');
  const savedTasks = localStorage.getItem('tasks');

  if (savedTasks) {
    const tasks = JSON.parse(savedTasks);

    tasks.forEach(function (task) {
      const li = document.createElement('li');
      li.id = task.id;
      li.className = 'task-item';
      if (task.completed) li.classList.add('completed');

      li.innerHTML = `
        <div class="task-content">
          <span class="task-text">${task.text}</span>
          ${task.time ? `<span class="task-time">${task.time}</span>` : ''}
        </div>
        <div class="task-actions">
          <button class="complete-btn" onclick="completeTask('${task.id}')">✓</button>
          <button class="edit-btn" onclick="editTask('${task.id}')">🖉</button>
          <button class="delete-btn" onclick="deleteTask('${task.id}')">🗑</button>
        </div>
      `;

      taskList.appendChild(li);
    });
  }
}
