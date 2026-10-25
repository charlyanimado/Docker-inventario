# 🐋 Dockerizando tu inventario en AWS ☁️

Guía práctica para tomar una aplicación web (frontend + backend), **dockerizarla** y desplegarla en AWS con **Amazon ECR** y **Amazon EC2**.

📝 Tutorial completo en AWS Builder Center: [Dockerizando tu inventario con AWS](https://builder.aws.com/content/33zYXJB15d9bYMflxwZagH2LnJS/dockerizando-tu-inventario-con-aws)

## Arquitectura

```
Navegador ──► :8080  frontend (Nginx)  ──/api/──►  backend (Flask + Gunicorn) :8000
                     sirve HTML/CSS/JS              solo accesible desde la red
                                                    interna de Docker Compose
```

- **Frontend:** Nginx sirve la página y hace de *reverse proxy* hacia la API. El navegador siempre llama a `/api/...`, así que no hay que escribir la IP del servidor en el código ni configurar CORS.
- **Backend:** API en Flask servida con Gunicorn. No publica ningún puerto: solo el frontend puede llegar a él.

## Buenas prácticas aplicadas

| | Backend | Frontend |
|---|---|---|
| Imagen base | `python:3.13-slim` | `nginx-unprivileged:stable-alpine` |
| Usuario sin root | ✅ `appuser` | ✅ `nginx` |
| `HEALTHCHECK` | ✅ `/health` | ✅ `/health` |
| `.dockerignore` | ✅ | ✅ |
| Caché de capas | `requirements.txt` se copia antes que el código | — |

Además, Compose espera a que el backend esté *healthy* antes de levantar el frontend y reinicia los contenedores si se caen.

## Probarlo en local

```bash
docker compose up -d --build
# abrir http://localhost:8080
docker compose ps        # ambos servicios deben aparecer como (healthy)
docker compose down
```

## Desplegar en AWS

1. **Crear los repositorios en ECR** y subir las imágenes:
   ```bash
   aws ecr create-repository --repository-name backend-inventario
   aws ecr create-repository --repository-name frontend-inventario

   REGISTRY=<ID_DE_CUENTA>.dkr.ecr.<REGION>.amazonaws.com
   aws ecr get-login-password | docker login --username AWS --password-stdin $REGISTRY

   docker compose build
   for img in backend-inventario frontend-inventario; do
     docker tag $img:latest $REGISTRY/$img:latest
     docker push $REGISTRY/$img:latest
   done
   ```
2. **Crear una instancia EC2** con Docker instalado y un rol de IAM con la política `AmazonEC2ContainerRegistryReadOnly`, para que pueda descargar las imágenes sin guardar credenciales en el servidor.
3. En el **Security Group**, abrir solo el puerto **8080** (el backend no necesita estar expuesto).
4. En la instancia, iniciar sesión en ECR, descargar las imágenes y levantar el `docker-compose.yml`.

> 💡 Cuando termines de probar, borra la instancia EC2 y los repositorios de ECR: lo que no usas, apágalo.

## Tecnologías

Docker · Docker Compose · Nginx · Python · Flask · Gunicorn · Amazon ECR · Amazon EC2 · AWS IAM · AWS CLI

## Autor

Carlos Roca · AWS Community Builder (Containers) · [LinkedIn](https://linkedin.com/in/carlosmroca)
