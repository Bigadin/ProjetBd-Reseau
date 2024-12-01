action_codes = {
    2333: "Ouvrir la porte",
    2433: "Bloquer la porte",
    2533: "Ouvrir la borne",
    2633: "Fermer la borne"
}

success_codes = {
    100: "OK/Opération effectuée avec succès sans problèmes",
    101: "Informations stockées dans la base de données",
    102: "Succès mais traitement toujours en cours"
}

client_error_codes = {
    201: "La requête est mal fournie (exemple : carte endommagée)",
    202: "Pas autorisé (carte invalide)",
    203: "Date d’expiration atteinte",
    204: "Utilisateur introuvable",
    205: "Vous avez deja validier"
}

server_error_codes = {
    301: "Erreur inattendue du serveur",
    302: "Le serveur est temporairement en panne",
    303: "Le serveur n’existe plus"
}

borne_error_codes = {
    401: "Borne introuvable",
    402: "Station liée à la borne introuvable",
    403: "Borne en maintenance",
    404: "Borne en arrêt ",
    405: "Station fermée"
}