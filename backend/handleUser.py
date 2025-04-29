import mysql.connector
from mysql.connector import Error
import bcrypt
import jwt
import datetime

def registerUser(username, password, email):
    try:
        # Validazione dei dati di input
        if not username or not password or not email:
            return "Errore: Tutti i campi sono obbligatori."

        # Hashing della password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Connessione al database
        connection = mysql.connector.connect(
            host='localhost',
            database='robolab',
            user='root',
            password=''
        )

        if connection.is_connected():
            cursor = connection.cursor(prepared=True)
            query = """
                INSERT INTO users (username, password, email)
                VALUES (%s, %s, %s)
            """
            values = (username.strip(), hashed_password, email.strip())
            cursor.execute(query, values)
            connection.commit()
            return "Utente registrato con successo."

    except Error as e:
        return f"Errore durante l'inserimento: {e}"

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Connessione al database chiusa.")
            

SECRET_KEY = "your_secret_key"
REFRESH_SECRET_KEY = "your_refresh_secret_key"  # Chiave separata per il refresh token

def loginUser(email, password):
    try:
        if not email or not password:
            return {"message": "Errore: Email e password sono obbligatori."}

        connection = mysql.connector.connect(
            host='localhost',
            database='robolab',
            user='root',
            password=''
        )

        if connection.is_connected():
            cursor = connection.cursor(prepared=True)
            query = "SELECT id, password FROM users WHERE email = %s"
            cursor.execute(query, (email.strip(),))
            result = cursor.fetchone()

            if result:
                user_id, stored_password = result
                if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                    # Genera access token
                    access_token = jwt.encode(
                        {
                            "user_id": user_id,
                            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
                        },
                        SECRET_KEY,
                        algorithm="HS256"
                    )
                    # Genera refresh token
                    refresh_token = jwt.encode(
                        {
                            "user_id": user_id,
                            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7)
                        },
                        REFRESH_SECRET_KEY,
                        algorithm="HS256"
                    )
                    return {
                        "message": "Login effettuato con successo.",
                        "access_token": access_token,
                        "refresh_token": refresh_token
                    }
                else:
                    return {"message": "Errore: Password errata."}
            else:
                return {"message": "Errore: Email non trovata."}

    except Error as e:
        return {"message": f"Errore durante il login: {e}"}

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def refreshAccessToken(refresh_token):
    try:
        decoded = jwt.decode(refresh_token, REFRESH_SECRET_KEY, algorithms=["HS256"])
        user_id = decoded["user_id"]
        # Genera un nuovo access token
        new_access_token = jwt.encode(
            {
                "user_id": user_id,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
            },
            SECRET_KEY,
            algorithm="HS256"
        )
        return {"access_token": new_access_token}
    except jwt.ExpiredSignatureError:
        return {"message": "Refresh token scaduto!"}, 401
    except jwt.InvalidTokenError:
        return {"message": "Refresh token non valido!"}, 401
            