from typing import Any, Sequence
from pydantic_settings import BaseSettings, SettingsConfigDict
from fastapi_keycloak_middleware import KeycloakConfiguration


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='FASTAPI_')

    secret_key: str
    frontend_url: str

    database_uri: str

    root_path: str = ''

    cors_allow_methods: Sequence[str] = ('GET', 'POST')
    cors_allow_headers: Sequence[str] = ('authorization',)
    cors_allow_credentials: bool = True
    cors_allow_origin_regex: str | None = None
    cors_expose_headers: Sequence[str] = tuple()
    cors_max_age: int = 600

    session_session_cookie: str = '__Secure-Session'
    session_cookie_same_site: str = 'strict'
    session_cookie_https_only: bool = True
    session_cookie_path: str = '/'
    session_max_age: int = 60 * 60 * 24 * 7 * 2
    session_domain: str | None = None

    keycloak_url: str
    keycloak_realm: str
    keycloak_client_id: str
    keycloak_client_secret: str

    def get_cors_arguments(self) -> dict[str, Any]:
        return {
            'allow_origins': (self.frontend_url,),
            'allow_methods': self.cors_allow_methods,
            'allow_headers': self.cors_allow_headers,
            'allow_credentials': self.cors_allow_credentials,
            'allow_origin_regex': self.cors_allow_origin_regex,
            'expose_headers': self.cors_expose_headers,
            'max_age': self.cors_max_age,
        }

    def get_session_arguments(self) -> dict[str, Any]:
        return {
            'secret_key': self.secret_key,
            'session_cookie': self.session_session_cookie,
            'max_age': self.session_max_age,
            'domain': self.session_domain,
            'path': self.session_cookie_path,
            'same_site': self.session_cookie_same_site,
            'https_only': self.session_cookie_https_only,
        }

    def get_keycloak_config(self) -> KeycloakConfiguration:
        return KeycloakConfiguration(
            url=self.keycloak_url,
            realm=self.keycloak_realm,
            client_id=self.keycloak_client_id,
            client_secret=self.keycloak_client_secret,
        )
