# Producir notificaciones

A continuación se presentan los comandos para desplegar la función en GCP

### Crear service account para cola

`
gcloud iam service-accounts create notificaciones-productor --description="Cuenta de servicio para productor notificaciones" --display-name="Productor notificaciones"
`

### Crear cola

`
gcloud tasks queues create notificaciones --location=us-central1
`

### Asignar service account a cola

`
gcloud projects add-iam-policy-binding miso-339504 --member="serviceAccount:notificaciones-productor@miso-339504.iam.gserviceaccount.com" --role="roles/cloudtasks.enqueuer"
`

### Crear función

`
gcloud functions deploy funcion-notificaciones-producir --entry-point producir --runtime python39 --trigger-http --allow-unauthenticated --memory 128MB --region us-central1 --timeout 60 --min-instances 0 --max-instances 1 --service-account "notificaciones-productor@miso-339504.iam.gserviceaccount.com" --set-env-vars LOCATION_ID=us-central1,PROJECT_ID=miso-339504,QUEUE_ID=notificaciones,URL_FUNCTION=<URL_FUNCION_CONSUMIR>
`