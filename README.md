
# 📲 THU Messaging – Open Source WhatsApp Integration

**TeleHelp Ukraine (THU)** Messaging is an open-source, Flask-based WhatsApp proxy and chat interface. It allows staff and volunteers to securely send messages using a Meta WhatsApp Business account — **without exposing access tokens.**

---

## 🚀 Features

- 🔐 Secure WhatsApp proxy using `pywa`
- 💬 Volunteer-safe `/send_whatsapp` endpoint
- 📄 Supports text and template messages
- 🧑‍⚕️ Staff view of recent chats, searchable and sortable
- 🆕 Unread message tracking (bold, pinned to top – coming soon)
- 🌐 Built with Flask, SQLAlchemy, and pywa
- ✅ Volunteer-friendly structure with tests, documentation, and certification

---

## 📦 Project Structure

```
thu-messaging/
├── app/                   # Flask app
│   ├── main/routes/       # WhatsApp webhook and proxy route
│   ├── templates/         # Chat HTML templates
│   ├── static/            # CSS/JS/images
│   └── models/            # SQLAlchemy models
├── tests/                 # Volunteer test suite
├── .env.example           # Sample environment file
├── requirements.txt       # Project dependencies
├── run.py                 # Application entry point
├── README.md              # This file
├── CONTRIBUTING.md        # Contribution guide
├── CERTIFICATION.md       # Recognition & badges
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

---

### 🔑 Volunteer Access Tokens

To protect our system, we use an access key system.

#### ✅ General Use
Use the shared volunteer access key in your request headers:

```
-H "VOLUNTEER_ACCESS_KEY: THU2025proxy"
```

This allows testing with approved test phone numbers and template messages only.

#### 🔐 Want Elevated Access?
If you’d like to test sensitive features or join the backend/core team:

- Complete [identity verification via Persona](https://inquiry.withpersona.com/verify?inquiry-template-id=itmpl_pVzBi48HcgD6g5xgWAtzaCRH&reference-id=your_user_id1)
- You’ll receive a personal access token upon approval

---

### 4. Set environment variables

Create a `.env` file based on `.env.example`:

```
VOLUNTEER_ACCESS_KEY=your_access_token
DATABASE_URL=postgresql://your_user:your_pass@localhost:5432/thu_messaging
```

---

### 5. Set up the database locally

We use PostgreSQL + SQLAlchemy for data storage.

1. Make sure PostgreSQL is installed and running.
2. Create the database:

```bash
createdb thu_messaging
```

3. Run migrations to initialize the schema:

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

---

## 🧪 Sending WhatsApp Messages

Volunteers can use the following `curl` command (template messages only):

```bash
curl -X POST http://localhost:5000/send_whatsapp   -H "Content-Type: application/json"   -H "VOLUNTEER_ACCESS_KEY: {your_access_token}"   -d '{
    "messaging_product": "whatsapp",
    "to": "+12049220575",
    "type": "template",
    "template": {
      "name": "hello_world",
      "language": { "code": "en_US" }
    }
  }'
```

This endpoint proxies your request to the WhatsApp Business API using a secure server token (not visible to volunteers).

---

## ✅ Running Tests

We use `pytest` for testing:

```bash
pytest
```

You can add new tests in the `tests/` folder. A working example is already included in `tests/test_basic.py`.

---

## 🙌 How to Contribute

1. Fork the repository
2. Create a new branch (`git checkout -b my-feature`)
3. Commit your changes
4. Push to your fork
5. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for full contributor guidelines.

---

## 🏅 Certification & Recognition

Contributors are eligible to receive downloadable, shareable certificates and badges for their work. These can be added to resumes or LinkedIn profiles.

See [CERTIFICATION.md](CERTIFICATION.md) for how to qualify.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

Made with ❤️ by [TeleHelp Ukraine](https://telehelpukraine.com/)
