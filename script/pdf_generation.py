from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

filename = 'process_developpement_app.pdf'

c = canvas.Canvas(filename, pagesize=A4)
width, height = A4

text = c.beginText(50, height - 50)
text.setFont('Helvetica-Bold', 16)
text.textLine("Processus de développement d'une application")

text.setFont('Helvetica', 11)
text.textLine("")

sections = [
    ("1. Idée, problème et objectifs", [
        "Définir le problème principal que l'application doit résoudre.",
        "Formuler les objectifs métiers (KPI, gains, valeur ajoutée).",
        "Réaliser un rapide benchmark des solutions existantes."]),
    ("2. Analyse et spécifications", [
        "Lister les besoins fonctionnels et non-fonctionnels.",
        "Rédiger un backlog ou cahier des charges simple (user stories).",
        "Définir le périmètre du MVP et les fonctionnalités futures."]),
    ("3. Design UX / UI et architecture", [
        "Dessiner les parcours utilisateurs et les écrans principaux.",
        "Créer des maquettes simples (wireframes) pour chaque écran.",
        "Choisir la stack technique (front, back, base de données, cloud)."]),
    ("4. Développement (implémentation)", [
        "Mettre en place le dépôt Git et l'environnement de dev.",
        "Coder les fonctionnalités par petites tâches (features).",
        "Écrire des tests unitaires et d'intégration de base."]),
    ("5. Tests et assurance qualité", [
        "Vérifier chaque fonctionnalité selon les scénarios définis.",
        "Corriger les bugs et améliorer l'expérience utilisateur.",
        "Faire tester une version beta par quelques utilisateurs."]),
    ("6. Déploiement et mise en production", [
        "Préparer l'infrastructure (serveur, hébergement, base de données).",
        "Automatiser autant que possible le déploiement.",
        "Mettre en place le monitoring (logs, erreurs, performances)."]),
    ("7. Maintenance, monitoring et évolutions", [
        "Suivre les métriques d'usage et de performance.",
        "Corriger les bugs et mettre à jour les dépendances.",
        "Planifier les évolutions en fonction des retours utilisateurs."])
]

for title, bullets in sections:
    text.textLine("")
    text.setFont('Helvetica-Bold', 12)
    text.textLine(title)
    text.setFont('Helvetica', 11)
    for b in bullets:
        text.textLine(f"- {b}")

c.drawText(text)
c.showPage()
c.save()

filename