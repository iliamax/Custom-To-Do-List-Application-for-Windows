document.addEventListener('DOMContentLoaded', function() {
    // Show tasks when the page loads
    fetchTasks();

    // Handle task form submission
    document.getElementById('taskForm').addEventListener('submit', function(event) {
        event.preventDefault();

        const title = document.getElementById('title').value;
        const description = document.getElementById('description').value;
        const dueDate = document.getElementById('due_date').value;
        const priority = document.getElementById('priority').value;

        // Send the data to the server to add the task
        fetch('/add_task', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                title: title,
                description: description,
                due_date: dueDate,
                priority: priority
            })
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            fetchTasks(); // Refresh the task list after adding a new task
            document.getElementById('taskForm').style.display = 'none'; // Hide the form after submission
        })
        .catch(error => {
            console.error('Error adding task:', error);
        });
    });

    // Fetch and display tasks from the server
    function fetchTasks() {
        fetch('/get_tasks')
            .then(response => response.json())
            .then(tasks => {
                const taskList = document.getElementById('taskList');
                taskList.innerHTML = ''; // Clear the existing task list

                tasks.forEach(task => {
                    const taskItem = document.createElement('li');
                    taskItem.innerHTML = `
                        <strong>${task.title}</strong>
                        <em>${task.priority}</em><br>
                        <p>${task.description}</p>
                        <small>Due: ${task.due_date}</small>
                    `;
                    taskList.appendChild(taskItem);
                });

                // Show the task list after it's fetched
                taskList.style.display = 'block';
            })
            .catch(error => {
                console.error('Error fetching tasks:', error);
            });
    }

    // Show the task form when "Add Task" button is clicked
    document.getElementById('addTaskButton').addEventListener('click', function() {
        document.getElementById('taskForm').style.display = 'block';
        document.getElementById('taskList').style.display = 'none';
    });

    // Show the task list when "Show Tasks" button is clicked
    document.getElementById('showTasksButton').addEventListener('click', function() {
        document.getElementById('taskForm').style.display = 'none';
        fetchTasks();
    });
});
