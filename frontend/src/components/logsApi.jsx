const API_URL = process.env.REACT_APP_BACKEND_URL || "http://localhost:8000";

export async function logChat(userEmail, message, sender) {
  const res = await fetch(`${API_URL}/log/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_email: userEmail, message, sender }),
  });
  if (!res.ok) throw new Error("Failed to log chat");
  return res.json();
}

export async function logMood(userEmail, mood, intensity) {
  const res = await fetch(`${API_URL}/log/mood`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_email: userEmail, mood, intensity }),
  });
  if (!res.ok) throw new Error("Failed to log mood");
  return res.json();
}

export async function logSymptom(userEmail, symptom, severity) {
  const res = await fetch(`${API_URL}/log/symptom`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_email: userEmail, symptom, severity }),
  });
  if (!res.ok) throw new Error("Failed to log symptom");
  return res.json();
}

export async function logMeal(userEmail, mealType, items) {
  const res = await fetch(`${API_URL}/log/meal`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_email: userEmail, meal_type: mealType, items }),
  });
  if (!res.ok) throw new Error("Failed to log meal");
  return res.json();
}
