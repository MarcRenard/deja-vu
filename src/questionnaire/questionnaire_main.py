"""
Interface principale du questionnaire d'évaluation
Point d'entrée pour la saisie des données
"""

import streamlit as st
from typing import Dict, Any, Optional, List
from datetime import datetime, date
import sys
import os

# Ajout du chemin pour les imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from config.criteria import EVALUATION_CRITERIA, get_questions_by_category
from data.models import (
    Evaluation, ExhibitionMetadata, ExhibitionType,
    EvaluationStatus, CategoryResponse, SubCategoryResponse, QuestionResponse
)
from questionnaire.forms import QuestionnaireUI, SectionRenderer, QuestionnaireValidator

class QuestionnaireManager:
    """Gestionnaire principal du questionnaire"""

    def __init__(self):
        self.ui = QuestionnaireUI()
        self.section_renderer = SectionRenderer()
        self.validator = QuestionnaireValidator()

        # Initialiser la session si nécessaire
        if 'questionnaire_session' not in st.session_state:
            st.session_state.questionnaire_session = {}
        if 'current_evaluation' not in st.session_state:
            st.session_state.current_evaluation = None

    def run_questionnaire(self):
        """Point d'entrée principal pour le questionnaire"""

        # Vérifier s'il faut créer une nouvelle évaluation ou continuer une existante
        if st.session_state.current_evaluation is None:
            self._show_evaluation_setup()
        else:
            self._show_main_questionnaire()

    def _show_evaluation_setup(self):
        """Afficher l'interface de configuration d'une nouvelle évaluation"""

        st.markdown("# 🆕 Nouvelle Évaluation")
        st.markdown("Commencez par renseigner les informations générales de votre exposition.")

        with st.form("evaluation_setup"):
            st.markdown("## Informations générales")

            col1, col2 = st.columns(2)

            with col1:
                name = st.text_input(
                    "Nom de l'exposition *",
                    placeholder="Ex: Art Contemporain 2024"
                )
                venue = st.text_input(
                    "Lieu *",
                    placeholder="Ex: Musée d'Art Moderne"
                )
                city = st.text_input(
                    "Ville",
                    placeholder="Ex: Paris"
                )

            with col2:
                exhibition_type = st.selectbox(
                    "Type d'exposition *",
                    options=list(ExhibitionType),
                    format_func=lambda x: self._format_exhibition_type(x)
                )
                start_date = st.date_input("Date de début *")
                end_date = st.date_input("Date de fin (optionnel)")

            st.markdown("## Informations détaillées (optionnel)")

            col1, col2, col3 = st.columns(3)

            with col1:
                surface_area = st.number_input(
                    "Surface (m²)",
                    min_value=0.0,
                    value=0.0,
                    step=10.0
                )

            with col2:
                estimated_visitors = st.number_input(
                    "Visiteurs estimés",
                    min_value=0,
                    value=0,
                    step=100
                )

            with col3:
                budget = st.number_input(
                    "Budget (€)",
                    min_value=0.0,
                    value=0.0,
                    step=1000.0
                )

            description = st.text_area(
                "Description de l'exposition",
                placeholder="Décrivez brièvement l'exposition, ses thèmes, objectifs...",
                max_chars=1000
            )

            # Informations de contact
            st.markdown("## Contact")

            col1, col2, col3 = st.columns(3)

            with col1:
                evaluator_name = st.text_input("Votre nom")
            with col2:
                evaluator_email = st.text_input("Votre email")
            with col3:
                evaluator_organization = st.text_input("Organisation")

            submitted = st.form_submit_button("🚀 Commencer l'évaluation", use_container_width=True, type="primary")

            if submitted:
                # Validation des champs obligatoires
                errors = []

                if not name.strip():
                    errors.append("Le nom de l'exposition est obligatoire")
                if not venue.strip():
                    errors.append("Le lieu est obligatoire")
                if end_date and end_date < start_date:
                    errors.append("La date de fin doit être postérieure à la date de début")

                if errors:
                    for error in errors:
                        st.error(error)
                else:
                    # Créer l'évaluation
                    self._create_new_evaluation(
                        name=name,
                        venue=venue,
                        city=city,
                        exhibition_type=exhibition_type,
                        start_date=start_date,
                        end_date=end_date,
                        surface_area=surface_area if surface_area > 0 else None,
                        estimated_visitors=estimated_visitors if estimated_visitors > 0 else None,
                        budget=budget if budget > 0 else None,
                        description=description if description.strip() else None,
                        evaluator_name=evaluator_name if evaluator_name.strip() else None,
                        evaluator_email=evaluator_email if evaluator_email.strip() else None,
                        evaluator_organization=evaluator_organization if evaluator_organization.strip() else None
                    )

    def _create_new_evaluation(self, **kwargs):
        """Créer une nouvelle évaluation avec les métadonnées"""

        try:
            metadata = ExhibitionMetadata(**kwargs)
            evaluation = Evaluation(metadata=metadata)

            st.session_state.current_evaluation = evaluation
            st.session_state.questionnaire_session = {
                'current_category': list(EVALUATION_CRITERIA.keys())[0],
                'start_time': datetime.now()
            }

            st.success("✅ Évaluation créée avec succès !")
            st.rerun()

        except Exception as e:
            st.error(f"Erreur lors de la création de l'évaluation : {str(e)}")

    def _show_main_questionnaire(self):
        """Afficher l'interface principale du questionnaire"""

        evaluation = st.session_state.current_evaluation

        # Header avec informations de l'évaluation
        self.ui.render_questionnaire_header(evaluation.metadata.dict())

        # Navigation par catégorie
        categories = list(EVALUATION_CRITERIA.keys())

        # Sélecteur de catégorie dans le contenu principal
        current_category = st.session_state.questionnaire_session.get('current_category', categories[0])

        # Navigation dans la sidebar
        with st.sidebar:
            st.markdown("### Navigation")

            # Sélecteur de catégorie
            selected_category = st.radio(
                "Sections :",
                categories,
                index=categories.index(current_category),
                format_func=lambda x: self._get_category_display_name(x)
            )

            # Mettre à jour la catégorie courante
            if selected_category != current_category:
                st.session_state.questionnaire_session['current_category'] = selected_category
                st.rerun()

            st.divider()

            # Indicateurs de progression
            self._show_progress_indicators(evaluation)

            st.divider()

            # Actions rapides
            st.markdown("### Actions")

            if st.button("💾 Sauvegarder", use_container_width=True):
                self._save_evaluation()

            if st.button("🏠 Retour au dashboard", use_container_width=True):
                self._return_to_dashboard()

            if st.button("🗑️ Nouvelle évaluation", use_container_width=True):
                self._reset_evaluation()

        # Contenu principal : formulaire de la catégorie courante
        current_category = st.session_state.questionnaire_session['current_category']
        self._render_category_form(current_category)

        # Navigation entre catégories
        self._render_category_navigation(categories, current_category)

        # Footer du questionnaire
        self.ui.render_questionnaire_footer()

    def _render_category_form(self, category_id: str):
        """Rendre le formulaire d'une catégorie"""

        # Récupérer les réponses actuelles pour cette catégorie
        evaluation = st.session_state.current_evaluation
        current_responses = {}

        if category_id in evaluation.responses:
            category_response = evaluation.responses[category_id]
            # Convertir en format pour le renderer
            for subcategory_id, subcategory in category_response.subcategories.items():
                current_responses[subcategory_id] = {
                    q_id: q.value for q_id, q in subcategory.questions.items()
                }

        # Rendre le formulaire
        with st.form(key=f"form_{category_id}", clear_on_submit=False):
            responses = self.section_renderer.render_category_section(
                category_id,
                current_responses
            )

            col1, col2, col3 = st.columns([1, 1, 2])

            with col1:
                submitted = st.form_submit_button("💾 Sauvegarder cette section", type="primary")

            with col2:
                draft_saved = st.form_submit_button("📝 Sauvegarder brouillon")

            with col3:
                if st.form_submit_button("➡️ Section suivante"):
                    self._go_to_next_category(category_id)

            if submitted or draft_saved:
                self._save_category_responses(category_id, responses)
                if submitted:
                    st.success("✅ Réponses sauvegardées avec succès !")
                else:
                    st.info("📝 Brouillon sauvegardé")

    def _save_category_responses(self, category_id: str, responses: Dict[str, Dict[str, Any]]):
        """Sauvegarder les réponses d'une catégorie"""

        evaluation = st.session_state.current_evaluation

        # Créer la CategoryResponse
        category_response = CategoryResponse(category_id=category_id)

        # Traiter chaque sous-catégorie
        for subcategory_id, subcategory_responses in responses.items():
            subcategory_response = SubCategoryResponse(subcategory_id=subcategory_id)

            # Traiter chaque question
            for question_id, response_value in subcategory_responses.items():
                if response_value is not None:  # Ignorer les réponses vides
                    question_response = QuestionResponse(
                        question_id=question_id,
                        value=response_value,
                        updated_at=datetime.now()
                    )
                    subcategory_response.add_response(question_id, question_response)

            category_response.add_subcategory_response(subcategory_id, subcategory_response)

        # Ajouter à l'évaluation
        evaluation.add_category_response(category_id, category_response)

        # Mettre à jour la session
        st.session_state.current_evaluation = evaluation

    def _show_progress_indicators(self, evaluation: Evaluation):
        """Afficher les indicateurs de progression"""

        st.markdown("### Progression")

        # Progression globale
        overall_progress = evaluation.completion_percentage
        st.progress(overall_progress / 100.0)
        st.caption(f"Global : {overall_progress:.0f}%")

        st.markdown("### Détail par section")

        # Progression par catégorie
        for category_id in EVALUATION_CRITERIA.keys():
            category_name = self._get_category_display_name(category_id)
            completion = evaluation.get_category_completion(category_id)

            col1, col2 = st.columns([3, 1])

            with col1:
                st.caption(category_name)
            with col2:
                if completion >= 90:
                    st.success(f"✅ {completion:.0f}%")
                elif completion >= 50:
                    st.warning(f"🟡 {completion:.0f}%")
                elif completion > 0:
                    st.info(f"🔵 {completion:.0f}%")
                else:
                    st.error(f"❌ {completion:.0f}%")

    def _render_category_navigation(self, categories: List[str], current_category: str):
        """Rendre la navigation entre catégories"""

        st.divider()

        col1, col2, col3 = st.columns([1, 2, 1])

        # Bouton précédent
        with col1:
            current_index = categories.index(current_category)
            if current_index > 0:
                if st.button("⬅️ Section précédente", use_container_width=True):
                    st.session_state.questionnaire_session['current_category'] = categories[current_index - 1]
                    st.rerun()

        # Indicateur de position
        with col2:
            st.markdown(f"**Section {current_index + 1} sur {len(categories)}**")
            progress = (current_index + 1) / len(categories)
            st.progress(progress)

        # Bouton suivant
        with col3:
            if current_index < len(categories) - 1:
                if st.button("Section suivante ➡️", use_container_width=True):
                    st.session_state.questionnaire_session['current_category'] = categories[current_index + 1]
                    st.rerun()
            else:
                if st.button("✅ Finaliser", use_container_width=True, type="primary"):
                    self._finalize_evaluation()

    def _go_to_next_category(self, current_category: str):
        """Aller à la catégorie suivante"""
        categories = list(EVALUATION_CRITERIA.keys())
        current_index = categories.index(current_category)

        if current_index < len(categories) - 1:
            st.session_state.questionnaire_session['current_category'] = categories[current_index + 1]
            st.rerun()

    def _save_evaluation(self):
        """Sauvegarder l'évaluation actuelle"""
        # TODO: Implémenter la sauvegarde persistante
        st.success("💾 Évaluation sauvegardée")
        st.info("La sauvegarde persistante sera implémentée dans la prochaine phase")

    def _return_to_dashboard(self):
        """Retourner au dashboard"""
        # Sauvegarder automatiquement avant de quitter
        self._save_evaluation()

        # Reset des états pour retourner au dashboard
        st.session_state.questionnaire_active = False
        st.rerun()

    def _reset_evaluation(self):
        """Réinitialiser pour créer une nouvelle évaluation"""
        if st.checkbox("Je confirme vouloir abandonner l'évaluation actuelle"):
            st.session_state.current_evaluation = None
            st.session_state.questionnaire_session = {}
            st.rerun()

    def _finalize_evaluation(self):
        """Finaliser l'évaluation"""
        evaluation = st.session_state.current_evaluation
        evaluation.status = EvaluationStatus.COMPLETED
        evaluation.completed_at = datetime.now()

        st.success("🎉 Évaluation finalisée avec succès !")
        st.balloons()

        st.info("Vous pouvez maintenant consulter vos résultats dans le dashboard.")

        # Proposer d'aller au dashboard
        if st.button("📊 Voir les résultats", type="primary"):
            self._return_to_dashboard()

    def _get_category_display_name(self, category_id: str) -> str:
        """Obtenir le nom d'affichage d'une catégorie"""
        category_config = get_questions_by_category(category_id)
        if category_config:
            title = category_config.get('title', category_id)
            # Raccourcir si trop long
            if len(title) > 30:
                return title[:27] + "..."
            return title
        return category_id.replace('_', ' ').title()

    def _format_exhibition_type(self, exhibition_type: ExhibitionType) -> str:
        """Formater le type d'exposition pour l'affichage"""
        type_labels = {
            ExhibitionType.SMALL_MUSEUM: "Petit musée",
            ExhibitionType.LARGE_MUSEUM: "Grand musée",
            ExhibitionType.TEMPORARY_EXHIBITION: "Exposition temporaire",
            ExhibitionType.OUTDOOR_EXHIBITION: "Exposition extérieure",
            ExhibitionType.TRAVELING_EXHIBITION: "Exposition itinérante",
            ExhibitionType.VIRTUAL_EXHIBITION: "Exposition virtuelle"
        }
        return type_labels.get(exhibition_type, exhibition_type.value)

# Fonction principale pour intégrer dans l'app
def run_questionnaire_page():
    """Point d'entrée pour la page questionnaire"""

    # Vérifier si le questionnaire est activé
    if 'questionnaire_active' not in st.session_state:
        st.session_state.questionnaire_active = False

    # Créer et lancer le gestionnaire
    manager = QuestionnaireManager()
    manager.run_questionnaire()
