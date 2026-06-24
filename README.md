# SecureVault (Cryptosafe) 

A robust, Python-based password manager designed with privacy and security as its primary focus. SecureVault utilizes **local-only storage** and strong cryptographic standards to ensure your credentials never leave your machine and remain inaccessible to unauthorized users.

## Features

* **Offline First:** 100% local-only storage. Your vault is never synced to a third-party cloud, giving you absolute control over your data.
* **AES Encryption:** SecureVault leverages industry-standard Advanced Encryption Standard (AES) to encrypt your password database, ensuring your data is mathematically secure against brute-force attacks.
* **Zero-Knowledge Architecture:** The master password is never stored or transmitted. The vault can only be decrypted locally by the user who holds the correct key.
* **Lightweight & Modular:** Built purely with Python, prioritizing a minimal attack surface and clean, maintainable code.

## Tech Stack

* **Language:** Python 3.x
* **Cryptography:** `cryptography` library (Standard AES implementation)

## 🗺️ Roadmap & Future Enhancements

* [ ] **Migration to XChaCha20-Poly1305:** Transitioning to the XChaCha20-Poly1305 AEAD cipher for enhanced security and performance, especially on devices lacking hardware AES acceleration.
* [ ] **Automated Clipboard Clearing:** Automatically wiping copied passwords from the system clipboard after a set timeout.
* [ ] **Password Generator:** Built-in utility to generate cryptographically secure, high-entropy passwords.

**Installation** install the _internal.zip file and extract everthing in one place you will see and exe file there simply run it if you have python installed on your device.
