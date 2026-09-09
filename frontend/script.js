const API_BASE = window.REXI_API_URL || "http://127.0.0.1:8000";
const app = document.querySelector("#app");
const state = {
  screen: localStorage.getItem("rexi_token") ? "chat" : "login",
  user: JSON.parse(localStorage.getItem("rexi_user") || "null"),
  token: localStorage.getItem("rexi_token") || "",
  operation: "summarize",
  language: "English",
  messages: [],
  busy: false,
};

const icons = { user: "♙", bot: "◉", bolt: "ϟ", lock: "♢", eye: "◉", mail: "✉", person: "♙" };
const languages = ["English", "French", "Spanish", "German", "Arabic", "Chinese (Simplified)", "Urdu"];

function logo(compact = false) {
  return `<div class="brand${compact ? " compact" : ""}"><div class="brand-mark">◡</div><div><div class="brand-name">Rexi<span>Chatbot</span></div><div class="brand-sub">${compact ? "Your AI companion for better conversations" : "Smart Conversations. Brighter Ideas."}</div></div></div>`;
}

function robotVisual() {
  return `<div class="robot-art"><div class="robot-head"><div class="robot-antenna"></div><div class="robot-face"></div></div></div>`;
}

function authVisual(register) {
  return `<section class="auth-visual">${logo()}<div class="visual-copy"><h1>${register ? "Join Rexi and<br>start your journey<br>with <span class=\"accent\">AI today</span>" : "Your AI Companion<br>for a <span class=\"accent\">Smarter Tomorrow</span>"}</h1><p>Get instant answers, explore ideas,<br>learn new things, and have meaningful<br>conversations — anytime, anywhere.</p></div><div class="feature-row"><div class="feature"><strong>ϟ</strong>Fast<br>Responses</div><div class="feature"><strong>♢</strong>Secure &<br>Private</div><div class="feature"><strong>✦</strong>Powered by<br>AI</div></div>${robotVisual()}</section>`;
}

function field(label, name, placeholder, type = "text", icon = "♙", max = "") {
  const toggle = type === "password" ? `<button type="button" class="password-toggle" data-toggle="${name}" aria-label="Show password">◉</button>` : "";
  return `<div class="form-group"><label for="${name}">${label}</label><div class="input-wrap"><span>${icon}</span><input id="${name}" name="${name}" type="${type}" placeholder="${placeholder}" ${max ? `maxlength="${max}"` : ""} required>${toggle}</div></div>`;
}

function authScreen(register = false) {
  state.screen = register ? "register" : "login";
  app.innerHTML = `<div class="auth-page"><div class="auth-card">${authVisual(register)}<section class="auth-form"><div class="form-head">${register ? '<div class="brand-mark" style="margin-bottom:20px">♙</div>' : ""}<h2>${register ? "Create Your Account" : "Welcome <span class=\"accent\">Back!</span>"}</h2><p>${register ? "Fill in the details below to get started with Rexi." : "Sign in to continue your conversation with Rexi."}</p></div><div id="form-message"></div><form id="auth-form">${register ? field("Full Name", "fullname", "Enter your full name", "text", "♙", "100") : ""}${field("Username", "username", register ? "Choose a unique username" : "Enter your username", "text", "♙", "100")}${register ? field("Email", "email", "Enter your email address", "email", "✉") : ""}${field("Password", "password", register ? "Create a strong password" : "Enter your password", "password", "♢", "8")}<button class="primary-btn" type="submit" id="submit-btn">${register ? "♙ &nbsp; Register" : "→ &nbsp; Login"}</button></form><div class="divider">or</div><div class="form-footer">${register ? "Already have an account?" : "Create a new account"}<button class="outline-btn" id="switch-auth" type="button">${register ? "↪ &nbsp; Login" : "♙+ &nbsp; Register"}</button></div></section></div></div>`;
  document.querySelector("#auth-form").addEventListener("submit", handleAuth);
  document.querySelector("#switch-auth").addEventListener("click", () => authScreen(!register));
  document.querySelectorAll("[data-toggle]").forEach((button) => button.addEventListener("click", () => {
    const input = document.querySelector(`#${button.dataset.toggle}`);
    input.type = input.type === "password" ? "text" : "password";
  }));
}

