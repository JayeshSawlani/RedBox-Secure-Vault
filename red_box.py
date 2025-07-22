import os
import pickle
import tkinter as tk
from tkinter import filedialog, messagebox
from cryptography.fernet import Fernet
import face_recognition
import sounddevice as sd
import wavio
from resemblyzer import VoiceEncoder, preprocess_wav
import numpy as np
import cv2

# --- Configuration ---
VAULT_DIRECTORY = "red_box_vault"
ENCRYPTED_VAULT_DIRECTORY = os.path.join(VAULT_DIRECTORY, "encrypted_files")
KEY_FILE = os.path.join(VAULT_DIRECTORY, "secret.key")
FACE_ENCODING_FILE = os.path.join(VAULT_DIRECTORY, "face_encoding.dat")
VOICE_SAMPLE_FILE = os.path.join(VAULT_DIRECTORY, "voice_enrollment.wav")
TEMP_LOGIN_VOICE_FILE = "login_voice.wav"
TEMP_FACE_IMAGE_FILE = "temp_face.jpg"
VOICE_SIMILARITY_THRESHOLD = 0.80


# --- Red Box Security Class ---
class RedBoxSecurity:
    def __init__(self):
        self.fernet = None
        self.voice_encoder = VoiceEncoder()
        self.enrolled_voice_embedding = None
        self.setup_vault()

    def setup_vault(self):
        os.makedirs(ENCRYPTED_VAULT_DIRECTORY, exist_ok=True)
        if not os.path.exists(KEY_FILE):
            self._generate_key()
        self._load_key()
        if os.path.exists(VOICE_SAMPLE_FILE):
            self.enrolled_voice_embedding = self._load_voice_embedding()

    def _generate_key(self):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)

    def _load_key(self):
        with open(KEY_FILE, "rb") as key_file:
            key = key_file.read()
        self.fernet = Fernet(key)

    def _load_voice_embedding(self):
        wav = preprocess_wav(VOICE_SAMPLE_FILE)
        return self.voice_encoder.embed_utterance(wav)

    def capture_face_image(self, prompt):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            messagebox.showerror("Error", "Cannot access the webcam.")
            return None
        messagebox.showinfo(prompt, "Press 'C' to capture, 'Q' to quit.")
        while True:
            ret, frame = cap.read()
            if not ret:
                continue
            cv2.imshow(prompt, frame)
            key = cv2.waitKey(1)
            if key & 0xFF == ord('c'):
                cv2.imwrite(TEMP_FACE_IMAGE_FILE, frame)
                break
            elif key & 0xFF == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                return None
        cap.release()
        cv2.destroyAllWindows()
        return TEMP_FACE_IMAGE_FILE

    def encrypt_and_add_file(self, source_path):
        try:
            with open(source_path, "rb") as file:
                original_data = file.read()
            encrypted_data = self.fernet.encrypt(original_data)
            filename = os.path.basename(source_path)
            encrypted_filepath = os.path.join(ENCRYPTED_VAULT_DIRECTORY, f"{filename}.enc")
            with open(encrypted_filepath, "wb") as file:
                file.write(encrypted_data)

            # 🔥 Delete original file after encryption
            os.remove(source_path)

            messagebox.showinfo("Success", f"File '{filename}' encrypted, stored, and original deleted.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to encrypt and add file:\n{e}")

    def decrypt_and_retrieve_file(self, filename, destination_path):
        self._secure_action(
            lambda: self._decrypt_file(filename, destination_path),
            "Unauthorized access detected! Encrypted file has been permanently deleted.",
            filename
        )

    def delete_file_secure(self, filename):
        self._secure_action(
            lambda: self._delete_file(filename),
            "Unauthorized access detected! Encrypted file has been permanently deleted.",
            filename
        )

    def _secure_action(self, action, fail_message, filename=None):
        attempts = 2
        while attempts > 0:
            if self.verify_biometrics():
                action()
                return
            else:
                attempts -= 1
                if attempts > 0:
                    messagebox.showwarning("Warning", "Biometric verification failed. You have 1 more attempt.")
                else:
                    if filename and os.path.exists(filename):
                        try:
                            os.remove(filename)
                            messagebox.showerror("Access Denied", f"{fail_message}\n\nDeleted: {os.path.basename(filename)}")
                        except Exception as e:
                            messagebox.showerror("Error", f"{fail_message}\n\nFailed to delete file: {e}")
                    else:
                        messagebox.showerror("Access Denied", fail_message)

    def _decrypt_file(self, filename, destination_path):
        try:
            with open(filename, "rb") as file:
                encrypted_data = file.read()
            decrypted_data = self.fernet.decrypt(encrypted_data)
            original_filename = os.path.basename(filename)[:-4]
            destination_filepath = os.path.join(destination_path, original_filename)
            with open(destination_filepath, "wb") as file:
                file.write(decrypted_data)
            messagebox.showinfo("Success", f"File '{original_filename}' decrypted and saved.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to decrypt file:\n{e}")

    def _delete_file(self, filename):
        try:
            os.remove(filename)
            messagebox.showinfo("Deleted", "File deleted successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not delete file:\n{e}")

    def list_files(self):
        files = [f for f in os.listdir(ENCRYPTED_VAULT_DIRECTORY) if f.endswith(".enc")]
        file_list = "\n".join(files) if files else "The vault is empty."
        messagebox.showinfo("Vault Files", file_list)

    def enroll_face(self):
        image_path = self.capture_face_image("Enroll Face - Press 'C' to Capture")
        if image_path:
            try:
                image = face_recognition.load_image_file(image_path)
                face_encodings = face_recognition.face_encodings(image)
                if face_encodings:
                    with open(FACE_ENCODING_FILE, "wb") as f:
                        pickle.dump(face_encodings[0], f)
                    os.remove(image_path)
                    messagebox.showinfo("Success", "Facial enrollment complete.")
                    return True
                else:
                    messagebox.showerror("Error", "No face detected in the captured image.")
            except Exception as e:
                messagebox.showerror("Error", f"Enrollment failed:\n{e}")
        return False

    def enroll_voice(self):
        try:
            duration = 5
            fs = 44100
            messagebox.showinfo("Voice Enrollment", "Recording voice for 5 seconds.\nSpeak clearly.")
            recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
            sd.wait()
            wavio.write(VOICE_SAMPLE_FILE, recording, fs, sampwidth=2)
            self.enrolled_voice_embedding = self._load_voice_embedding()
            messagebox.showinfo("Success", "Voice enrollment complete.")
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Voice enrollment failed:\n{e}")
            return False

    def verify_biometrics(self):
        if not os.path.exists(FACE_ENCODING_FILE) or not os.path.exists(VOICE_SAMPLE_FILE):
            messagebox.showerror("Error", "Face or voice not enrolled.")
            return False
        login_image_path = self.capture_face_image("Login Face - Press 'C' to Capture")
        if not login_image_path or not self._verify_face(login_image_path):
            messagebox.showerror("Access Denied", "Facial recognition failed.")
            return False
        if not self._verify_voice():
            messagebox.showerror("Access Denied", "Voice recognition failed.")
            return False
        return True

    def _verify_face(self, login_image_path):
        try:
            with open(FACE_ENCODING_FILE, "rb") as f:
                enrolled_encoding = pickle.load(f)
            login_image = face_recognition.load_image_file(login_image_path)
            login_encodings = face_recognition.face_encodings(login_image)
            os.remove(login_image_path)
            return login_encodings and face_recognition.compare_faces([enrolled_encoding], login_encodings[0])[0]
        except Exception:
            return False

    def _verify_voice(self):
        try:
            duration = 5
            fs = 44100
            messagebox.showinfo("Voice Authentication", "Recording login voice for 5 seconds.")
            recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
            sd.wait()
            wavio.write(TEMP_LOGIN_VOICE_FILE, recording, fs, sampwidth=2)
            login_wav = preprocess_wav(TEMP_LOGIN_VOICE_FILE)
            login_embedding = self.voice_encoder.embed_utterance(login_wav)
            os.remove(TEMP_LOGIN_VOICE_FILE)
            similarity = np.dot(self.enrolled_voice_embedding, login_embedding) / (
                np.linalg.norm(self.enrolled_voice_embedding) * np.linalg.norm(login_embedding)
            )
            return similarity >= VOICE_SIMILARITY_THRESHOLD
        except Exception:
            return False


