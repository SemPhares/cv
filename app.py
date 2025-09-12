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
            'activity': 'Activité',
            'experiences': 'Expériences',
            'projects': 'Projets',
            'contact': 'Contact'
        },
        'hero': {
            'typed_text': ['INGÉNIERIE IA', 'ANALYSE DE DONNÉES', 'INNOVATION'],
            'subtitle': '"Les données sont le nouveau pétrole, mais contrairement au pétrole, plus on les partage, plus elles prennent de la valeur !" 🚀',
            'cta_text': 'Découvrir mon profil'
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
        'activity': {
            'title': 'Activité',
            'link': 'https://easylife-planner-1ts9v6m.gamma.site/accueil-easylifeplanner',
            'name': 'EasyLife Planner',
            'description': 'Avec mon épouse nous avons lancé "EasyLife Planner", une structure qui propose des services sur mesure pour simplifier la vie quotidienne, notamment la planification personnalisée de repas et de voyages. L\'activité se concentre sur l\'organisation efficace du quotidien pour dégager du temps, réduire le stress et offrir des solutions totalement adaptées à chaque utilisateur, avec une touche d\'humour et beaucoup de bienveillance.'
        },
        'skills': {
            'title': 'Domaines d\'expertise'
        },
        'experiences': {
            'title': 'Expériences',
            'formation_title': 'Formation',
            'present': 'Présent',
            'previous': 'Précédente',
            'technical_environment': 'Environnement technique',
            'companies': {
                'cgi': {
                    'name': 'CGI FRANCE',
                    'roles': [
                        {
                            'title': 'Consultant Data - DGFIP (FINANCES PUBLIQUES)',
                            'missions': [
                                'Accompagnement & conduite du changement : support des agents DGFIP pour la migration des scripts legacy vers Python.',
                                'Développement Python : conception de packages pour automatiser la migration des données et du code SAS.',
                                'Migration & architecture cloud : transfert des données et conception d\'une architecture intermédiaire vers une cible cloud.',
                                'Analyses métiers & conseil : identification des besoins, optimisation des processus et recommandations de bonnes pratiques.'
                            ],
                            'tech': 'Python'
                        },
                        {
                            'title': 'Data Scientist - MONNOYEUR',
                            'missions': [
                                'Développement de parseurs spécialisés pour l\'analyse statique et l\'identification des dépendances de champs et du code mort.',
                                'Conception de graphes de dépendances reliant champs et programmes pour évaluer l\'impact des modifications de code.',
                                'Base de connaissance vectorielle : construction à partir de descriptions de chunks de code générées par LLM.',
                                'Automatisation via micro-services : analyse et requêtage du code en langage naturel.'
                            ],
                            'tech': 'Python, LangChain, Ollama, Pytest, NetworkX, RegEx, Deep Eval'
                        },
                        {
                            'title': 'Consultant Data - SOCIETE GENERALE',
                            'missions': [
                                'Conception et fiabilisation d\'un système de migration des flux de données Talend vers un environnement interne client.',
                                'Développement Python : création d\'un module pour la génération automatique de flux métiers.',
                                'Contrôle qualité & validation : mise en place de scripts de vérification et de validation des flux.'
                            ],
                            'tech': 'Python, PostgreSQL'
                        },
                        {
                            'title': 'Data Scientist - SPECBOT',
                            'missions': [
                                'Vectorisation & bases vectorielles : création et gestion d\'une base ChromaDB.',
                                'RAG (Retrieval-Augmented Generation) : développement d\'un système d\'extraction d\'informations à partir de fichiers Excel/PDF.',
                                'NLP & ranking : mise en œuvre d\'approches de query rewriting, classification et priorisation.',
                                'Architecture logicielle : développement de micro-services et tests unitaires.'
                            ],
                            'tech': 'Python, LangChain, Docker, Deep Eval, Flask, Pytest'
                        },
                        {
                            'title': 'Consultant Data - AG2R LA MONDIALE',
                            'missions': [
                                'Cadrage fonctionnel & recueil des besoins métiers, analyses et restitution client.',
                                'Développement Python (modules, backend Flask) et bases de données relationnelles (SQL).',
                                'Industrialisation & optimisation : automatisation de processus, intégration continue et DevOps.',
                                'Gestion de projet agile : suivi et coordination via JIRA.'
                            ],
                            'tech': 'Python, SQL, JIRA, UML, MCD, API, GitLab, DevOps'
                        },
                        {
                            'title': 'Data Scientist - REVITALISE',
                            'missions': [
                                'Recherche & état de l\'art : étude des approches de classification et de similarité des séries temporelles.',
                                'Feature engineering avancé : développement de classes pour l\'extraction de features (DTW, Shapelet, Time Forest).',
                                'Modélisation & machine learning : classification des signaux et détection de changements temporels.',
                                'Évaluation & benchmark : comparaison et analyse de performance des différentes approches.'
                            ],
                            'tech': 'Python, PyTorch'
                        }
                    ]
                },
                'bpce': {
                    'name': 'BPCE',
                    'roles': [
                        {
                            'title': 'Data Scientist – Lutte Anti-Blanchiment',
                            'missions': [
                                'Data acquisition : récupération de données via scraping et APIs (INPI – open data).',
                                'Développement applicatif : conception d\'une application web de génération automatique de graphes.',
                                'Analyse de graphes & machine learning : modélisation de graphes multi-couches pour la détection de liens suspects.',
                                'Industrialisation & optimisation : automatisation et déploiement en production.'
                            ],
                            'tech': 'Python, R, SQL, PySpark, PyTorch, NetworkX, Pyvis, BeautifulSoup, Flask, Azure, Docker, API REST, Git'
                        }
                    ]
                },
                'allianz': {
                    'name': 'ALLIANZ FRANCE',
                    'roles': [
                        {
                            'title': 'Data Scientist - Risques Climatiques',
                            'missions': [
                                'Pilotage sinistres climatiques : dashboarding Excel/VBA, datamart, cadrage besoins métiers.',
                                'Analyses spatiales & géomatiques : géocodage, shapefiles, IGN, interpolations.',
                                'Data engineering : constitution bases d\'apprentissage, préparation données.',
                                'Modélisation prédictive : classification binaire (inondations ruissellement), sinistres sécheresse.'
                            ],
                            'tech': 'Python, Scikit-Learn, TensorFlow, XGBoost, SAS, SQL, PySpark, VBA, Excel, ArcGIS'
                        }
                    ]
                }
            }
        },
        'tech_skills': {
            'title': 'Outils et Technologies',
            'categories': {
                'programming': 'Programmation',
                'databases': 'Bases de données',
                'ml_computing': 'Calculs et apprentissage',
                'devops': 'DevOps',
                'systems': 'Systèmes'
            }
        },
        'education': [
            {
                'year': '2022',
                'title': 'Master Data Science and Business Analysis',
                'institution': 'EDC Paris Business School'
            },
            {
                'year': '2020',
                'title': 'Licence Professionnelle Métiers du décisionnel et de la statistique',
                'institution': 'Aix Marseille Université'
            },
            {
                'year': '2019',
                'title': 'Licence Professionnelle Statistique Économique',
                'institution': 'École Nationale d\'Économie Appliquée (ENEAM)'
            }
        ],
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
            'send': 'Envoyer',
            'social_title': 'Retrouvez-moi sur'
        },
        'footer': {
            'copyright': '© 2025 Sem EGLOH LOKOH. Tous droits réservés.'
        }
    },
    'en': {
        'nav': {
            'presentation': 'About',
            'activity': 'Activity',
            'experiences': 'Experience',
            'projects': 'Projects',
            'contact': 'Contact'
        },
        'hero': {
            'typed_text': ['AI ENGINEERING', 'DATA ANALYTICS', 'INNOVATION'],
            'subtitle': '"Data is the new oil, but unlike oil, the more you share it, the more valuable it becomes!" 🚀',
            'cta_text': 'Discover my profile'
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
        'activity': {
            'title': 'Activity',
            'link': 'https://easylife-planner-1ts9v6m.gamma.site/accueil-easylifeplanner',
            'name': 'EasyLife Planner',
            'description': 'With my wife, we launched "EasyLife Planner", a structure that offers custom services to simplify daily life, including personalized meal and travel planning. The activity focuses on efficient daily organization to free up time, reduce stress and provide solutions totally adapted to each user, with a touch of humor and a lot of benevolence.'
        },
        'skills': {
            'title': 'Areas of Expertise'
        },
        'experiences': {
            'title': 'Experience',
            'formation_title': 'Education',
            'present': 'Present',
            'previous': 'Previous',
            'technical_environment': 'Technical Environment',
            'companies': {
                'cgi': {
                    'name': 'CGI FRANCE',
                    'roles': [
                        {
                            'title': 'Data Consultant - DGFIP (PUBLIC FINANCES)',
                            'missions': [
                                'Change management & support: assistance to DGFIP agents for legacy script migration to Python.',
                                'Python development: design of packages to automate data and SAS code migration.',
                                'Cloud migration & architecture: data transfer and design of intermediate architecture towards cloud target.',
                                'Business analysis & consulting: needs identification, process optimization and best practices recommendations.'
                            ],
                            'tech': 'Python'
                        },
                        {
                            'title': 'Data Scientist - MONNOYEUR',
                            'missions': [
                                'Development of specialized parsers for static analysis and identification of field dependencies and dead code.',
                                'Design of dependency graphs linking fields and programs to assess code modification impact.',
                                'Vector knowledge base: construction from LLM-generated code chunk descriptions.',
                                'Automation via micro-services: code analysis and querying in natural language.'
                            ],
                            'tech': 'Python, LangChain, Ollama, Pytest, NetworkX, RegEx, Deep Eval'
                        },
                        {
                            'title': 'Data Consultant - SOCIETE GENERALE',
                            'missions': [
                                'Design and reliability of Talend data flow migration system to internal client environment.',
                                'Python development: creation of module for automatic business flow generation.',
                                'Quality control & validation: implementation of verification and validation scripts for flows.'
                            ],
                            'tech': 'Python, PostgreSQL'
                        },
                        {
                            'title': 'Data Scientist - SPECBOT',
                            'missions': [
                                'Vectorization & vector databases: creation and management of ChromaDB database.',
                                'RAG (Retrieval-Augmented Generation): development of information extraction system from Excel/PDF files.',
                                'NLP & ranking: implementation of query rewriting, classification and prioritization approaches.',
                                'Software architecture: development of micro-services and unit tests.'
                            ],
                            'tech': 'Python, LangChain, Docker, Deep Eval, Flask, Pytest'
                        },
                        {
                            'title': 'Data Consultant - AG2R LA MONDIALE',
                            'missions': [
                                'Functional scoping & business requirements gathering, analysis and client reporting.',
                                'Python development (modules, Flask backend) and relational databases (SQL).',
                                'Industrialization & optimization: process automation, continuous integration and DevOps.',
                                'Agile project management: monitoring and coordination via JIRA.'
                            ],
                            'tech': 'Python, SQL, JIRA, UML, MCD, API, GitLab, DevOps'
                        },
                        {
                            'title': 'Data Scientist - REVITALISE',
                            'missions': [
                                'Research & state of the art: study of time series classification and similarity approaches.',
                                'Advanced feature engineering: development of feature extraction classes (DTW, Shapelet, Time Forest).',
                                'Modeling & machine learning: signal classification and temporal change detection.',
                                'Evaluation & benchmark: comparison and performance analysis of different approaches.'
                            ],
                            'tech': 'Python, PyTorch'
                        }
                    ]
                },
                'bpce': {
                    'name': 'BPCE',
                    'roles': [
                        {
                            'title': 'Data Scientist – Anti-Money Laundering',
                            'missions': [
                                'Data acquisition: data retrieval via scraping and APIs (INPI – open data).',
                                'Application development: design of automatic graph generation web application.',
                                'Graph analysis & machine learning: multi-layer graph modeling for suspicious link detection.',
                                'Industrialization & optimization: automation and production deployment.'
                            ],
                            'tech': 'Python, R, SQL, PySpark, PyTorch, NetworkX, Pyvis, BeautifulSoup, Flask, Azure, Docker, REST API, Git'
                        }
                    ]
                },
                'allianz': {
                    'name': 'ALLIANZ FRANCE',
                    'roles': [
                        {
                            'title': 'Data Scientist - Climate Risks',
                            'missions': [
                                'Climate claims management: Excel/VBA dashboarding, datamart, business requirements scoping.',
                                'Spatial & geomatics analysis: geocoding, shapefiles, IGN, interpolations.',
                                'Data engineering: learning database constitution, data preparation.',
                                'Predictive modeling: binary classification (runoff flooding), drought claims.'
                            ],
                            'tech': 'Python, Scikit-Learn, TensorFlow, XGBoost, SAS, SQL, PySpark, VBA, Excel, ArcGIS'
                        }
                    ]
                }
            }
        },
        'tech_skills': {
            'title': 'Tools and Technologies',
            'categories': {
                'programming': 'Programming',
                'databases': 'Databases',
                'ml_computing': 'ML & Computing',
                'devops': 'DevOps',
                'systems': 'Systems'
            }
        },
        'education': [
            {
                'year': '2022',
                'title': 'Master Data Science and Business Analysis',
                'institution': 'EDC Paris Business School'
            },
            {
                'year': '2020',
                'title': 'Professional Bachelor in Decision-Making and Statistics',
                'institution': 'Aix Marseille University'
            },
            {
                'year': '2019',
                'title': 'Professional Bachelor in Economic Statistics',
                'institution': 'National School of Applied Economics (ENEAM)'
            }
        ],
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
            'send': 'Send',
            'social_title': 'Find me on'
        },
        'footer': {
            'copyright': '© 2025 Sem EGLOH LOKOH. All rights reserved.'
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