async function handleAuth(event) {
  event.preventDefault();
  const form = new FormData(event.currentTarget);
  const register = state.screen === "register";
  const payload = Object.fromEntries(form.entries());
  const message = document.querySelector("#form-message");
  const submit = document.querySelector("#submit-btn");
  message.innerHTML = "";
  submit.disabled = true;
  try {
    const response = await fetch(`${API_BASE}/auth/${register ? "register" : "login"}`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) });
    const data = await response.json().catch(() => ({}));
    if (!response.ok) throw new Error(Array.isArray(data.detail) ? data.detail.map((item) => item.msg).join(". ") : data.detail || "Something went wrong. Please try again.");
    if (register) {
      message.innerHTML = `<div class="success-box">Account created. You can sign in now.</div>`;
      setTimeout(() => authScreen(false), 850);
    } else {
      state.token = data.access_token;
      state.user = data.user;
      localStorage.setItem("rexi_token", state.token);
      localStorage.setItem("rexi_user", JSON.stringify(state.user));
      chatScreen();
    }
  } catch (error) {
    message.innerHTML = `<div class="error-box"><strong>Unable to ${register ? "create account" : "sign in"}.</strong>${error.message}</div>`;
  } finally { submit.disabled = false; }
}

function chatScreen() {
  state.screen = "chat";
  app.innerHTML = `<div class="app-shell"><aside class="sidebar">${logo(true)}<nav class="nav-list"><button class="nav-btn active"><span class="nav-icon">☏</span>Chat</button><button class="nav-btn"><span class="nav-icon">◷</span>History</button><button class="nav-btn"><span class="nav-icon">♙</span>Profile</button><button class="nav-btn"><span class="nav-icon">⚙</span>Settings</button></nav><div class="quick"><h3>Quick Actions</h3><button data-action="explain">▣ &nbsp; Ask about American History</button><button data-action="summarize">✤ &nbsp; Get a Summary</button><button data-action="explain">♧ &nbsp; Ask a Question</button><button data-action="translate">◎ &nbsp; Translate &nbsp; ›</button><button data-action="podcast">♬ &nbsp; Create Podcast &nbsp; ›</button></div><div class="profile"><div class="profile-row"><div class="avatar">♙</div><div>${state.user?.fullname || state.user?.username || "Guest"}<small>Free Plan</small></div></div><button class="logout" id="logout">↪ &nbsp; Logout</button></div></aside><section class="chat-panel"><header class="chat-header"><div class="chat-brand"><div class="brand-mark">◡</div><div><h2>Rexi</h2><p>Your AI companion for better conversations</p></div></div><span class="online">Online</span></header><div class="messages" id="messages"></div><div class="action-row"><button data-action="explain">▣ &nbsp; Read More</button><button data-action="summarize">▤ &nbsp; Summarize</button><button class="active" data-action="translate">◎ &nbsp; Translate</button><button data-action="podcast">♬ &nbsp; Podcast</button><button data-action="explain">⌕ &nbsp; Ask a Question</button></div><form class="composer" id="composer"><button type="button" class="attach">⌕</button><input id="message-input" placeholder="Type your message..." autocomplete="off"><button class="send" type="submit">➤</button></form></section><aside class="right-panel"><div class="tool-panel"><div class="tool-title"><span style="font-size:25px;color:#a98aff">◎</span><div><h2>Translate</h2><p>Translate the response to your preferred language.</p></div><button class="close-tool">×</button></div><input class="search" id="language-search" placeholder="⌕  Search languages..."><div class="language-list" id="language-list"></div><div class="how"><p>How it works</p><div class="how-step"><span class="step-num">1</span>Choose your target language from the list.</div><div class="how-step"><span class="step-num">2</span>Rexi will translate the last response for you.</div><div class="how-step"><span class="step-num">3</span>You can copy or listen to the translation.</div></div></div></aside></div>`;
  renderWelcome(); renderLanguages();
  document.querySelector("#composer").addEventListener("submit", sendMessage);
  document.querySelector("#logout").addEventListener("click", logout);
  document.querySelectorAll("[data-action]").forEach((button) => button.addEventListener("click", () => { state.operation = button.dataset.action; document.querySelector("#message-input").focus(); toast(`${button.textContent.trim()} selected`); }));
  document.querySelector("#language-search").addEventListener("input", renderLanguages);
}