# --- Tkinter GUI ---
class RedBoxApp:
    def __init__(self, master, box):
        self.master = master
        self.box = box
        master.title("🔒 Red Box Secure Vault")
        master.geometry("700x600")
        master.config(bg="#1a1a1a")

        tk.Label(master, text="Red Box 🔒\n( A BioMetric Secure Vault )", bg="#1a1a1a", fg="#FF3C3C",
                 font=("Times New Roman", 32, "bold"), justify="center").pack(pady=20)

        btn_cfg = {"width": 20, "height": 2, "bg": "#FF3C3C", "fg": "white",
                   "activebackground": "#FF6666", "font": ("Times New Roman", 12, "bold"), "relief": "raised", "bd": 4}

        frame = tk.Frame(master, bg="#1a1a1a")
        frame.pack(pady=10)

        # Center Auth Button
        self.buttons = {}
        self.buttons['auth'] = tk.Button(frame, text="Authenticate & Open Vault", command=self.authenticate, **btn_cfg)
        self.buttons['auth'].grid(row=0, column=0, columnspan=2, pady=15)

        # Left Column Buttons
        self.buttons['add'] = tk.Button(frame, text="Add File", command=self.add_file, state="disabled", **btn_cfg)
        self.buttons['add'].grid(row=1, column=0, padx=20, pady=10)

        self.buttons['list'] = tk.Button(frame, text="List Files", command=self.box.list_files, state="disabled", **btn_cfg)
        self.buttons['list'].grid(row=2, column=0, padx=20, pady=10)

        # Right Column Buttons
        self.buttons['retrieve'] = tk.Button(frame, text="Retrieve File", command=self.retrieve_file, state="disabled", **btn_cfg)
        self.buttons['retrieve'].grid(row=1, column=1, padx=20, pady=10)

        self.buttons['delete'] = tk.Button(frame, text="Delete File", command=self.delete_file, state="disabled", **btn_cfg)
        self.buttons['delete'].grid(row=2, column=1, padx=20, pady=10)

        # Exit Button
        self.buttons['exit'] = tk.Button(master, text="Exit", command=master.quit, bg="#333", fg="white",
                                         activebackground="#555", font=("Helvetica", 12, "bold"))
        self.buttons['exit'].pack(pady=20)

        # Auto enroll if needed
        if not os.path.exists(FACE_ENCODING_FILE) or not os.path.exists(VOICE_SAMPLE_FILE):
            messagebox.showinfo("First Time Setup", "Face & voice not enrolled. Starting enrollment.")
            if not self.box.enroll_face() or not self.box.enroll_voice():
                messagebox.showerror("Setup Failed", "Enrollment failed. Exiting.")
                master.destroy()

    def enable_buttons(self):
        for key in ['add', 'retrieve', 'list', 'delete']:
            self.buttons[key].config(state="normal")

    def authenticate(self):
        if self.box.verify_biometrics():
            messagebox.showinfo("Access Granted", "Welcome to the Vault!")
            self.enable_buttons()
            self.buttons['auth'].config(state="disabled")

    def add_file(self):
        file_path = filedialog.askopenfilename(title="Select File to Encrypt")
        if file_path:
            self.box.encrypt_and_add_file(file_path)

    def retrieve_file(self):
        file_path = filedialog.askopenfilename(initialdir=ENCRYPTED_VAULT_DIRECTORY, title="Select Encrypted File")
        dest_dir = filedialog.askdirectory(title="Select Destination Folder")
        if file_path and dest_dir:
            self.box.decrypt_and_retrieve_file(file_path, dest_dir)

    def delete_file(self):
        file_path = filedialog.askopenfilename(initialdir=ENCRYPTED_VAULT_DIRECTORY, title="Select File to Delete")
        if file_path:
            self.box.delete_file_secure(file_path)


# --- Launch App ---
if __name__ == "__main__":
    box = RedBoxSecurity()
    root = tk.Tk()
    app = RedBoxApp(root, box)
    root.mainloop()
