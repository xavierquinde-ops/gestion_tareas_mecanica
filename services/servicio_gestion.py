"""Servicio de gestión académica que orquesta la lógica de negocio."""

from typing import List, Optional, Dict
from datetime import date, datetime

from models.estudiante import Estudiante
from models.tarea import Tarea, TareaPractica, TareaTeorica, EstadoTarea
from models.entrega import Entrega, EstadoEntrega
from repositories import (
    RepositorioEstudiante,
    RepositorioTarea,
    RepositorioEntrega
)
from repositories.database import GestorDB


class ServicioGestionAcademica:
    """Coordina todas las operaciones del sistema académico.

    Implementa la lógica de negocio encapsulando los repositorios
    y proporcionando una interfaz unificada para el controlador.
    """

    def __init__(self) -> None:
        self._db = GestorDB()
        self._repo_estudiante = RepositorioEstudiante(self._db)
        self._repo_tarea = RepositorioTarea(self._db)
        self._repo_entrega = RepositorioEntrega(self._db)

    # --- OPERACIONES DE ESTUDIANTES ---

    def registrar_estudiante(
        self, codigo: str, nombre: str, apellido: str, email: str
    ) -> Estudiante:
        """Registra un nuevo estudiante en el sistema."""
        estudiante = Estudiante(
            codigo=codigo,
            nombre=nombre,
            apellido=apellido,
            email=email
        )
        return self._repo_estudiante.crear(estudiante)

    def buscar_estudiante(self, codigo: str) -> Optional[Estudiante]:
        """Busca un estudiante por su código."""
        return self._repo_estudiante.buscar_por_codigo(codigo)

    def listar_estudiantes(self) -> List[Estudiante]:
        """Lista todos los estudiantes activos."""
        return self._repo_estudiante.listar_todos()

    # --- OPERACIONES DE TAREAS ---

    def crear_tarea_practica(
        self,
        titulo: str,
        descripcion: str,
        fecha_entrega: date,
        material_requerido: List[str],
        horas_estimadas: float,
        puntos: float = 10.0
    ) -> TareaPractica:
        """Crea una nueva tarea práctica."""
        tarea = TareaPractica(
            id=None,
            titulo=titulo,
            descripcion=descripcion,
            fecha_creacion=datetime.now(),
            fecha_entrega=fecha_entrega,
            estado=EstadoTarea.PUBLICADA,
            puntos=puntos,
            material_requerido=material_requerido,
            horas_estimadas=horas_estimadas
        )
        return self._repo_tarea.crear(tarea)

    def crear_tarea_teorica(
        self,
        titulo: str,
        descripcion: str,
        fecha_entrega: date,
        palabras_minimas: int,
        referencias_requeridas: int,
        puntos: float = 10.0
    ) -> TareaTeorica:
        """Crea una nueva tarea teórica."""
        tarea = TareaTeorica(
            id=None,
            titulo=titulo,
            descripcion=descripcion,
            fecha_creacion=datetime.now(),
            fecha_entrega=fecha_entrega,
            estado=EstadoTarea.PUBLICADA,
            puntos=puntos,
            palabras_minimas=palabras_minimas,
            referencias_requeridas=referencias_requeridas
        )
        return self._repo_tarea.crear(tarea)

    def listar_tareas(self, estado: Optional[str] = None) -> List[Tarea]:
        """Lista tareas filtradas por estado."""
        if estado:
            estado_enum = EstadoTarea(estado)
            return self._repo_tarea.listar_todas(estado_enum)
        return self._repo_tarea.listar_todas()

    def cerrar_tarea(self, tarea_id: int) -> bool:
        """Cierra una tarea para nuevas entregas."""
        return self._repo_tarea.actualizar_estado(tarea_id, EstadoTarea.CERRADA)

    # --- OPERACIONES DE ENTREGAS ---

    def entregar_tarea(
        self,
        tarea_id: int,
        estudiante_codigo: str,
        archivo_adjunto: Optional[str] = None,
        observaciones: Optional[str] = None
    ) -> Entrega:
        """Registra la entrega de una tarea por un estudiante."""
        # Validar que la tarea existe y está abierta
        tarea = self._repo_tarea.buscar_por_id(tarea_id)
        if not tarea:
            raise ValueError(f"Tarea con ID {tarea_id} no encontrada")

        if tarea.estado not in [EstadoTarea.PUBLICADA]:
            raise ValueError(f"La tarea {tarea.titulo} no acepta entregas")

        # Validar que el estudiante existe
        if not self._repo_estudiante.buscar_por_codigo(estudiante_codigo):
            raise ValueError(f"Estudiante {estudiante_codigo} no encontrado")

        # Verificar si ya existe entrega previa
        entrega_existente = self._repo_entrega.buscar_por_tarea_y_estudiante(
            tarea_id, estudiante_codigo
        )
        if entrega_existente:
            raise ValueError("Ya existe una entrega para esta tarea")

        entrega = Entrega(
            tarea_id=tarea_id,
            estudiante_codigo=estudiante_codigo,
            fecha_entrega=datetime.now(),
            archivo_adjunto=archivo_adjunto,
            observaciones=observaciones,
            estado=EstadoEntrega.ENTREGADA
        )
        return self._repo_entrega.crear(entrega)

    def calificar_entrega(
        self, entrega_id: int, nota: float, feedback: str
    ) -> bool:
        """Registra la calificación de una entrega."""
        entrega = self._repo_entrega.buscar_por_id(entrega_id)
        if not entrega:
            raise ValueError(f"Entrega con ID {entrega_id} no encontrada")

        return self._repo_entrega.calificar(entrega_id, nota, feedback)

    def listar_entregas_tarea(self, tarea_id: int) -> List[Entrega]:
        """Lista todas las entregas de una tarea."""
        return self._repo_entrega.listar_por_tarea(tarea_id)

    def listar_entregas_estudiante(self, estudiante_codigo: str) -> List[Entrega]:
        """Lista todas las entregas de un estudiante."""
        return self._repo_entrega.listar_por_estudiante(estudiante_codigo)

    # --- CONSULTAS ANALÍTICAS ---

    def obtener_estadisticas_tarea(self, tarea_id: int) -> Dict:
        """Estadísticas de entregas para una tarea."""
        entregas = self._repo_entrega.listar_por_tarea(tarea_id)
        tarea = self._repo_tarea.buscar_por_id(tarea_id)

        if not tarea:
            raise ValueError(f"Tarea {tarea_id} no encontrada")

        notas = [e.nota for e in entregas if e.nota is not None]

        return {
            "tarea_id": tarea_id,
            "titulo": tarea.titulo,
            "total_entregas": len(entregas),
            "entregadas": sum(1 for e in entregas if e.estado == EstadoEntrega.ENTREGADA),
            "calificadas": sum(1 for e in entregas if e.estado == EstadoEntrega.CALIFICADA),
            "promedio_nota": sum(notas) / len(notas) if notas else None,
            "nota_maxima": max(notas) if notas else None,
            "nota_minima": min(notas) if notas else None
        }

    def obtener_promedio_estudiante(self, estudiante_codigo: str) -> Optional[float]:
        """Calcula el promedio de un estudiante."""
        entregas = self._repo_entrega.listar_por_estudiante(estudiante_codigo)
        notas = [e.nota for e in entregas if e.nota is not None]
        return sum(notas) / len(notas) if notas else None