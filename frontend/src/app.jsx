import { useState, useEffect } from "react";

const API = "";

export default function App() {
  const [items,   setItems]   = useState([]);
  const [title,   setTitle]   = useState("");
  const [desc,    setDesc]    = useState("");
  const [loading, setLoading] = useState(false);
  const [error,   setError]   = useState(null);

  async function fetchItems() {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API}/api/items`);
      if (!res.ok) throw new Error("Failed to fetch items");
      setItems(await res.json());
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { fetchItems(); }, []);

  async function addItem(e) {
    e.preventDefault();
    if (!title.trim()) return;
    try {
      const res = await fetch(`${API}/api/items`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title, description: desc }),
      });
      if (!res.ok) throw new Error("Failed to create item");
      setTitle("");
      setDesc("");
      fetchItems();
    } catch (e) {
      setError(e.message);
    }
  }

  async function deleteItem(id) {
    try {
      await fetch(`${API}/api/items/${id}`, { method: "DELETE" });
      setItems((prev) => prev.filter((i) => i.id !== id));
    } catch (e) {
      setError(e.message);
    }
  }

  return (
    <div style={s.page}>
      <div style={s.card}>
        <h1 style={s.title}>Items</h1>

        <form onSubmit={addItem} style={s.form}>
          <input
            style={s.input}
            placeholder="Title *"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
          />
          <input
            style={s.input}
            placeholder="Description (optional)"
            value={desc}
            onChange={(e) => setDesc(e.target.value)}
          />
          <button style={s.btn} type="submit">Add Item</button>
        </form>

        {error   && <p style={s.error}>{error}</p>}
        {loading && <p style={s.muted}>Loading…</p>}

        {!loading && items.length === 0 && (
          <p style={s.muted}>No items yet. Add one above!</p>
        )}

        <ul style={s.list}>
          {items.map((item) => (
            <li key={item.id} style={s.listItem}>
              <div>
                <strong>{item.title}</strong>
                {item.description && <p style={s.muted}>{item.description}</p>}
                <span style={s.date}>
                  {new Date(item.created_at).toLocaleString()}
                </span>
              </div>
              <button style={s.del} onClick={() => deleteItem(item.id)}>✕</button>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

const s = {
  page:     { minHeight:"100vh", background:"#f0f2f5", display:"flex", alignItems:"center", justifyContent:"center", fontFamily:"system-ui,sans-serif" },
  card:     { background:"#fff", borderRadius:12, padding:32, width:"100%", maxWidth:540, boxShadow:"0 4px 24px rgba(0,0,0,.08)" },
  title:    { margin:"0 0 24px", fontSize:24, fontWeight:700 },
  form:     { display:"flex", flexDirection:"column", gap:10, marginBottom:24 },
  input:    { padding:"10px 14px", border:"1px solid #ddd", borderRadius:8, fontSize:15 },
  btn:      { padding:"10px 14px", background:"#4f46e5", color:"#fff", border:"none", borderRadius:8, fontSize:15, cursor:"pointer", fontWeight:600 },
  list:     { listStyle:"none", margin:0, padding:0, display:"flex", flexDirection:"column", gap:10 },
  listItem: { display:"flex", justifyContent:"space-between", alignItems:"flex-start", padding:"12px 16px", border:"1px solid #eee", borderRadius:8 },
  del:      { background:"none", border:"none", cursor:"pointer", color:"#999", fontSize:16 },
  error:    { color:"#dc2626", fontSize:14 },
  muted:    { color:"#9ca3af", fontSize:13, margin:"4px 0" },
  date:     { color:"#c4c4c4", fontSize:12 },
};