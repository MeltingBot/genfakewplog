#!/usr/bin/env python3
import random
from datetime import datetime, timedelta
import ipaddress
import argparse

def generate_random_ip():
    """
    Génère une IP aléatoire valide (pas d'octet à 0)
    """
    octets = [random.randint(1, 255)]  # Premier octet non nul
    octets.extend(random.randint(1, 255) for _ in range(3))  # Autres octets non nuls
    return '.'.join(map(str, octets))



LEGITIMATE_USER_AGENTS = [
    # Chrome Windows
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    
    # Firefox Windows
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
    
    # Safari macOS
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15',
    
    # Chrome macOS
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_3_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    
    # Edge Windows
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.2365.66',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.2277.128',
    
    # Mobile Chrome (Android)
    'Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.64 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.64 Mobile Safari/537.36',
    
    # Mobile Safari (iOS)
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPad; CPU OS 17_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1',
    
    # Firefox Mobile
    'Mozilla/5.0 (Android 14; Mobile; rv:123.0) Gecko/123.0 Firefox/123.0',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/123.0 Mobile/15E148 Safari/605.1.15',
]

# User Agents pour la reconnaissance et le scan
RECON_USER_AGENTS = [
    # Outils de scan
    'Nmap Scripting Engine (https://nmap.org/book/nse.html)',
    'Nikto/2.1.6',
    'Nuclei - Open-source project (github.com/projectdiscovery/nuclei)',
    'masscan/1.0 (https://github.com/robertdavidgraham/masscan)',
    'Wappalyzer',
    'WPScan v3.8.22 (https://wpscan.org/)',
    
    # Bibliothèques et outils de développement
    'curl/7.88.1',
    'curl/8.4.0',
    'Wget/1.21.3',
    'Wget/1.21.4 (linux-gnu)',
    'Python-urllib/3.10',
    'Python-requests/2.31.0',
    'Go-http-client/1.1',
    'Go-http-client/2.0',
    'Apache-HttpClient/4.5.14 (Java/17.0)',
    'node-fetch/1.0 (+https://github.com/bitinn/node-fetch)',
    'axios/1.6.2',
    
    # Bots malveillants communs
    'Mozilla/5.0 (compatible; Baiduspider/2.0)',
    'Mozilla/5.0 (compatible; YandexBot/3.0)',
    'zgrab/0.x',
    'Expanse indexes the network perimeters of our customers.',
    'CheckHost (https://check-host.net/)',
    'fasthttp',
    
    # Scripts personnalisés
    'Python-httpx/0.24.1',
    'shellshock-scan',
    'sqlmap/1.7.2#stable',
    'Drupal security Scanner',
    'CensysInspect/1.1',
    'NetSystemsResearch studies the availability of various services across the internet.',
]


