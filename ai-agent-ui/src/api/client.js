const BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";

export async function loginUser(username, password) {
  const res = await fetch(`${BASE}/api/token/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });
  if (!res.ok) throw new Error("Invalid credentials");
  const data = await res.json();
  return data.access;
}

export async function sendMessage(token, message) {
  const res = await fetch(`${BASE}/api/chat/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ message }),
  });
  if (!res.ok) throw new Error("Request failed");
  return res.json();
}

export async function signupUser(username, password) {
  const res = await fetch(`${BASE}/api/signup/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });
  if (!res.ok) {
    const data = await res.json();
    throw new Error(data.error || "Signup failed");
  }
  return res.json();
}