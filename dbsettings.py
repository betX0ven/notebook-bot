import sqlite3

tasks_db = sqlite3.connect('Tasks2.db')
projects_db = sqlite3.connect('Projects2.db')

tasks_cursor = tasks_db.cursor()
projects_cursor = projects_db.cursor()

tasks_cursor.execute('''
CREATE TABLE IF NOT EXISTS All_tasks (
id INTEGER PRIMARY KEY,
task_text TEXT NOT NULL,
display_order INTEGER NOT NULL UNIQUE
)
''')

projects_cursor.execute('''
CREATE TABLE IF NOT EXISTS All_projects (
id INTEGER PRIMARY KEY,
project_text TEXT NOT NULL,
display_order INTEGER NOT NULL UNIQUE
)
''')

tasks_db.commit()
projects_db.commit()


def add_task(new_task):
  # tasks_cursor.execute('INSERT INTO All_tasks (task_text) VALUES (?)', (new_task,))
  # Считаем общее количество задач
  tasks_cursor.execute("SELECT MAX(display_order) FROM All_tasks")
  max_order = tasks_cursor.fetchone()[0] or 0  # Если таблица пуста, вернет 0
  
  # Добавляем новую задачу с порядком на 1 больше
  tasks_cursor.execute(
      "INSERT INTO All_tasks (task_text, display_order) VALUES (?, ?)",
      (new_task, max_order + 1)
  )
  tasks_db.commit()

def delete_task(task_id):
  tasks_cursor.execute('DELETE FROM All_tasks WHERE display_order = ?', (task_id,))

  tasks_cursor.execute("SELECT id FROM All_tasks ORDER BY display_order")
  all_tasks = tasks_cursor.fetchall()

  for new_id, (old_id,) in enumerate(all_tasks, start=1):
    tasks_cursor.execute("UPDATE All_tasks SET display_order = ? WHERE id = ?", (new_id, old_id))

  tasks_db.commit()

def update_task(task_id, new_task):
  tasks_cursor.execute('UPDATE All_tasks SET task_text = ? WHERE display_order = ?', (new_task, int(task_id)))
  tasks_db.commit()

def delete_all_tasks():
  tasks_cursor.execute('DELETE FROM All_tasks')
  tasks_db.commit()

def show_tasks():
  tasks_cursor.execute('SELECT display_order FROM All_tasks ORDER BY id DESC')

  ids = []
  for id in tasks_cursor.fetchall():
    ids.append(id[0])

  tasks_cursor.execute('SELECT task_text FROM All_tasks ORDER BY display_order DESC')

  tasks = []
  for task in tasks_cursor.fetchall():
    tasks.append(task[0])

  list_final = ''

  for i in range(len(ids)):
    list_final += str(ids[i]) + '. '
    list_final += str(tasks[i]) + '\n'

  if list_final:
    return list_final
  else:
    return 'Ваш список дел пустой'

def show_tasks_ids():
  tasks_cursor.execute('SELECT display_order FROM All_tasks ORDER BY id DESC')

  ids = []
  for id in tasks_cursor.fetchall():
    ids.append(id[0])

  list_final = ''

  for i in range(len(ids)):
    list_final += str(ids[i])
  return list_final




def add_project(new_project):
  projects_cursor.execute("SELECT MAX(display_order) FROM All_projects")
  max_order = projects_cursor.fetchone()[0] or 0  # Если таблица пуста, вернет 0
  
  # Добавляем новую задачу с порядком на 1 больше
  projects_cursor.execute(
      "INSERT INTO All_projects (project_text, display_order) VALUES (?, ?)",
      (new_project, max_order + 1)
  )
  projects_db.commit()

def delete_project(project_id):
  projects_cursor.execute('DELETE FROM All_projects WHERE display_order = ?', (project_id,))

  projects_cursor.execute("SELECT id FROM All_projects ORDER BY display_order")
  all_projects = projects_cursor.fetchall()

  for new_id, (old_id,) in enumerate(all_projects, start=1):
    projects_cursor.execute("UPDATE All_projects SET display_order = ? WHERE id = ?", (new_id, old_id))

  tasks_db.commit()

def update_project(project_id, new_project):
  projects_cursor.execute('UPDATE All_projects SET project_text = ? WHERE display_order = ?', (new_project, int(project_id)))
  projects_db.commit()

def delete_all_projects():
  projects_cursor.execute('DELETE FROM All_projects')
  projects_db.commit()

def show_projects():
  projects_cursor.execute('SELECT display_order FROM All_projects ORDER BY id DESC')

  ids = []
  for id in projects_cursor.fetchall():
    ids.append(id[0])

  projects_cursor.execute('SELECT project_text FROM All_projects ORDER BY display_order DESC')

  projects = []
  for project in projects_cursor.fetchall():
    projects.append(project[0])

  list_final = ''

  for i in range(len(ids)):
    list_final += str(ids[i]) + '. '
    list_final += str(projects[i]) + '\n'

  if list_final:
    return list_final
  else:
    return 'Ваш список проектов пустой'

def show_projects_ids():
  projects_cursor.execute('SELECT display_order FROM All_projects ORDER BY id DESC')

  ids = []
  for id in projects_cursor.fetchall():
    ids.append(id[0])

  list_final = ''

  for i in range(len(ids)):
    list_final += str(ids[i])
  return list_final
