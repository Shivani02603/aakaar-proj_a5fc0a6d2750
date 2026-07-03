import { useEffect, useState } from "react";
import { api } from "../api/client";
import { Todo } from "../types";

export default function Todos() {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [newTodo, setNewTodo] = useState<Partial<Todo>>({
    title: "",
    description: "",
    due_date: "",
  });

  useEffect(() => {
    fetchTodos();
  }, []);

  const fetchTodos = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.get<Todo[]>("/api/todos");
      setTodos(response.data);
    } catch (err) {
      setError("Failed to load todos.");
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTodo = async () => {
    if (!newTodo.title) return;
    setError(null);
    try {
      const response = await api.post<Todo>("/api/todos", newTodo);
      setTodos((prev) => [...prev, response.data]);
      setNewTodo({ title: "", description: "", due_date: "" });
    } catch (err) {
      setError("Failed to create todo.");
    }
  };

  const handleUpdateTodo = async (id: string, updatedFields: Partial<Todo>) => {
    setError(null);
    try {
      const response = await api.patch<Todo>(`/api/todos/${id}`, updatedFields);
      setTodos((prev) =>
        prev.map((todo) => (todo.id === id ? response.data : todo))
      );
    } catch (err) {
      setError("Failed to update todo.");
    }
  };

  const handleDeleteTodo = async (id: string) => {
    setError(null);
    try {
      await api.delete(`/api/todos/${id}`);
      setTodos((prev) => prev.filter((todo) => todo.id !== id));
    } catch (err) {
      setError("Failed to delete todo.");
    }
  };

  if (loading) {
    return <div className="p-4 text-center">Loading...</div>;
  }

  if (error) {
    return <div className="p-4 text-center text-red-500">{error}</div>;
  }

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Todos</h1>
      <div className="mb-4">
        <input
          type="text"
          placeholder="Title"
          value={newTodo.title}
          onChange={(e) => setNewTodo({ ...newTodo, title: e.target.value })}
          className="border p-2 mr-2"
        />
        <input
          type="text"
          placeholder="Description"
          value={newTodo.description || ""}
          onChange={(e) =>
            setNewTodo({ ...newTodo, description: e.target.value })
          }
          className="border p-2 mr-2"
        />
        <input
          type="datetime-local"
          value={newTodo.due_date || ""}
          onChange={(e) =>
            setNewTodo({ ...newTodo, due_date: e.target.value })
          }
          className="border p-2 mr-2"
        />
        <button
          onClick={handleCreateTodo}
          className="bg-blue-500 text-white px-4 py-2 rounded"
        >
          Add Todo
        </button>
      </div>
      {todos.length === 0 ? (
        <div className="text-center text-gray-500">No todos found.</div>
      ) : (
        <ul className="space-y-4">
          {todos.map((todo) => (
            <li
              key={todo.id}
              className="border p-4 rounded flex justify-between items-center"
            >
              <div>
                <h2 className="text-lg font-bold">{todo.title}</h2>
                <p className="text-sm text-gray-500">{todo.description}</p>
                {todo.due_date && (
                  <p className="text-sm text-gray-500">
                    Due: {new Date(todo.due_date).toLocaleString()}
                  </p>
                )}
                <p
                  className={`text-sm ${
                    todo.completed ? "text-green-500" : "text-red-500"
                  }`}
                >
                  {todo.completed ? "Completed" : "Incomplete"}
                </p>
              </div>
              <div className="flex space-x-2">
                <button
                  onClick={() =>
                    handleUpdateTodo(todo.id, { completed: !todo.completed })
                  }
                  className="bg-yellow-500 text-white px-4 py-2 rounded"
                >
                  {todo.completed ? "Mark Incomplete" : "Mark Complete"}
                </button>
                <button
                  onClick={() => handleDeleteTodo(todo.id)}
                  className="bg-red-500 text-white px-4 py-2 rounded"
                >
                  Delete
                </button>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}