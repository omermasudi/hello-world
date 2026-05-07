const list = document.getElementById("todo-list");
const form = document.getElementById("add-form");
const input = document.getElementById("new-todo");

async function apiFetch(path, options = {}) {
  const res = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (res.status === 204) return null;
  return res.json();
}

function renderItem(todo) {
  const li = document.createElement("li");
  li.className = "todo-item" + (todo.done ? " done" : "");
  li.dataset.id = todo.id;

  const checkbox = document.createElement("input");
  checkbox.type = "checkbox";
  checkbox.checked = !!todo.done;
  checkbox.addEventListener("change", async () => {
    const updated = await apiFetch(`/todos/${todo.id}`, { method: "PATCH" });
    li.className = "todo-item" + (updated.done ? " done" : "");
    checkbox.checked = !!updated.done;
  });

  const span = document.createElement("span");
  span.className = "todo-text";
  span.textContent = todo.text;

  const del = document.createElement("button");
  del.className = "delete-btn";
  del.textContent = "✕";
  del.title = "Delete";
  del.addEventListener("click", async () => {
    await apiFetch(`/todos/${todo.id}`, { method: "DELETE" });
    li.remove();
  });

  li.append(checkbox, span, del);
  return li;
}

async function loadTodos() {
  const todos = await apiFetch("/todos");
  list.innerHTML = "";
  todos.forEach((t) => list.appendChild(renderItem(t)));
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const text = input.value.trim();
  if (!text) return;
  const todo = await apiFetch("/todos", {
    method: "POST",
    body: JSON.stringify({ text }),
  });
  list.prepend(renderItem(todo));
  input.value = "";
  input.focus();
});

loadTodos();
