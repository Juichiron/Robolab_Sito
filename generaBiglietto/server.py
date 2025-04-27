from flask import Flask,request,send_file
import os
from provaBiglietto import draw_ticket

app=Flask(__name__)

@app.route('/generaBiglietto', methods=['POST'])
def generaBiglietto():
    data=request.json
    title_text = data.get('title_text')
    nome = data.get('nome')
    cognome = data.get('cognome')
    identifier = data.get('identifier')
    event_date = data.get('event_date')
    aula_text = data.get('aula_text')
    piano_text = data.get('piano_text')
    # Call the draw_ticket function with the provided data
    draw_ticket(title_text, nome, cognome, identifier, event_date, aula_text, piano_text)
    # Construct the filename based on the provided data
    filename = f"{nome}{cognome}{identifier}.pdf"
    # Check if the file exists before sending it
    if os.path.exists(filename):
        # Send the file as a response
        return send_file(filename, as_attachment=True)
    else:
        return "File not found", 404

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5000)