"""
Paramètres généraux de l'application
Configuration globale et constantes
"""

import os
from pathlib import Path
from typing import Dict, Any

# Chemins de l'application
BASE_DIR = Path(__file__).parent.parent.parent
SRC_DIR = BASE_DIR / "src"
DATA_DIR = BASE_DIR / "data"
TESTS_DIR = BASE_DIR / "tests"

# Création des dossiers de données s'ils n'existent pas
DATA_DIR.mkdir(exist_ok=True)
(DATA_DIR / "evaluations").mkdir(exist_ok=True)
(DATA_DIR / "templates").mkdir(exist_ok=True)
(DATA_DIR / "exports").mkdir(exist_ok=True)

# Configuration de l'application
APP_CONFIG = {
    "name": "Dashboard Éco-Évaluation",
    "version": "1.0.0",
    "description": "Évaluation environnementale et éco-sociale des expositions culturelles",
    "author": "Équipe Développement",
    "license": "MIT",
    "debug": os.getenv("DEBUG", "False").lower() == "true"
}

# Configuration Streamlit
STREAMLIT_CONFIG = {
    "page_title": "Éco-Évaluation Expositions",
    "page_icon": "🌱",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
    "menu_items": {
        "Get Help": None,
        "Report a bug": None,
        "About": f"{APP_CONFIG['name']} v{APP_CONFIG['version']}"
    }
}

# Configuration de stockage
STORAGE_CONFIG = {
    "format": "json",  # ou "sqlite"
    "backup_enabled": True,
    "backup_frequency": "daily",
    "max_file_size": 10 * 1024 * 1024,  # 10MB
    "evaluations_file": DATA_DIR / "evaluations" / "evaluations.json",
    "templates_dir": DATA_DIR / "templates",
    "exports_dir": DATA_DIR / "exports"
}

# Configuration des couleurs et thèmes
THEME_CONFIG = {
    "primary_color": "#2E7D32",      # Vert foncé
    "secondary_color": "#1976D2",    # Bleu
    "success_color": "#388E3C",      # Vert succès
    "warning_color": "#F57C00",      # Orange
    "error_color": "#D32F2F",        # Rouge
    "info_color": "#0288D1",         # Bleu info
    "background_color": "#FAFAFA",   # Gris très clair
    "text_color": "#212121"          # Gris foncé
}

# Configuration des graphiques
CHART_CONFIG = {
    "default_height": 400,
    "color_palette": [
        "#2E7D32", "#1976D2", "#F57C00", "#7B1FA2", "#00796B",
        "#5D4037", "#455A64", "#E53935", "#00ACC1", "#8BC34A"
    ],
    "performance_colors": {
        "excellent": "#4CAF50",
        "good": "#8BC34A",
        "average": "#FFC107",
        "poor": "#FF5722"
    }
}

# Configuration des exports
EXPORT_CONFIG = {
    "pdf": {
        "page_size": "A4",
        "orientation": "portrait",
        "margins": {"top": 2, "bottom": 2, "left": 2, "right": 2},
        "font_family": "Helvetica",
        "include_charts": True
    },
    "excel": {
        "format": "xlsx",
        "include_formulas": True,
        "include_charts": True,
        "sheet_protection": False
    }
}

# Configuration de validation
VALIDATION_CONFIG = {
    "required_fields_strict": True,
    "numeric_bounds_check": True,
    "percentage_validation": True,
    "date_format": "%Y-%m-%d",
    "max_text_length": 1000
}

# Messages d'interface utilisateur
UI_MESSAGES = {
    "fr": {
        "welcome": "Bienvenue dans le Dashboard d'Éco-Évaluation",
        "questionnaire_start": "Commencer une nouvelle évaluation",
        "save_success": "Évaluation sauvegardée avec succès",
        "save_error": "Erreur lors de la sauvegarde",
        "load_success": "Évaluation chargée avec succès",
        "load_error": "Erreur lors du chargement",
        "validation_error": "Veuillez corriger les erreurs avant de continuer",
        "export_success": "Export réalisé avec succès",
        "required_field": "Ce champ est obligatoire",
        "invalid_number": "Veuillez saisir un nombre valide",
        "invalid_percentage": "Veuillez saisir un pourcentage entre 0 et 100",
        "confirm_delete": "Êtes-vous sûr de vouloir supprimer cette évaluation ?",
        "no_data": "Aucune donnée disponible",
        "loading": "Chargement en cours...",
        "processing": "Traitement en cours..."
    }
}

