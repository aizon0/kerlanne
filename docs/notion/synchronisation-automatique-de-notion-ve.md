---

---

# Synchronisation automatique de Notion vers Github

## Principe

La synchronisation est unidirectionnelle : Notion constitue la source de référence et le dépôt Git conserve une copie des pages au format Markdown.

```plain text
Pages Notion > Export Python > Fichiers markdown > Commit sur main
```

Un workflow Github Actions lance l’export selon une planification ou manuellement avec workflow_dispatch. Il récupère le dépôt, installe l’exporteur, lit les pages Notion, puis écrit les fichiers dans docs/notion/. Un commit est créé et poussé uniquement si des changements sont détectés.
Les modifications doivent être effectuées dans Notion : les changements apportés aux fichiers générés ne sont pas renvoyés vers Notion et peuvent être écrasés lors d’un prochain export.

## Exporteur et fork

L’export repose sur un fork de notion-git-sync, adapté pour permettre l’export de pages sans bloc YAML de métadonnées (appelé frontmatter).
Dans la version d’origine, une page sans frontmatter reconnu était ignorée, même avec required_frontmatter=set(). Le fork modifie ce comportement :

* Une page sans frontmatter est exportée normalement.
* Un frontmatter valide est conservé en tête du fichier Markdown.
* Le bloc YAML reconnu est retiré du corps du document pour éviter sa duplication.
* Le nom du fichier reste fondé sur le titre de la page Notion.

Les modifications sont conservées dans le fork plutôt que dans .venv. Le workflow installe une révision précise du fork, identifiée par son hash de commit, afin de maîtriser la version exécutée.

## Accès à Notion

Une connexion interne Notion, disposant de la capacité Read content, permet de lire les pages explicitement partagées avec elle.
Le workflow utilise deux secrets :


| Secret           | Rôle                                        |
| ---------------- | ------------------------------------------- |
| NOTION_TOKEN     | Authentifier les requêtes vers l’API Notion |
| NOTION_PARENT_ID | Identifier la page parente à parcourir      |


Les identifiants sont les UUID des pages, et non leurs titres ou leurs URL complètes.

## Github App et branche protégée

Une GitHub App dédiée permet au workflow de publier sur main sans désactiver sa protection.
L’application est installée uniquement sur le dépôt concerné, avec la permission Contents: Read and write. Elle figure dans la liste de contournement du ruleset applicable à main, en mode Always allow, pour autoriser les pushes directs.
Le workflow utilise :


| Configuration                 | Rôle                                       |
| ----------------------------- | ------------------------------------------ |
| Variable EXPORT_APP_CLIENT_ID | Identifier l’application                   |
| Secret EXPORT_APP_PRIVATE_KEY | Générer un jeton d’installation temporaire |


Ce jeton est transmis à l’étape de checkout, puis utilisé pour authentifier le push. Le nom d’auteur du commit ne donne aucun droit supplémentaire.
L’autorisation de contournement appartient à l’application, pas à un fichier de workflow particulier. Sa clé privée doit donc rester accessible uniquement à du code de confiance.

## Points de vigilance

* Ne pas modifier manuellement les fichiers générés dans docs/notion/.
* Vérifier le résultat après une modification du fork ou une mise à jour des dépendances.
* Tester les renommages, suppressions, liens et pièces jointes avant de considérer leur gestion comme garantie.
* Conserver, si possible, les interdictions de suppression et de force-push dans un ruleset distinct, sans contournement pour l’application.
