from flask import Flask, request, jsonify
import os
from generaBiglietto import draw_ticket
from handleUser import registerUser, loginUser, refreshAccessToken
from flask_cors import CORS
from auth import token_required
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins

@app.route('/refresh', methods=['POST'])
def refresh():
    data = request.get_json()
    refresh_token = data.get('refresh_token')
    if not refresh_token:
        return jsonify({"message": "Refresh token mancante!"}), 401
    response = refreshAccessToken(refresh_token)
    return jsonify(response)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    # Ottieni il messaggio dalla funzione registerUser
    message = registerUser(username, password, email)
    # Restituisci il messaggio come risposta JSON
    return jsonify({"message": message})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    # Ottieni il messaggio dalla funzione loginUser
    message = loginUser(email, password)
    # Restituisci il messaggio come risposta JSON
    return jsonify({"message": message})

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5000)
    
#     @app.route('/generaBiglietto', methods=['POST'])
# def generaBiglietto():
#     data=request.json
#     title_text = data.get('title_text')
#     nome = data.get('nome')
#     cognome = data.get('cognome')
#     identifier = data.get('identifier')
#     event_date = data.get('event_date')
#     aula_text = data.get('aula_text')
#     piano_text = data.get('piano_text')
#     # Call the draw_ticket function with the provided data
#     draw_ticket(title_text, nome, cognome, identifier, event_date, aula_text, piano_text)
#     # Construct the filename based on the provided data
#     filename = f"{nome}{cognome}{identifier}.pdf"
#     # Check if the file exists before sending it
#     if os.path.exists(filename):
#         # Send the file as a response
#         return send_file(filename, as_attachment=True)
#     else:
#         return "File not found", 404