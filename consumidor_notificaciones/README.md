# Consumir notificaciones

A continuación se presentan los comandos para desplegar la función en GCP

### Crear función

```
gcloud functions deploy funcion-notificaciones-consumir --entry-point consumir --runtime python39 --trigger-http --allow-unauthenticated --memory 128MB --region us-central1 --timeout 60 --min-instances 0 --max-instances 1
```
