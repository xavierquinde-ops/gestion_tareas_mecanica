"""Sistema de Gestión Académica.

Sistema de gestión de tareas para estudiantes de Ingeniería Mecánica.
Permite registrar estudiantes, crear tareas (prácticas/teóricas),
gestionar entregas y calificaciones de forma interactiva.
"""

import csv
import os
from datetime import date, timedelta, datetime
from services.servicio_gestion import ServicioGestionAcademica


def formatear_fecha(fecha: date | datetime) -> str:
    """Formatea una fecha en formato dd-mm-aaaa."""
    if isinstance(fecha, datetime):
        fecha = fecha.date()
    return fecha.strftime("%d-%m-%Y")


def formatear_fecha_hora(fecha: datetime) -> str:
    """Formatea una fecha con hora en formato dd-mm-aaaa HH:MM."""
    return fecha.strftime("%d-%m-%Y %H:%M")


def pedir_fecha(mensaje: str) -> date:
    """Solicita una fecha al usuario en formato YYYY-MM-DD."""
    while True:
        fecha_str = input(f"{mensaje} (YYYY-MM-DD): ").strip()
        try:
            return date.fromisoformat(fecha_str)
        except ValueError:
            print("  ✗ Formato inválido. Use YYYY-MM-DD")


def menu_principal() -> None:
    """Muestra el menú principal y gestiona las opciones."""
    servicio = ServicioGestionAcademica()

    while True:
        print("\n" + "=" * 60)
        print("SISTEMA DE GESTIÓN ACADÉMICA - INGENIERÍA MECÁNICA")
        print("=" * 60)
        print("1. Registrar estudiante")
        print("2. Crear tarea práctica")
        print("3. Crear tarea teórica")
        print("4. Registrar entrega de tarea")
        print("5. Calificar entrega")
        print("6. Ver estadísticas de tarea")
        print("7. Listar estudiantes")
        print("8. Listar tareas")
        print("9. Listar entregas por tarea")
        print("10. Ver promedio de estudiante")
        print("11. Reporte: Estudiantes registrados (CSV)")
        print("12. Reporte: Entregas tareas prácticas (CSV)")
        print("13. Reporte: Entregas tareas teóricas (CSV)")
        print("14. Reporte: Calificaciones (CSV)")
        print("0. Salir")
        print("-" * 60)

        opcion = input("Seleccione una opción: ").strip()

        try:
            if opcion == "1":
                registrar_estudiante(servicio)
            elif opcion == "2":
                crear_tarea_practica(servicio)
            elif opcion == "3":
                crear_tarea_teorica(servicio)
            elif opcion == "4":
                registrar_entrega(servicio)
            elif opcion == "5":
                calificar_entrega(servicio)
            elif opcion == "6":
                ver_estadisticas(servicio)
            elif opcion == "7":
                listar_estudiantes(servicio)
            elif opcion == "8":
                listar_tareas(servicio)
            elif opcion == "9":
                listar_entregas_tarea(servicio)
            elif opcion == "10":
                ver_promedio_estudiante(servicio)
            elif opcion == "11":
                reporte_estudiantes_csv(servicio)
            elif opcion == "12":
                reporte_entregas_practicas_csv(servicio)
            elif opcion == "13":
                reporte_entregas_teoricas_csv(servicio)
            elif opcion == "14":
                reporte_calificaciones_csv(servicio)
            elif opcion == "0":
                print("\n¡Hasta luego!")
                break
            else:
                print("  ✗ Opción inválida")
        except Exception as e:
            print(f"  ✗ Error: {e}")


def registrar_estudiante(servicio: ServicioGestionAcademica) -> None:
    """Registra un nuevo estudiante."""
    print("\n--- REGISTRAR ESTUDIANTE ---")
    codigo = input("Código (carnet): ").strip()
    nombre = input("Nombre: ").strip()
    apellido = input("Apellido: ").strip()
    email = input("Email institucional: ").strip()

    try:
        servicio.registrar_estudiante(codigo, nombre, apellido, email)
        print(f"  ✓ {nombre} {apellido} registrado exitosamente")
    except ValueError as e:
        print(f"  ✗ Error: {e}")


