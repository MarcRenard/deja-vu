"""
Générateur de formulaires dynamiques pour le questionnaire
Création des widgets Streamlit selon les types de questions
"""

import streamlit as st
from typing import Dict, Any, Optional, Union, List
from datetime import date, datetime
import sys
import os

# Ajout du chemin pour les imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from config.criteria import QuestionType, EVALUATION_CRITERIA, get_questions_by_category
from data.models import QuestionResponse, ResponseValue

class QuestionRenderer:
    """Classe pour rendre les questions selon leur type"""

    def __init__(self):
        self.response_cache = {}

    def render_question(
        self,
        question_id: str,
        question_config: Dict[str, Any],
        current_value: Optional[ResponseValue] = None,
        key_suffix: str = ""
    ) -> Optional[ResponseValue]:
        """
        Rendre une question selon son type

        Args:
            question_id: Identifiant unique de la question
            question_config: Configuration de la question depuis criteria.py
            current_value: Valeur actuelle si elle existe
            key_suffix: Suffixe pour la clé Streamlit (éviter les doublons)

        Returns:
            Valeur de la réponse ou None si pas de réponse
        """
        question_type = question_config.get("type")
        question_text = question_config.get("question", "Question non définie")
        help_text = question_config.get("help_text")
        required = question_config.get("required", False)
        unit = question_config.get("unit")

        # Créer une clé unique pour Streamlit
        widget_key = f"{question_id}_{key_suffix}" if key_suffix else question_id

        # Afficher le titre de la question avec indicateur obligatoire
        question_label = question_text
        if required:
            question_label += " *"
        if unit:
            question_label += f" ({unit})"

        # Dispatcher selon le type de question
        if question_type == QuestionType.NUMERIC:
            return self._render_numeric_question(
                question_label, question_config, current_value, widget_key, help_text
            )
        elif question_type == QuestionType.PERCENTAGE:
            return self._render_percentage_question(
                question_label, question_config, current_value, widget_key, help_text
            )
        elif question_type == QuestionType.BOOLEAN:
            return self._render_boolean_question(
                question_label, question_config, current_value, widget_key, help_text
            )
        elif question_type == QuestionType.MULTIPLE_CHOICE:
            return self._render_multiple_choice_question(
                question_label, question_config, current_value, widget_key, help_text
            )
        elif question_type == QuestionType.SCALE:
            return self._render_scale_question(
                question_label, question_config, current_value, widget_key, help_text
            )
        elif question_type == QuestionType.TEXT:
            return self._render_text_question(
                question_label, question_config, current_value, widget_key, help_text
            )
        else:
            st.error(f"Type de question non supporté : {question_type}")
            return None

    def _render_numeric_question(
        self,
        label: str,
        config: Dict[str, Any],
        current_value: Optional[ResponseValue],
        key: str,
        help_text: Optional[str]
    ) -> Optional[float]:
        """Rendre une question numérique"""

        min_value = config.get("min_value", 0.0)
        max_value = config.get("max_value", 1000000.0)
        step = config.get("step", 0.1)

        # Convertir current_value en float si nécessaire
        value = None
        if current_value is not None:
            try:
                value = float(current_value)
            except (ValueError, TypeError):
                value = min_value

        return st.number_input(
            label=label,
            min_value=min_value,
            max_value=max_value,
            value=value,
            step=step,
            help=help_text,
            key=key
        )

    def _render_percentage_question(
        self,
        label: str,
        config: Dict[str, Any],
        current_value: Optional[ResponseValue],
        key: str,
        help_text: Optional[str]
    ) -> Optional[float]:
        """Rendre une question de pourcentage (0-100)"""

        # Convertir current_value en float si nécessaire
        value = None
        if current_value is not None:
            try:
                value = float(current_value)
                # S'assurer que c'est dans la plage 0-100
                value = max(0.0, min(100.0, value))
            except (ValueError, TypeError):
                value = 0.0

        return st.slider(
            label=label,
            min_value=0.0,
            max_value=100.0,
            value=value if value is not None else 0.0,
            step=1.0,
            format="%.0f%%",
            help=help_text,
            key=key
        )

    def _render_boolean_question(
        self,
        label: str,
        config: Dict[str, Any],
        current_value: Optional[ResponseValue],
        key: str,
        help_text: Optional[str]
    ) -> Optional[bool]:
        """Rendre une question booléenne (Oui/Non)"""

        # Options personnalisables
        true_label = config.get("true_label", "Oui")
        false_label = config.get("false_label", "Non")

        # Convertir current_value en index pour selectbox
        options = [false_label, true_label]
        index = 0

        if current_value is not None:
            if isinstance(current_value, bool):
                index = 1 if current_value else 0
            elif isinstance(current_value, str):
                index = 1 if current_value.lower() in ['oui', 'yes', 'true', '1'] else 0

        selected = st.selectbox(
            label=label,
            options=options,
            index=index,
            help=help_text,
            key=key
        )

        return selected == true_label

    def _render_multiple_choice_question(
        self,
        label: str,
        config: Dict[str, Any],
        current_value: Optional[ResponseValue],
        key: str,
        help_text: Optional[str]
    ) -> Optional[str]:
        """Rendre une question à choix multiples"""

        options = config.get("options", [])
        if not options:
            st.error("Aucune option définie pour cette question")
            return None

        # Déterminer l'index actuel
        index = 0
        if current_value is not None and str(current_value) in options:
            index = options.index(str(current_value))

        return st.selectbox(
            label=label,
            options=options,
            index=index,
            help=help_text,
            key=key
        )

    def _render_scale_question(
        self,
        label: str,
        config: Dict[str, Any],
        current_value: Optional[ResponseValue],
        key: str,
        help_text: Optional[str]
    ) -> Optional[int]:
        """Rendre une question d'échelle (1-5, 1-10, etc.)"""

        scale_min = config.get("scale_min", 1)
        scale_max = config.get("scale_max", 10)
        scale_labels = config.get("scale_labels", {})

        # Convertir current_value en int si nécessaire
        value = scale_min
        if current_value is not None:
            try:
                value = int(current_value)
                value = max(scale_min, min(scale_max, value))
            except (ValueError, TypeError):
                value = scale_min

        # Créer le slider avec labels si disponibles
        result = st.slider(
            label=label,
            min_value=scale_min,
            max_value=scale_max,
            value=value,
            step=1,
            help=help_text,
            key=key
        )

        # Afficher les labels d'échelle si définis
        if scale_labels:
            labels_text = " | ".join([
                f"{k}: {v}" for k, v in scale_labels.items()
                if k in [str(scale_min), str(scale_max)]
            ])
            if labels_text:
                st.caption(labels_text)

        return result

    def _render_text_question(
        self,
        label: str,
        config: Dict[str, Any],
        current_value: Optional[ResponseValue],
        key: str,
        help_text: Optional[str]
    ) -> Optional[str]:
        """Rendre une question de texte libre"""

        max_length = config.get("max_length", 1000)
        multiline = config.get("multiline", True)

        # Convertir current_value en string si nécessaire
        value = ""
        if current_value is not None:
            value = str(current_value)

        if multiline:
            return st.text_area(
                label=label,
                value=value,
                max_chars=max_length,
                help=help_text,
                key=key
            )
        else:
            return st.text_input(
                label=label,
                value=value,
                max_chars=max_length,
                help=help_text,
                key=key
            )

