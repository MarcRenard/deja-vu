"""
Modèles de données pour l'évaluation environnementale et éco-sociale
Utilisation de Pydantic pour la validation des données
"""

from pydantic import BaseModel, Field, validator
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, date
from enum import Enum
import uuid

class ExhibitionType(str, Enum):
    """Types d'expositions"""
    SMALL_MUSEUM = "small_museum"
    LARGE_MUSEUM = "large_museum"
    TEMPORARY_EXHIBITION = "temporary_exhibition"
    OUTDOOR_EXHIBITION = "outdoor_exhibition"
    TRAVELING_EXHIBITION = "traveling_exhibition"
    VIRTUAL_EXHIBITION = "virtual_exhibition"

class EvaluationStatus(str, Enum):
    """Statut d'une évaluation"""
    DRAFT = "draft"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    VALIDATED = "validated"
    ARCHIVED = "archived"

class QuestionResponse(BaseModel):
    """Réponse à une question individuelle"""
    question_id: str
    value: Union[str, int, float, bool, List[str]]
    unit: Optional[str] = None
    confidence_level: Optional[int] = Field(None, ge=1, le=5)  # Niveau de confiance 1-5
    comments: Optional[str] = None
    source: Optional[str] = None  # Source de l'information
    updated_at: datetime = Field(default_factory=datetime.now)

    @validator('confidence_level')
    def validate_confidence(cls, v):
        if v is not None and not 1 <= v <= 5:
            raise ValueError('Le niveau de confiance doit être entre 1 et 5')
        return v

    @validator('comments')
    def validate_comments(cls, v):
        if v is not None and len(v) > 1000:
            raise ValueError('Les commentaires ne peuvent pas dépasser 1000 caractères')
        return v

class SubCategoryResponse(BaseModel):
    """Réponses d'une sous-catégorie"""
    subcategory_id: str
    questions: Dict[str, QuestionResponse] = Field(default_factory=dict)
    completion_percentage: float = Field(default=0.0, ge=0.0, le=100.0)

    def add_response(self, question_id: str, response: QuestionResponse):
        """Ajouter une réponse à la sous-catégorie"""
        self.questions[question_id] = response
        self._calculate_completion()

    def _calculate_completion(self):
        """Calculer le pourcentage de completion"""
        # Cette méthode sera implémentée avec la logique métier
        pass

class CategoryResponse(BaseModel):
    """Réponses d'une catégorie principale"""
    category_id: str
    subcategories: Dict[str, SubCategoryResponse] = Field(default_factory=dict)
    completion_percentage: float = Field(default=0.0, ge=0.0, le=100.0)
    score: Optional[float] = Field(None, ge=0.0, le=10.0)

    def add_subcategory_response(self, subcategory_id: str, response: SubCategoryResponse):
        """Ajouter les réponses d'une sous-catégorie"""
        self.subcategories[subcategory_id] = response
        self._calculate_completion()

    def _calculate_completion(self):
        """Calculer le pourcentage de completion de la catégorie"""
        if not self.subcategories:
            self.completion_percentage = 0.0
            return

        total_completion = sum(
            sub.completion_percentage for sub in self.subcategories.values()
        )
        self.completion_percentage = total_completion / len(self.subcategories)

class ExhibitionMetadata(BaseModel):
    """Métadonnées de l'exposition évaluée"""
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    venue: str = Field(..., min_length=1, max_length=200)
    city: Optional[str] = Field(None, max_length=100)
    country: str = Field(default="France", max_length=100)

    start_date: date
    end_date: Optional[date] = None
    duration_days: Optional[int] = Field(None, gt=0)

    exhibition_type: ExhibitionType
    surface_area: Optional[float] = Field(None, gt=0)  # m²
    estimated_visitors: Optional[int] = Field(None, gt=0)
    budget: Optional[float] = Field(None, gt=0)  # €

    organizer: Optional[str] = Field(None, max_length=200)
    contact_email: Optional[str] = Field(None, pattern=r'^[^@]+@[^@]+\.[^@]+$')

    @validator('end_date')
    def validate_end_date(cls, v, values):
        if v is not None and 'start_date' in values and v < values['start_date']:
            raise ValueError('La date de fin doit être postérieure à la date de début')
        return v

    @validator('duration_days')
    def calculate_duration(cls, v, values):
        if v is None and 'start_date' in values and 'end_date' in values:
            if values['end_date'] is not None:
                delta = values['end_date'] - values['start_date']
                return delta.days
        return v

