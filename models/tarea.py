"""Modelos de tareas académicas con herencia para distintos tipos."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, date
from typing import Optional, List
from enum import Enum


class TipoTarea(Enum):
    """Enumeración de tipos de tareas disponibles."""
    PRACTICA = "practica"
    TEORICA = "teorica"
    PROYECTO = "proyecto"


class EstadoTarea(Enum):
    """Estados de una tarea en el sistema."""
    PENDIENTE = "pendiente"
    PUBLICADA = "publicada"
    CERRADA = "cerrada"
    CALIFICADA = "calificada"


@dataclass
class Tarea(ABC):
    """Clase abstracta base para todas las tareas académicas.

    Attributes:
        id: Identificador único de la tarea
        titulo: Título descriptivo de la tarea
        descripcion: Descripción detallada del enunciado
        fecha_creacion: Fecha de creación en el sistema
        fecha_entrega: Fecha límite de entrega
        estado: Estado actual de la tarea
        puntos: Puntuación máxima de la tarea
    """

    id: Optional[int]
    titulo: str
    descripcion: str
    fecha_creacion: datetime
    fecha_entrega: date
    estado: EstadoTarea
    puntos: float = 10.0

    @abstractmethod
    def validar_fecha_entrega(self, fecha_entrega: date) -> bool:
        """Método abstracto para validar fechas según tipo de tarea."""
        pass

    @property
    def esta_vencida(self) -> bool:
        """Determina si la tarea ya pasó su fecha de entrega."""
        return date.today() > self.fecha_entrega

    @property
    def dias_restantes(self) -> int:
        """Días restantes hasta la fecha de entrega."""
        return (self.fecha_entrega - date.today()).days

    def __repr__(self) -> str:
        return f"Tarea(id={self.id}, titulo='{self.titulo}', estado={self.estado.value})"


@dataclass
class TareaPractica(Tarea):
    """Tareas prácticas de laboratorio o taller para ingeniería mecánica.

    Additional Attributes:
        material_requerido: Lista de materiales necesarios
        horas_estimadas: Horas de trabajo estimadas
    """

    material_requerido: List[str] = field(default_factory=list)
    horas_estimadas: float = 2.0
    tipo: TipoTarea = TipoTarea.PRACTICA

    def validar_fecha_entrega(self, fecha_entrega: date) -> bool:
        """Las tareas prácticas permiten entregas hasta 48hrs después."""
        from datetime import timedelta
        fecha_limite = self.fecha_entrega + timedelta(days=2)
        return fecha_entrega <= fecha_limite

    def __repr__(self) -> str:
        return f"TareaPractica(id={self.id}, titulo='{self.titulo}')"


@dataclass
class TareaTeorica(Tarea):
    """Tareas teóricas, ensayos o informes técnicos.

    Additional Attributes:
        palabras_minimas: Requerimiento de extensión mínima
        referencias_requeridas: Número de referencias bibliográficas
    """

    palabras_minimas: int = 500
    referencias_requeridas: int = 3
    tipo: TipoTarea = TipoTarea.TEORICA

    def validar_fecha_entrega(self, fecha_entrega: date) -> bool:
        """Las tareas teóricas no permiten extensiones."""
        return fecha_entrega <= self.fecha_entrega

    @property
    def extension_calculada(self) -> int:
        """Calcula extensión basada en palabras (aproximación)."""
        return len(self.descripcion.split()) * 2

    def __repr__(self) -> str:
        return f"TareaTeorica(id={self.id}, titulo='{self.titulo}')"