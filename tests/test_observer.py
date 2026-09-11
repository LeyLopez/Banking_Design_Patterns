import logging

from src.infraestructura.notificaciones import (
    AuditoriaLogger,
    NotificadorConsola,
    SujetoTransaccion,
)


def test_sujeto_notifica_a_consola_y_auditoria(caplog, capsys):
    sujeto = SujetoTransaccion()
    auditoria = AuditoriaLogger()
    sujeto.suscribir(NotificadorConsola())
    sujeto.suscribir(auditoria)
    transaccion = {"id": "tx-001", "estado": "CREADA"}

    with caplog.at_level(logging.INFO):
        sujeto.cambiar_estado(transaccion, "COMPLETADA")

    assert transaccion["estado"] == "COMPLETADA"
    assert "Notificacion de transaccion tx-001: estado COMPLETADA" in capsys.readouterr().out
    assert "Transaccion tx-001 cambio a estado COMPLETADA" in caplog.text


def test_suscripcion_no_se_duplica_y_desuscripcion_detiene_notificaciones(capsys):
    sujeto = SujetoTransaccion()
    notificador = NotificadorConsola()
    sujeto.suscribir(notificador)
    sujeto.suscribir(notificador)
    sujeto.desuscribir(notificador)

    sujeto.cambiar_estado({"id": "tx-002", "estado": "RECHAZADA"}, "REVERSADA")

    assert capsys.readouterr().out == ""