class SectionRenderer:
    """Classe pour rendre les sections du questionnaire"""

    def __init__(self):
        self.question_renderer = QuestionRenderer()

    def render_category_section(
        self,
        category_id: str,
        current_responses: Dict[str, Any] = None
    ) -> Dict[str, Dict[str, Any]]:
        """
        Rendre une catégorie complète avec toutes ses sous-catégories

        Args:
            category_id: ID de la catégorie à rendre
            current_responses: Réponses actuelles si elles existent

        Returns:
            Dict des réponses par sous-catégorie et question
        """
        category_config = get_questions_by_category(category_id)
        if not category_config:
            st.error(f"Catégorie {category_id} non trouvée")
            return {}

        # Titre de la catégorie
        st.markdown(f"## {category_config.get('title', 'Catégorie')}")

        if category_config.get('description'):
            st.info(category_config['description'])

        responses = {}
        subcategories = category_config.get('subcategories', {})

        # Créer des onglets pour les sous-catégories si plus de 2
        if len(subcategories) > 2:
            tabs = st.tabs(list(subcategories.keys()))

            for idx, (subcategory_id, subcategory_config) in enumerate(subcategories.items()):
                with tabs[idx]:
                    responses[subcategory_id] = self._render_subcategory(
                        subcategory_id,
                        subcategory_config,
                        current_responses.get(subcategory_id, {}) if current_responses else {}
                    )
        else:
            # Affichage direct pour 1-2 sous-catégories
            for subcategory_id, subcategory_config in subcategories.items():
                responses[subcategory_id] = self._render_subcategory(
                    subcategory_id,
                    subcategory_config,
                    current_responses.get(subcategory_id, {}) if current_responses else {}
                )

        return responses

    def _render_subcategory(
        self,
        subcategory_id: str,
        subcategory_config: Dict[str, Any],
        current_responses: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Rendre une sous-catégorie avec ses questions"""

        st.markdown(f"### {subcategory_config.get('title', 'Sous-catégorie')}")

        responses = {}
        questions = subcategory_config.get('questions', {})

        # Grouper les questions par colonnes si plus de 3
        if len(questions) > 3:
            # Utiliser des colonnes pour optimiser l'espace
            for idx, (question_id, question_config) in enumerate(questions.items()):
                if idx % 2 == 0:
                    col1, col2 = st.columns(2)

                with col1 if idx % 2 == 0 else col2:
                    current_value = current_responses.get(question_id) if current_responses else None
                    response_value = self.question_renderer.render_question(
                        question_id,
                        question_config,
                        current_value,
                        key_suffix=subcategory_id
                    )

                    if response_value is not None:
                        responses[question_id] = response_value
        else:
            # Affichage simple pour peu de questions
            for question_id, question_config in questions.items():
                current_value = current_responses.get(question_id) if current_responses else None
                response_value = self.question_renderer.render_question(
                    question_id,
                    question_config,
                    current_value,
                    key_suffix=subcategory_id
                )

                if response_value is not None:
                    responses[question_id] = response_value

        return responses

    def render_category_navigation(self, categories: List[str], current_category: str) -> str:
        """Rendre la navigation entre catégories"""

        # Créer une sidebar avec navigation
        with st.sidebar:
            st.markdown("### Navigation du questionnaire")

            # Afficher le progrès global
            progress = self._calculate_progress(categories, current_category)
            st.progress(progress / 100.0)
            st.caption(f"Progrès global : {progress:.0f}%")

            st.divider()

            # Boutons de navigation
            selected_category = st.radio(
                "Sections :",
                categories,
                index=categories.index(current_category) if current_category in categories else 0,
                format_func=lambda x: self._format_category_name(x)
            )

        return selected_category

    def _calculate_progress(self, categories: List[str], current_category: str) -> float:
        """Calculer le progrès approximatif"""
        if not categories:
            return 0.0

        try:
            current_index = categories.index(current_category)
            return (current_index / len(categories)) * 100
        except ValueError:
            return 0.0

    def _format_category_name(self, category_id: str) -> str:
        """Formater le nom d'affichage d'une catégorie"""
        category_config = get_questions_by_category(category_id)
        if category_config:
            return category_config.get('title', category_id.replace('_', ' ').title())
        return category_id.replace('_', ' ').title()

class QuestionnaireValidator:
    """Classe pour valider les réponses du questionnaire"""

    @staticmethod
    def validate_response(
        question_id: str,
        question_config: Dict[str, Any],
        response_value: ResponseValue
    ) -> List[str]:
        """
        Valider une réponse individuelle

        Returns:
            Liste des erreurs de validation (vide si valide)
        """
        errors = []

        # Vérifier si la question est obligatoire
        if question_config.get('required', False) and response_value is None:
            errors.append(f"Cette question est obligatoire")
            return errors

        if response_value is None:
            return errors  # Pas d'erreur si la question n'est pas obligatoire

        question_type = question_config.get('type')

        # Validation selon le type
        if question_type == QuestionType.NUMERIC:
            errors.extend(QuestionnaireValidator._validate_numeric(question_config, response_value))
        elif question_type == QuestionType.PERCENTAGE:
            errors.extend(QuestionnaireValidator._validate_percentage(response_value))
        elif question_type == QuestionType.SCALE:
            errors.extend(QuestionnaireValidator._validate_scale(question_config, response_value))
        elif question_type == QuestionType.MULTIPLE_CHOICE:
            errors.extend(QuestionnaireValidator._validate_multiple_choice(question_config, response_value))
        elif question_type == QuestionType.TEXT:
            errors.extend(QuestionnaireValidator._validate_text(question_config, response_value))

        return errors

    @staticmethod
    def _validate_numeric(config: Dict[str, Any], value: ResponseValue) -> List[str]:
        """Valider une valeur numérique"""
        errors = []

        try:
            num_value = float(value)

            min_value = config.get('min_value')
            max_value = config.get('max_value')

            if min_value is not None and num_value < min_value:
                errors.append(f"La valeur doit être supérieure ou égale à {min_value}")

            if max_value is not None and num_value > max_value:
                errors.append(f"La valeur doit être inférieure ou égale à {max_value}")

        except (ValueError, TypeError):
            errors.append("La valeur doit être un nombre valide")

        return errors

    @staticmethod
    def _validate_percentage(value: ResponseValue) -> List[str]:
        """Valider un pourcentage"""
        errors = []

        try:
            num_value = float(value)
            if not 0.0 <= num_value <= 100.0:
                errors.append("Le pourcentage doit être entre 0 et 100")
        except (ValueError, TypeError):
            errors.append("La valeur doit être un pourcentage valide")

        return errors

    @staticmethod
    def _validate_scale(config: Dict[str, Any], value: ResponseValue) -> List[str]:
        """Valider une valeur d'échelle"""
        errors = []

        try:
            num_value = int(value)
            scale_min = config.get('scale_min', 1)
            scale_max = config.get('scale_max', 10)

            if not scale_min <= num_value <= scale_max:
                errors.append(f"La valeur doit être entre {scale_min} et {scale_max}")

        except (ValueError, TypeError):
            errors.append("La valeur doit être un nombre entier valide")

        return errors

    @staticmethod
    def _validate_multiple_choice(config: Dict[str, Any], value: ResponseValue) -> List[str]:
        """Valider un choix multiple"""
        errors = []

        options = config.get('options', [])
        if str(value) not in options:
            errors.append(f"La valeur doit être l'une des options proposées : {', '.join(options)}")

        return errors

    @staticmethod
    def _validate_text(config: Dict[str, Any], value: ResponseValue) -> List[str]:
        """Valider un texte"""
        errors = []

        text_value = str(value)
        max_length = config.get('max_length', 1000)

        if len(text_value) > max_length:
            errors.append(f"Le texte ne peut pas dépasser {max_length} caractères")

        min_length = config.get('min_length', 0)
        if len(text_value.strip()) < min_length:
            errors.append(f"Le texte doit faire au moins {min_length} caractères")

        return errors

class QuestionnaireUI:
    """Interface utilisateur principale du questionnaire"""

    def __init__(self):
        self.section_renderer = SectionRenderer()
        self.validator = QuestionnaireValidator()

    def render_questionnaire_header(self, evaluation_metadata: Dict[str, Any] = None):
        """Rendre l'en-tête du questionnaire"""

        st.markdown("# 📋 Questionnaire d'Évaluation Éco-Responsable")

        if evaluation_metadata:
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Exposition", evaluation_metadata.get('name', 'Non définie'))
            with col2:
                st.metric("Lieu", evaluation_metadata.get('venue', 'Non défini'))
            with col3:
                duration = evaluation_metadata.get('duration_days', 0)
                st.metric("Durée", f"{duration} jours" if duration else 'Non définie')

        # Afficher les instructions
        with st.expander("ℹ️ Instructions pour remplir le questionnaire", expanded=False):
            st.markdown("""
            ### Comment utiliser ce questionnaire :

            1. **Navigation** : Utilisez la barre latérale pour naviguer entre les sections
            2. **Champs obligatoires** : Marqués par un astérisque (*)
            3. **Sauvegarde automatique** : Vos réponses sont sauvegardées automatiquement
            4. **Aide contextuelle** : Survolez les (?) pour plus d'informations
            5. **Progression** : La barre de progression indique votre avancement

            ### Temps estimé : 45-60 minutes

            **Vous pouvez interrompre et reprendre à tout moment.**
            """)

    def render_questionnaire_footer(self):
        """Rendre le pied de page du questionnaire"""

        st.divider()

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("💾 Sauvegarder et continuer plus tard", use_container_width=True):
                st.success("✅ Progression sauvegardée")
                st.info("Vous pouvez reprendre votre évaluation à tout moment depuis le dashboard")

        with col2:
            if st.button("📊 Voir l'aperçu des résultats", use_container_width=True):
                st.info("🚧 Fonctionnalité en développement")

        with col3:
            if st.button("✅ Finaliser l'évaluation", use_container_width=True, type="primary"):
                st.success("🎉 Évaluation finalisée !")
                st.balloons()

    def render_category_selector(self) -> str:
        """Rendre le sélecteur de catégorie principal"""

        categories = list(EVALUATION_CRITERIA.keys())
        category_names = [
            EVALUATION_CRITERIA[cat_id].get('title', cat_id)
            for cat_id in categories
        ]

        selected_name = st.selectbox(
            "Choisissez une section à remplir :",
            category_names,
            help="Sélectionnez la section du questionnaire que vous souhaitez compléter"
        )

        # Retrouver l'ID de la catégorie
        selected_id = categories[category_names.index(selected_name)]
        return selected_id

    def show_validation_errors(self, errors: Dict[str, List[str]]):
        """Afficher les erreurs de validation"""

        if not errors:
            return

        st.error("❌ Veuillez corriger les erreurs suivantes :")

        for question_id, error_list in errors.items():
            for error in error_list:
                st.error(f"**{question_id}** : {error}")

    def show_completion_summary(self, completion_stats: Dict[str, float]):
        """Afficher un résumé de completion"""

        st.markdown("### 📊 Résumé de completion")

        for category_id, completion in completion_stats.items():
            category_config = get_questions_by_category(category_id)
            category_name = category_config.get('title', category_id) if category_config else category_id

            col1, col2 = st.columns([3, 1])

            with col1:
                st.write(category_name)
            with col2:
                st.progress(completion / 100.0)
                st.caption(f"{completion:.0f}%")

# Fonctions utilitaires

def get_category_list() -> List[str]:
    """Obtenir la liste des catégories disponibles"""
    return list(EVALUATION_CRITERIA.keys())

def get_category_title(category_id: str) -> str:
    """Obtenir le titre d'affichage d'une catégorie"""
    category_config = get_questions_by_category(category_id)
    if category_config:
        return category_config.get('title', category_id.replace('_', ' ').title())
    return category_id.replace('_', ' ').title()

def create_questionnaire_session() -> Dict[str, Any]:
    """Créer une nouvelle session de questionnaire"""
    return {
        'current_category': get_category_list()[0],
        'responses': {},
        'start_time': datetime.now(),
        'last_update': datetime.now()
    }
