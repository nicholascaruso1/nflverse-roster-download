import pandas as pd, numpy as np
df=pd.read_pickle('board.pkl')
p=pd.read_parquet('/home/claude/data/play_by_play_2026.parquet')
q=p[(p.play_type.isin(['pass','run']))&(p.two_point_attempt==0)]
rows=[]
for t in ['SEA','LV','LA','ARI','SF','DAL']:
    o=q[q.posteam==t]; d=q[q.defteam==t]; g=o.game_id.nunique()
    pa=o[(o.pass_attempt==1)&(o.qb_spike==0)]; ra=o[(o.rush_attempt==1)&(o.qb_kneel==0)]
    rows.append((t,o.epa.mean(),d.epa.mean(),len(pa)/g,len(ra)/g,g))
ctx=pd.DataFrame(rows,columns=['t','oepa','depa','pa','ra','g'])
exec(open('/home/claude/work/model.py').read().split('# ---------- roster')[0])
ctxs=''.join(f"| {r.t} | {r.oepa:+.3f} | {r.depa:+.3f} | {r.pa:.1f} | {r.ra:.1f} | {opp_ypc[r.t]:.2f} | {opp_ypa[r.t]:.2f} |\n" for r in ctx.itertuples())
def fmt_inputs(r):
    if r.mkt=='rec': return f"tgtEW {r.mu:.1f} catch {r.catch:.2f} g={int(r.g)}"
    if r.mkt=='rush': return f"carEW {r.mu:.1f} ypc {r.ypc:.2f} adj x{r.adj:.3f} g={int(r.g)}"
    if r.mkt=='pass': return f"attEW {r.mu:.1f} ypa {r.ypa:.2f} adj x{r.adj:.3f} g={int(r.g)}"
    return f"lambda {r.lam:.2f} ({r.pts:.2f} pts) g={int(r.g)}"
mk={'rec':'receptions','rush':'rush yds','pass':'pass yds','pass_td':'pass TD'}
def pr(x): return f"{int(x):+d}"
tab=[]
for r in df.sort_values(['game','team','mkt'],key=lambda s:s.map({'rec':0,'rush':1,'pass':2,'pass_td':3}) if s.name=='mkt' else s).itertuples():
    if r.side=='NA' or (isinstance(r.side,float)):
        tab.append(f"| {r.player} ({r.team}) | {mk[r.mkt]} | {r.line} | {pr(r.over) if r.over==r.over else 'n/a'} / {pr(r.under) if r.under==r.under else 'n/a'} | n/a | n/a | n/a | n/a | n/a | n/a | no usable sample, Level C |")
        continue
    tab.append(f"| {r.player} ({r.team}) | {mk[r.mkt]} | {r.line} | {pr(r.over)} / {pr(r.under)} | {r.p_over:.1f}% | {r.side} | {r.p_best:.1f}% | {r.be:.1f}% | {r.base_edge:+.1f} | {r.min_edge:+.1f} ({r.min_lab}) | {fmt_inputs(r)} |")
table='\n'.join(tab)
card=open('card_template.md').read().replace('{{CTX}}',ctxs).replace('{{TABLE}}',table)
open('week10-nfl-sun-4pm-prop-model-card.md','w').write(card)
print(len(card))
