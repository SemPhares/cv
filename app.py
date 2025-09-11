from flask import Flask, render_template, request, jsonify, session
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

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

@app.route('/')
def index():
    lang = request.args.get('lang', 'fr')
    if lang not in LANGUAGES:
        lang = 'fr'
    session['lang'] = lang
    return render_template('index.html', texts=LANGUAGES[lang], current_lang=lang)

@app.route('/contact', methods=['POST'])
def contact():
    data = request.json
    # Ici vous pouvez traiter le formulaire de contact
    # Par exemple, envoyer un email ou sauvegarder en base
    return jsonify({'status': 'success', 'message': 'Message envoyé avec succès!'})

if __name__ == '__main__':
    app.run(debug=True)
