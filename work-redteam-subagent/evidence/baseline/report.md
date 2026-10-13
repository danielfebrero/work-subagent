# Audit limité — baseline

## Portée et identité

Dépôt demandé : `danielfebrero/work-subagent`, branche `test/baseline-20261013`, commit distant indiqué par le mandat : `e34f95ea9caab6beb4d8768d4c4969db25fb9958`.
L'audit porte sur la copie locale fournie. Le commit distant n'a pas été vérifié sur le réseau ; le commit Git local est distinct selon le mandat. Les empreintes des trois fichiers lus sont dans `source-sha256.json`.

## Constat unique — acceptation de constantes non JSON

**Priorité proposée : P2 (validation incorrecte).** Dans `auditlog.py:37`, `json.loads(line)` accepte les extensions Python `NaN`, `Infinity` et `-Infinity`. `validate_event` contrôle les champs obligatoires (`auditlog.py:15-27`) mais retourne ensuite l'objet avec ses champs supplémentaires (`auditlog.py:28`). Un champ supplémentaire contenant l'une de ces constantes permet donc à une ligne qui n'est pas du JSON valide d'être annoncée valide par la CLI (`auditlog.py:53-54`).

Le contrat `README.md:7-13` exige un objet JSON par ligne non vide, préserve les champs supplémentaires et prescrit un code de sortie 1 pour une entrée invalide. Cela affecte les consommateurs qui utilisent cette CLI comme porte de validation avant un parseur JSON strict : le succès du validateur ne garantit pas que le journal sera lisible par ce consommateur.

### Reproduction vérifiée

Les fichiers `nan.jsonl`, `infinity.jsonl`, `negative-infinity.jsonl` contiennent chacun un événement autrement valide, plus respectivement `"extra": NaN`, `"extra": Infinity` ou `"extra": -Infinity`.

```sh
python3 -m unittest discover -s tests -v
python3 auditlog.py audit-output/baseline/nan.jsonl
python3 auditlog.py audit-output/baseline/infinity.jsonl
python3 auditlog.py audit-output/baseline/negative-infinity.jsonl
```

Résultats réels : les 5 tests existants passent ; chacune des trois invocations CLI retourne **0**, stdout `{"valid": true, "events": 1}`, stderr vide. Le contrôle de parsing strict utilisant le paramètre standard `parse_constant` rejette le fichier NaN avec `ValueError: non-JSON numeric token: NaN` et retourne **1**. Sa commande exacte et sa sortie sont dans `strict-json-control.json`.

La couverture `tests/test_auditlog.py:12-30` comprend un JSON syntaxiquement cassé (`:25-27`), mais aucun cas de constante non JSON dans un champ supplémentaire. Ce manque explique pourquoi les tests restent verts malgré le constat.

### Suite recommandée, non appliquée

Rejeter les constantes non standard pendant le parsing JSON via `parse_constant`, puis ajouter une régression couvrant les trois constantes et vérifiant le message avec numéro de ligne ainsi que le code CLI 1. Aucun code du projet ni test existant n'a été corrigé.

## Preuves et limites

Les fichiers `*-cli.json`, `unit-tests.json` et `strict-json-control.json` conservent les tableaux argv, codes de sortie et stdout/stderr réellement capturés. `source-read.txt` conserve la lecture numérotée du contrat et du code ; `source-read-command.json` sa commande et ses sorties. `environment.json` documente la version Python et l'état local observés. `journal.jsonl` est un journal déclaratif horodaté des lectures/actions de cet audit, sans prétention à une trace interne exhaustive ou invisible. Les deux premières actions y ont été inscrites après l'inventaire initial ; leurs heures sont des heures de consignation.

Aucun accès aux secrets, aux fichiers personnels ou au réseau externe. Exécution limitée aux tests documentés et à des commandes locales explicites de reproduction et de collecte de preuves. Audit volontairement limité à ce constat, sans certification générale de sécurité.