function renderWelcome() {
  document.querySelector("#messages").innerHTML = `<div class="message user"><div><div class="message-bubble">Tell me about American history</div><div class="message-meta">10:24 AM ✓✓</div></div><div class="message-icon">♙</div></div><div class="message bot"><div class="message-icon">◡</div><div><div class="message-bubble">American history is a story of how a vast land inhabited by indigenous peoples became a diverse, powerful modern nation. It is a journey marked by incredible growth, struggles for freedom, technological innovation, and continuous efforts to live up to the founding ideals of liberty and equality.</div><div class="message-meta">10:24 AM</div></div></div>`;
}
function renderLanguages() { const filter = (document.querySelector("#language-search")?.value || "").toLowerCase(); document.querySelector("#language-list").innerHTML = languages.filter((language) => language.toLowerCase().includes(filter)).map((language, index) => `<button class="language ${language === state.language ? "selected" : ""}" data-language="${language}"><span>${["🇺🇸", "🇫🇷", "🇪🇸", "🇩🇪", "🇦🇪", "🇨🇳", "🇵🇰"][index]}</span>${language}</button>`).join(""); document.querySelectorAll("[data-language]").forEach((button) => button.addEventListener("click", () => { state.language = button.dataset.language; renderLanguages(); })); }

async function sendMessage(event) {
  event.preventDefault();
  const input = document.querySelector("#message-input"); const text = input.value.trim(); if (!text || state.busy) return;
  const messages = document.querySelector("#messages"); state.busy = true; input.value = "";
  messages.insertAdjacentHTML("beforeend", `<div class="message user"><div><div class="message-bubble">${escapeHtml(text)}</div><div class="message-meta">Now ✓✓</div></div><div class="message-icon">♙</div></div><div class="message bot" id="pending"><div class="message-icon">◡</div><div><div class="message-bubble">Rexi is thinking...</div></div></div>`); messages.scrollTop = messages.scrollHeight;
  try { const response = await fetch(`${API_BASE}/chat/`, { method: "POST", headers: { "Content-Type": "application/json", ...(state.token ? { Authorization: `Bearer ${state.token}` } : {}) }, body: JSON.stringify({ text, operation: state.operation, target_language: state.language }) }); const data = await response.json().catch(() => ({})); if (!response.ok) throw new Error(data.detail || "The chatbot could not respond."); document.querySelector("#pending")?.remove(); messages.insertAdjacentHTML("beforeend", podcastResponse(data.text)); } catch (error) { document.querySelector("#pending")?.remove(); messages.insertAdjacentHTML("beforeend", `<div class="error-box">${escapeHtml(error.message)}</div>`); } finally { state.busy = false; messages.scrollTop = messages.scrollHeight; }
}
function podcastResponse(text) {
  if (state.operation !== "podcast") {
    return `<div class="message bot"><div class="message-icon">◡</div><div><div class="message-bubble">${escapeHtml(text)}</div><div class="message-meta">Now</div></div></div>`;
  }
  const turns = [...String(text).matchAll(/(?:^|\s)(Host|Guest):\s*([\s\S]*?)(?=\s+(?:Host|Guest):|$)/gi)];
  if (!turns.length) return `<div class="message bot"><div class="message-icon">◡</div><div><div class="message-bubble">${escapeHtml(text)}</div><div class="message-meta">Now</div></div></div>`;
  const speakerRows = turns.map(([, speaker, words]) => `<div class="podcast-turn"><div class="podcast-speaker-icon ${speaker.toLowerCase()}">${speaker === "Host" ? "◉" : "♬"}</div><div class="podcast-turn-copy"><strong>${speaker}</strong><span>${escapeHtml(words.trim())}</span></div></div>`).join("");
  return `<div class="message bot podcast-message"><div class="message-icon">◡</div><div><div class="message-bubble podcast-bubble">${speakerRows}</div><div class="message-meta">Now</div></div></div>`;
}
function escapeHtml(value) { return String(value).replace(/[&<>"']/g, (char) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;" })[char]); }
function logout() { localStorage.removeItem("rexi_token"); localStorage.removeItem("rexi_user"); state.token = ""; state.user = null; authScreen(false); }
function toast(message) { const node = document.createElement("div"); node.className = "toast"; node.textContent = message; document.body.appendChild(node); setTimeout(() => node.remove(), 1800); }

if (state.screen === "chat") chatScreen(); else authScreen(false);
