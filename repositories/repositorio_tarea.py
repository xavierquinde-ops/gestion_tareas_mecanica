"""Repositorio para gestión de tareas académicas."""

from typing import List, Optional
from datetime import datetime
from models.tarea import Tarea, TareaPractica, TareaTeorica, EstadoTarea


class RepositorioTarea:
    """Manipula datos de tareas en la base de datos."""

    def __init__(self, db: 'GestorDB') -> None:
        self._db = db

    def crear(self, tarea: Tarea) -> Tarea:
        """Registra una nueva tarea en la base de datos."""
        if isinstance(tarea, TareaPractica):
            tipo = "practica"
            material = ",".join(tarea.material_requerido)
            horas = tarea.horas_estimadas
            palabras = None
            refs = None
        elif isinstance(tarea, TareaTeorica):
            tipo = "teorica"
            material = None
            horas = None
            palabras = tarea.palabras_minimas
            refs = tarea.referencias_requeridas
        else:
            raise TypeError(f"Tipo de tarea no soportado: {type(tarea)}")

        cursor = self._db.ejecutar(
            """INSERT INTO tareas
               (titulo, descripcion, fecha_creacion, fecha_entrega, estado,
                puntos, tipo, material_requerido, horas_estimadas,
                palabras_minimas, referencias_requeridas)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (tarea.titulo, tarea.descripcion,
             tarea.fecha_creacion.isoformat(), tarea.fecha_entrega.isoformat(),
             tarea.estado.value, tarea.puntos, tipo, material, horas, palabras, refs)
        )
        tarea.id = cursor.lastrowid
        return tarea

    def buscar_por_id(self, id: int) -> Optional[Tarea]:
        """Busca una tarea por su ID."""
        resultado = self._db.consultar(
            "SELECT * FROM tareas WHERE id = ?", (id,)
        )
        if not resultado:
            return None
        return self._mapear_tarea(resultado[0])

    def listar_todas(self, estado: Optional[EstadoTarea] = None) -> List[Tarea]:
        """Lista todas las tareas, opcionalmente filtradas por estado."""
        if estado:
            resultados = self._db.consultar(
                "SELECT * FROM tareas WHERE estado = ? ORDER BY fecha_entrega",
                (estado.value,)
            )
        else:
            resultados = self._db.consultar(
                "SELECT * FROM tareas ORDER BY fecha_entrega"
            )
        return [self._mapear_tarea(fila) for fila in resultados]

    def listar_pendientes(self) -> List[Tarea]:
        """Lista tareas pendientes de entrega."""
        return self.listar_todas(EstadoTarea.PUBLICADA)

    def actualizar_estado(self, id: int, estado: EstadoTarea) -> bool:
        """Actualiza el estado de una tarea."""
        filas = self._db.ejecutar(
            "UPDATE tareas SET estado = ? WHERE id = ?",
            (estado.value, id)
        ).rowcount
        return filas > 0

    def _mapear_tarea(self, fila) -> Tarea:
        """Convierte una fila de BD en el tipo de tarea correspondiente."""
        tipo = fila["tipo"]
        kwargs = {
            "id": fila["id"],
            "titulo": fila["titulo"],
            "descripcion": fila["descripcion"],
            "fecha_creacion": datetime.fromisoformat(fila["fecha_creacion"]),
            "fecha_entrega": datetime.fromisoformat(fila["fecha_entrega"]).date(),
            "estado": EstadoTarea(fila["estado"]),
            "puntos": fila["puntos"]
        }

        if tipo == "practica":
            return TareaPractica(
                **kwargs,
                material_requerido=fila["material_requerido"].split(",") if fila["material_requerido"] else [],
                horas_estimadas=fila["horas_estimadas"] or 2.0
            )
        else:
            return TareaTeorica(
                **kwargs,
                palabras_minimas=fila["palabras_minimas"] or 500,
                referencias_requeridas=fila["referencias_requeridas"] or 3
            )