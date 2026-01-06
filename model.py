"""
Модели данных для Карты гипотез.

Определяет структуры данных для всех элементов карты гипотез
согласно методологии из README.md.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict
from enum import Enum
import uuid


class Priority(Enum):
    """Приоритет элемента карты."""
    HIGH = "high"      # Красный #FF7373
    MEDIUM = "medium"  # Желтый #FFD723
    LOW = "low"        # Зеленый #9EE25B
    NONE = "none"      # Серый #70736D


class TopologyType(Enum):
    """Тип топологии карты."""
    CLASSIC = "classic"  # Классическая
    MANY_LEVELS = "many_levels"  # Многоуровневая
    SEPARATED_METRICS = "separated_metrics"  # Метрики на отдельном уровне
    GOALS_HIERARCHY = "goals_hierarchy"  # Иерархия целей
    MANY_GOALS = "many_goals"  # Многоцелевая
    SEPARATED_MOTIVATION = "separated_motivation"  # Мотивация на отдельном уровне
    GROUPED_TASKS = "grouped_tasks"  # Разбивка задач по направлениям
    TASKS_BOARD = "tasks_board"  # Доска с задачами


@dataclass
class Metric:
    """Метрика цели."""
    name: str
    current_value: str
    target_value: str
    is_leading: bool = False  # Опережающая метрика
    is_lagging: bool = True   # Запаздывающая метрика


@dataclass
class Goal:
    """Цель карты гипотез."""
    description: str
    metrics: List[Metric] = field(default_factory=list)
    balancing_metrics: List[Metric] = field(default_factory=list)
    deadline: Optional[str] = None
    priority: Priority = Priority.NONE
    id: str = field(default_factory=lambda: f"goal_{uuid.uuid4().hex[:8]}")


@dataclass
class Subject:
    """Субъект карты гипотез."""
    description: str
    pains_desires: List[str] = field(default_factory=list)
    is_negative: bool = False  # Негативный субъект
    priority: Priority = Priority.NONE
    id: str = field(default_factory=lambda: f"subject_{uuid.uuid4().hex[:8]}")


@dataclass
class Hypothesis:
    """Гипотеза карты гипотез."""
    if_part: str  # Воздействие, приводящее к изменению поведения субъекта
    then_part: str  # Изменение поведения субъекта
    because_part: str  # Идея, связывающая "если" и "то"
    then_metric: str  # Влияние на метрики цели
    subject_id: Optional[str] = None  # ID субъекта, если связана через субъект
    goal_id: Optional[str] = None  # ID цели, если связана напрямую
    priority: Priority = Priority.NONE
    is_validated: bool = False  # Сработала ли гипотеза
    id: str = field(default_factory=lambda: f"hypothesis_{uuid.uuid4().hex[:8]}")


@dataclass
class Task:
    """Задача для проверки гипотезы."""
    description: str
    hypothesis_id: str  # Обязательная связь с гипотезой
    deadline: Optional[str] = None
    priority: Priority = Priority.NONE
    id: str = field(default_factory=lambda: f"task_{uuid.uuid4().hex[:8]}")


@dataclass
class Blocker:
    """Блокер, мешающий продвижению."""
    reason: str
    actions: List[str] = field(default_factory=list)
    responsible: Optional[str] = None
    deadline: Optional[str] = None
    id: str = field(default_factory=lambda: f"blocker_{uuid.uuid4().hex[:8]}")


@dataclass
class Note:
    """Заметка для сохранения деталей."""
    content: str
    related_element_id: Optional[str] = None
    id: str = field(default_factory=lambda: f"note_{uuid.uuid4().hex[:8]}")


@dataclass
class HypothesisMap:
    """Полная карта гипотез."""
    goals: List[Goal] = field(default_factory=list)
    subjects: List[Subject] = field(default_factory=list)
    hypotheses: List[Hypothesis] = field(default_factory=list)
    tasks: List[Task] = field(default_factory=list)
    blockers: List[Blocker] = field(default_factory=list)
    notes: List[Note] = field(default_factory=list)
    topology: TopologyType = TopologyType.CLASSIC
    
    def get_goal_by_id(self, goal_id: str) -> Optional[Goal]:
        """Получить цель по ID."""
        return next((g for g in self.goals if g.id == goal_id), None)
    
    def get_subject_by_id(self, subject_id: str) -> Optional[Subject]:
        """Получить субъект по ID."""
        return next((s for s in self.subjects if s.id == subject_id), None)
    
    def get_hypothesis_by_id(self, hypothesis_id: str) -> Optional[Hypothesis]:
        """Получить гипотезу по ID."""
        return next((h for h in self.hypotheses if h.id == hypothesis_id), None)
    
    def get_tasks_for_hypothesis(self, hypothesis_id: str) -> List[Task]:
        """Получить все задачи для гипотезы."""
        return [t for t in self.tasks if t.hypothesis_id == hypothesis_id]


@dataclass
class SessionState:
    """Состояние сессии построения карты."""
    map: HypothesisMap = field(default_factory=HypothesisMap)
    current_step: str = "goal"  # goal, subject, hypothesis, task, review
    current_goal_id: Optional[str] = None
    current_subject_id: Optional[str] = None
    current_hypothesis_id: Optional[str] = None
    is_complete: bool = False