class CalculatedScores(BaseModel):
    """Scores calculés de l'évaluation"""
    # Scores par catégorie (0-10)
    environmental_direct_score: Optional[float] = Field(None, ge=0.0, le=10.0)
    environmental_indirect_score: Optional[float] = Field(None, ge=0.0, le=10.0)
    eco_social_score: Optional[float] = Field(None, ge=0.0, le=10.0)
    temporal_contextual_score: Optional[float] = Field(None, ge=0.0, le=10.0)
    transversal_score: Optional[float] = Field(None, ge=0.0, le=10.0)

    # Score global pondéré
    global_score: Optional[float] = Field(None, ge=0.0, le=10.0)

    # Métriques spécifiques
    carbon_footprint_total: Optional[float] = Field(None, ge=0.0)  # kg CO2eq
    carbon_footprint_per_visitor: Optional[float] = Field(None, ge=0.0)  # kg CO2eq/visiteur
    carbon_footprint_per_m2: Optional[float] = Field(None, ge=0.0)  # kg CO2eq/m²

    energy_consumption_total: Optional[float] = Field(None, ge=0.0)  # kWh
    energy_consumption_per_visitor: Optional[float] = Field(None, ge=0.0)  # kWh/visiteur
    energy_consumption_per_m2: Optional[float] = Field(None, ge=0.0)  # kWh/m²

    water_consumption_total: Optional[float] = Field(None, ge=0.0)  # litres
    water_consumption_per_m2: Optional[float] = Field(None, ge=0.0)  # litres/m²

    waste_total: Optional[float] = Field(None, ge=0.0)  # kg
    waste_per_visitor: Optional[float] = Field(None, ge=0.0)  # kg/visiteur
    recycling_rate: Optional[float] = Field(None, ge=0.0, le=100.0)  # %

    renewable_energy_percentage: Optional[float] = Field(None, ge=0.0, le=100.0)  # %
    local_sourcing_percentage: Optional[float] = Field(None, ge=0.0, le=100.0)  # %
    recycled_materials_percentage: Optional[float] = Field(None, ge=0.0, le=100.0)  # %

    # Performance par rapport aux benchmarks
    carbon_performance_vs_benchmark: Optional[str] = None  # excellent, good, average, poor
    energy_performance_vs_benchmark: Optional[str] = None
    waste_performance_vs_benchmark: Optional[str] = None

    # Timestamp du calcul
    calculated_at: datetime = Field(default_factory=datetime.now)

