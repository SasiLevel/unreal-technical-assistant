const chatHistory = document.getElementById("chat-history");
const chatForm = document.getElementById("chat-form");
const chatInput = document.getElementById("chat-input");
const sendButton = document.getElementById("send-button");
const newChatButton = document.getElementById("new-chat-button");

const LOADING_PHRASES = ["Cogitateing...", "Noodleing...", "Manefesting..."];
const LOADING_INTERVAL_MS = 3000;

let loadingTimer = null;

function appendMessage(text, role) {
    const el = document.createElement("div");
    el.classList.add("message", role);
    el.textContent = text;
    chatHistory.appendChild(el);
    chatHistory.scrollTop = chatHistory.scrollHeight;
    return el;
}

function startLoadingMessage() {
    let index = 0;
    const el = appendMessage(LOADING_PHRASES[index], "loading");

    loadingTimer = setInterval(() => {
        index = (index + 1) % LOADING_PHRASES.length;
        el.style.opacity = 0;
        setTimeout(() => {
            el.textContent = LOADING_PHRASES[index];
            el.style.opacity = 1;
        }, 150);
    }, LOADING_INTERVAL_MS);

    return el;
}

function stopLoadingMessage(el) {
    if (loadingTimer) {
        clearInterval(loadingTimer);
        loadingTimer = null;
    }
    el.remove();
}

async function sendMessage(message) {
    appendMessage(message, "user");
    chatInput.value = "";
    sendButton.disabled = true;

    const loadingEl = startLoadingMessage();

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message }),
        });

        const data = await response.json();

        stopLoadingMessage(loadingEl);

        if (!response.ok || data.error) {
            appendMessage(data.error || "Something went wrong. Please try again.", "error");
            return;
        }

        appendMessage(data.reply, "assistant");
    } catch (err) {
        stopLoadingMessage(loadingEl);
        appendMessage("Network error. Please check your connection and try again.", "error");
    } finally {
        sendButton.disabled = false;
        chatInput.focus();
    }
}

chatForm.addEventListener("submit", (event) => {
    event.preventDefault();
    const message = chatInput.value.trim();
    if (!message) return;
    sendMessage(message);
});

async function startNewChat() {
    newChatButton.disabled = true;

    try {
        await fetch("/new-chat", { method: "POST" });
        chatHistory.innerHTML = "";
    } catch (err) {
        appendMessage("Could not start a new chat. Please try again.", "error");
    } finally {
        newChatButton.disabled = false;
        chatInput.focus();
    }
}

newChatButton.addEventListener("click", startNewChat);
