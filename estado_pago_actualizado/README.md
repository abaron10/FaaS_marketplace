
# Estado de pago actualizado

<img width="641" alt="image" src="https://user-images.githubusercontent.com/64280930/156932260-83d334cd-66c5-4074-b2aa-39a012315d11.png">

## Como desplegar la función:

### Por medio de la interfaz:
#### 1. Dar click en crear nueva función
<img width="1417" alt="image" src="https://user-images.githubusercontent.com/64280930/156932795-f9b17760-dd96-406b-b471-dac5034fae02.png">


#### 2. Otorgar nombre de la función correspondiente y dar permisos de acceso no autenticado.
<img width="581" alt="image" src="https://user-images.githubusercontent.com/64280930/156932763-5d5e1697-34c9-4573-9503-34d34a09be1c.png">

#### 3. Configurar numero de instancias minimo para el despliegue
<img width="588" alt="image" src="https://user-images.githubusercontent.com/64280930/156932835-0fb7f734-153b-4000-849f-357328f4c3c2.png">

#### 4. Set de variables de entorno requeridas en el codigo
<img width="550" alt="image" src="https://user-images.githubusercontent.com/64280930/156932859-4affd51b-aa2d-4681-99d1-d11630ec349c.png">

#### 5. Adición de requirements y codigo pertinente para la ejecución.
<img width="1389" alt="image" src="https://user-images.githubusercontent.com/64280930/156932919-d0ccb50e-e5ff-43e3-a56d-326cc4359cd1.png">

#### 6. Click en implementar
<img width="329" alt="image" src="https://user-images.githubusercontent.com/64280930/156932933-57165b2e-cacc-4a9c-8525-33f35f151475.png">

#### 7. Validar creación de función con exito
<img width="1532" alt="image" src="https://user-images.githubusercontent.com/64280930/156932952-fe4bbdff-4d1b-4ef7-b303-29c4ff2b2e84.png">

### Por medio de la consola:
```
gcloud functions deploy <NOMBRE_FUNCION> --entry-point <NOMBRE_FUNCION_EJECUTABLE>--runtime python39 --trigger-http --allow-unauthenticated --memory 128MB --region us-central1 --timeout 60 --min-instances 0 --max-instances 1 --set-env-vars BASE_URL=<MICROSERVICES_API>
```


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
