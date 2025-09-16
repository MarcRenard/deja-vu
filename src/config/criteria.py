"""
Configuration des critères d'évaluation environnementale et éco-sociale
Basée sur le document de référence fourni
"""

from typing import Dict, List, Any
from enum import Enum

class QuestionType(Enum):
    """Types de questions pour le questionnaire"""
    NUMERIC = "numeric"          # Valeur numérique (kg, kWh, %, etc.)
    BOOLEAN = "boolean"          # Oui/Non
    MULTIPLE_CHOICE = "multiple_choice"  # Choix multiples
    SCALE = "scale"              # Échelle (1-10, 1-5, etc.)
    TEXT = "text"                # Texte libre
    PERCENTAGE = "percentage"    # Pourcentage (0-100)

class ImpactLevel(Enum):
    """Niveaux d'impact pour la classification"""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

# Structure principale des critères
EVALUATION_CRITERIA = {
    "impacts_environnementaux_directs": {
        "title": "1. Impacts Environnementaux Directs",
        "description": "Évaluation des impacts directs de l'exposition sur l'environnement",
        "weight": 0.3,  # Pondération dans le score global
        "subcategories": {
            "materiaux_ressources": {
                "title": "Matériaux et Ressources",
                "questions": {
                    "empreinte_carbone_materiaux": {
                        "question": "Quelle est l'empreinte carbone estimée des matériaux utilisés ?",
                        "type": QuestionType.NUMERIC,
                        "unit": "kg CO₂eq",
                        "help_text": "Inclure extraction, transformation et transport des matériaux",
                        "required": True,
                        "impact_level": ImpactLevel.HIGH
                    },
                    "consommation_eau_production": {
                        "question": "Consommation d'eau lors de la production des matériaux",
                        "type": QuestionType.NUMERIC,
                        "unit": "litres",
                        "required": False,
                        "impact_level": ImpactLevel.MEDIUM
                    },
                    "materiaux_recycles": {
                        "question": "Pourcentage de matériaux recyclés utilisés",
                        "type": QuestionType.PERCENTAGE,
                        "help_text": "% de matériaux issus du recyclage",
                        "required": True,
                        "impact_level": ImpactLevel.HIGH
                    },
                    "materiaux_biosources": {
                        "question": "Pourcentage de matériaux biosourcés",
                        "type": QuestionType.PERCENTAGE,
                        "required": False,
                        "impact_level": ImpactLevel.MEDIUM
                    },
                    "toxicite_materiaux": {
                        "question": "Les matériaux utilisés présentent-ils une toxicité (COV, formaldéhyde, métaux lourds) ?",
                        "type": QuestionType.MULTIPLE_CHOICE,
                        "options": ["Aucune toxicité", "Toxicité faible", "Toxicité modérée", "Toxicité élevée"],
                        "required": True,
                        "impact_level": ImpactLevel.HIGH
                    },
                    "reutilisation_apres_exposition": {
                        "question": "Capacité de réutilisation des matériaux après exposition",
                        "type": QuestionType.SCALE,
                        "scale_min": 1,
                        "scale_max": 10,
                        "scale_labels": {"1": "Aucune réutilisation", "10": "Réutilisation totale"},
                        "required": True,
                        "impact_level": ImpactLevel.HIGH
                    }
                }
            },
            "energie_climat": {
                "title": "Énergie et Climat",
                "questions": {
                    "consommation_eclairage": {
                        "question": "Consommation énergétique pour l'éclairage",
                        "type": QuestionType.NUMERIC,
                        "unit": "kWh",
                        "required": True,
                        "impact_level": ImpactLevel.HIGH
                    },
                    "consommation_climatisation": {
                        "question": "Consommation énergétique pour climatisation/chauffage",
                        "type": QuestionType.NUMERIC,
                        "unit": "kWh",
                        "required": True,
                        "impact_level": ImpactLevel.HIGH
                    },
                    "energies_renouvelables": {
                        "question": "Pourcentage d'énergies renouvelables utilisées",
                        "type": QuestionType.PERCENTAGE,
                        "required": True,
                        "impact_level": ImpactLevel.HIGH
                    },
                    "efficacite_energetique": {
                        "question": "Niveau d'efficacité énergétique des équipements",
                        "type": QuestionType.MULTIPLE_CHOICE,
                        "options": ["Classe A+++", "Classe A++", "Classe A+", "Classe A", "Classe B ou inférieure"],
                        "required": False,
                        "impact_level": ImpactLevel.MEDIUM
                    }
                }
            },
            "transport_logistique": {
                "title": "Transport et Logistique",
                "questions": {
                    "distance_transport_materiaux": {
                        "question": "Distance moyenne de transport des matériaux",
                        "type": QuestionType.NUMERIC,
                        "unit": "km",
                        "required": True,
                        "impact_level": ImpactLevel.HIGH
                    },
                    "mode_transport": {
                        "question": "Principal mode de transport utilisé",
                        "type": QuestionType.MULTIPLE_CHOICE,
                        "options": ["Train", "Camion", "Bateau", "Avion", "Transport multimodal"],
                        "required": True,
                        "impact_level": ImpactLevel.HIGH
                    },
                    "optimisation_livraisons": {
                        "question": "Niveau d'optimisation des livraisons",
                        "type": QuestionType.SCALE,
                        "scale_min": 1,
                        "scale_max": 5,
                        "scale_labels": {"1": "Aucune optimisation", "5": "Optimisation maximale"},
                        "required": False,
                        "impact_level": ImpactLevel.MEDIUM
                    }
                }
            },
            "dechets_pollution": {
                "title": "Déchets et Pollution",
                "questions": {
                    "volume_dechets_construction": {
                        "question": "Volume de déchets générés pendant la construction",
                        "type": QuestionType.NUMERIC,
                        "unit": "kg",
                        "required": True,
                        "impact_level": ImpactLevel.HIGH
                    },
                    "taux_recyclage": {
                        "question": "Taux de recyclage des déchets d'exposition",
                        "type": QuestionType.PERCENTAGE,
                        "required": True,
                        "impact_level": ImpactLevel.HIGH
                    },
                    "dechets_dangereux": {
                        "question": "Production de déchets dangereux ou toxiques",
                        "type": QuestionType.BOOLEAN,
                        "required": True,
                        "impact_level": ImpactLevel.HIGH
                    },
                    "pollution_air_interieur": {
                        "question": "Mesures prises contre la pollution de l'air intérieur",
                        "type": QuestionType.MULTIPLE_CHOICE,
                        "options": ["Aucune mesure", "Ventilation basique", "Filtration avancée", "Matériaux faibles émissions", "Contrôle complet COV"],
                        "required": False,
                        "impact_level": ImpactLevel.MEDIUM
                    }
                }
            }
        }
    },

    "impacts_environnementaux_indirects": {
        "title": "2. Impacts Environnementaux Indirects",
        "description": "Évaluation des impacts indirects et du cycle de vie",
        "weight": 0.15,
        "subcategories": {
            "cycle_de_vie": {
                "title": "Cycle de Vie",
                "questions": {
                    "fin_de_vie_materiaux": {
                        "question": "Impact de la fin de vie des matériaux",
                        "type": QuestionType.MULTIPLE_CHOICE,
                        "options": ["Réutilisation totale", "Recyclage majoritaire", "Incinération valorisation", "Enfouissement partiel", "Enfouissement total"],
                        "required": True,
                        "impact_level": ImpactLevel.HIGH
                    },
                    "circularite": {
                        "question": "Potentiel de circularité des éléments d'exposition",
                        "type": QuestionType.SCALE,
                        "scale_min": 1,
                        "scale_max": 10,
                        "scale_labels": {"1": "Linéaire", "10": "Totalement circulaire"},
                        "required": True,
                        "impact_level": ImpactLevel.MEDIUM
                    }
                }
            },
            "effets_systemiques": {
                "title": "Effets Systémiques",
                "questions": {
                    "ilot_chaleur_urbain": {
                        "question": "Contribution à l'îlot de chaleur urbain",
                        "type": QuestionType.SCALE,
                        "scale_min": 1,
                        "scale_max": 5,
                        "scale_labels": {"1": "Aucune contribution", "5": "Contribution majeure"},
                        "required": False,
                        "impact_level": ImpactLevel.LOW
                    }
                }
            }
        }
    },

    "impacts_eco_sociaux": {
        "title": "3. Impacts Éco-Sociaux",
        "description": "Évaluation de la justice sociale, équité et impact local",
        "weight": 0.3,
        "subcategories": {
            "justice_sociale": {
                "title": "Justice Sociale et Équité",
                "questions": {
                    "conditions_travail": {
                        "question": "Évaluation des conditions de travail dans la chaîne d'approvisionnement",
                        "type": QuestionType.SCALE,
                        "scale_min": 1,
                        "scale_max": 10,
                        "scale_labels": {"1": "Conditions précaires", "10": "Conditions excellentes"},
                        "required": True,
                        "impact_level": ImpactLevel.HIGH
                    },
                    "respect_droits_humains": {
                        "question": "Respect des droits humains (travail des enfants, sécurité)",
                        "type": QuestionType.BOOLEAN,
                        "required": True,
                        "impact_level": ImpactLevel.HIGH
                    },
                    "egalite_homme_femme": {
                        "question": "Égalité homme-femme dans les métiers sollicités",
                        "type": QuestionType.SCALE,
                        "scale_min": 1,
                        "scale_max": 10,
                        "required": False,
                        "impact_level": ImpactLevel.MEDIUM
                    },
                    "accessibilite_mobilite_reduite": {
                        "question": "Accessibilité aux personnes à mobilité réduite",
                        "type": QuestionType.MULTIPLE_CHOICE,
                        "options": ["Non accessible", "Partiellement accessible", "Accessible avec aide", "Totalement accessible"],
                        "required": True,
                        "impact_level": ImpactLevel.HIGH
                    },
                    "accessibilite_economique": {
                        "question": "Tarification d'entrée",
                        "type": QuestionType.MULTIPLE_CHOICE,
                        "options": ["Gratuit", "Tarif social disponible", "Prix modéré", "Prix élevé"],
                        "required": True,
                        "impact_level": ImpactLevel.MEDIUM
                    }
                }
            },
            "economie_locale": {
                "title": "Économie Locale et Territoriale",
                "questions": {
                    "approvisionnement_local": {
                        "question": "Pourcentage d'approvisionnement local (< 200 km)",
                        "type": QuestionType.PERCENTAGE,
                        "required": True,
                        "impact_level": ImpactLevel.HIGH
                    },
                    "emplois_locaux": {
                        "question": "Création d'emplois locaux",
                        "type": QuestionType.NUMERIC,
                        "unit": "nombre d'emplois",
                        "required": False,
                        "impact_level": ImpactLevel.MEDIUM
                    },
                    "transfert_competences": {
                        "question": "Transfert de compétences vers les acteurs locaux",
                        "type": QuestionType.BOOLEAN,
                        "required": False,
                        "impact_level": ImpactLevel.MEDIUM
                    }
                }
            },
            "education_sensibilisation": {
                "title": "Éducation et Sensibilisation",
                "questions": {
                    "dimension_pedagogique": {
                        "question": "Dimension pédagogique sur les enjeux environnementaux",
                        "type": QuestionType.SCALE,
                        "scale_min": 1,
                        "scale_max": 10,
                        "scale_labels": {"1": "Aucune dimension", "10": "Très développée"},
                        "required": True,
                        "impact_level": ImpactLevel.MEDIUM
                    },
                    "formation_equipes": {
                        "question": "Formation des équipes aux enjeux durables",
                        "type": QuestionType.BOOLEAN,
                        "required": False,
                        "impact_level": ImpactLevel.LOW
                    }
                }
            }
        }
    },

    "impacts_temporels_contextuels": {
        "title": "4. Impacts Temporels et Contextuels",
        "description": "Évaluation de la durée, gouvernance et transparence",
        "weight": 0.15,
        "subcategories": {
            "duree_intensite": {
                "title": "Durée et Intensité",
                "questions": {
                    "duree_exposition": {
                        "question": "Durée totale de l'exposition",
                        "type": QuestionType.NUMERIC,
                        "unit": "jours",
                        "required": True,
                        "impact_level": ImpactLevel.MEDIUM
                    },
                    "nombre_visiteurs": {
                        "question": "Nombre estimé de visiteurs",
                        "type": QuestionType.NUMERIC,
                        "unit": "visiteurs",
                        "required": True,
                        "impact_level": ImpactLevel.MEDIUM
                    },
                    "reversibilite": {
                        "question": "Réversibilité des aménagements",
                        "type": QuestionType.SCALE,
                        "scale_min": 1,
                        "scale_max": 10,
                        "scale_labels": {"1": "Irréversible", "10": "Totalement réversible"},
                        "required": True,
                        "impact_level": ImpactLevel.MEDIUM
                    }
                }
            },
            "gouvernance_transparence": {
                "title": "Gouvernance et Transparence",
                "questions": {
                    "tracabilite_materiaux": {
                        "question": "Traçabilité de l'origine des matériaux",
                        "type": QuestionType.SCALE,
                        "scale_min": 1,
                        "scale_max": 10,
                        "scale_labels": {"1": "Aucune traçabilité", "10": "Traçabilité complète"},
                        "required": True,
                        "impact_level": ImpactLevel.MEDIUM
                    },
                    "certifications_fournisseurs": {
                        "question": "Certifications environnementales des fournisseurs",
                        "type": QuestionType.MULTIPLE_CHOICE,
                        "options": ["Aucune", "ISO 14001", "Labels sectoriels", "Multiples certifications"],
                        "required": False,
                        "impact_level": ImpactLevel.MEDIUM
                    },
                    "transparence_couts": {
                        "question": "Transparence sur les coûts environnementaux",
                        "type": QuestionType.BOOLEAN,
                        "required": False,
                        "impact_level": ImpactLevel.LOW
                    }
                }
            }
        }
    },

    "criteres_transversaux": {
        "title": "5. Critères Transversaux",
        "description": "Innovation, mesure et exemplarité",
        "weight": 0.1,
        "subcategories": {
            "mesure_quantification": {
                "title": "Mesure et Quantification",
                "questions": {
                    "methode_acv": {
                        "question": "Utilisation de méthodes d'Analyse de Cycle de Vie (ACV)",
                        "type": QuestionType.BOOLEAN,
                        "required": False,
                        "impact_level": ImpactLevel.MEDIUM
                    },
                    "objectifs_chiffres": {
                        "question": "Définition d'objectifs chiffrés de réduction d'impact",
                        "type": QuestionType.BOOLEAN,
                        "required": False,
                        "impact_level": ImpactLevel.MEDIUM
                    },
                    "systeme_compensation": {
                        "question": "Mise en place d'un système de compensation carbone",
                        "type": QuestionType.BOOLEAN,
                        "required": False,
                        "impact_level": ImpactLevel.LOW
                    }
                }
            },
            "innovation_exemplarite": {
                "title": "Innovation et Exemplarité",
                "questions": {
                    "materiaux_innovants": {
                        "question": "Utilisation de matériaux innovants éco-responsables",
                        "type": QuestionType.BOOLEAN,
                        "required": False,
                        "impact_level": ImpactLevel.MEDIUM
                    },
                    "potentiel_replication": {
                        "question": "Potentiel de réplication du modèle",
                        "type": QuestionType.SCALE,
                        "scale_min": 1,
                        "scale_max": 10,
                        "scale_labels": {"1": "Non réplicable", "10": "Facilement réplicable"},
                        "required": False,
                        "impact_level": Impact
