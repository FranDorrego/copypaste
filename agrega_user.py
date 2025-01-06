import sys
import sqlite3
import random
import string
import hashlib
import crypt

# Función para generar una contraseña aleatoria de 8 caracteres
def generar_password():
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choice(caracteres) for _ in range(8))

# Función para hashear la contraseña usando SHA512-CRYPT
def hash_password(password):
    salt = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))
    return crypt.crypt(password, f'$6${salt}')

# Verifica que se haya pasado un argumento por línea de comando
if len(sys.argv) != 2:
    print("Uso: python3 agrega_user.py <nueva_cuenta>")
    sys.exit(1)

# Obtiene el correo desde la línea de comando
nueva_cuenta = sys.argv[1]

# Genera una contraseña aleatoria
password = generar_password()
hashed_password = hash_password(password)

# Conexión a la base de datos SQLite
db_path = '/data/users.db'  # Cambia esta ruta si es necesario
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Inserta el nuevo usuario en la tabla "users"
try:
    cursor.execute("INSERT INTO users (address, password) VALUES (?, ?)", (nueva_cuenta, hashed_password))
    conn.commit()
    print(f"Cuenta creada: {nueva_cuenta}")
    print(f"Contraseña: {password}")
except sqlite3.IntegrityError as e:
    print("Error: La cuenta ya existe.", e)
except Exception as e:
    print('Erorr grande', e)
finally:
    conn.close()
