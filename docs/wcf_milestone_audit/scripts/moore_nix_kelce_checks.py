"""Recomputation for WCF audit part 3 (Moore, Nix, Kelce). Inputs were hand-transcribed by the
auditor from NFL.com game-log pages retrieved 2026-11-20 (raw pages are NOT stored here).
CAVEAT: Moore opponent lists could not be re-verified in this pass (2019/2020 log re-fetch returned an
unrendered template) and the 2019 list has 16 rows vs 15 GP on the career table, so the AFC count
is provisional. Run: python3 -I this_file"""
from datetime import date
AFC = {"Bills","Dolphins","Patriots","Jets","Ravens","Bengals","Browns","Steelers","Texans","Colts","Jaguars","Titans","Broncos","Chiefs","Raiders","Chargers"}
# DJ Moore regular-season opponents with a stat row (NFL.com logs); '@' prefixes dropped
moore = {
 2018:"Cowboys Falcons Bengals Giants Redskins Eagles Ravens Buccaneers Steelers Lions Seahawks Buccaneers Browns Saints Falcons Saints",
 2019:"Saints Colts Seahawks Falcons Redskins Saints Falcons Packers Titans 49ers Buccaneers Jaguars Texans Cardinals Buccaneers Rams",
 2020:"Saints FootballTeam Packers Vikings Lions Buccaneers Chiefs Falcons Saints Bears Falcons Cardinals Chargers Buccaneers Raiders",
 2021:"Jets Saints Texans Cowboys Eagles Vikings Giants Falcons Patriots Cardinals FootballTeam Dolphins Falcons Bills Buccaneers Saints Buccaneers",
 2022:"Saints Buccaneers Lions Steelers Seahawks Broncos Ravens Falcons Bengals Falcons Buccaneers Rams 49ers Cardinals Saints Giants Browns",
 2023:"Packers Falcons Cardinals Browns Lions Vikings Lions Panthers Saints Chargers Raiders Vikings Commanders Broncos Chiefs Buccaneers Packers",
 2024:"Packers Seahawks Lions Vikings 49ers Lions Vikings Packers Patriots Cardinals Commanders Jaguars Panthers Rams Colts Texans Titans",
 2025:"Lions 49ers Packers Browns Packers Eagles Steelers Vikings Giants Bengals Ravens Saints Commanders Raiders Cowboys Lions Vikings",
}
tot=0
for y,s in moore.items():
    o=s.split(); n=sum(t in AFC for t in o); tot+=n; print("Moore",y,"rows",len(o),"AFC",n)
print("Moore AFC through 2025:",tot,"| 2026 pregame AFC (@HOU 9/13, LAC 9/27; Lions 9/17 is NFC):",2,"-> target (NE, 10/4) is #",tot+2+1)
print("Moore rec TD 2018-25:",2+4+4+4+7+8+6+6,"rush:",1+1,"reg-season total thru 2025:",41+2,"+2026 pregame(9/13 HOU)=",41+2+1)
print("Moore postseason TDs: 1/10/2026 GB 1, 1/18/2026 LAR 1 ->",2,"; combined pregame",44+2,"next",44+2+1)
print("Moore 1/18->10/4 days",(date(2026,10,4)-date(2026,1,18)).days,(date(2026,10,4)-date(2026,1,18)).days/7)
# Nix
reg_thru_2025=17+17; post=2; pre2026=5
print("Nix games before 10/15: reg",reg_thru_2025+pre2026,"incl post",reg_thru_2025+pre2026+post,"-> target #",reg_thru_2025+pre2026+post+1,"(reg-only #",reg_thru_2025+pre2026+1,")")
home_rush={"2024":2,"2025":3,"2026":1}
print("Nix home rushing TDs:",sum(home_rush.values()),"-> points",6*sum(home_rush.values()),"(TDs only; 2pt/other not checked)")
print("Nix 9/27->10/15",(date(2026,10,15)-date(2026,9,27)).days,"| 12/25/2025->10/15",(date(2026,10,15)-date(2025,12,25)).days,(date(2026,10,15)-date(2025,12,25)).days/7)
# Kelce
rec_thru_2025=5+5+4+8+10+5+11+9+12+5+3+5; rush=2; ret=1
print("Kelce rec thru 2025",rec_thru_2025)
for lab,v in [("receiving only",rec_thru_2025+2),("rec+rush",rec_thru_2025+rush+2),("rec+rush+return",rec_thru_2025+rush+ret+2)]:
    print("Kelce reg-season thru 10/18/2026",lab,v,"| +20 postseason receiving ->",v+20)
print("Workbook claim 82+3+2 =",82+3+2,"; NFL.com career rush total 3 includes 11/8/2026 TD")

# --- cipher + calendar rechecks (conventions: see audit-3 section 0) ---
def L(x): return [ord(c)-64 for c in x.upper() if c.isalpha()]
def red(n): return (n-1)%9+1
pyth=lambda x: sum(red(v) for v in L(x)); rrev=lambda x: sum(red(27-v) for v in L(x))
for w in ["Touchdown","New York","New England","Patriots","Seattle"]:
    print("cipher",w,"Reduction",pyth(w),"RevReduction",rrev(w))
d=date(2026,10,15); print("Oct 15 2026 weekday",d.strftime("%A"),"| Thursday number in 2026:",(d.timetuple().tm_yday-1)//7+1)
print("12/25/2025 weekday",date(2025,12,25).strftime("%A"))
print("Nix inclusive days 9/27..10/15:",(date(2026,10,15)-date(2026,9,27)).days+1)
