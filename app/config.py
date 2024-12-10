# Path: fta_profile/app/config.pyfrom functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict


class Settings(BaseSettings):
    # Application Settings
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    app_log_level: str = "debug"
    app_env: str = "dev"
    app_name: str = "fta_profile"
    app_workers: int = 2

    # GCP
    ## Firestore
    firestore_project_id: str = Field(json_schema_extra={"env": "FIRESTORE_PROJECT_ID"})
    firestore_database: str = Field(json_schema_extra={"env": "FIRESTORE_DATABASE"})
    firestore_collection: str = Field(json_schema_extra={"env": "FIRESTORE_COLLECTION"})
    
    # Firestore Emulator
    use_firestore_emulator: bool = False
    firestore_emulator_host: str = "localhost:8080"
    
    # Middleware
    ## CORS
    cors_allow_origins: str = "*"
    cors_allow_methods: str = "*"
    cors_allow_headers: str = "*"
    cors_allow_credentials: bool = False
    cors_max_age: int = 86400

    ## TrustedHostMiddleware
    trusted_hosts: str = "*"

    ## GZipMiddleware
    gzip_min_length: int = 512

    ## LOGGER
    use_aiologger: bool = False

    ## OpenTelemetry
    otel_exporter_otlp_endpoint: str = "otel-collector:4317"
    otel_exporter_otlp_insecure: bool = True
    otel_exporter_otlp_headers_str: str = ""
    otel_sampling_rate: float = 1.0  # Default to always sample
    @property
    def otel_exporter_otlp_headers(self) -> dict[str, str]:
        headers_str = self.otel_exporter_otlp_headers_str
        headers = {}
        if headers_str:
            for header in headers_str.split(","):
                key, value = header.strip().split("=")
                headers[key.strip()] = value.strip()
        return headers
    # Loading .env file if present
    model_config = ConfigDict(env_file=".env", env_file_encoding="utf-8")