"""
Dashboard Éco-Évaluation des Expositions Culturelles
Point d'entrée principal de l'application Streamlit - Version corrigée NumPy
Repo: https://github.com/MarcRenard/deja-vu
"""

import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime
import os
import sys
import warnings

# Supprimer les warnings de compatibilité
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=UserWarning)

# Ajouter le dossier src au path pour les imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Configuration de la page Streamlit
st.set_page_config(
    page_title="Éco-Évaluation Expositions - Déjà Vu",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
<style>
.main-header {
    font-size: 2.5rem;
    color: #2E7D32;
    text-align: center;
    margin-bottom: 2rem;
}
.metric-card {
    background-color: #f0f8ff;
    padding: 1rem;
    border-radius: 10px;
    border-left: 4px solid #2E7D32;
}
.section-header {
    color: #1976D2;
    border-bottom: 2px solid #1976D2;
    padding-bottom: 0.5rem;
}
.questionnaire-card {
    background: linear-gradient(135deg, #E8F5E8 0%, #C8E6C9 100%);
    padding: 2rem;
    border-radius: 15px;
    border: 1px solid #4CAF50;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

def create_dummy_dashboard():
    """Créer un dashboard dummy pour tester l'interface"""

    st.markdown('<h1 class="main-header">🌱 Dashboard Éco-Évaluation</h1>', unsafe_allow_html=True)

    # Informations sur le développement
    col1, col2 = st.columns([3, 1])

    with col1:
        st.info("✅ **Phase 2 implémentée** : Questionnaire complet avec validation des données")

    with col2:
        if st.button("🆕 Nouvelle évaluation", type="primary", use_container_width=True):
            st.session_state.current_page = "questionnaire"
            st.rerun()

    st.divider()

    # Métriques principales (dummy data)
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Empreinte Carbone",
            value="2.4 t CO₂eq",
            delta="-0.3 vs moyenne"
        )

    with col2:
        st.metric(
            label="Score Éco-Social",
            value="7.8/10",
            delta="1.2"
        )

    with col3:
        st.metric(
            label="Matériaux Recyclés",
            value="65%",
            delta="15%"
        )

    with col4:
        st.metric(
            label="Énergie Renouvelable",
            value="80%",
            delta="10%"
        )

    st.divider()

    # Graphiques dummy
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<h3 class="section-header">Impact par Catégorie</h3>', unsafe_allow_html=True)

        # Données dummy pour graphique radar
        categories = ['Matériaux', 'Énergie', 'Transport', 'Déchets', 'Éco-Social']
        scores = [7.2, 8.1, 6.5, 7.8, 8.3]

        # Créer un graphique en barres horizontal
        df_categories = pd.DataFrame({
            'Catégorie': categories,
            'Score': scores
        })

        fig_bar = px.bar(
            df_categories,
            x='Score',
            y='Catégorie',
            orientation='h',
            color='Score',
            color_continuous_scale='RdYlGn',
            title="Scores par Catégorie d'Impact"
        )
        fig_bar.update_layout(height=400)
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        st.markdown('<h3 class="section-header">Évolution Temporelle</h3>', unsafe_allow_html=True)

        # Données dummy pour série temporelle - CORRECTION du warning
        dates = pd.date_range(start='2023-01-01', end='2024-01-01', freq='ME')  # 'ME' au lieu de 'M'
        co2_data = 2.4 + np.random.normal(0, 0.2, len(dates)).cumsum() * 0.1

        df_temporal = pd.DataFrame({
            'Date': dates,
            'Empreinte CO₂ (t)': co2_data
        })

        fig_line = px.line(
            df_temporal,
            x='Date',
            y='Empreinte CO₂ (t)',
            title="Évolution de l'Empreinte Carbone",
            markers=True
        )
        fig_line.update_traces(line_color='#2E7D32')
        fig_line.update_layout(height=400)
        st.plotly_chart(fig_line, use_container_width=True)

    # Section des évaluations
    st.markdown('<h3 class="section-header">Évaluations Récentes</h3>', unsafe_allow_html=True)

    # Vérifier s'il y a une évaluation en cours
    if 'current_evaluation' in st.session_state and st.session_state.current_evaluation:
        evaluation = st.session_state.current_evaluation

        st.markdown('<div class="questionnaire-card">', unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Évaluation en cours", evaluation.metadata.name)
        with col2:
            st.metric("Progression", f"{evaluation.completion_percentage:.0f}%")
        with col3:
            st.metric("Statut", evaluation.status.title())
        with col4:
            if st.button("📝 Continuer", type="primary", use_container_width=True):
                st.session_state.current_page = "questionnaire"
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    # Tableau dummy des évaluations - Version simplifiée pour éviter pyarrow
    st.markdown("### 📊 Historique des évaluations")

    # Affichage simple sans st.dataframe pour éviter pyarrow
    evaluation_data = [
        {"Date": "2024-01-15", "Exposition": "Art Contemporain 2024", "Score": 7.8, "CO₂": "2.4t", "Statut": "✅ Complété"},
        {"Date": "2024-01-10", "Exposition": "Histoire Locale", "Score": 6.9, "CO₂": "3.1t", "Statut": "🔄 En cours"},
        {"Date": "2024-01-05", "Exposition": "Sciences & Nature", "Score": 8.2, "CO₂": "1.8t", "Statut": "✅ Complété"}
    ]

    for eval_data in evaluation_data:
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.write(eval_data["Date"])
        with col2:
            st.write(eval_data["Exposition"])
        with col3:
            st.write(f"⭐ {eval_data['Score']}/10")
        with col4:
            st.write(f"🌍 {eval_data['CO₂']}")
        with col5:
            st.write(eval_data["Statut"])

def show_questionnaire_page():
    """Afficher la page du questionnaire"""
    try:
        from questionnaire.questionnaire_main import run_questionnaire_page
        run_questionnaire_page()
    except ImportError as e:
        st.error("❌ Erreur d'importation du module questionnaire")
        st.error(f"Détail : {str(e)}")

        # Fallback vers l'ancien placeholder
        st.markdown('<h1 class="main-header">📋 Questionnaire d\'Évaluation</h1>', unsafe_allow_html=True)

        st.warning("🚧 **Module questionnaire en cours de finalisation**")

        st.markdown("""
        ### ✅ Fonctionnalités implémentées :

        **1. Modèles de données complets**
        - Validation Pydantic des réponses
        - 93 critères d'évaluation structurés
        - Types de questions multiples (numérique, échelle, choix multiples...)

        **2. Générateur de formulaires dynamiques**
        - Rendu automatique selon le type de question
        - Validation en temps réel
        - Interface responsive

        **3. Interface utilisateur complète**
        - Navigation par sections
        - Sauvegarde automatique
        - Indicateurs de progression
        - Gestion des erreurs
        """)

        if st.button("🏠 Retour au Dashboard", type="primary"):
            st.session_state.current_page = "dashboard"
            st.rerun()

def show_about_page():
    """Afficher la page À propos"""
    st.markdown('<h1 class="main-header">ℹ️ À propos</h1>', unsafe_allow_html=True)

    st.markdown("""
    ## Dashboard d'Éco-Évaluation des Expositions Culturelles

    Cette application permet d'évaluer l'impact environnemental et éco-social
    des expositions culturelles et des musées selon les standards internationaux.

    ### ✅ Phase 2 - Questionnaire (Actuelle) :
    - 📋 **93 critères d'évaluation** organisés en 5 catégories
    - 🔧 **Modèles de données robustes** avec validation Pydantic
    - 📝 **Interface de questionnaire** dynamique et intuitive
    - 💾 **Sauvegarde automatique** des réponses en cours
    - ✅ **Validation en temps réel** des saisies

    ### Fonctionnalités :
    - 📊 **Dashboard interactif** avec visualisations avancées
    - 💾 **Sauvegarde** et historique des évaluations
    - 📈 **Comparaisons** et benchmarks sectoriels
    - 📑 **Export** PDF et Excel des résultats (à venir)

    ### Normes de référence :
    - **ISO 14001** : Management environnemental
    - **ISO 26000** : Responsabilité sociétale
    - **ADEME** : Bilan carbone et méthodes de calcul
    - **Loi française 2005** : Accessibilité universelle

    ### Développé avec :
    - 🐍 Python & Streamlit
    - 📊 Plotly & Pandas
    - 🔬 Pydantic pour la validation des données
    - 🎨 Interface Material Design
    """)

    # Statistiques du projet
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Questions", "93", help="Nombre total de critères d'évaluation")
    with col2:
        st.metric("Catégories", "5", help="Catégories principales d'impact")
    with col3:
        st.metric("Types de questions", "6", help="Types de widgets de saisie")

    st.info("🚧 **Version de développement** - Phase 3 (Calculs et métriques) en préparation.")

def main():
    """Fonction principale de l'application"""

    # Initialiser l'état de la page
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "dashboard"

    # Sidebar pour navigation
    with st.sidebar:
        st.markdown("### Navigation")

        # Navigation avec boutons radio
        selected_page = st.radio(
            "Choisir une section:",
            ["dashboard", "questionnaire", "about"],
            format_func=lambda x: {
                "dashboard": "🏠 Dashboard",
                "questionnaire": "📋 Questionnaire",
                "about": "ℹ️ À propos"
            }[x],
            index=["dashboard", "questionnaire", "about"].index(st.session_state.current_page)
        )

        # Mettre à jour la page si changement
        if selected_page != st.session_state.current_page:
            st.session_state.current_page = selected_page
            st.rerun()

        st.divider()

        # Actions rapides
        st.markdown("### Actions rapides")

        if st.button("➕ Nouvelle évaluation", use_container_width=True):
            st.session_state.current_page = "questionnaire"
            # Réinitialiser l'évaluation pour en créer une nouvelle
            if 'current_evaluation' in st.session_state:
                st.session_state.current_evaluation = None
            st.rerun()

        if st.button("📊 Dashboard", use_container_width=True):
            st.session_state.current_page = "dashboard"
            st.rerun()

        st.divider()

        # Informations système
        st.markdown("### Informations")
        st.caption(f"📅 {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        st.caption("🔧 Version 1.1.0 (Phase 2)")

        # Statut du questionnaire
        if 'current_evaluation' in st.session_state and st.session_state.current_evaluation:
            st.success("📝 Évaluation en cours")
            completion = st.session_state.current_evaluation.completion_percentage
            st.progress(completion / 100.0)
            st.caption(f"Progression : {completion:.0f}%")
        else:
            st.info("✨ Prêt pour nouvelle évaluation")

    # Contenu principal selon la page sélectionnée
    if st.session_state.current_page == "dashboard":
        create_dummy_dashboard()

    elif st.session_state.current_page == "questionnaire":
        show_questionnaire_page()

    elif st.session_state.current_page == "about":
        show_about_page()

# Point d'entrée de l'application
if __name__ == "__main__":
    main()
