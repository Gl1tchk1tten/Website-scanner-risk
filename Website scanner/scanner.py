import requests
from bs4 import BeautifulSoup
import tldextract
from js_watcher import watch_js_activity  

def scan_website(url):
    report = {
        "external_links": [],
        "js_scripts": [],
        "redirects": [],
        "risk_score": 0,
        "reasons": []
    }

    try:
        r = requests.get(url, timeout=10)
    except Exception as e:
        report["reasons"].append("Erreur lors de la connexion au site.")
        return report

    soup = BeautifulSoup(r.text, "html.parser")
    domain_name = tldextract.extract(url).domain

    # zerma pour les lien extern
    for a in soup.find_all("a", href=True):
        href = a['href']
        if href.startswith("http") and domain_name not in href:
            report["external_links"].append(href)

    # la meme mais pour les script
    for script in soup.find_all("script", src=True):
        src = script['src']
        if domain_name not in src:
            report["js_scripts"].append(src)

    # ça redirige
    if "meta http-equiv=\"refresh\"" in r.text.lower() or "window.location" in r.text.lower():
        report["redirects"].append("Possibly JS or meta redirect")

    # analyse dinamique
    js_data = watch_js_activity(url)
    report["popup_detected"] = bool(js_data["popups"])

    # Analyse des logs JS chelou
    sus_keywords = ["eval", "document.write", "atob", "new Function", "setTimeout(", "setInterval(", "location.href"]
    if any(any(k in log for k in sus_keywords) for log in js_data["logs"]):
        report["reasons"].append("Comportement JS potentiellement dangereux détecté.")
        report["risk_score"] += 20

    # popup
    if js_data["popups"]:
        report["reasons"].append("Popup détectée via JavaScript.")
        report["risk_score"] += 15

    # réseau
    if len(js_data["requests"]) > 10:
        report["reasons"].append("Nombre élevé de requêtes JS.")
        report["risk_score"] += 10

    # trop de liens
    if len(report["external_links"]) > 5:
        report["reasons"].append("Nombre élevé de liens externes.")
        report["risk_score"] += 20

    # trop de scripts
    if len(report["js_scripts"]) > 3:
        report["reasons"].append("Scripts JS externes suspects.")
        report["risk_score"] += 25

    # redirection
    if len(report["redirects"]) > 0:
        report["reasons"].append("Présence de redirection automatique.")
        report["risk_score"] += 10

    if len(report["reasons"]) == 0:
        report["reasons"].append("Aucun comportement dangereux évident détecté.")

    report["risk_score"] = min(report["risk_score"], 100)
    return report
