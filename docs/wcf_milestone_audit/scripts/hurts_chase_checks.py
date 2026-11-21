"""Part 4 recompute (Hurts 10/11, Chase 11/1). Inputs hand-transcribed from NFL.com log/career pages
(retrieved 2026-11-20 via a page-to-text summarizer; raw HTML not archived). See data/ CSV extracts. python3 -I"""
import csv,sys
from datetime import date
def L(x): return [ord(c)-64 for c in x.upper() if c.isalpha()]
red=lambda n:(n-1)%9+1
ordn=lambda x:sum(L(x)); pyth=lambda x:sum(red(v) for v in L(x)); rrev=lambda x:sum(red(27-v) for v in L(x))
for w in ["United Kingdom","Philadelphia","Ja'Marr Chase","Touchdown","Titans","Football"]:
    print(f"{w:16s} Ord {ordn(w):4d} Red {pyth(w):3d} RevRed {rrev(w):3d} Rev {sum(27-v for v in L(w))}")
# Hurts
hurts_career={2020:3,2021:10,2022:13,2023:15,2024:14,2025:8,2026:1}
print("Hurts reg-season rush TD career table sum:",sum(hurts_career.values()),"(2026 TD = 9/28 @CHI only; 10/4 and 10/11 rows 0)")
print("Hurts 2024 postseason rush TDs (not in career table):",1+3+1)
print("Hurts 11/3/2024 -> 10/11/2026 days",(date(2026,10,11)-date(2024,11,3)).days,"weeks",(date(2026,10,11)-date(2024,11,3)).days/7)
print("Hurts DOB 8/7/1998 (workbook source, not re-fetched) -> 10/11/2026 days",(date(2026,10,11)-date(2026,8,7)).days)
# Chase
rows={}
for y,f in [(2021,"2021"),(2022,"2022"),(2023,"2023"),(2024,"2024"),(2025,"2025"),(2026,"2026")]: pass
chase_tds={2021:13,2022:9,2023:7,2024:17,2025:8}
print("Chase TD thru 2025:",sum(chase_tds.values()),"+2026 pregame(2+1+1+1)=",sum(chase_tds.values())+5)
home_rows={2021:9,2022:7,2023:9,2024:8,2025:8}
home_played_low={2021:9,2022:6,2023:8,2024:8,2025:8}   # 2022 Panthers row 'Not listed'; 2023 17 rows vs GP 16 -> one home row may be DNP
home_played_hi={2021:9,2022:6,2023:9,2024:8,2025:8}
print("Chase home games thru 2025: rows",sum(home_rows.values()),"played range",sum(home_played_low.values()),"-",sum(home_played_hi.values()),"(workbook/StatMuse 40)")
print("+2026 pregame home (TB 9/13, JAX 10/4)=2 -> Titans 11/1 is #",sum(home_played_low.values())+3,"to #",sum(home_played_hi.values())+3)
print("Chase 9/20->11/1",(date(2026,11,1)-date(2026,9,20)).days,"| 1/4/2026->11/1",(date(2026,11,1)-date(2026,1,4)).days,(date(2026,11,1)-date(2026,1,4)).days/7)
print("Chase DOB 3/1/2000 (workbook source) -> next bday days",(date(2027,3,1)-date(2026,11,1)).days)
