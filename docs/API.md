# Ngoerah Smart Assistant - API Documentation

## Base URL

```
http://localhost:8000/api/v1
```

## Endpoints

### Health Check

```http
GET /health
```

Returns API health status.

### Chat

```http
POST /api/v1/chat
Content-Type: application/json

{
    "message": "Jam besuk ICU jam berapa?",
    "session_id": "optional-uuid"
}
```

Response:

```json
{
  "response": "Jam besuk ICU adalah...",
  "intent": "FAQ_QUERY",
  "confidence": 0.95,
  "sources": [
    {
      "document": "Pedoman_Pasien.pdf",
      "page": 15,
      "relevance": 0.89
    }
  ],
  "session_id": "uuid",
  "response_time_ms": 2341
}
```

### Feedback

```http
POST /api/v1/feedback
Content-Type: application/json

{
    "message_id": 123,
    "rating": 1,
    "comment": "Very helpful!"
}
```

### Upload Document (Admin)

```http
POST /api/v1/admin/documents
Content-Type: multipart/form-data

file: [PDF file]
title: "Document Title"
document_type: "pedoman"
```

### Analytics (Admin)

```http
GET /api/v1/admin/analytics?days=30
```

## Error Codes

- `400` - Bad Request (invalid input)
- `429` - Rate Limited
- `500` - Internal Server Error