def generate_wordpress_logs(start_date, end_date, attacker_ip, min_entries_per_day=1500):
    """
    Génère des logs WordPress avec des attaques d'une IP spécifique
    """
    logs = []
    current_date = start_date
    days_total = (end_date - start_date).days + 1
    entries_per_hour = max(int(min_entries_per_day/24), 65)
    random_legit_agents = random.sample(LEGITIMATE_USER_AGENTS, 5)  # 5 agents légitimes pour l'attaquant
    
    attack_events = [
        {
            'path': '/wp-admin/admin-ajax.php',
            'method': 'POST',
            'data': '?id="%20AND%205%3D0%20AND%20%28SELECT%206087%20FROM%20SELECT%20COUNT%28%2A%29%2CCONCAT%280x717a767071%2C%28SELECT%20%28ELT%285492%3D5492%2C1%29%29%29%2C0x71716b7671%2CFLOOR%28R AND%280%29%2CRAND%285346%29%29%29x%20FROM%20INFORMATION_SCHEMA.PLUGINS%20GROUP%20BY%20x%29a%29%20--%20-"}',
            'status': 200,
            'ua': random.choice(random_legit_agents)  # Assigner un UA légitime fixe pour chaque événement
        },
        {
            'path': '/index.php',
            'method': 'GET',
            'path_suffix': '?id=1%20AND%20(SELECT%209999%20FROM%20(SELECT%20SLEEP(5)))--',
            'data': '-',
            'status': 200,
            'ua': random.choice(random_legit_agents)  # Assigner un UA légitime fixe pour chaque événement
        },
        {
            'path': '/wp-admin/admin-ajax.php',
            'method': 'POST',
            'data': 'action=revslider_ajax_action&client_action=update_plugin%22+AND+extractvalue(1,concat(0x7e,(SELECT+@@version)))--',
            'status': 500,
            'ua': random.choice(random_legit_agents)  # Assigner un UA légitime fixe pour chaque événement
        },
        {
            'path': '/xmlrpc.php',
            'method': 'POST',
            'data': '<?xml version="1.0"?><methodCall><methodName>system.multicall</methodName></methodCall>',
            'status': 403,
            'ua': random.choice(random_legit_agents)  # Assigner un UA légitime fixe pour chaque événement
        },
        {
            'path': '/wp-comments-post.php',
            'method': 'POST',
            'data': 'comment=test&comment_post_ID=-1 UNION ALL SELECT NULL,NULL,NULL,NULL,NULL,NULL,(SELECT CONCAT(user_login,0x3a,user_pass) FROM wp_users WHERE ID=1),NULL#',
            'status': 500,
            'ua': random.choice(random_legit_agents)  # Assigner un UA légitime fixe pour chaque événement
        }
    ]

    normal_paths = [
        '/',
        '/about',
        '/contact',
        '/solutions',
        '/sitemap.xml',
        '/wp-content/uploads/2024/09/2024-09-17_09-50.png',
        '/wp-content/uploads/2024/09/antidrone-1.png',
        '/wp-content/themes/twentytwentyfour/style.css',
        '/wp-includes/js/jquery/jquery.min.js',
        '/technologies',
        '/news',
        '/wp-content/plugins/pagelayer/js/givejs.php?give=pagelayer-frontend.js%2Cnivo-lightbox.min.js%2Cwow.min.js%2Cjquery-numerator.js%2CsimpleParallax.min.js%2Cowl.carousel.min.js&amp;ver=1.8.9"',
	'/?p=98',
	'/wp-json/oembed/1.0/embed?url=https%3A%2F%2Fwww.aeroguard-technologies.eu%2Ftechnologies%2F&#038;format=xml',
    ]

    recon_paths = [
        '/wp-login.php',
        '/wp-admin/',
        '/wp-config.php',
        '/.env',
        '/wp-admin/install.php',
        '/wp-content/debug.log',
        '/wp-json/wp/v2/users'
    ]

    while current_date <= end_date:
        day_start = current_date.replace(hour=0, minute=0, second=0)
        day_end = current_date.replace(hour=23, minute=59, second=59)
        
        # User agents fixes pour l'attaquant ce jour
        random_legit_agents = random.sample(LEGITIMATE_USER_AGENTS, 5)
        
        # Répartir les 5 attaques sur la journée
        attack_times = []
        for i in range(5):
            segment_start = day_start + timedelta(hours=i*4, minutes=30)  # 4h par segment, début après 30min
            segment_end = day_start + timedelta(hours=(i+1)*4, minutes=-30)  # fin 30min avant
            attack_time = segment_start + timedelta(
                seconds=random.randint(0, int((segment_end - segment_start).total_seconds()))
            )
            attack_times.append(attack_time)

        # Phase de reconnaissance au début de chaque jour
        recon_start = day_start + timedelta(minutes=random.randint(5, 20))
        recon_end = recon_start + timedelta(minutes=15)
        
        attacks_done = 0
        hour_entries = 0
        current_hour = current_date.hour
        
        # Génération des logs pour la journée
        while current_date <= day_end:
            timestamp = current_date.strftime("%d/%b/%Y:%H:%M:%S +0000")
            
            if attacks_done < 5 and current_date >= attack_times[attacks_done]:
                # Insertion d'une attaque
                event = attack_events[attacks_done]
                path = event['path']
                if 'path_suffix' in event:
                    path += event['path_suffix']
                
                log_entry = f'{attacker_ip} - - [{timestamp}] "{event["method"]} {path} HTTP/1.1" {event["status"]} {random.randint(500, 1500)} "-" "{random_legit_agents[attacks_done]}" "{event["data"]}"'
                logs.append(log_entry)
                attacks_done += 1
                hour_entries += 1
                
            elif recon_start <= current_date <= recon_end:
                # Reconnaissance avec IPs aléatoires
                ip = generate_random_ip()
                path = random.choice(recon_paths)
                log_entry = f'{ip} - - [{timestamp}] "GET {path} HTTP/1.1" {random.choice([403, 404,500])} {random.randint(200, 800)} "-" "{random.choice(RECON_USER_AGENTS)}" "-"'
                logs.append(log_entry)
                hour_entries += 1
                
            else:
                # Trafic normal
                ip = generate_random_ip()
                path = random.choice(normal_paths)
                log_entry = f'{ip} - - [{timestamp}] "GET {path} HTTP/1.1" {random.choice([200, 302])} {random.randint(1024, 102400)} "-" "{random.choice(LEGITIMATE_USER_AGENTS)}" "-"'
                logs.append(log_entry)
                hour_entries += 1
            
            current_date += timedelta(seconds=random.randint(1, 60))

            # Vérifier les entrées par heure
            if current_date.hour != current_hour:
                if hour_entries < entries_per_hour:
                    needed = entries_per_hour - hour_entries
                    for _ in range(needed):
                        ip = generate_random_ip()
                        path = random.choice(normal_paths)
                        timestamp = current_date.strftime("%d/%b/%Y:%H:%M:%S +0000")
                        log_entry = f'{ip} - - [{timestamp}] "GET {path} HTTP/1.1" 200 {random.randint(1024, 102400)} "-" "{random.choice(LEGITIMATE_USER_AGENTS)}" "-"'
                        logs.append(log_entry)
                current_hour = current_date.hour
                hour_entries = 0

        # Passer au jour suivant
        current_date = (current_date + timedelta(days=1)).replace(hour=0, minute=0, second=0)

    return logs

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Génère des logs WordPress avec une IP attaquante sur une période')
    parser.add_argument('start_date', help='Date de début (format: YYYY-MM-DD)')
    parser.add_argument('end_date', help='Date de fin (format: YYYY-MM-DD)')
    parser.add_argument('ip', help='IP de l\'attaquant')
    args = parser.parse_args()

    try:
        start_date = datetime.strptime(args.start_date, "%Y-%m-%d")
        end_date = datetime.strptime(args.end_date, "%Y-%m-%d")
        
        if end_date < start_date:
            raise ValueError("La date de fin doit être après la date de début")
        
        # Valider l'IP
        ipaddress.ip_address(args.ip)
        
        logs = generate_wordpress_logs(start_date, end_date, args.ip)
        
        # Nom de fichier avec période
        filename = f"wordpress_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.log"
        
        with open(filename, 'w') as f:
            for log in logs:
                f.write(log + '\n')
        
        # Vérification des attaques
        days_count = (end_date - start_date).days + 1
        attack_count = sum(1 for log in logs if args.ip in log)
        expected_attacks = 5 * days_count
        
        print(f"Fichier généré : {filename}")
        print(f"Période : {args.start_date} à {args.end_date} ({days_count} jours)")
        print(f"Nombre total de lignes : {len(logs)}")
        print(f"Nombre d'attaques de l'IP {args.ip} : {attack_count}/{expected_attacks} ({attack_count/days_count:.1f} par jour)")

    except ValueError as e:
        print(f"Erreur : {str(e)}")
        print("Usage : python3 script.py YYYY-MM-DD YYYY-MM-DD IP")
        print("Exemple : python3 script.py 2024-03-15 2024-03-17 45.33.22.211")
