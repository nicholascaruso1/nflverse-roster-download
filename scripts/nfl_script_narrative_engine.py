#!/usr/bin/env python3
"""NFL Script & Narrative Engine v1.0.

Pregame-only descriptive discovery of gematria, calendar, schedule-record,
head-to-head, scoreline and optional roster-name relationships. Not a betting
model. All output is non-directional and preserves competing narratives.
"""
from __future__ import annotations
import argparse, json, re
from datetime import date, datetime
from pathlib import Path
import pandas as pd

NICK = {
"ARI":"CARDINALS","ATL":"FALCONS","BAL":"RAVENS","BUF":"BILLS","CAR":"PANTHERS",
"CHI":"BEARS","CIN":"BENGALS","CLE":"BROWNS","DAL":"COWBOYS","DEN":"BRONCOS",
"DET":"LIONS","GB":"PACKERS","HOU":"TEXANS","IND":"COLTS","JAX":"JAGUARS",
"KC":"CHIEFS","LV":"RAIDERS","LAC":"CHARGERS","LA":"RAMS","MIA":"DOLPHINS",
"MIN":"VIKINGS","NE":"PATRIOTS","NO":"SAINTS","NYG":"GIANTS","NYJ":"JETS",
"PHI":"EAGLES","PIT":"STEELERS","SF":"FORTY NINERS","SEA":"SEAHAWKS",
"TB":"BUCCANEERS","TEN":"TITANS","WAS":"COMMANDERS"}
CITY = {
"ARI":"ARIZONA","ATL":"ATLANTA","BAL":"BALTIMORE","BUF":"BUFFALO",
"CAR":"CAROLINA","CHI":"CHICAGO","CIN":"CINCINNATI","CLE":"CLEVELAND",
"DAL":"DALLAS","DEN":"DENVER","DET":"DETROIT","GB":"GREEN BAY",
"HOU":"HOUSTON","IND":"INDIANAPOLIS","JAX":"JACKSONVILLE","KC":"KANSAS CITY",
"LV":"LAS VEGAS","LAC":"LOS ANGELES","LA":"LOS ANGELES","MIA":"MIAMI",
"MIN":"MINNESOTA","NE":"NEW ENGLAND","NO":"NEW ORLEANS","NYG":"NEW YORK",
"NYJ":"NEW YORK","PHI":"PHILADELPHIA","PIT":"PITTSBURGH",
"SF":"SAN FRANCISCO","SEA":"SEATTLE","TB":"TAMPA BAY","TEN":"TENNESSEE",
"WAS":"WASHINGTON"}
FULL = {
"ARI":"Arizona Cardinals","ATL":"Atlanta Falcons","BAL":"Baltimore Ravens",
"BUF":"Buffalo Bills","CAR":"Carolina Panthers","CHI":"Chicago Bears",
"CIN":"Cincinnati Bengals","CLE":"Cleveland Browns","DAL":"Dallas Cowboys",
"DEN":"Denver Broncos","DET":"Detroit Lions","GB":"Green Bay Packers",
"HOU":"Houston Texans","IND":"Indianapolis Colts","JAX":"Jacksonville Jaguars",
"KC":"Kansas City Chiefs","LV":"Las Vegas Raiders","LAC":"Los Angeles Chargers",
"LA":"Los Angeles Rams","MIA":"Miami Dolphins","MIN":"Minnesota Vikings",
"NE":"New England Patriots","NO":"New Orleans Saints","NYG":"New York Giants",
"NYJ":"New York Jets","PHI":"Philadelphia Eagles","PIT":"Pittsburgh Steelers",
"SF":"San Francisco 49ers","SEA":"Seattle Seahawks","TB":"Tampa Bay Buccaneers",
"TEN":"Tennessee Titans","WAS":"Washington Commanders"}

def letters(value):
    return re.sub(r"[^A-Z]", "", str(value).upper())

def digital_root(value):
    value = abs(int(value))
    return 0 if value == 0 else 1 + (value - 1) % 9

def ciphers(value):
    nums = [ord(ch)-64 for ch in letters(value)]
    ordinal = sum(nums)
    reverse = sum(27-n for n in nums)
    pyth = sum(((n-1) % 9)+1 for n in nums)
    return {"ordinal":ordinal,"ordinal_root":digital_root(ordinal),
            "reverse_ordinal":reverse,"reverse_root":digital_root(reverse),
            "pythagorean":pyth,"pythagorean_root":digital_root(pyth),
            "letters":len(nums)}

