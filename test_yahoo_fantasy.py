"""
Test di connessione alla lega Yahoo Fantasy NBA (ID 233219) con yfpy.

Setup:
  1) pip install yfpy python-dotenv
  2) Nella stessa cartella crea un file .env con:
       YAHOO_CONSUMER_KEY=il_tuo_client_id
       YAHOO_CONSUMER_SECRET=il_tuo_client_secret
  3) python test_yahoo_fantasy.py
     La prima volta si apre il browser: accedi a Yahoo, autorizza e incolla
     il codice di verifica nel terminale. Il token viene salvato nel .env.

NOTA: non ho potuto testare questo script. Se un metodo dà errore, copia
l'errore completo e mandamelo: i nomi dei metodi di yfpy possono cambiare
tra versioni.
"""
import os
from pathlib import Path

from dotenv import load_dotenv
from yfpy.query import YahooFantasySportsQuery

LEAGUE_ID = "233219"
MY_TEAM_ID = None  # dopo il primo run, metti qui il numero della tua squadra

load_dotenv()

query = YahooFantasySportsQuery(
    league_id=LEAGUE_ID,
    game_code="nba",
    yahoo_consumer_key=os.environ["YAHOO_CONSUMER_KEY"],
    yahoo_consumer_secret=os.environ["YAHOO_CONSUMER_SECRET"],
    env_file_location=Path("."),
    save_token_data_to_env_file=True,
)


def run(title, fn):
    print(f"\n=== {title} ===")
    try:
        print(fn())
    except Exception as exc:  # noqa: BLE001
        print(f"ERRORE: {type(exc).__name__}: {exc}")


run("Info lega", query.get_league_metadata)
run("Squadre", query.get_league_teams)
run("Classifica", query.get_league_standings)

if MY_TEAM_ID:
    run("Il mio roster", lambda: query.get_team_roster_player_info_by_week(MY_TEAM_ID))
else:
    print("\nImposta MY_TEAM_ID (numero della tua squadra tra quelle sopra) per vedere il roster.")
