from playwright.sync_api import sync_playwright

def watch_js_activity(url):
    logs = []
    popups = []
    requests = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Log tt tes mort
        page.on("console", lambda msg: logs.append(msg.text))
        # popup
        page.on("popup", lambda popup: popups.append("Popup ouverte"))
        # et pour le reseau
        page.on("request", lambda req: requests.append(req.url))

        try:
            page.goto(url, timeout=15000)
            page.wait_for_timeout(5000)  # ça attend l'execution du JS
        except Exception as e:
            logs.append(f"Erreur de chargement: {e}")
        
        browser.close()

    return {
        "logs": logs,
        "popups": popups,
        "requests": requests
    }
