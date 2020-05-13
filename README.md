ssword Manager

My implementation of a password manager. It uses RSA 4096-bit encryption and was written in python3

## Installation


```bash
pip3 -r requirements.txt
```

## Info
The script currently saves the private key and the encrypted file to ./manager_key.pem and ./passwords.krypt, respectively. This can be changed by editing the "save_location" and "key_location" variables in the file.

## Usage
```bash
python3 manager.py
```

## Contributing
Changes are welcome! Simply open a pull request


## License
[GPL3](https://choosealicense.com/licenses/gpl-3.0//)

