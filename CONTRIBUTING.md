
# 🤝 Contributing to THU Messaging

Thank you for your interest in contributing to the **TeleHelp Ukraine (THU) Messaging** project! Your help makes this open-source WhatsApp integration better for everyone.

We welcome all types of contributions: code, design, testing, documentation, and more.

---

## 📋 Table of Contents

1. [Getting Started](#getting-started)
2. [How You Can Help](#how-you-can-help)
3. [Code Standards](#code-standards)
4. [Testing](#testing)
5. [How to Submit Changes](#how-to-submit-changes)
6. [Certification & Recognition](#certification--recognition)

---

## 🚀 Getting Started

1. Fork this repository
2. Clone your fork
3. Create a virtual environment
4. Install dependencies with `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and fill in local dummy values (no real secrets required for testing)

---

## 🙌 How You Can Help

### 🧑‍💻 Developers
- Implement Flask routes (`/chats`, `/chat/<phone>`, unread handling)
- Integrate frontend templates for chat display
- Add filters/search to chat listings

### 🧪 QA / Testers
- Use the `/send_whatsapp` proxy route to test message sending
- Write `pytest` tests in the `tests/` folder
- Report issues and bugs

### 🎨 UI/UX Designers
- Improve layout and usability of:
  - `chat_list.html` – recent chats
  - `chat.html` – message thread
  - `chat_start.html` – search and start new chat

### 📚 Writers
- Improve or translate documentation
- Create onboarding guides for new contributors
- Add curl usage examples

---

## 🧼 Code Standards

- Follow PEP8 (Python style guide)
- Keep functions small and meaningful
- Add comments or docstrings where helpful
- Avoid committing secrets or `.env` files

---

## 🧪 Testing

We use `pytest`. Run:

```bash
pytest
```

All new features should include test coverage.

---

## 🏅 Certification & Recognition

All contributors are eligible to receive:

- ✅ Contribution badges
- 📜 Printable/open badge certifications
- 💬 Recognition in the project README (Hall of Fame section coming soon)

See [CERTIFICATION.md](CERTIFICATION.md) for full details.

---

## 💬 Questions?

Open an [issue](https://github.com/TeleHelpUkraine/thu-messaging/issues) or ask in our contributor discussions.

Made with ❤️ by [TeleHelp Ukraine](https://telehelpukraine.org/)
