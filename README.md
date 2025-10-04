# From-Zero-to-Vertex-AI-Invoke-Gemini-using-Responsible-AI-Principles

(Ref : https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/configure-safety-filters)

## Safety configuration (Responsible-AI)

You define safety_settings as a list of SafetySetting objects—each declares a harm category and a block threshold. Here you cover: Dangerous content, Harassment, Hate speech, and Sexually explicit content, and you set BLOCK_LOW_AND_ABOVE (strict) for all of them. These categories/thresholds are the same ones documented for the Gemini API; unlisted categories fall back to defaults. 

Practically, these settings screen both inputs and outputs. If the model judges the content to meet/exceed the threshold, the call is blocked (no text returned). By default, Gemini uses a severity-aware harm-block method in Vertex AI; you can tune this behavior as needed.

Example when detection of Harm Speech is there
```
{
  "summary": {
    "content": {
      "parts": null,
      "role": null
    },
    "citationMetadata": null,
    "finishMessage": null,
    "tokenCount": null,
    "finishReason": "SAFETY",
    "urlContextMetadata": null,
    "avgLogprobs": null,
    "groundingMetadata": null,
    "index": null,
    "logprobsResult": null,
    "safetyRatings": [
      {
        "blocked": true,
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "overwrittenThreshold": null,
        "probability": "LOW",
        "probabilityScore": 0.14913946,
        "severity": "HARM_SEVERITY_LOW",
        "severityScore": 0.5322947
      },
      {
        "blocked": null,
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "overwrittenThreshold": null,
        "probability": "NEGLIGIBLE",
        "probabilityScore": 0.009629141,
        "severity": "HARM_SEVERITY_LOW",
        "severityScore": 0.30252504
      },
      {
        "blocked": null,
        "category": "HARM_CATEGORY_HARASSMENT",
        "overwrittenThreshold": null,
        "probability": "NEGLIGIBLE",
        "probabilityScore": 0.0006751251,
        "severity": "HARM_SEVERITY_LOW",
        "severityScore": 0.28615037
      },
      {
        "blocked": null,
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "overwrittenThreshold": null,
        "probability": "NEGLIGIBLE",
        "probabilityScore": 7.06525e-8,
        "severity": "HARM_SEVERITY_NEGLIGIBLE",
        "severityScore": 0.081496745
      }
    ]
  }
}
```

## Choose Cloud Run Functions if:

You need to respond to events or HTTP triggers quickly.

You want minimal configuration—all infrastructure handled for you.

You're working with concise functions rather than full-fledged services.


## Velox

Vellox is an adapter for running ASGI applications ((Asynchronous Server Gateway Interface) ) in GCP Cloud Functions.

## HTTPBearer

HTTPBearer in FastAPI is a security utility provided by the fastapi.security module. It is designed to handle Bearer token authentication, which is a common method for securing API endpoints.
HTTPBearer primarily handles the presence and extraction of the Bearer token.

## Steps 

### Dev Setup
Use devcontainer to install ( I am using so this is easy )

create main.py with fastapi and vellox

### Log On
gcloud init

### Enable Services
gcloud services enable artifactregistry.googleapis.com cloudbuild.googleapis.com run.googleapis.com logging.googleapis.com aiplatform.googleapis.com

### IAM 
[In IAM give project role of 'roles/aiplatform.user' to current project](https://cloud.google.com/vertex-ai/generative-ai/docs/start/api-keys?usertype=existinguser) 

### Deploy with ENV, Variables
gcloud run deploy fastapi-func --source . --function handler --base-image python313 --region asia-south1 --set-env-vars API_TOKEN="damn-long-token",GOOGLE_GENAI_USE_VERTEXAI=True,GOOGLE_CLOUD_LOCATION=global  --allow-unauthenticated