def team_record(frame, team):
    w=l=t=0
    for row in frame.itertuples(index=False):
        if team == row.away_team: own,opp=row.away_score,row.home_score
        elif team == row.home_team: own,opp=row.home_score,row.away_score
        else: continue
        if pd.isna(own) or pd.isna(opp): continue
        if own>opp: w+=1
        elif own<opp: l+=1
        else: t+=1
    return {"wins":w,"losses":l,"ties":t,"games":w+l+t,"record":f"{w}-{l}-{t}"}

def team_games(frame, team):
    return frame[(frame.away_team==team)|(frame.home_team==team)]

def last_result_date(frame, team, result):
    rows=team_games(frame,team).sort_values("gameday")
    for row in rows.iloc[::-1].itertuples(index=False):
        own,opp=((row.away_score,row.home_score) if row.away_team==team
                 else (row.home_score,row.away_score))
        if ((result=="win" and own>opp) or (result=="loss" and own<opp)
            or (result=="tie" and own==opp)):
            return row.gameday
    return None

def load_games(path, target):
    frame=pd.read_csv(path,low_memory=False)
    required={"game_id","season","game_type","week","gameday","gametime",
              "away_team","away_score","home_team","home_score"}
    missing=required-set(frame.columns)
    if missing: raise ValueError(f"games.csv missing required columns: {sorted(missing)}")
    frame["gameday"]=pd.to_datetime(frame.gameday,errors="coerce").dt.date
    frame=frame[frame.gameday.notna() & (frame.gameday<target)].copy()
    frame=frame[frame.away_score.notna() & frame.home_score.notna()].copy()
    frame["season"]=pd.to_numeric(frame.season,errors="coerce")
    frame["week"]=pd.to_numeric(frame.week,errors="coerce")
    frame["gametime"]=frame.gametime.fillna("").astype(str)
    frame["weekday"]=frame.gameday.map(lambda d:d.strftime("%A"))
    return frame

def hour(value):
    try: return int(str(value).split(":")[0])
    except (TypeError,ValueError): return None

