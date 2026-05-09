"""Configuración y gestión de la base de datos SQLite."""

import sqlite3
from pathlib import Path
from typing import Optional
from contextlib import contextmanager


class GestorDB:
    """Gestor singleton de conexión a la base de datos."""

    _instancia: Optional['GestorDB'] = None

    def __new__(cls, db_path: str = "gestion_academica.db") -> 'GestorDB':
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._db_path = db_path
            cls._instancia._inicializar_db()
        return cls._instancia

    def _inicializar_db(self) -> None:
        """Crea las tablas si no existen."""
        with self._obtener_conexion() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS estudiantes (
                    codigo TEXT PRIMARY KEY,
                    nombre TEXT NOT NULL,
                    apellido TEXT NOT NULL,
                    email TEXT NOT NULL,
                    activo INTEGER DEFAULT 1
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tareas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT NOT NULL,
                    descripcion TEXT NOT NULL,
                    fecha_creacion TEXT NOT NULL,
                    fecha_entrega TEXT NOT NULL,
                    estado TEXT NOT NULL,
                    puntos REAL DEFAULT 10.0,
                    tipo TEXT NOT NULL,
                    material_requerido TEXT,
                    horas_estimadas REAL,
                    palabras_minimas INTEGER,
                    referencias_requeridas INTEGER
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS entregas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tarea_id INTEGER NOT NULL,
                    estudiante_codigo TEXT NOT NULL,
                    fecha_entrega TEXT NOT NULL,
                    archivo_adjunto TEXT,
                    observaciones TEXT,
                    nota REAL,
                    estado TEXT NOT NULL,
                    feedback TEXT,
                    FOREIGN KEY (tarea_id) REFERENCES tareas(id),
                    FOREIGN KEY (estudiante_codigo) REFERENCES estudiantes(codigo)
                )
            """)
            conn.commit()

    @contextmanager
    def _obtener_conexion(self):
        """Contexto para obtener conexión con manejo de errores."""
        conn = sqlite3.connect(self._db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        except sqlite3.Error as e:
            conn.rollback()
            raise RuntimeError(f"Error de base de datos: {e}")
        finally:
            conn.close()

    def ejecutar(self, query: str, params: tuple = ()):
        """Ejecuta una consulta y retorna el cursor."""
        with self._obtener_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor

    def consultar(self, query: str, params: tuple = ()) -> list:
        """Ejecuta una consulta SELECT y retorna los resultados."""
        with self._obtener_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()