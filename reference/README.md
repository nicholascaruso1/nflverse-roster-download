# Reference data

## team_identity_eras.csv
Era-aware franchise identity table. Three separate dimensions:

| Column | Meaning |
|---|---|
| `franchise_id` | Franchise continuity key (the *current* nflverse code, e.g. `LV` for the Oakland/Las Vegas Raiders). |
| `code`, `season_start`, `season_end` | nflverse schedule code used in that NFL-season range (e.g. `OAK` 1999-2019, `LV` 2020+). |
| `city`, `nickname` | Historical city/market and nickname in effect for that season range. |
| `display_name` | Human-readable full name (e.g. "San Francisco 49ers"). Never used for ciphers. |

Cipher policy: the "full identity" string is always `city + " " + nickname` using the spelled-out
nickname (`Forty Niners`), so full identity, city, and nickname are mutually consistent. The digits in
"49ers" are never silently dropped. Historical identity is primary; current identity is a separate
comparison field and never overwrites it.

## tnf_broadcast_games.csv
Branded Thursday Night Football broadcast table. **Intentionally empty (header only) in v1.0.1.**
The engine counts a game as branded TNF only when a row has `tnf_brand_status = branded_tnf` AND
`verification_status = verified` AND a `source_url`. Thursday kickoff times and all-Thursday games are
never substituted. Thanksgiving games, Saturday games, Sunday prime-time games and ordinary Thursday
games must not be entered as branded TNF.