# Configuration des notifications
NOTIFICATION_CONFIG = {
    "auto_dismiss": True,
    "dismiss_delay": 5000,  # millisecondes
    "position": "top-right"
}

# Limites et contraintes
LIMITS = {
    "max_evaluations": 1000,
    "max_file_upload_size": 5 * 1024 * 1024,  # 5MB
    "session_timeout": 3600,  # 1 heure en secondes
    "max_concurrent_users": 100,
    "rate_limit_requests_per_minute": 60
}

# Configuration de sécurité
SECURITY_CONFIG = {
    "sanitize_inputs": True,
    "validate_file_types": True,
    "allowed_file_extensions": [".json", ".xlsx", ".csv"],
    "max_upload_files": 10
}

# Configuration des logs (pour version future)
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": DATA_DIR / "logs" / "app.log",
    "max_size": 10 * 1024 * 1024,  # 10MB
    "backup_count": 5
}

# URLs et liens utiles
EXTERNAL_LINKS = {
    "ademe_base_empreinte": "https://base-empreinte.ademe.fr/",
    "iso_14001": "https://www.iso.org/iso-14001-environmental-management.html",
    "iso_26000": "https://www.iso.org/iso-26000-social-responsibility.html",
    "documentation": "https://github.com/votre-repo/docs",
    "support": "mailto:support@exemple.com"
}

# Configuration des benchmarks sectoriels (valeurs de référence)
SECTOR_BENCHMARKS = {
    "small_museum": {
        "carbon_footprint_per_visitor": 2.5,  # kg CO₂eq
        "energy_consumption_per_m2": 150,     # kWh/m²/an
        "waste_generation_per_day": 5.0,      # kg/jour
        "recycling_rate": 45                  # %
    },
    "large_museum": {
        "carbon_footprint_per_visitor": 3.2,  # kg CO₂eq
        "energy_consumption_per_m2": 180,     # kWh/m²/an
        "waste_generation_per_day": 25.0,     # kg/jour
        "recycling_rate": 55                  # %
    },
    "temporary_exhibition": {
        "carbon_footprint_per_visitor": 1.8,  # kg CO₂eq
        "energy_consumption_per_m2": 120,     # kWh/m²/an
        "waste_generation_per_day": 3.0,      # kg/jour
        "recycling_rate": 40                  # %
    },
    "outdoor_exhibition": {
        "carbon_footprint_per_visitor": 0.8,  # kg CO₂eq
        "energy_consumption_per_m2": 50,      # kWh/m²/an
        "waste_generation_per_day": 2.0,      # kg/jour
        "recycling_rate": 60                  # %
    }
}

def get_config(section: str) -> Dict[str, Any]:
    """Récupérer une section de configuration"""
    configs = {
        "app": APP_CONFIG,
        "streamlit": STREAMLIT_CONFIG,
        "storage": STORAGE_CONFIG,
        "theme": THEME_CONFIG,
        "chart": CHART_CONFIG,
        "export": EXPORT_CONFIG,
        "validation": VALIDATION_CONFIG,
        "ui": UI_MESSAGES,
        "notification": NOTIFICATION_CONFIG,
        "limits": LIMITS,
        "security": SECURITY_CONFIG,
        "logging": LOGGING_CONFIG,
        "links": EXTERNAL_LINKS,
        "benchmarks": SECTOR_BENCHMARKS
    }

    return configs.get(section, {})

def get_message(key: str, language: str = "fr") -> str:
    """Récupérer un message d'interface utilisateur"""
    messages = UI_MESSAGES.get(language, UI_MESSAGES["fr"])
    return messages.get(key, key)

def is_debug_mode() -> bool:
    """Vérifier si le mode debug est activé"""
    return APP_CONFIG["debug"]

def get_data_path(subfolder: str = "") -> Path:
    """Obtenir le chemin vers un dossier de données"""
    if subfolder:
        path = DATA_DIR / subfolder
        path.mkdir(exist_ok=True)
        return path
    return DATA_DIR

def get_benchmark_for_type(exhibition_type: str) -> Dict[str, float]:
    """Obtenir les benchmarks pour un type d'exposition"""
    return SECTOR_BENCHMARKS.get(exhibition_type, SECTOR_BENCHMARKS["small_museum"])
