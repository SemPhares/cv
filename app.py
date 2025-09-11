from flask import Flask, render_template, request, jsonify, session
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import traceback

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'your-secret-key-here')

# Configuration SMTP
SMTP_CONFIG = {
    'SMTP_SERVER': os.environ.get('SMTP_SERVER', 'smtp.gmail.com'),
    'SMTP_PORT': int(os.environ.get('SMTP_PORT', 587)),
    'SMTP_USERNAME': os.environ.get('SMTP_USERNAME', 'your-email@gmail.com'),
    'SMTP_PASSWORD': os.environ.get('SMTP_PASSWORD', 'your-app-password'),
    'FROM_EMAIL': os.environ.get('FROM_EMAIL', 'your-email@gmail.com'),
    'TO_EMAIL': os.environ.get('TO_EMAIL', 'sem_phares@yahoo.com')
}

# Configuration des langues
LANGUAGES = {
    'fr': {
        'nav': {
            'presentation': 'Présentation',
            'experiences': 'Expériences',
            'projects': 'Projets',
            'contact': 'Contact'
        },
        'hero': {
            'typed_text': ['INGÉNIERIE IA', 'ANALYSE DE DONNÉES', 'INNOVATION'],
            'subtitle': '"Les données sont le nouveau pétrole, mais contrairement au pétrole, plus on les partage, plus elles prennent de la valeur !" 🚀'
        },
        'about': {
            'title': 'À Propos',
            'role': 'Data Scientist',
            'bio': [
                'Je dispose de 5 années d\'expérience dans le développement de modèles de Machine Learning et la mise en place de solutions d\'Intelligence Artificielle.',
                'Je suis passionné par les sujets liés à l\'IA générative, l\'analyse de données et la modélisation statistique.',
                'J\'ai démontré ma capacité à concevoir des solutions innovantes telles que la classification de séries temporelles, la modélisation de graphes et les systèmes RAG.',
                'Mon expertise couvre l\'ensemble de la chaîne de valeur data, de l\'acquisition à la mise en production, en passant par l\'analyse et la visualisation.'
            ]
        },
        'skills': {
            'title': 'Domaines d\'expertise'
        },
        'experiences': {
            'title': 'Expériences',
            'formation_title': 'Formation'
        },
        'projects': {
            'title': 'Projets',
            'all': 'Tous',
            'osint': 'OSINT',
            'ai': 'IA',
            'web': 'Web'
        },
        'contact': {
            'title': 'Contact',
            'name': 'Nom',
            'email': 'Email',
            'message': 'Message',
            'send': 'Envoyer'
        }
    },
    'en': {
        'nav': {
            'presentation': 'About',
            'experiences': 'Experience',
            'projects': 'Projects',
            'contact': 'Contact'
        },
        'hero': {
            'typed_text': ['AI ENGINEERING', 'DATA ANALYTICS', 'INNOVATION'],
            'subtitle': '"Data is the new oil, but unlike oil, the more you share it, the more valuable it becomes!" 🚀'
        },
        'about': {
            'title': 'About Me',
            'role': 'Data Scientist',
            'bio': [
                'I have 5 years of experience in developing Machine Learning models and implementing Artificial Intelligence solutions.',
                'I am passionate about generative AI, data analysis, and statistical modeling.',
                'I have demonstrated my ability to design innovative solutions such as time series classification, graph modeling, and RAG systems.',
                'My expertise covers the entire data value chain, from acquisition to production deployment, including analysis and visualization.'
            ]
        },
        'skills': {
            'title': 'Areas of Expertise'
        },
        'experiences': {
            'title': 'Experience',
            'formation_title': 'Education'
        },
        'projects': {
            'title': 'Projects',
            'all': 'All',
            'osint': 'OSINT',
            'ai': 'AI',
            'web': 'Web'
        },
        'contact': {
            'title': 'Contact',
            'name': 'Name',
            'email': 'Email',
            'message': 'Message',
            'send': 'Send'
        }
    }
}

def send_email(name, email, message):
    """
    Envoie un email via SMTP avec les données du formulaire de contact
    """
    try:
        # Création du message
        msg = MIMEMultipart()
        msg['From'] = SMTP_CONFIG['FROM_EMAIL']
        msg['To'] = SMTP_CONFIG['TO_EMAIL']
        msg['Subject'] = f"Nouveau message de contact - Portfolio Sem EGLOH LOKOH"
        
        # Corps du message
        body = f"""
        Nouveau message reçu depuis votre portfolio :
        
        Nom: {name}
        Email: {email}
        
        Message:
        {message}
        
        ---
        Ce message a été envoyé depuis le formulaire de contact de votre portfolio.
        """
        
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        
        # Connexion au serveur SMTP
        server = smtplib.SMTP(SMTP_CONFIG['SMTP_SERVER'], SMTP_CONFIG['SMTP_PORT'])
        server.starttls()  # Activation du chiffrement TLS
        server.login(SMTP_CONFIG['SMTP_USERNAME'], SMTP_CONFIG['SMTP_PASSWORD'])
        
        # Envoi de l'email
        text = msg.as_string()
        server.sendmail(SMTP_CONFIG['FROM_EMAIL'], SMTP_CONFIG['TO_EMAIL'], text)
        server.quit()
        
        return True, "Email envoyé avec succès"
        
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email: {str(e)}")
        print(traceback.format_exc())
        return False, f"Erreur lors de l'envoi: {str(e)}"

@app.route('/')
def index():
    lang = request.args.get('lang', 'fr')
    if lang not in LANGUAGES:
        lang = 'fr'
    session['lang'] = lang
    return render_template('index.html', texts=LANGUAGES[lang], current_lang=lang)

@app.route('/contact', methods=['POST'])
def contact():
    try:
        data = request.json
        if not data:
            return jsonify({
                'status': 'error', 
                'message': 'Aucune donnée reçue'
            }), 400
            
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        message = data.get('message', '').strip()
        
        # Validation des données
        if not name or not email or not message:
            return jsonify({
                'status': 'error', 
                'message': 'Tous les champs sont obligatoires'
            }), 400
        
        # Validation basique de l'email
        if '@' not in email or '.' not in email:
            return jsonify({
                'status': 'error', 
                'message': 'Format d\'email invalide'
            }), 400
        
        # Envoi de l'email
        success, message_result = send_email(name, email, message)
        
        if success:
            return jsonify({
                'status': 'success', 
                'message': 'Message envoyé avec succès! Je vous répondrai dans les plus brefs délais.'
            })
        else:
            return jsonify({
                'status': 'error', 
                'message': 'Erreur lors de l\'envoi du message. Veuillez réessayer ou me contacter directement.'
            }), 500
            
    except Exception as e:
        print(f"Erreur dans la route contact: {str(e)}")
        return jsonify({
            'status': 'error', 
            'message': 'Une erreur inattendue s\'est produite'
        }), 500

if __name__ == '__main__':
    # Configuration pour la production
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
