import requests
import json
import base64
from typing import Dict, Optional
from abc import ABC, abstractmethod


class EmailProvider(ABC):
    """Clase abstracta para proveedores de email"""
    
    @abstractmethod
    def send_email(
        self,
        from_email: str,
        to_email: str,
        to_name: str,
        subject: str,
        html_content: str,
        substitutions: Optional[Dict[str, str]] = None
    ) -> Dict:
        pass


class SendGridProvider(EmailProvider):
    """Proveedor de email usando SendGrid"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.sendgrid.com/v3/mail/send"
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        }
    
    def send_email(
        self,
        from_email: str,
        to_email: str,
        to_name: str,
        subject: str,
        html_content: str,
        substitutions: Optional[Dict[str, str]] = None
    ) -> Dict:
        """Enviar email usando SendGrid"""
        
        payload = {
            "from": {
                "email": from_email
            },
            "personalizations": [
                {
                    "to": [
                        {
                            "email": to_email,
                            "name": to_name
                        }
                    ],
                    "subject": subject
                }
            ],
            "content": [
                {
                    "type": "text/html",
                    "value": html_content
                }
            ]
        }
        
        # Añadir sustituciones si se proporcionan
        if substitutions:
            payload["personalizations"][0]["substitutions"] = substitutions
        
        try:
            response = requests.post(
                self.base_url,
                headers=self.headers,
                data=json.dumps(payload)
            )
            
            return {
                "status_code": response.status_code,
                "response_text": response.text,
                "success": response.status_code == 202,
                "provider": "sendgrid"
            }
            
        except Exception as e:
            return {
                "status_code": None,
                "response_text": str(e),
                "success": False,
                "error": str(e),
                "provider": "sendgrid"
            }


class MailgunProvider(EmailProvider):
    """Proveedor de email usando Mailgun"""
    
    def __init__(self, api_key: str, domain: str):
        self.api_key = api_key
        self.domain = domain
        self.base_url = f"https://api.mailgun.net/v3/{domain}/messages"
        
        # Crear la autorización básica
        auth_string = f"api:{api_key}"
        auth_bytes = auth_string.encode('ascii')
        auth_b64 = base64.b64encode(auth_bytes).decode('ascii')
        
        self.headers = {
            'Authorization': f'Basic {auth_b64}'
        }
    
    def send_email(
        self,
        from_email: str,
        to_email: str,
        to_name: str,
        subject: str,
        html_content: str,
        substitutions: Optional[Dict[str, str]] = None
    ) -> Dict:
        """Enviar email usando Mailgun"""
        
        # Aplicar sustituciones al contenido HTML si se proporcionan
        final_content = html_content
        if substitutions:
            for key, value in substitutions.items():
                final_content = final_content.replace(f"{{{key}}}", value)
        
        payload = {
            'from': from_email,
            'to': to_email,
            'subject': subject,
            'html': final_content
        }
        
        try:
            response = requests.post(
                self.base_url,
                headers=self.headers,
                data=payload
            )
            
            return {
                "status_code": response.status_code,
                "response_text": response.text,
                "success": response.status_code == 200,
                "provider": "mailgun"
            }
            
        except Exception as e:
            return {
                "status_code": None,
                "response_text": str(e),
                "success": False,
                "error": str(e),
                "provider": "mailgun"
            }


class EmailService:
    """Servicio de email con soporte para múltiples proveedores y fallback automático"""
    
    def __init__(self, sendgrid_api_key: str = None, mailgun_api_key: str = None, mailgun_domain: str = None):
        self.providers = {}
        
        # Configurar SendGrid si se proporciona la API key
        if sendgrid_api_key:
            self.providers['sendgrid'] = SendGridProvider(sendgrid_api_key)
        
        # Configurar Mailgun si se proporcionan las credenciales
        if mailgun_api_key and mailgun_domain:
            self.providers['mailgun'] = MailgunProvider(mailgun_api_key, mailgun_domain)
        
        if not self.providers:
            raise ValueError("Se debe configurar al menos un proveedor de email")
    
    def send_email(
        self,
        from_email: str,
        to_email: str,
        to_name: str,
        subject: str,
        html_content: str,
        substitutions: Optional[Dict[str, str]] = None,
        provider: str = None,
        use_fallback: bool = True
    ) -> Dict:
        """
        Enviar un email usando el proveedor especificado o con fallback automático
        
        Args:
            from_email: Dirección de email del remitente
            to_email: Dirección de email del destinatario
            to_name: Nombre del destinatario
            subject: Asunto del email
            html_content: Contenido HTML del email
            substitutions: Diccionario de sustituciones para variables de plantilla
            provider: Proveedor específico a usar ('sendgrid' o 'mailgun'). Si no se especifica, usa el primero disponible
            use_fallback: Si es True, intenta con otros proveedores si el primero falla
            
        Returns:
            Dict que contiene la respuesta del proveedor de email
        """
        
        # Determinar el orden de proveedores a usar
        if provider and provider in self.providers:
            provider_order = [provider]
            if use_fallback:
                provider_order.extend([p for p in self.providers.keys() if p != provider])
        else:
            provider_order = list(self.providers.keys())
        
        last_result = None
        
        for current_provider in provider_order:
            if current_provider not in self.providers:
                continue
                
            result = self.providers[current_provider].send_email(
                from_email, to_email, to_name, subject, html_content, substitutions
            )
            
            if result.get('success'):
                return result
            else:
                last_result = result
                
                if not use_fallback:
                    break
        
        # Si llegamos aquí, todos los proveedores fallaron
        return last_result or {
            "success": False,
            "error": "No hay proveedores de email disponibles",
            "provider": "none"
        }
    
    def get_available_providers(self) -> list:
        """Devuelve la lista de proveedores configurados"""
        return list(self.providers.keys())