class Evaluation(BaseModel):
    """Modèle principal d'une évaluation complète"""
    # Identifiants
    evaluation_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    version: str = Field(default="1.0.0")

    # Métadonnées
    metadata: ExhibitionMetadata

    # Réponses par catégorie
    responses: Dict[str, CategoryResponse] = Field(default_factory=dict)

    # Scores calculés
    calculated_scores: Optional[CalculatedScores] = None

    # Statut et suivi
    status: EvaluationStatus = Field(default=EvaluationStatus.DRAFT)
    completion_percentage: float = Field(default=0.0, ge=0.0, le=100.0)

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None

    # Informations de l'évaluateur
    evaluator_name: Optional[str] = Field(None, max_length=100)
    evaluator_email: Optional[str] = Field(None, pattern=r'^[^@]+@[^@]+\.[^@]+$')
    evaluator_organization: Optional[str] = Field(None, max_length=200)

    # Notes et commentaires
    general_comments: Optional[str] = Field(None, max_length=2000)
    recommendations: List[str] = Field(default_factory=list)

    # Pièces jointes et documents
    attachments: List[str] = Field(default_factory=list)  # URLs ou chemins vers fichiers

    class Config:
        use_enum_values = True
        validate_assignment = True

    def add_category_response(self, category_id: str, response: CategoryResponse):
        """Ajouter les réponses d'une catégorie"""
        self.responses[category_id] = response
        self.updated_at = datetime.now()
        self._calculate_completion()

    def _calculate_completion(self):
        """Calculer le pourcentage de completion global"""
        if not self.responses:
            self.completion_percentage = 0.0
            return

        total_completion = sum(
            cat.completion_percentage for cat in self.responses.values()
        )
        self.completion_percentage = total_completion / len(self.responses)

        # Mettre à jour le statut
        if self.completion_percentage >= 100.0:
            self.status = EvaluationStatus.COMPLETED
            if self.completed_at is None:
                self.completed_at = datetime.now()
        elif self.completion_percentage > 0:
            self.status = EvaluationStatus.IN_PROGRESS

    def get_response_by_question_id(self, question_id: str) -> Optional[QuestionResponse]:
        """Récupérer une réponse spécifique par ID de question"""
        for category in self.responses.values():
            for subcategory in category.subcategories.values():
                if question_id in subcategory.questions:
                    return subcategory.questions[question_id]
        return None

    def get_category_completion(self, category_id: str) -> float:
        """Obtenir le pourcentage de completion d'une catégorie"""
        if category_id in self.responses:
            return self.responses[category_id].completion_percentage
        return 0.0

    def is_category_completed(self, category_id: str, threshold: float = 90.0) -> bool:
        """Vérifier si une catégorie est considérée comme complète"""
        return self.get_category_completion(category_id) >= threshold

    def get_missing_required_questions(self) -> List[str]:
        """Obtenir la liste des questions obligatoires non remplies"""
        # Cette méthode sera implémentée avec la logique métier
        # en croisant avec les critères définis dans criteria.py
        return []

    def can_calculate_scores(self) -> bool:
        """Vérifier si l'évaluation peut être calculée"""
        return self.completion_percentage >= 80.0  # Seuil minimum pour le calcul

    def to_export_dict(self) -> Dict[str, Any]:
        """Exporter les données pour PDF/Excel"""
        return {
            "metadata": self.metadata.dict(),
            "responses": {
                cat_id: {
                    "subcategories": {
                        sub_id: {
                            "questions": {
                                q_id: q.dict() for q_id, q in sub.questions.items()
                            }
                        } for sub_id, sub in cat.subcategories.items()
                    }
                } for cat_id, cat in self.responses.items()
            },
            "scores": self.calculated_scores.dict() if self.calculated_scores else None,
            "summary": {
                "completion": self.completion_percentage,
                "status": self.status.value,
                "created_at": self.created_at.isoformat(),
                "updated_at": self.updated_at.isoformat()
            }
        }

class EvaluationSession(BaseModel):
    """Session d'évaluation pour le stockage temporaire"""
    session_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    evaluation: Evaluation
    current_category: Optional[str] = None
    current_subcategory: Optional[str] = None
    current_question_index: int = Field(default=0)
    auto_save_enabled: bool = Field(default=True)
    last_auto_save: datetime = Field(default_factory=datetime.now)

    def save_progress(self):
        """Sauvegarder le progrès de la session"""
        self.last_auto_save = datetime.now()
        # La logique de sauvegarde sera implémentée dans storage.py

class ValidationError(BaseModel):
    """Erreur de validation"""
    field: str
    message: str
    code: str
    value: Any

class ValidationResult(BaseModel):
    """Résultat de validation"""
    is_valid: bool
    errors: List[ValidationError] = Field(default_factory=list)
    warnings: List[ValidationError] = Field(default_factory=list)

    def add_error(self, field: str, message: str, code: str, value: Any = None):
        """Ajouter une erreur de validation"""
        self.errors.append(ValidationError(
            field=field, message=message, code=code, value=value
        ))
        self.is_valid = False

    def add_warning(self, field: str, message: str, code: str, value: Any = None):
        """Ajouter un avertissement de validation"""
        self.warnings.append(ValidationError(
            field=field, message=message, code=code, value=value
        ))

# Fonctions utilitaires pour la validation

def validate_numeric_range(value: Union[int, float], min_val: float, max_val: float) -> bool:
    """Valider qu'une valeur numérique est dans une plage"""
    return min_val <= value <= max_val

def validate_percentage(value: Union[int, float]) -> bool:
    """Valider qu'une valeur est un pourcentage valide"""
    return 0.0 <= value <= 100.0

def validate_positive_number(value: Union[int, float]) -> bool:
    """Valider qu'une valeur est un nombre positif"""
    return value >= 0.0

def validate_email(email: str) -> bool:
    """Valider une adresse email"""
    import re
    pattern = r'^[^@]+@[^@]+\.[^@]+$'
    return bool(re.match(pattern, email))

# Types utilitaires
ResponseValue = Union[str, int, float, bool, List[str]]
ScoreDict = Dict[str, float]
MetricsDict = Dict[str, Union[float, str]]
