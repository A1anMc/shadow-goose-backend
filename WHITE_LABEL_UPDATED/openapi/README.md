# OpenAPI Export

FastAPI serves OpenAPI at `/openapi.json`.

- Staging: `curl -s https://navimpact-api-staging.onrender.com/openapi.json -o latest-openapi.json`
- Production: `curl -s https://navimpact-api.onrender.com/openapi.json -o latest-openapi.json`

Add the exported file to this folder for client API use or import into Postman/Insomnia.
