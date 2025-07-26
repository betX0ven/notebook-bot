import sqlite3

tasks_db = sqlite3.connect('tasks.db')
projects_db = sqlite3.connect('projects.db')

tasks_cursor = tasks_db.cursor()
projects_cursor = projects_db.cursor()

tasks_cursor.execute('''
CREATE TABLE IF NOT EXISTS All_tasks (
id INTEGER PRIMARY KEY,
task_text TEXT NOT NULL
)
''')

projects_cursor.execute('''
CREATE TABLE IF NOT EXISTS All_projects (
id INTEGER PRIMARY KEY,
project_text TEXT NOT NULL
)
''')

tasks_db.commit()
projects_db.commit()

def add_task(new_task):
  tasks_cursor.execute('INSERT INTO All_tasks (task_text) VALUES (?)', (new_task,))
  tasks_db.commit()

def delete_task(task_id):
  tasks_cursor.execute('DELETE FROM All_tasks WHERE id = ?', (task_id,))
  tasks_db.commit()

def update_task(task_id, new_task):
  tasks_cursor.execute('UPDATE All_tasks SET task_text = ? WHERE id = ?', (new_task, task_id))
  tasks_db.commit()

def delete_all_tasks():
  tasks_cursor.execute('DELETE FROM All_tasks')
  tasks_db.commit()

def show_tasks():
  tasks_cursor.execute('SELECT id FROM All_tasks ORDER BY id DESC')

  ids = []
  for id in tasks_cursor.fetchall():
    ids.append(id[0])

  tasks_cursor.execute('SELECT task_text FROM All_tasks ORDER BY id DESC')

  tasks = []
  for task in tasks_cursor.fetchall():
    tasks.append(task[0])

  list_final = ''

  for i in range(len(ids)):
    list_final += str(ids[i]) + '. '
    list_final += str(tasks[i]) + '\n'

  return list_final


