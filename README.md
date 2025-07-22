# 🔒 Red Box Secure Vault

A **Biometric Secure Vault** for sensitive files with advanced **AES encryption**, **Facial Recognition**, and **Voice Authentication**. Powered by Python and OpenCV.  

---

## 📦 Features

- 🔐 **AES-256 Encryption**: Securely encrypt and decrypt your files.
- 👁️ **Facial Recognition**: Authenticate users with webcam-based face detection.
- 🎤 **Voice Recognition**: Adds a second layer of security using voice biometrics.
- 🗂️ Simple GUI: Intuitive Tkinter-based interface for managing your vault.
- 💣 Failsafe: Permanently deletes files on failed authentication attempts.
- 📋 File management: Add, retrieve, list, and delete files securely.

---

## 🛠️ Tech Stack

- Python 3.11
- [Cryptography](https://cryptography.io/) (AES Encryption)
- [face_recognition](https://github.com/ageitgey/face_recognition)
- [Resemblyzer](https://github.com/resemble-ai/Resemblyzer) (Voice embedding)
- Tkinter (GUI)
- OpenCV (Webcam Access)

---

## 🚀 Getting Started

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/JayeshSawlani/RedBox-Secure-Vault.git
cd RedBox-Secure-Vault
2️⃣ Create Virtual Environment
bash
Copy
Edit
python -m venv redbox_env
3️⃣ Activate Virtual Environment
Windows:

bash
Copy
Edit
redbox_env\Scripts\activate
Linux/Mac:

bash
Copy
Edit
source redbox_env/bin/activate
4️⃣ Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
5️⃣ Run the App
bash
Copy
Edit
python redbox.py
📂 Folder Structure
pgsql
Copy
Edit
RedBox-Secure-Vault/
│
├── redbox.py              # Main application
├── requirements.txt       # All dependencies
├── red_box_vault/         # Encrypted files and keys
├── README.md              # Project documentation
└── .gitignore             # Ignored files/folders
📸 Screenshots
Login Face Recognition	Voice Authentication	Vault Dashboard

🤝 Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

📜 License
This project is licensed under the MIT License - see the LICENSE file for details.

👨‍💻 Author
Jayesh Sawlani
GitHub | LinkedIn
