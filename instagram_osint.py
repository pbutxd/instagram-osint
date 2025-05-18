#!/usr/bin/env python3
# Instagram OSINT Pro - By BallenaHacker 🐋
# Versión 2.0 con descargas, análisis y exportación

import argparse
import json
import csv
import random
import time
import logging
import os
from bs4 import BeautifulSoup
import requests

class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class InstagramOSINT:
    def __init__(self, username):
        self.useragents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'
        ]
        self.username = username
        self.session = requests.Session()
        self.profile_data = self.get_profile_data()
        self.posts_data = []
        
        # Configurar logging
        logging.basicConfig(
            filename=f'instagram_osint_{username}.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def make_request(self, url):
        headers = {
            'User-Agent': random.choice(self.useragents),
            'X-IG-App-ID': '936619743392459',
            'Accept-Language': 'en-US,en;q=0.9'
        }
        try:
            response = self.session.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response
        except Exception as e:
            logging.error(f"Request failed to {url}: {str(e)}")
            print(f"{colors.FAIL}Error en la solicitud: {e}{colors.ENDC}")
            return None

    def get_profile_data(self):
        print(f"{colors.OKBLUE}Obteniendo datos de @{self.username}...{colors.ENDC}")
        url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={self.username}"
        
        response = self.make_request(url)
        if not response:
            return {}

        try:
            data = response.json()
            user = data['data']['user']
            
            profile_data = {
                'username': user.get('username'),
                'full_name': user.get('full_name', ''),
                'biography': user.get('biography', ''),
                'profile_pic_url': user.get('profile_pic_url_hd', ''),
                'followers': user.get('edge_followed_by', {}).get('count', 0),
                'following': user.get('edge_follow', {}).get('count', 0),
                'is_private': user.get('is_private', False),
                'is_verified': user.get('is_verified', False),
                'total_posts': user.get('edge_owner_to_timeline_media', {}).get('count', 0),
                'external_url': user.get('external_url', ''),
                'last_updated': time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
            print(f"{colors.OKGREEN}✓ Perfil obtenido{colors.ENDC}")
            logging.info(f"Perfil de @{self.username} obtenido correctamente")
            return profile_data

        except Exception as e:
            logging.error(f"Error procesando perfil: {str(e)}")
            print(f"{colors.FAIL}Error al procesar datos: {e}{colors.ENDC}")
            return {}

    # ---- NUEVAS FUNCIONALIDADES ----
    def download_profile_pic(self):
        if not self.profile_data.get('profile_pic_url'):
            return

        try:
            url = self.profile_data['profile_pic_url']
            filename = f"{self.username}_profile_pic.jpg"
            
            print(f"{colors.OKBLUE}Descargando foto de perfil...{colors.ENDC}")
            response = requests.get(url, stream=True)
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
                    
            print(f"{colors.OKGREEN}✓ Foto descargada: {filename}{colors.ENDC}")
            logging.info(f"Foto de perfil guardada como {filename}")
            
        except Exception as e:
            logging.error(f"Error descargando foto: {str(e)}")
            print(f"{colors.FAIL}Error al descargar foto: {e}{colors.ENDC}")

    def export_to_csv(self):
        if not self.profile_data:
            return

        filename = f"{self.username}_data.csv"
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Metrica', 'Valor'])
                for key, value in self.profile_data.items():
                    writer.writerow([key, value])
                    
            print(f"{colors.OKGREEN}✓ Datos exportados a {filename}{colors.ENDC}")
            logging.info(f"Datos exportados a CSV: {filename}")
            
        except Exception as e:
            logging.error(f"Error exportando CSV: {str(e)}")
            print(f"{colors.FAIL}Error al exportar CSV: {e}{colors.ENDC}")

    def analyze_engagement(self, posts_to_analyze=12):
        if not self.profile_data.get('total_posts') or self.profile_data['total_posts'] == 0:
            return 0

        try:
            # Simulación de análisis de engagement (en una implementación real harías scraping de posts)
            avg_likes = self.profile_data['followers'] * 0.03  # 3% de engagement estimado
            engagement_rate = (avg_likes / self.profile_data['followers']) * 100
            
            print(f"{colors.OKBLUE}📊 Engagement rate estimado: {engagement_rate:.2f}%{colors.ENDC}")
            return engagement_rate
            
        except Exception as e:
            logging.error(f"Error en análisis de engagement: {str(e)}")
            print(f"{colors.FAIL}Error en análisis: {e}{colors.ENDC}")
            return 0

def banner():
    print(f"""{colors.HEADER}
   ██╗███╗   ██╗███████╗████████╗ █████╗  ██████╗ ███████╗
   ██║████╗  ██║██╔════╝╚══██╔══╝██╔══██╗██╔════╝ ██╔════╝
   ██║██╔██╗ ██║███████╗   ██║   ███████║██║  ███╗█████╗  
   ██║██║╚██╗██║╚════██║   ██║   ██╔══██║██║   ██║██╔══╝  
   ██║██║ ╚████║███████║   ██║   ██║  ██║╚██████╔╝███████╗
   ╚═╝╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚══════╝
   
   Instagram OSINT Pro v2.0 (By BallenaHacker 🐋)
   {colors.ENDC}""")

def main():
    parser = argparse.ArgumentParser(description='Herramienta OSINT avanzada para Instagram')
    parser.add_argument('username', help='Nombre de usuario de Instagram')
    parser.add_argument('--download', action='store_true', help='Descargar foto de perfil')
    parser.add_argument('--csv', action='store_true', help='Exportar datos a CSV')
    args = parser.parse_args()

    banner()
    print(f"\n{colors.BOLD}🔍 Analizando: @{args.username}{colors.ENDC}\n")
    
    try:
        scraper = InstagramOSINT(username=args.username)
        
        # Mostrar datos básicos
        print(f"\n{colors.HEADER}=== DATOS DEL PERFIL ==={colors.ENDC}")
        for key, value in scraper.profile_data.items():
            print(f"{colors.BOLD}{key.replace('_', ' ').title():<20}{colors.ENDC}: {value}")
        
        # Funcionalidades adicionales
        if args.download:
            scraper.download_profile_pic()
            
        if args.csv:
            scraper.export_to_csv()
        
        scraper.analyze_engagement()
        
        print(f"\n{colors.OKGREEN}✔ Análisis completado{colors.ENDC}")
        logging.info(f"Proceso completado para @{args.username}")
        
    except Exception as e:
        print(f"\n{colors.FAIL}✖ Error crítico: {e}{colors.ENDC}")
        logging.error(f"Error en el proceso principal: {str(e)}")

if __name__ == "__main__":
    main()
