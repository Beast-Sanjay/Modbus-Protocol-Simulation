# 🔌 Modbus TCP Server in Python

This is a **simple Modbus TCP Server** implemented in Python using `socket` and `scapy`. It is designed for educational and testing purposes, simulating responses for various Modbus function codes.

---

## ✅ Supported Modbus Function Codes

| Function Code | Description                  |
|---------------|------------------------------|
| `0x01`        | Read Coils                   |
| `0x03`        | Read Holding Registers       |
| `0x04`        | Read Input Registers         |
| `0x05`        | Write Single Coil            |
| `0x06`        | Write Single Register        |
| `0x0F`        | Write Multiple Coils         |
| `0x10`        | Write Multiple Registers     |
| `0x11`        | Report Slave ID              |

---

## 🚧 Project Status

This project is **still under development**.

- 🔄 Future plans include support for additional Modbus function codes.
- ❗ Improved exception handling and logging will be added.
- 🛡️ This server is **not** intended for use in production environments.

---

## 🧰 Requirements

- Python 3.x
- [Scapy](https://scapy.readthedocs.io/en/latest/)

### Install Dependencies

```bash
pip install scapy