def crear_tarea_practica(servicio: ServicioGestionAcademica) -> None:
    """Crea una tarea práctica."""
    print("\n--- CREAR TAREA PRÁCTICA ---")
    titulo = input("Título: ").strip()
    descripcion = input("Descripción: ").strip()
    fecha_entrega = pedir_fecha("Fecha de entrega")
    puntos = float(input("Puntos (default 10): ").strip() or 10)
    horas = float(input("Horas estimadas (default 2): ").strip() or 2)

    print("Materiales requeridos (separados por coma):")
    materiales_input = input().strip()
    materiales = [m.strip() for m in materiales_input.split(",")] if materiales_input else []

    try:
        tarea = servicio.crear_tarea_practica(
            titulo=titulo,
            descripcion=descripcion,
            fecha_entrega=fecha_entrega,
            material_requerido=materiales,
            horas_estimadas=horas,
            puntos=puntos
        )
        print(f"  ✓ Tarea práctica creada (ID: {tarea.id})")
    except ValueError as e:
        print(f"  ✗ Error: {e}")


def crear_tarea_teorica(servicio: ServicioGestionAcademica) -> None:
    """Crea una tarea teórica."""
    print("\n--- CREAR TAREA TEÓRICA ---")
    titulo = input("Título: ").strip()
    descripcion = input("Descripción: ").strip()
    fecha_entrega = pedir_fecha("Fecha de entrega")
    puntos = float(input("Puntos (default 10): ").strip() or 10)
    palabras = int(input("Palabras mínimas (default 500): ").strip() or 500)
    refs = int(input("Referencias requeridas (default 3): ").strip() or 3)

    try:
        tarea = servicio.crear_tarea_teorica(
            titulo=titulo,
            descripcion=descripcion,
            fecha_entrega=fecha_entrega,
            palabras_minimas=palabras,
            referencias_requeridas=refs,
            puntos=puntos
        )
        print(f"  ✓ Tarea teórica creada (ID: {tarea.id})")
    except ValueError as e:
        print(f"  ✗ Error: {e}")


def registrar_entrega(servicio: ServicioGestionAcademica) -> None:
    """Registra la entrega de una tarea."""
    print("\n--- REGISTRAR ENTREGA ---")

    # Listar tareas disponibles
    tareas = servicio.listar_tareas()
    if not tareas:
        print("  ✗ No hay tareas disponibles")
        return

    print("Tareas disponibles:")
    for t in tareas:
        print(f"  [{t.id}] {t.titulo} - {t.estado.value} (Entrega: {formatear_fecha(t.fecha_entrega)})")

    try:
        tarea_id = int(input("\nID de la tarea: ").strip())
        estudiante_codigo = input("Código del estudiante: ").strip()
        archivo = input("Archivo adjunto (opcional): ").strip() or None
        obs = input("Observaciones (opcional): ").strip() or None

        entrega = servicio.entregar_tarea(
            tarea_id=tarea_id,
            estudiante_codigo=estudiante_codigo,
            archivo_adjunto=archivo,
            observaciones=obs
        )
        print(f"  ✓ Entrega registrada (ID: {entrega.id})")
    except ValueError as e:
        print(f"  ✗ Error: {e}")
    except Exception as e:
        print(f"  ✗ Error: {e}")


def calificar_entrega(servicio: ServicioGestionAcademica) -> None:
    """Califica una entrega."""
    print("\n--- CALIFICAR ENTREGA ---")

    # Listar entregas pendientes
    tareas = servicio.listar_tareas()
    if not tareas:
        print("  ✗ No hay tareas")
        return

    tarea_id = int(input("ID de la tarea: ").strip())
    entregas = servicio.listar_entregas_tarea(tarea_id)

    if not entregas:
        print("  ✗ No hay entregas para esta tarea")
        return

    print("Entregas pendientes de calificación:")
    for e in entregas:
        if e.estado.value == "entregada":
            print(f"  [{e.id}] Estudiante: {e.estudiante_codigo} - Fecha: {formatear_fecha_hora(e.fecha_entrega)}")

    if not any(e.estado.value == "entregada" for e in entregas):
        print("  ✗ No hay entregas pendientes")
        return

    try:
        entrega_id = int(input("\nID de entrega a calificar: ").strip())
        nota = float(input("Nota (0-100): ").strip())
        feedback = input("Feedback: ").strip()

        exito = servicio.calificar_entrega(entrega_id, nota, feedback)
        if exito:
            print(f"  ✓ Calificación registrada: {nota}/100")
    except ValueError as e:
        print(f"  ✗ Error: {e}")


