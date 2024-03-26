from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Semplice configurazione di un database per la memorizzazione dei punteggi
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///punteggi.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Definizione dell'utente con i suoi dati
class Utente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), unique=True, nullable=False)
    miglior_punteggio = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<Utente {self.nome} con punteggio {self.miglior_punteggio}>'

# Creazione effettiva db e tabelle
with app.app_context():
    db.create_all()
    
# Funzione che aggiorna il punteggio migliore
def aggiorna_punteggio(nome_utente, punteggio):
    # Individuo la prima occorrenza dell'utente all'interno del db
    utente = Utente.query.filter_by(nome=nome_utente).first()
    # Se presente...
    if utente:
        # e se ha ottenuto un risultato migliore al quiz
        if punteggio > utente.miglior_punteggio:
            # aggiorno e salvo il nuovo punteggio
            utente.miglior_punteggio = punteggio
            db.session.commit()
    else:
        # altrimenti creo un nuovo utente da zero
        nuovo_utente = Utente(nome=nome_utente, miglior_punteggio=punteggio)
        db.session.add(nuovo_utente)
        db.session.commit()
    return utente.miglior_punteggio if utente else punteggio 

# Definizione della route di default che rimanda al quiz.
@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        total_score = 0
        # Ottengo le risposte date dall'utente
        username = request.form.get('username')
        question1 = request.form.get('question1')
        question2 = request.form.get('question2')
        question3 = request.form.get('question3')
        question4 = request.form.get('question4')
        question5 = request.form.get('question5')

        # Logica molto sciocca per il calcolo del punteggio che potrebbe essere banalmente ottimizzata
        if question1 == 'answer3':
            total_score += 20
        
        if question2 == 'answer3':
            total_score += 20
        
        if question3 == 'answer3':
            total_score += 20
        
        if question4 == 'answer3':
            total_score += 20
        
        if question5 == 'answer3':
            total_score += 20
        
        # Richiamo la funzione responsabile della valutazione del punteggio migliore per l'utente selezionato
        best_score = aggiorna_punteggio(username, total_score)

        # Aggiorno la pagina con il punteggio ottenuto
        return render_template('index.html', total_score=total_score, best_score=best_score)
    else:
        return render_template('index.html', total_score=0)


# Esecuzione dell'applicazione in modalità debug.
if __name__ == '__main__':
    app.run(debug=True)