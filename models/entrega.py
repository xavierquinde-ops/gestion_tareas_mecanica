"""Modelo de entrega de tareas por parte de los estudiantes."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from enum import Enum


class EstadoEntrega(Enum):
    """Estados posibles de una entrega."""
    PENDIENTE = "pendiente"
    ENTREGADA = "entregada"
    CALIFICADA = "calificada"
    RECHAZADA = "rechazada"


@dataclass
class Entrega:
    """Representa la entrega de una tarea por un estudiante.

    Attributes:
        id: Identificador único de la entrega
        tarea_id: ID de la tarea entregada
        estudiante_codigo: Código del estudiante que entrega
        fecha_entrega: Momento en que se realizó la entrega
        archivo_adjunto: Ruta al archivo de respuesta
        observaciones: Comentarios del estudiante
        nota: Calificación asignada (None si no está calificada)
        estado: Estado actual de la entrega
        feedback: Retroalimentación del profesor
    """

    id: Optional[int] = None
    tarea_id: int = 0
    estudiante_codigo: str = ""
    fecha_entrega: datetime = field(default_factory=datetime.now)
    archivo_adjunto: Optional[str] = None
    observaciones: Optional[str] = None
    nota: Optional[float] = None
    estado: EstadoEntrega = EstadoEntrega.PENDIENTE
    feedback: Optional[str] = None

    @property
    def esta_pendiente(self) -> bool:
        """Verifica si la entrega está pendiente de revisión."""
        return self.estado == EstadoEntrega.PENDIENTE

    @property
    def esta_calificada(self) -> bool:
        """Verifica si la entrega ya fue calificada."""
        return self.estado == EstadoEntrega.CALIFICADA

    def __repr__(self) -> str:
        return f"Entrega(id={self.id}, tarea={self.tarea_id}, estudiante={self.estudiante_codigo})"