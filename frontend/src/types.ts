// ── AAKAAR:STAMPED_TYPES (do not remove this marker) ──────────────────────────────
// Entity interfaces are stamped here from the build contract; they mirror
// backend/schemas.py exactly. Generated components must import from this file.

export interface Todo {
  id: string;
  title: string;
  description?: string;
  due_date?: string;
  completed: boolean;
  created_at: string;
  updated_at: string;
  user_id: string;
}

export interface TodoCreate {
  title: string;
  description?: string;
  due_date?: string;
  completed: boolean;
}
