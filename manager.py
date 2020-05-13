import os

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto import Random
from base64 import b64encode, b64decode

save_location = "./passwords.krypt"
key_location  = "./manager_key.pem"


def newkeys(keysize):
   random_generator = Random.new().read
   key = RSA.generate(keysize, random_generator)
   private, public = key, key.publickey()
   return public, private


def importKey(externKey):
   return RSA.importKey(externKey)


def getpublickey(priv_key):
   return priv_key.publickey()


def encrypt(message, pub_key):
   cipher = PKCS1_OAEP.new(pub_key)
   return cipher.encrypt(message)


def decrypt(ciphertext, priv_key):
   cipher = PKCS1_OAEP.new(priv_key)
   return cipher.decrypt(ciphertext)


class Crud:
    def __init__(self, save_location):
        self.save_location = save_location

    def create(self, plaintext):
        f = open(self.save_location, "ab")
        cyphertext = encrypt(plaintext.encode(), public)
        f.write(cyphertext)
        f.close()


    def print_all(self):
        try:
            if os.path.isfile(self.save_location):
                size_of_file = os.path.getsize(self.save_location)
                with open(self.save_location, "rb") as f:

                    for i in range(int(size_of_file/512)):
                        l = f.read(512)
                        l = decrypt(l, private)
                        l = l.decode().split(" - ")
                        print(f"Servico  = \"{l[0]}\"\nLogin    = \"{l[1]}\"\nSenha    = \"{l[2]}\"\n\n")
            
            else:
                print("Nao existe nada escrito ainda!")
        except Exception as error:
            print(error)


class Credentials:
    def create_pair(self):
        service =  input("Qual o nome do site/app?\nNome site/app: ")
        login   =  input("Qual o nome/email de cadastro?\nNome: ")
        passwd  =  input("Qual a senha de cadastro?\nSenha: ")

        self.content = (f"{service} - {login} - {passwd}")


def main():
    crud = Crud(save_location)
    
    selecao = input("[1] para criar novo par de cadastro/senha\n" +
                        "[2] para ver todos pares cadastrados\n"  +
                        "[0] para sair\n"                         +
                        "Selecao: ")
    
    while( (selecao != "1") and (selecao != "2") and (selecao != "0") ):
        print("Escolha entre as opcoes dadas!")
        selecao = int(input("[1] para criar novo par de cadastro/senha\n" +
                            "[2] para ver todos pares cadastrados\n"      +
                            "[0] para sair\n"                             +
                            "Selecao: "))

    
    if(selecao == "1"):
        new_credentials = Credentials()
        new_credentials.create_pair()
        crud.create(new_credentials.content)

    elif(selecao == "2"):
        crud.print_all()



passphrase = input("Qual a senha da chave mestre?\nSenha: ")
passed     = True

try:
    if os.path.isfile(key_location):
        private =  RSA.import_key(open(key_location).read(), passphrase=passphrase)
        public  =  private.publickey()

    else:
        public, private = newkeys(4096)
        private = private.export_key(passphrase=passphrase)
        with open(key_location, "wb") as f:
            f.write(private)

except (ValueError, IndexError, TypeError):
    print("ERRO! Sua senha esta incorreta!")
    passed = False
except Exception as error:
    print(error)
    passed = False

if passed:
    main()

exit(0)
