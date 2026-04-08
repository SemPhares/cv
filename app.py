from flask import Flask, render_template, request, jsonify, session, send_from_directory
import os
from dotenv import load_dotenv
import smtplib

load_dotenv()  # charge automatiquement le fichier .env
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
            'services': 'Services',
            'contact': 'Contact'
        },
        'hero': {
            'typed_text': ['ARCHITECTE IA', 'PIPELINES LLM & RAG', 'LEAD TECHNIQUE'],
            'subtitle': 'Vous avez un problème métier. Je conçois la solution IA qui le résout — de l\'architecture au déploiement.',
            'cta_text': 'Découvrir mon profil',
            'cta_download': 'Télécharger mon CV',
            'cta_linkedin': 'Me contacter sur LinkedIn'
        },
        'about': {
            'title': 'À Propos',
            'role': 'Ingénieur IA',
            'bio': [
                'Ingénieur IA avec 5 années d\'expérience, spécialisé dans la conception de systèmes d\'IA end-to-end, le développement de pipelines LLM et l\'architecture de solutions RAG.',
                'Je suis passionné par l\'IA générative, le traitement du langage naturel et la mise en production de solutions robustes et scalables.',
                'J\'ai démontré ma capacité à concevoir et piloter des produits IA de A à Z, notamment des architectures RAG hybrides, des sys­tèmes de retro-documentation intelligente et des modèles de graphes.',
                'Mon expertise couvre l\'ensemble de la chaîne de valeur data, de l\'acquisition à l\'industrialisation, en passant par l\'ingénierie LLM, l\'évaluation et le déploiement.'
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
        'metrics': [
            {'value': '5+', 'label': 'Années d\'expérience'},
            {'value': '+50 TB', 'label': 'Données migrées (DGFIP)'},
            {'value': '+25 000', 'label': 'Documents indexés (RAG)'},
            {'value': '< 7 s', 'label': 'Temps de réponse RAG'},
            {'value': '2', 'label': 'Data Scientists encadrés'},
        ],
        'services': {
            'title': 'Services',
            'subtitle': 'Trois offres concrètes pour transformer vos données en valeur.',
            'cta': 'Discutons de votre projet',
            'cards': [
                {
                    'icon': 'fas fa-drafting-compass',
                    'title': 'Audit & Architecture IA',
                    'description': 'Évaluation de votre stack actuelle, définition d\'une architecture RAG/LLM adaptée à vos besoins, état de l\'art et recommandations technologiques.'
                },
                {
                    'icon': 'fas fa-code',
                    'title': 'Développement & Intégration',
                    'description': 'Conception et développement de pipelines LLM complets, APIs scalables, systèmes RAG hybrides et déploiement en production.'
                },
                {
                    'icon': 'fas fa-users-cog',
                    'title': 'Lead Technique & Accompagnement',
                    'description': 'Pilotage de product IA, encadrement d\'équipes, revue de code, POC, et transfert de compétences sur les technologies IA modernes.'
                }
            ]
        },
        'experiences': {
            'title': 'Expériences',
            'formation_title': 'Formation',
            'present': 'Présent',
            'previous': 'Précédente',
            'technical_environment': 'Environnement technique',
            'companies': {
                'aquila': {
                    'name': 'AQUILA DATA',
                    'roles': [
                        {
                            'title': 'AI Engineer – ADP GSI (Rétro-documentation Paie)',
                            'missions': [
                                'Lead technique du produit IA « Retrodocpaie » : conception from scratch d\'une API scalable validée par les experts ADP. Encadrement de deux Data Scientists juniors.',
                                'Pipeline LLM : génération unitaire et batch de règles de paie (GPT-4.1, Claude Sonnet 4.5), gestion avancée des limites TPM, module d\'évaluation automatique de la qualité (60-90 s par règle).',
                                'Architecture RAG hybride : pipelines d\'ingestion Elasticsearch / Amazon OpenSearch, recherche vectorielle + BM25, reranking, validation Pydantic, prompts de sécurité stricts. Temps de réponse < 7 secondes.',
                                'Observabilité & industrialisation : monitoring et traçabilité bout-en-bout du pipeline RAG, conteneurisation Docker, déploiement via Artifactory ADP. Développement d\'une application frontend autonome pour les tests et la validation UX.'
                            ],
                            'tech': 'Python, GPT-4.1, Claude Sonnet 4.5, Elasticsearch, Amazon OpenSearch, Docker, Pydantic, FastAPI'
                        }
                    ]
                },
                'cgi': {
                    'name': 'CGI FRANCE',
                    'roles': [
                        {
                            'title': 'Consultant Data - DGFIP (FINANCES PUBLIQUES)',
                            'missions': [
                                'Migration de base de code SAS vers Python (Spark et Polars) : conception de connecteurs personnalisés lecture/écriture.',
                                'Développement et packaging de modules Python pour l\'analyse statistique des données DGFIP.',
                                'Orchestration et migration de base de données vers Spark (+50 TB) avec double-run pour assurer la disponibilité des données.',
                                'Accompagnement & conduite du changement : support des agents DGFIP pour la migration des scripts legacy vers Python.'
                            ],
                            'tech': 'Python, PySpark, Polars'
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
            'services': 'Services',
            'contact': 'Contact'
        },
        'hero': {
            'typed_text': ['AI ARCHITECT', 'LLM & RAG PIPELINES', 'TECHNICAL LEAD'],
            'subtitle': 'You have a business problem. I build the AI system that solves it — from architecture to deployment.',
            'cta_text': 'Discover my profile',
            'cta_download': 'Download my CV',
            'cta_linkedin': 'Connect on LinkedIn'
        },
        'about': {
            'title': 'About Me',
            'role': 'AI Engineer',
            'bio': [
                'AI Engineer with more than 5 years of experience, specialized in designing end-to-end AI systems, LLM pipeline development, and RAG solution architecture.',
                'I am passionate about generative AI, natural language processing, and deploying robust, scalable solutions to production.',
                'I have demonstrated my ability to lead and build AI products from scratch, including hybrid RAG architectures, intelligent retro-documentation systems, and graph models.',
                'My expertise covers the entire data value chain, from acquisition to industrialization, including LLM engineering, evaluation, and deployment.'
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
        'metrics': [
            {'value': '5+', 'label': 'Years of experience'},
            {'value': '+50 TB', 'label': 'Data migrated (DGFIP)'},
            {'value': '+25,000', 'label': 'Documents indexed (RAG)'},
            {'value': '< 7 s', 'label': 'RAG response time'},
            {'value': '2', 'label': 'Junior Data Scientists mentored'},
        ],
        'services': {
            'title': 'Services',
            'subtitle': 'Three concrete offerings to turn your data into value.',
            'cta': 'Let\'s discuss your project',
            'cards': [
                {
                    'icon': 'fas fa-drafting-compass',
                    'title': 'AI Audit & Architecture',
                    'description': 'Assessment of your current stack, definition of a RAG/LLM architecture tailored to your needs, state-of-the-art review and technology recommendations.'
                },
                {
                    'icon': 'fas fa-code',
                    'title': 'Development & Integration',
                    'description': 'End-to-end LLM pipeline design and development, scalable APIs, hybrid RAG systems and production deployment.'
                },
                {
                    'icon': 'fas fa-users-cog',
                    'title': 'Technical Lead & Coaching',
                    'description': 'AI product leadership, team mentoring, code review, POC delivery, and skills transfer on modern AI technologies.'
                }
            ]
        },
        'experiences': {
            'title': 'Experience',
            'formation_title': 'Education',
            'present': 'Present',
            'previous': 'Previous',
            'technical_environment': 'Technical Environment',
            'companies': {
                'aquila': {
                    'name': 'AQUILA DATA',
                    'roles': [
                        {
                            'title': 'AI Engineer – ADP GSI (Payroll Retro-Documentation)',
                            'missions': [
                                'Technical lead of the “Retrodocpaie” AI product: from-scratch design of a scalable API, validated by ADP technical experts. Daily mentoring of two junior Data Scientists.',
                                'LLM pipeline: unit and batch generation of payroll rules (GPT-4.1, Claude Sonnet 4.5), advanced TPM limit management, automatic quality evaluation module (60-90 s per rule).',
                                'Hybrid RAG architecture: ingestion pipelines on Elasticsearch / Amazon OpenSearch, vector + BM25 hybrid search, reranking, Pydantic validation, strict security prompts. End-to-end response time < 7 seconds.',
                                'Observability & industrialization: full API monitoring and end-to-end RAG pipeline traceability, Docker containerization and deployment via ADP Artifactory. Development of a standalone frontend application for testing and UX validation.'
                            ],
                            'tech': 'Python, GPT-4.1, Claude Sonnet 4.5, Elasticsearch, Amazon OpenSearch, Docker, Pydantic, FastAPI'
                        }
                    ]
                },
                'cgi': {
                    'name': 'CGI FRANCE',
                    'roles': [
                        {
                            'title': 'Data Consultant - DGFIP (PUBLIC FINANCES)',
                            'missions': [
                                'SAS codebase migration to Python (Spark and Polars): design of custom read/write connectors.',
                                'Development and packaging of Python modules for statistical analysis of DGFIP data.',
                                'Database orchestration and migration to Spark (+50 TB) with double-run to ensure data availability.',
                                'Change management & support: assistance to DGFIP agents for legacy script migration to Python.'
                            ],
                            'tech': 'Python, PySpark, Polars'
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

@app.route('/cv/download')
def download_cv():
    return send_from_directory(
        os.path.join(app.root_path, 'static', 'folder'),
        'CV_Sem_EGLOH LOKOH.pdf',
        as_attachment=True,
        download_name='CV_Sem_EGLOH_LOKOH.pdf'
    )

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
    port = int(os.environ.get('PORT'))
    debug_mode = os.environ.get('ENVIRONMENT') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug_mode, use_reloader=debug_mode)
