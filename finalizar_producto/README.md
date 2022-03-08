# Finalizar fabricación

<img width="610" alt="Screen Shot 2022-03-06 at 11 42 02 AM" src="https://misovirtual.virtual.uniandes.edu.co/codelabs/dann-proyecto-3-038a6078cab0/img/7d5a0f270a033286.png">

## Por medio de la interfaz:

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


## Por medio de la consola:

```
gcloud functions deploy funcion-finalizar-producto --entry-point finalizar_producto --runtime python39 --trigger-http --allow-unauthenticated --memory 128MB --region us-central1 --timeout 60 --min-instances 0 --max-instances 1 --set-env-vars SERVER=<MICROSERVICES_API>,INTEGRATIONS_SERVER=<INTEGRATIONS_API>,NOTIFICATIONS_SERVER=<NOTIFICATIONS_API>
```

## Proceso de ejecución

El producto finaliza su fabricación por lo que debe ser actualizado el estado del pedido, crear entrega del pedido y noitificar al comprador el cambio de estado, finalmente se agenda la entrega con el proveedor

## Como ejecutar la prueba ?

Esta funcion requiere de un body para enviar por medio de un POST, para aclarar, se debe contar con una order creado previamente (tener el order_id) con el fin de adjuntar este valor en el campo extra1 del payload mostrado a continuación:

La url de la función corresponde a : https://us-central1-apisentrega3.cloudfunctions.net/funcion-finalizar-producto y se debe enviar el header `x-auth-token` con un token de sesion.

```
{
    "orderId":"{{orderId}}",
    "sellerId":"{{sellerId}}"
}
```

En el caso de obtener una respuesta exitosa por parte de la función, se obtendra el siguiente resultado:


```
{
    "message": "Producto finalizado correctamente, se agenda entrega con el proveedor"
}
```