def run(args):
    target=date.fromisoformat(args.date)
    away,home=args.away.upper(),args.home.upper()
    if away not in NICK or home not in NICK or away==home:
        raise ValueError("Supply two different valid nflverse team codes.")
    history=load_games(args.games,target)
    regular=history[history.game_type.eq("REG")].copy()
    season_games=regular[regular.season.eq(target.year)]
    records={t:team_record(season_games,t) for t in (away,home)}
    week=args.week
    if week is None:
        raw=pd.read_csv(args.games,usecols=["season","week","gameday","away_team","home_team"])
        match=raw[(raw.gameday.astype(str)==target.isoformat()) &
                  (raw.away_team==away)&(raw.home_team==home)]
        if len(match): week=int(match.iloc[0].week)
    findings=[]
    def add(category,label,value,caveat):
        findings.append({"category":category,"finding":label,"value":str(value),"caveat":caveat})
    context={"engine":"NFL Script & Narrative Engine","version":"1.0",
      "frozen_at":datetime.now().astimezone().isoformat(timespec="seconds"),
      "target_date":target.isoformat(),"away":away,"home":home,"week":week,
      "historical_cutoff_exclusive":target.isoformat(),
      "data_scope":{"completed_regular_season_games":len(regular),
        "first_game":str(regular.gameday.min()),"last_game":str(regular.gameday.max())},
      "governance":["Target-date and later results are excluded.",
        "No odds, market prices, or market-implied probabilities are used.",
        "All narrative clusters are descriptive and non-directional.",
        "Cipher variants are dependent, not independent evidence.",
        "Thursday kickoff-time proxies are not verified TNF broadcast records.",
        "Historical frequencies are descriptive and in-sample."],
      "season_records_before_game":records}
    if (records[away]["wins"]==records[home]["losses"] and
        records[away]["losses"]==records[home]["wins"] and
        records[away]["ties"]==records[home]["ties"]):
        add("records","Mirrored current-season records",
            f"{away} {records[away]['record']} / {home} {records[home]['record']}",
            "Descriptive symmetry; not a winner prediction.")
    thursdays=regular[regular.weekday.eq("Thursday")]
    for team in (away,home):
        all_thu=team_games(thursdays,team)
        night=all_thu[all_thu.gametime.map(hour).fillna(0)>=19]
        add("schedule_records",f"{team} all-Thursday record",
            team_record(all_thu,team)["record"],
            "Includes all Thursday regular-season games; not branded TNF.")
        add("schedule_records",f"{team} Thursday kickoff >= 7 PM proxy",
            team_record(night,team)["record"],
            "Schedule-time proxy only; branded TNF membership not verified.")
        last_win=last_result_date(all_thu,team,"win")
        if last_win:
            add("calendar",f"{team} elapsed time since last Thursday win",
                f"{(target-last_win).days} days; {(target.year-last_win.year)*12+target.month-last_win.month} calendar months",
                f"Last qualifying Thursday win: {last_win}.")
    h2h=regular[((regular.away_team==away)&(regular.home_team==home))|
                ((regular.away_team==home)&(regular.home_team==away))].sort_values("gameday")
    context["head_to_head"]={away:team_record(h2h,away),home:team_record(h2h,home),"games":len(h2h)}
    if len(h2h):
        prev=h2h.iloc[-1]
        context["previous_meeting"]={"date":str(prev.gameday),"away":prev.away_team,
          "away_score":int(prev.away_score),"home":prev.home_team,"home_score":int(prev.home_score)}
        if prev.away_score==prev.home_score:
            add("head_to_head","Previous meeting was tied",
                f"{int(prev.away_score)}-{int(prev.home_score)} on {prev.gameday}",
                "Historical context only; not a rematch prediction.")
    remaining=(date(target.year,12,31)-target).days
    digit_sum=sum(int(ch) for ch in target.strftime("%Y%m%d"))
    add("calendar","Days remaining in year, excluding game date",remaining,
        "December 31 minus target date.")
    add("calendar","Date digit sum / digital root",
        f"{digit_sum}/{digital_root(digit_sum)}","Date format YYYYMMDD.")
    add("calendar","Weekday number / root",
        f"{target.isoweekday()}/{digital_root(target.isoweekday())}",
        "ISO weekday: Monday=1 through Sunday=7.")
    team_values={}
    for team in (away,home):
        team_values[team]={"city":ciphers(CITY[team]),"nickname":ciphers(NICK[team]),
                           "full_identity":ciphers(FULL[team])}
        add("gematria",f"{team} city Pythagorean sum",
            team_values[team]["city"]["pythagorean"],
            "City name; distinct from nickname and full identity.")
        add("gematria",f"{team} nickname Pythagorean sum",
            team_values[team]["nickname"]["pythagorean"],
            "Nickname only; distinct from city and full identity.")
    context["team_ciphers"]=team_values
    context["combined_nickname_ciphers"]=ciphers(NICK[away]+" "+NICK[home])
    n=len(regular)
    score27=int((regular.away_score.eq(27)|regular.home_score.eq(27)).sum())
    ties=int(regular.away_score.eq(regular.home_score).sum())
    tie2727=int((regular.away_score.eq(27)&regular.home_score.eq(27)).sum())
    total54=int((regular.away_score+regular.home_score).eq(54).sum())
    context["scoreline_base_rates"]={"games":n,"either_team_27":score27,
      "either_team_27_rate":score27/n if n else None,"ties":ties,
      "tie_rate":ties/n if n else None,"exact_27_27":tie2727,
      "exact_27_27_rate":tie2727/n if n else None,"total_54":total54,
      "total_54_rate":total54/n if n else None}
    add("base_rates","Historical exact 27-27 frequency",
        f"{tie2727}/{n} ({tie2727/n:.3%})" if n else "n/a",
        "Completed regular-season games in supplied schedule file.")
    add("base_rates","Historical total-54 frequency",
        f"{total54}/{n} ({total54/n:.3%})" if n else "n/a",
        "Completed regular-season games; descriptive only.")
    for team in (away,home):
        for result in ("win","loss"):
            d=last_result_date(regular,team,result)
            if d: add("streaks",f"Days since {team} last {result}",(target-d).days,
                      f"Last {result}: {d}; target date excluded.")
    player_matches=[]
    if args.rosters and week is not None:
        roster_path=args.rosters/f"roster_weekly_{target.year}.csv"
        if roster_path.exists():
            roster=pd.read_csv(roster_path,low_memory=False)
            roster["season"]=pd.to_numeric(roster.season,errors="coerce")
            roster["week"]=pd.to_numeric(roster.week,errors="coerce")
            weeks=sorted(roster.loc[(roster.season==target.year)&(roster.week<=week),"week"].dropna().unique())
            snapshot=int(weeks[-1]) if weeks else None
            context["roster_snapshot_week"]=snapshot
            context["roster_snapshot_caveat"]="Latest weekly roster at or before target week; not official game-day inactives."
            if snapshot is not None:
                roster=roster[(roster.season==target.year)&(roster.week==snapshot)]
                if "status" in roster: roster=roster[roster.status.astype(str).str.upper().eq("ACT")]
                for opponent,player_team in ((away,home),(home,away)):
                    target_cipher=ciphers(NICK[opponent])
                    for row in roster[roster.team.eq(player_team)].itertuples():
                        name=getattr(row,"full_name",None)
                        if not name or pd.isna(name): continue
                        cv=ciphers(name)
                        exact=[k for k in ("ordinal","reverse_ordinal","pythagorean") if cv[k]==target_cipher[k]]
                        roots=[k for k in ("ordinal_root","reverse_root","pythagorean_root") if cv[k]==target_cipher[k]]
                        if exact or roots:
                            player_matches.append({"player":name,"team":player_team,
                              "opponent_nickname":NICK[opponent],"exact_systems":exact,"root_systems":roots})
    context["player_name_matches"]=player_matches
    for item in player_matches:
        if item["exact_systems"]:
            add("player_names",f'{item["player"]} matches {item["opponent_nickname"]}',
                ",".join(item["exact_systems"]),"Name-value match only; no player-performance inference.")
    if args.claimed_away_tnf_record or args.claimed_home_tnf_record:
        claims={away:args.claimed_away_tnf_record,home:args.claimed_home_tnf_record}
        context["external_tnf_claims"]={k:v for k,v in claims.items() if v}
        for team,claim in claims.items():
            if claim:
                proxy=team_record(team_games(thursdays[thursdays.gametime.map(hour).fillna(0)>=19],team),team)["record"]
                add("claim_audit",f"{team} external TNF claim vs Thursday-night proxy",
                    f"claimed {claim}; proxy {proxy}",
                    "Schedule data does not verify branded TNF broadcast membership.")
    out=args.output
    out.mkdir(parents=True,exist_ok=True)
    pd.DataFrame(findings).to_csv(out/"findings.csv",index=False)
    (out/"frozen_context.json").write_text(json.dumps(context,indent=2,default=str))
    report=[f"# NFL Script & Narrative Engine v1.0 — {away} @ {home}","",
      f"**Target:** {target.isoformat()} | **Week:** {week} | **Frozen:** {context['frozen_at']}","",
      "## Governance","- Pregame cutoff excludes target-date and later results.",
      "- Descriptive research only; no betting recommendation.",
      "- Thursday kickoff-time proxy is not verified TNF membership.",
      "- Cipher variants are dependent, not independent confirmations.","",
      "## Current records",f"- {away}: {records[away]['record']}",
      f"- {home}: {records[home]['record']}","","## Findings",
      "| Category | Finding | Value | Caveat |","|---|---|---|---|"]
    for item in findings:
        report.append("| "+" | ".join(str(item[k]).replace("|","/") for k in
                      ("category","finding","value","caveat"))+" |")
    report += ["","## Interpretation",
      "Do not select the narrative with the most matches. Report both sides.",
      "Historical frequencies are descriptive and in-sample, not predictive.",
      "Predictive evaluation requires preregistration and chronological holdout testing."]
    (out/"report.md").write_text("\n".join(report)+"\n")
    return context,findings

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--games",type=Path,required=True)
    parser.add_argument("--date",required=True,help="Target game date YYYY-MM-DD")
    parser.add_argument("--away",required=True)
    parser.add_argument("--home",required=True)
    parser.add_argument("--week",type=int)
    parser.add_argument("--rosters",type=Path)
    parser.add_argument("--claimed-away-tnf-record")
    parser.add_argument("--claimed-home-tnf-record")
    parser.add_argument("--output",type=Path,default=Path("narrative_output"))
    run(parser.parse_args())

if __name__=="__main__":
    main()
