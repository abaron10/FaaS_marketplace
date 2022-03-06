
# Estado de pago actualizado

<img width="641" alt="image" src="https://user-images.githubusercontent.com/64280930/156932260-83d334cd-66c5-4074-b2aa-39a012315d11.png">

## Como desplegar la función:



## Proceso de ejecución

1. Al completar la transacción en la pasarela de pagos, el procesador de transacciones notifica el resultado mediante el llamado a un webhook expuesto para tal propósito.
2. Una vez se ha procesado el pago de la compra por parte del cliente, si el pago fue exitoso, se debe enviar una notificación al vendedor indicando el estado del pedido.

## Como ejecutar la prueba ?

Esta funcion requiere de un body para enviar por medio de un POST, para aclarar, se debe contar con un pago creado previamente (tener el payment_id) con el fin de adjuntar este valor en el campo extra1 del payload mostrado a continuación:

La url de la función corresponde a : https://us-central1-miso-my-first-project-339515.cloudfunctions.net/estado_pago_actualizacion 

```
{
  "id": "GTAFFE3553",
  "updateId": "DFGGFDDG2342345",
  "extra1": <payment_id>,
  "timestamp": "YYYY-DD-MM HH:MM:SS",
  "signature": "5E9DA426AA7D4A585E9DA426AA7D4A585E9DA426AA7D4A585E9DA426AA7D4A585E9DA426AA7D4A58",
  "estado": "ACEPTADO"
}
```
En el caso de obtener una respuesta exitosa por parte de la función, se obtendra el siguiente resultado:

```
{"msg":"succesfull update"}
```

De lo contrario obtendra un mensaje de error como el siguiente:
```
{"msg":"error while updating delivery"},404
```
