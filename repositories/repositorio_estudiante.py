"""Repositorio para gestión de estudiantes en la base de datos."""

from typing import List, Optional
from models.estudiante import Estudiante


class RepositorioEstudiante:
    """Manipula datos de estudiantes en la base de datos."""

    def __init__(self, db: 'GestorDB') -> None:
        self._db = db

    def crear(self, estudiante: Estudiante) -> Estudiante:
        """Registra un nuevo estudiante en la base de datos."""
        self._db.ejecutar(
            """INSERT INTO estudiantes (codigo, nombre, apellido, email, activo)
               VALUES (?, ?, ?, ?, ?)""",
            (estudiante.codigo, estudiante.nombre, estudiante.apellido,
             estudiante.email, 1 if estudiante.activo else 0)
        )
        return estudiante

    def buscar_por_codigo(self, codigo: str) -> Optional[Estudiante]:
        """Busca un estudiante por su código."""
        resultado = self._db.consultar(
            "SELECT * FROM estudiantes WHERE codigo = ?", (codigo,)
        )
        if not resultado:
            return None
        return self._mapear_estudiante(resultado[0])

    def listar_todos(self) -> List[Estudiante]:
        """Retorna todos los estudiantes activos."""
        resultados = self._db.consultar(
            "SELECT * FROM estudiantes WHERE activo = 1 ORDER BY apellido"
        )
        return [self._mapear_estudiante(fila) for fila in resultados]

    def actualizar(self, estudiante: Estudiante) -> bool:
        """Actualiza los datos de un estudiante."""
        filas = self._db.ejecutar(
            """UPDATE estudiantes
               SET nombre = ?, apellido = ?, email = ?, activo = ?
               WHERE codigo = ?""",
            (estudiante.nombre, estudiante.apellido, estudiante.email,
             1 if estudiante.activo else 0, estudiante.codigo)
        ).rowcount
        return filas > 0

    def eliminar(self, codigo: str) -> bool:
        """Elimina (desactiva) un estudiante."""
        filas = self._db.ejecutar(
            "UPDATE estudiantes SET activo = 0 WHERE codigo = ?", (codigo,)
        ).rowcount
        return filas > 0

    def _mapear_estudiante(self, fila) -> Estudiante:
        """Convierte una fila de BD en un objeto Estudiante."""
        return Estudiante(
            codigo=fila["codigo"],
            nombre=fila["nombre"],
            apellido=fila["apellido"],
            email=fila["email"],
            activo=bool(fila["activo"])
        )