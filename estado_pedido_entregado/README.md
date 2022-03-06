
# Estado de pago en tránsito


## Como desplegar la función:

#### 1. Dar click en crear nueva función
<img width="1417" alt="image" src="https://user-images.githubusercontent.com/64280930/156932795-f9b17760-dd96-406b-b471-dac5034fae02.png">

#### 2. Otorgar nombre de la función correspondiente y dar permisos de acceso no autenticado.
<img width="581" alt="image" src="https://user-images.githubusercontent.com/64280930/156932763-5d5e1697-34c9-4573-9503-34d34a09be1c.png">

#### 3. Configurar número de instancias mínimo para el despliegue
<img width="588" alt="image" src="https://user-images.githubusercontent.com/64280930/156932835-0fb7f734-153b-4000-849f-357328f4c3c2.png">

#### 4. Set de variables de entorno requeridas en el código
<img width="550" alt="image" src="https://user-images.githubusercontent.com/64280930/156932859-4affd51b-aa2d-4681-99d1-d11630ec349c.png">

#### 5. Adición de requirements y código pertinente para la ejecución.

#### 6. Click en implementar
<img width="329" alt="image" src="https://user-images.githubusercontent.com/64280930/156932933-57165b2e-cacc-4a9c-8525-33f35f151475.png">

#### 7. Validar creación de función con éxito

### Por medio de la consola:
```
gcloud functions deploy funcion-actualizacion-pedido-entregado --entry-point actualizacion_estado_pedido_entregado --runtime python39 --trigger-http --allow-unauthenticated --memory 128MB --region us-central1 --timeout 60 --min-instances 0 --max-instances 1
```

## Proceso de ejecución

1. Después de que se entrega el pedido, el vendedor actualiza el estado del pedido
2. Se genera la factura correspondiente al pedido
3. Se le notifica al vendedor que la factura se generó

## ¿Cómo ejecutar la prueba?

Esta función requiere de un body para enviar por medio de un POST, para aclarar, se debe contar con un pedido existente para asignarle valor al campo orderId:

La url de la función corresponde a: https://us-central1-cloud-functions-343223.cloudfunctions.net/funcion-actualizacion-pedido-entregado

```
{
    "orderId": "336f0721-e3ab-4a9c-a094-fa443d6955a6",
    "externalId": "d8047ced-362d-4524-8f9e-0ecaffaee75f"
}
```
En el caso de obtener una respuesta exitosa por parte de la función, se obtendrá el siguiente resultado:

```
{"msg":"succesfull update"}
```

De lo contrario obtendrá un mensaje de error como el siguiente:
```
{"msg":"error while updating delivery"}
```
