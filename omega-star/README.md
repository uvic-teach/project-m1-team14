# Omega Star

Hosted at https://seng350.kjs.dev

To deploy a new version: Send me a dm

To run: `docker compose up`

Exposes port 5000 for requests. Make sure to include th API_KEY environment variable.

## API

POST /register

Registers a patient to receive an email when space is available in the ER.

Body: json

```json
{
    "username": "",
    "token": "",
    "email": ""
}
```

Must include x-api-key header
