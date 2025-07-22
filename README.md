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
git clone https://github.com/JayeshSawlani/RedBox-Secure-Vault.git
cd RedBox-Secure-Vault

### 2️⃣ Create Virtual Environment
python -m venv redbox_env

### 3️⃣ Activate Virtual Environment
redbox_env\Scripts\activate

### 4️⃣ Install Dependencies
pip install -r requirements.txt

### 5️⃣ Run the App
python redbox.py

## 📂 Folder Structure
RedBox-Secure-Vault/

├── redbox.py            
├── requirements.txt     
├── red_box_vault/       
├── README.md             
├── .gitignore            
└── screenshots/          

📸 Screenshots

Login Face Recognition

<img width="342" height="180" alt="image" src="https://github.com/user-attachments/assets/4a7690d0-5639-45b5-924e-d559784b4698" />

Voice Authentication

<img width="306" height="189" alt="image" src="https://github.com/user-attachments/assets/c694c324-41fe-4db8-bc2f-4e79ebdd172d" />

Vault Dashboard

<img width="874" height="668" alt="image" src="https://github.com/user-attachments/assets/15b2ba05-94c9-4823-9cb5-2e2222b19062" />


## 🤝 Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## 📜 License
This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author
Jayesh Sawlani
