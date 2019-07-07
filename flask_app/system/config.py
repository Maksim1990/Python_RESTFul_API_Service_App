from datetime import timedelta

# MAIN APPLICATION CONFIGURATION
config={
    "api_prefix":"/api/v1",
    "jwt_auth_header_prefix":"Bearer",
    "secret_key":"base64:QAJqjgvMf5se3mNEb6PDmj/Y4MG1kTpybjKQiLR0hp4=",
    "token_expiration_time": timedelta(seconds=3600), # Set expiration time as 1 HOUR
}
