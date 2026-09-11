"""Version inicial del banco, deliberadamente acoplada para ser diagnosticada."""


class TarjetaProvider:
    """Proveedor fake para simular un deposito con tarjeta."""

    def cobrar(self, monto):
        print(f"Tarjeta fake procesando {monto:.2f}")
        return True


class PSEProvider:
    """Proveedor fake para simular un deposito con PSE."""

    def cobrar(self, monto):
        print(f"PSE fake procesando {monto:.2f}")
        return True


class BilleteraProvider:
    """Proveedor fake para simular un deposito con billetera."""

    def cobrar(self, monto):
        print(f"Billetera fake procesando {monto:.2f}")
        return True


class Banco:
    def __init__(self):
        self.cuentas = {}
        self.transacciones = []
        self.siguiente_transaccion = 1

    def crear_cuenta(self, cuenta_id, titular, saldo_inicial=0.0):
        self.cuentas[cuenta_id] = {
            "id": cuenta_id,
            "titular": titular,
            "saldo": float(saldo_inicial),
            "historial": [],
        }
        print(f"Cuenta creada: {cuenta_id} - {titular}")
        return self.cuentas[cuenta_id]

    def depositar(self, cuenta_id, monto, canal="tarjeta"):
        transaccion = {
            "id": self.siguiente_transaccion,
            "tipo": "deposito",
            "cuenta": cuenta_id,
            "monto": float(monto),
            "canal": canal,
            "estado": "CREADA",
        }
        self.siguiente_transaccion += 1
        self.transacciones.append(transaccion)
        return self.procesar_transaccion(transaccion)

    def retirar(self, cuenta_id, monto):
        transaccion = {
            "id": self.siguiente_transaccion,
            "tipo": "retiro",
            "cuenta": cuenta_id,
            "monto": float(monto),
            "canal": "interno",
            "estado": "CREADA",
        }
        self.siguiente_transaccion += 1
        self.transacciones.append(transaccion)
        return self.procesar_transaccion(transaccion)

    def transferir(self, origen_id, destino_id, monto, canal="interno"):
        transaccion = {
            "id": self.siguiente_transaccion,
            "tipo": "transferencia",
            "cuenta": origen_id,
            "destino": destino_id,
            "monto": float(monto),
            "canal": canal,
            "estado": "CREADA",
        }
        self.siguiente_transaccion += 1
        self.transacciones.append(transaccion)
        return self.procesar_transaccion(transaccion)

    def calcular_comision(self, monto, canal):
        if canal == "tarjeta":
            return monto * 0.029 + 0.30
        elif canal == "pse":
            return monto * 0.015
        elif canal == "billetera":
            return monto * 0.02
        else:
            return 0.0

    def procesar_transaccion(self, transaccion):
        cuenta = self.cuentas.get(transaccion["cuenta"])
        if cuenta is None:
            transaccion["estado"] = "RECHAZADA"
            print(f"Transaccion {transaccion['id']} rechazada: cuenta inexistente")
            return False

        monto = transaccion["monto"]
        comision = self.calcular_comision(monto, transaccion["canal"])
        total = monto + comision
        transaccion["comision"] = comision

        proveedor = None
        if transaccion["canal"] == "tarjeta":
            proveedor = TarjetaProvider()
        elif transaccion["canal"] == "pse":
            proveedor = PSEProvider()
        elif transaccion["canal"] == "billetera":
            proveedor = BilleteraProvider()

        if transaccion["tipo"] == "deposito":
            if proveedor is not None and not proveedor.cobrar(monto):
                transaccion["estado"] = "RECHAZADA"
                print(f"Transaccion {transaccion['id']} rechazada por proveedor")
                return False
        elif transaccion["tipo"] == "retiro":
            if cuenta["saldo"] < total:
                transaccion["estado"] = "RECHAZADA"
                print(f"Transaccion {transaccion['id']} rechazada: saldo insuficiente")
                return False
        elif transaccion["tipo"] == "transferencia":
            destino = self.cuentas.get(transaccion["destino"])
            if destino is None:
                transaccion["estado"] = "RECHAZADA"
                print(f"Transaccion {transaccion['id']} rechazada: destino inexistente")
                return False
            if cuenta["saldo"] < total:
                transaccion["estado"] = "RECHAZADA"
                print(f"Transaccion {transaccion['id']} rechazada: saldo insuficiente")
                return False

        if transaccion["estado"] == "CREADA":
            transaccion["estado"] = "VALIDADA"
        if transaccion["estado"] == "VALIDADA":
            transaccion["estado"] = "AUTORIZADA"
        if transaccion["estado"] == "AUTORIZADA":
            transaccion["estado"] = "PROCESADA"

        if transaccion["tipo"] == "deposito":
            cuenta["saldo"] += monto - comision
        elif transaccion["tipo"] == "retiro":
            cuenta["saldo"] -= total
        elif transaccion["tipo"] == "transferencia":
            cuenta["saldo"] -= total
            destino["saldo"] += monto

        if transaccion["estado"] == "PROCESADA":
            transaccion["estado"] = "COMPLETADA"
        cuenta["historial"].append(transaccion)
        print(
            f"Transaccion {transaccion['id']} completada: "
            f"{transaccion['tipo']} por {monto:.2f}"
        )
        print(f"Notificacion: nuevo saldo de {cuenta['id']}: {cuenta['saldo']:.2f}")
        return True

    def mostrar_saldo(self, cuenta_id):
        cuenta = self.cuentas.get(cuenta_id)
        if cuenta is None:
            return None
        return cuenta["saldo"]


if __name__ == "__main__":
    banco = Banco()
    banco.crear_cuenta("A-001", "Ana", 100.00)
    banco.crear_cuenta("B-001", "Bruno", 20.00)
    banco.depositar("A-001", 50.10, "tarjeta")
    banco.retirar("A-001", 10.00)
    banco.transferir("A-001", "B-001", 25.00)
    print(f"Saldo final Ana: {banco.mostrar_saldo('A-001'):.2f}")
    print(f"Saldo final Bruno: {banco.mostrar_saldo('B-001'):.2f}")