def ver_estadisticas(servicio: ServicioGestionAcademica) -> None:
    """Muestra estadísticas de una tarea."""
    print("\n--- ESTADÍSTICAS DE TAREA ---")

    tareas = servicio.listar_tareas()
    if not tareas:
        print("  ✗ No hay tareas")
        return

    for t in tareas:
        print(f"  [{t.id}] {t.titulo}")

    tarea_id = int(input("ID de la tarea: ").strip())

    try:
        stats = servicio.obtener_estadisticas_tarea(tarea_id)
        print(f"\n--- {stats['titulo']} ---")
        print(f"Total entregas: {stats['total_entregas']}")
        print(f"Entregadas: {stats['entregadas']}")
        print(f"Calificadas: {stats['calificadas']}")
        if stats['promedio_nota']:
            print(f"Promedio: {stats['promedio_nota']:.2f}")
            print(f"Máxima: {stats['nota_maxima']:.2f}")
            print(f"Mínima: {stats['nota_minima']:.2f}")
        else:
            print("Sin calificaciones aún")
    except ValueError as e:
        print(f"  ✗ Error: {e}")


def listar_estudiantes(servicio: ServicioGestionAcademica) -> None:
    """Lista todos los estudiantes."""
    print("\n--- LISTADO DE ESTUDIANTES ---")
    estudiantes = servicio.listar_estudiantes()

    if not estudiantes:
        print("  ✗ No hay estudiantes registrados")
        return

    for est in estudiantes:
        promedio = servicio.obtener_promedio_estudiante(est.codigo)
        promedio_str = f"{promedio:.2f}" if promedio else "Sin entregas"
        print(f"  [{est.codigo}] {est.nombre} {est.apellido} - Email: {est.email} - Promedio: {promedio_str}")


def listar_tareas(servicio: ServicioGestionAcademica) -> None:
    """Lista todas las tareas."""
    print("\n--- LISTADO DE TAREAS ---")
    tareas = servicio.listar_tareas()

    if not tareas:
        print("  ✗ No hay tareas")
        return

    for t in tareas:
        print(f"  [{t.id}] {t.titulo}")
        print(f"      Tipo: {type(t).__name__} | Estado: {t.estado.value} | Puntos: {t.puntos}")
        print(f"      Entrega: {formatear_fecha(t.fecha_entrega)}")


def listar_entregas_tarea(servicio: ServicioGestionAcademica) -> None:
    """Lista entregas de una tarea."""
    print("\n--- ENTREGAS POR TAREA ---")

    tareas = servicio.listar_tareas()
    if not tareas:
        print("  ✗ No hay tareas")
        return

    for t in tareas:
        print(f"  [{t.id}] {t.titulo}")

    tarea_id = int(input("ID de la tarea: ").strip())
    entregas = servicio.listar_entregas_tarea(tarea_id)

    if not entregas:
        print("  ✗ No hay entregas")
        return

    for e in entregas:
        print(f"\n  Entrega [{e.id}]")
        print(f"    Estudiante: {e.estudiante_codigo}")
        print(f"    Estado: {e.estado.value}")
        print(f"    Fecha: {formatear_fecha_hora(e.fecha_entrega)}")
        if e.nota:
            print(f"    Nota: {e.nota}")
            print(f"    Feedback: {e.feedback}")


def ver_promedio_estudiante(servicio: ServicioGestionAcademica) -> None:
    """Muestra el promedio de un estudiante."""
    print("\n--- PROMEDIO DE ESTUDIANTE ---")

    estudiantes = servicio.listar_estudiantes()
    if not estudiantes:
        print("  ✗ No hay estudiantes")
        return

    for est in estudiantes:
        print(f"  [{est.codigo}] {est.nombre} {est.apellido}")

    codigo = input("Código del estudiante: ").strip()

    promedio = servicio.obtener_promedio_estudiante(codigo)
    if promedio:
        print(f"  Promedio: {promedio:.2f}")
    else:
        print("  Sin entregas calificadas")


