"""Modelo de Estudiante para el sistema de gestión académica."""

from typing import Optional
from dataclasses import dataclass, field


@dataclass
class Estudiante:
    """Representa un estudiante de ingeniería mecánica.

    Attributes:
        codigo: Identificador único del estudiante (carnet)
        nombre: Nombre completo del estudiante
        apellido: Apellido del estudiante
        email: Correo institucional del estudiante
        activo: Estado de inscripción en el curso
    """

    codigo: str
    nombre: str
    apellido: str
    email: str
    activo: bool = field(default=True)

    def __post_init__(self) -> None:
        """Valida los datos del estudiante después de la creación."""
        self._validar_codigo()
        self._validar_email()

    def _validar_codigo(self) -> None:
        """Valida que el código del estudiante no esté vacío."""
        if not self.codigo or not self.codigo.strip():
            raise ValueError("El código del estudiante no puede estar vacío")

    def _validar_email(self) -> None:
        """Valida formato básico del email institucional."""
        if not self.email or "@" not in self.email:
            raise ValueError(f"Email inválido para {self.nombre}: {self.email}")

    @property
    def nombre_completo(self) -> str:
        """Retorna el nombre completo del estudiante."""
        return f"{self.nombre} {self.apellido}"

    @property
    def iniciales(self) -> str:
        """Retorna las iniciales del estudiante."""
        return f"{self.nombre[0]}{self.apellido[0]}".upper()

    def __repr__(self) -> str:
        return f"Estudiante(codigo='{self.codigo}', nombre='{self.nombre_completo}')"