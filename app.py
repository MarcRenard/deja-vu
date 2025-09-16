"""
Dashboard Éco-Évaluation des Expositions Culturelles
Point d'entrée principal de l'application Streamlit
Repo: https://github.com/MarcRenard/deja-vu
"""

import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime
import os
import sys

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
.section-header {
    color: #1976D2;
    border-bottom: 2px solid #1976D2;
    padding-bottom: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

def main():
    """Fonction principale de l'application"""

    # Header principal
    st.markdown('<h1 class="main-header">🌱 Dashboard Éco-Évaluation - Déjà Vu</h1>', unsafe_allow_html=True)

    # Message de statut
    st.info("🚧 **Phase 1 - Foundation** : Structure de base créée avec succès !")

    # Métriques dummy
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Empreinte Carbone", "2.4 t CO₂eq", "-0.3")
    with col2:
        st.metric("Score Éco-Social", "7.8/10", "1.2")
    with col3:
        st.metric("Matériaux Recyclés", "65%", "15%")
    with col4:
        st.metric("Énergie Renouvelable", "80%", "10%")

    st.divider()

    # Graphique dummy
    st.markdown('<h3 class="section-header">Impact par Catégorie (Dummy Data)</h3>', unsafe_allow_html=True)

    categories = ['Matériaux', 'Énergie', 'Transport', 'Déchets', 'Éco-Social']
    scores = [7.2, 8.1, 6.5, 7.8, 8.3]

    df = pd.DataFrame({'Catégorie': categories, 'Score': scores})

    fig = px.bar(df, x='Score', y='Catégorie', orientation='h',
                 color='Score', color_continuous_scale='RdYlGn',
                 title="Scores par Catégorie d'Impact")
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

    # Section suivante
    st.markdown('<h3 class="section-header">Prochaines Étapes</h3>', unsafe_allow_html=True)

    st.markdown("""
    ### 🔄 Phases de développement :

    - ✅ **Phase 1** : Foundation & Structure (Actuelle)
    - 🔄 **Phase 2** : Modèles de données avec Pydantic
    - 🔄 **Phase 3** : Questionnaire interactif complet
    - 🔄 **Phase 4** : Calculs selon normes officielles
    - 🔄 **Phase 5** : Dashboard avancé avec exports

    ### 📊 Statistiques du projet :
    - **93 critères** d'évaluation définis
    - **5 catégories** principales d'impact
    - **4 normes** internationales respectées
    """)

    # Footer
    st.divider()
    col1, col2, col3 = st.columns(3)

    with col1:
        st.caption("🔗 [Repo GitHub](https://github.com/MarcRenard/deja-vu)")
    with col2:
        st.caption("🔧 Version 1.0.0")
    with col3:
        st.caption(f"📅 {datetime.now().strftime('%d/%m/%Y %H:%M')}")

if __name__ == "__main__":
    main()
