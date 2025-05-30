
# 📲 THU Messaging – Open Source WhatsApp Integration

**TeleHelp Ukraine (THU)** Messaging is an open-source, Flask-based WhatsApp proxy and chat interface. It allows staff and volunteers to securely send messages using a Meta WhatsApp Business account **without exposing access tokens.**

---

## 🚀 Features

- 🔐 Secure WhatsApp proxy using `pywa`
- 💬 Volunteer-safe `/send_whatsapp` endpoint
- 📄 Supports text and template messages
- 🧑‍⚕️ Staff view of recent chats, searchable and sortable
- 🆕 Unread messages tracking (bold, pinned to top – coming soon)
- 🌐 Built with Flask, SQLAlchemy, and pywa
- ✅ Volunteer-friendly structure with testing, docs, and certs

---

## 📦 Project Structure

```
thu-messaging/
├── app/                   # Flask app
│   ├── main/routes/       # WhatsApp webhook and send route
│   ├── templates/         # Chat HTML templates
│   ├── static/            # CSS/JS/images
│   └── models/            # Database models (Message, etc.)
├── tests/                 # Volunteer test suite
├── .env.example           # Environment variables template
├── requirements.txt       # Dependencies
├── run.py                 # Entry point
├── README.md              # This file
├── CONTRIBUTING.md        # Contribution guide
├── CERTIFICATION.md       # Volunteer recognition
├── LICENSE                # MIT License
```

---

## 🔧 Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/TeleHelpUkraine/thu-messaging.git
cd thu-messaging
```

### 2. Create a virtual environment

```bash
python3 -m venv env
source env/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set environment variables

Create a `.env` file based on `.env.example`:

```
WA_ACCESS_TOKEN=your_production_token
WA_PHONE_NUMBER_ID=your_number_id
VOLUNTEER_ACCESS_KEY=THU2025proxy
```

---

## 🧪 Sending WhatsApp Messages

Volunteers can use the following `curl` command without needing any secret keys:

```bash
curl -X POST http://localhost:5000/send_whatsapp \
  -H "Content-Type: application/json" \
  -H "X-Access-Key: {your_access_token}" \
  -H "VOLUNTEER_ACCESS_KEY: {your_access_token}" \
  -d '{
    "messaging_product": "whatsapp",
    "to": "+12049220575",
    "type": "template",
    "template": {
      "name": "hello_world",
      "language": { "code": "en_US" }
    }
  }'
```

This endpoint proxies your request to Meta WhatsApp servers using a secured internal token stored on the server (not visible to volunteers).

---

## ✅ Running Tests

We use `pytest` for testing. Run all tests with:

```bash
pytest
```

You can add new tests under the `tests/` folder. An example test is already included in `tests/test_basic.py`.

---

## 🙌 How to Contribute

1. Fork the repository
2. Create a new branch (`git checkout -b my-feature`)
3. Commit your changes
4. Push to your fork
5. Create a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidance on how to help.

---

## 🏅 Certification & Recognition

Contributors are eligible to receive downloadable, shareable certificates and badges for their work. These can be added to resumes or LinkedIn profiles.

See [CERTIFICATION.md](CERTIFICATION.md) for contribution levels and how to qualify.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

Made with ❤️ by [TeleHelp Ukraine](https://telehelpukraine.com/)
