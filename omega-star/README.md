# Omaga Star

To run: `docker compose up`

Exposes port 5000 for requests.

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
