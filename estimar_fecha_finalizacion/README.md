# Estimar fecha de finalización

A continuación se presentan los comandos para desplegar la función en GCP

`
gcloud functions deploy funcion-estimar-fecha-finalizacion --entry-point estimar_fecha_finalizacion --runtime python39 --trigger-http --allow-unauthenticated --memory 128MB --region us-central1 --timeout 60 --min-instances 0 --max-instances 1 --set-env-vars BASE_URL=<MICROSERVICES_API>
`