def reporte_estudiantes_csv(servicio: ServicioGestionAcademica) -> None:
    """Genera un reporte CSV de estudiantes registrados."""
    print("\n--- REPORTE: ESTUDIANTES REGISTRADOS ---")

    estudiantes = servicio.listar_estudiantes()
    if not estudiantes:
        print("  ✗ No hay estudiantes registrados")
        return

    archivo = "reporte_estudiantes.csv"
    with open(archivo, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Código", "Nombre", "Apellido", "Email", "Estado"])

        for est in estudiantes:
            promedio = servicio.obtener_promedio_estudiante(est.codigo)
            promedio_str = f"{promedio:.2f}" if promedio else "Sin entregas"
            writer.writerow([est.codigo, est.nombre, est.apellido, est.email, f"Promedio: {promedio_str}"])

    print(f"  ✓ Reporte generado: {archivo}")


def reporte_entregas_practicas_csv(servicio: ServicioGestionAcademica) -> None:
    """Genera un reporte CSV de entregas de tareas prácticas."""
    print("\n--- REPORTE: ENTREGAS TAREAS PRÁCTICAS ---")

    tareas = servicio.listar_tareas()
    tareas_practicas = [t for t in tareas if type(t).__name__ == "TareaPractica"]

    if not tareas_practicas:
        print("  ✗ No hay tareas prácticas")
        return

    archivo = "reporte_entregas_practicas.csv"
    with open(archivo, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["ID Entrega", "Tarea", "Estudiante", "Fecha Entrega", "Archivo", "Observaciones", "Estado", "Nota", "Feedback"])

        for tarea in tareas_practicas:
            entregas = servicio.listar_entregas_tarea(tarea.id)
            for e in entregas:
                writer.writerow([
                    e.id,
                    tarea.titulo,
                    e.estudiante_codigo,
                    formatear_fecha_hora(e.fecha_entrega),
                    e.archivo_adjunto or "",
                    e.observaciones or "",
                    e.estado.value,
                    e.nota if e.nota else "",
                    e.feedback or ""
                ])

    print(f"  ✓ Reporte generado: {archivo}")


def reporte_entregas_teoricas_csv(servicio: ServicioGestionAcademica) -> None:
    """Genera un reporte CSV de entregas de tareas teóricas."""
    print("\n--- REPORTE: ENTREGAS TAREAS TEÓRICAS ---")

    tareas = servicio.listar_tareas()
    tareas_teoricas = [t for t in tareas if type(t).__name__ == "TareaTeorica"]

    if not tareas_teoricas:
        print("  ✗ No hay tareas teóricas")
        return

    archivo = "reporte_entregas_teoricas.csv"
    with open(archivo, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["ID Entrega", "Tarea", "Estudiante", "Fecha Entrega", "Archivo", "Observaciones", "Estado", "Nota", "Feedback"])

        for tarea in tareas_teoricas:
            entregas = servicio.listar_entregas_tarea(tarea.id)
            for e in entregas:
                writer.writerow([
                    e.id,
                    tarea.titulo,
                    e.estudiante_codigo,
                    formatear_fecha_hora(e.fecha_entrega),
                    e.archivo_adjunto or "",
                    e.observaciones or "",
                    e.estado.value,
                    e.nota if e.nota else "",
                    e.feedback or ""
                ])

    print(f"  ✓ Reporte generado: {archivo}")


def reporte_calificaciones_csv(servicio: ServicioGestionAcademica) -> None:
    """Genera un reporte CSV de todas las calificaciones."""
    print("\n--- REPORTE: CALIFICACIONES ---")

    tareas = servicio.listar_tareas()
    if not tareas:
        print("  ✗ No hay tareas")
        return

    archivo = "reporte_calificaciones.csv"
    with open(archivo, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["ID Entrega", "Tarea", "Tipo Tarea", "Estudiante", "Fecha Entrega", "Fecha Calificación", "Nota", "Puntos Máx", "Feedback"])

        for tarea in tareas:
            entregas = servicio.listar_entregas_tarea(tarea.id)
            for e in entregas:
                if e.nota is not None:
                    writer.writerow([
                        e.id,
                        tarea.titulo,
                        type(tarea).__name__,
                        e.estudiante_codigo,
                        formatear_fecha_hora(e.fecha_entrega),
                        formatear_fecha_hora(e.fecha_entrega),  #同一 fecha como ejemplo
                        e.nota,
                        tarea.puntos,
                        e.feedback or ""
                    ])

    print(f"  ✓ Reporte generado: {archivo}")


if __name__ == "__main__":
    menu_principal()