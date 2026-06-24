# Prodigy_CS_T4
Keystroke Logger
# Keystroke Logger (Scoped Alternative)

A Flask-based educational project that demonstrates keystroke event capture, timestamp logging, and file handling in a safe, transparent, and consent-based environment. This application records keystrokes typed only within a designated text area on the webpage and stores them in a local log file.

## 📌 Project Information

**Repository Name:** Prodigy_CS_T4

**GitHub Profile:**
https://github.com/shivamshuklabtech

## 🚀 Features

* Real-time keystroke logging
* Timestamped key event recording
* Local file-based logging system
* Live log viewer
* Refresh log functionality
* Clear log functionality
* Interactive web interface
* REST API endpoints for log management
* Educational and consent-based design

## 🔒 Important Security Note

This project is **NOT a traditional keylogger**.

### What It Does

✅ Logs keystrokes typed inside the provided text box

✅ Records timestamps for each keystroke

✅ Stores logs in a local file (`keystroke_log.txt`)

✅ Displays logged events on the webpage

### What It Does NOT Do

❌ Capture keystrokes outside the browser tab

❌ Run in the background

❌ Hide from the user

❌ Monitor system-wide keyboard activity

❌ Collect sensitive information

This project is designed strictly for educational purposes to demonstrate:

* Keyboard event handling
* Flask API development
* File input/output operations
* Client-server communication

## 🛠️ Technologies Used

* Python 3
* Flask
* HTML5
* CSS3
* JavaScript
* REST API
* File Handling

## 📂 Project Structure

```text
Prodigy_CS_T4/
│
├── typing_logger_app.py
├── keystroke_log.txt
├── requirements.txt
└── README.md
```

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/shivamshuklabtech/Prodigy_CS_T4.git
cd Prodigy_CS_T4
```

### 2. Create a Virtual Environment (Optional)

```bash
python -m venv venv
```

Activate the environment:

#### Windows

```bash
venv\Scripts\activate
```

#### Linux/macOS

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install flask
```

or

```bash
pip install -r requirements.txt
```

## ▶️ Running the Application

Start the Flask development server:

```bash
python typing_logger_app.py
```

Open your browser and navigate to:

```text
http://127.0.0.1:5000
```

## 📸 How to Use

1. Start the application.
2. Open the webpage.
3. Type inside the provided text area.
4. Each keystroke will:

   * Be timestamped
   * Be stored in `keystroke_log.txt`
   * Appear in the log viewer
5. Click **Refresh Log** to reload entries.
6. Click **Clear Log** to delete all logged data.

## 🌐 API Endpoints

### Log a Keystroke

**POST**

```http
/api/log
```

#### Request

```json
{
  "key": "A"
}
```

#### Response

```json
{
  "ok": true,
  "logged": "A",
  "time": "2026-06-24 14:30:45.123"
}
```

---

### View Logged Keystrokes

**GET**

```http
/api/log
```

#### Response

```json
{
  "lines": [
    "[2026-06-24 14:30:45.123] A",
    "[2026-06-24 14:30:45.456] B"
  ]
}
```

---

### Clear Log File

**DELETE**

```http
/api/log
```

#### Response

```json
{
  "ok": true
}
```

## 📄 Example Log Output

```text
[2026-06-24 14:30:45.123] H
[2026-06-24 14:30:45.567] e
[2026-06-24 14:30:45.890] l
[2026-06-24 14:30:46.100] l
[2026-06-24 14:30:46.345] o
[2026-06-24 14:30:46.789] Enter
```

## 🎯 Learning Objectives

This project demonstrates:

* Keyboard event handling in JavaScript
* Flask API development
* AJAX and Fetch API requests
* File creation and management in Python
* Client-server communication
* Timestamp generation
* Safe logging practices
* Web application development

## 🔐 Ethical Considerations

This project was intentionally designed to avoid the behavior of real-world keyloggers. It only records user input within a visible, consent-based environment and serves as an educational demonstration of event handling and logging mechanisms.

## 🤝 Contributing

Contributions and improvements are welcome.

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to your branch
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Author

**Shivam Shukla**

GitHub: https://github.com/shivamshuklabtech

---

⭐ If you found this project useful, consider giving it a star on GitHub.

