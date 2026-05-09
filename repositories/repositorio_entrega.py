"""Repositorio para gestión de entregas de tareas."""

from typing import List, Optional
from datetime import datetime
from models.entrega import Entrega, EstadoEntrega


class RepositorioEntrega:
    """Manipula datos de entregas en la base de datos."""

    def __init__(self, db: 'GestorDB') -> None:
        self._db = db

    def crear(self, entrega: Entrega) -> Entrega:
        """Registra una nueva entrega en la base de datos."""
        cursor = self._db.ejecutar(
            """INSERT INTO entregas
               (tarea_id, estudiante_codigo, fecha_entrega, archivo_adjunto,
                observaciones, nota, estado, feedback)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (entrega.tarea_id, entrega.estudiante_codigo,
             entrega.fecha_entrega.isoformat(), entrega.archivo_adjunto,
             entrega.observaciones, entrega.nota, entrega.estado.value, entrega.feedback)
        )
        return entrega

    def buscar_por_id(self, id: int) -> Optional[Entrega]:
        """Busca una entrega por su ID."""
        resultado = self._db.consultar(
            "SELECT * FROM entregas WHERE id = ?", (id,)
        )
        if not resultado:
            return None
        return self._mapear_entrega(resultado[0])

    def buscar_por_tarea_y_estudiante(
        self, tarea_id: int, estudiante_codigo: str
    ) -> Optional[Entrega]:
        """Busca si un estudiante ya entregó una tarea."""
        resultado = self._db.consultar(
            """SELECT * FROM entregas
               WHERE tarea_id = ? AND estudiante_codigo = ?""",
            (tarea_id, estudiante_codigo)
        )
        if not resultado:
            return None
        return self._mapear_entrega(resultado[0])

    def listar_por_tarea(self, tarea_id: int) -> List[Entrega]:
        """Lista todas las entregas de una tarea."""
        resultados = self._db.consultar(
            "SELECT * FROM entregas WHERE tarea_id = ? ORDER BY fecha_entrega",
            (tarea_id,)
        )
        return [self._mapear_entrega(fila) for fila in resultados]

    def listar_por_estudiante(self, estudiante_codigo: str) -> List[Entrega]:
        """Lista todas las entregas de un estudiante."""
        resultados = self._db.consultar(
            """SELECT *
               FROM entregas
               WHERE estudiante_codigo = ? ORDER BY fecha_entrega DESC""",
            (estudiante_codigo,)
        )
        return [self._mapear_entrega(fila) for fila in resultados]

    def calificar(
        self, entrega_id: int, nota: float, feedback: str
    ) -> bool:
        """Registra la calificación de una entrega."""
        if not (0 <= nota <= 100):
            raise ValueError("La nota debe estar entre 0 y 100")

        filas = self._db.ejecutar(
            """UPDATE entregas
               SET nota = ?, feedback = ?, estado = ?
               WHERE id = ?""",
            (nota, feedback, EstadoEntrega.CALIFICADA.value, entrega_id)
        ).rowcount
        return filas > 0

    def _mapear_entrega(self, fila) -> Entrega:
        """Convierte una fila de BD en un objeto Entrega."""
        return Entrega(
            id=fila["id"],
            tarea_id=fila["tarea_id"],
            estudiante_codigo=fila["estudiante_codigo"],
            fecha_entrega=datetime.fromisoformat(fila["fecha_entrega"]),
            archivo_adjunto=fila["archivo_adjunto"],
            observaciones=fila["observaciones"],
            nota=fila["nota"],
            estado=EstadoEntrega(fila["estado"]),
            feedback=fila["feedback"]
        )