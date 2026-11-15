import pandas as pd, numpy as np, re, hashlib, json, sys, zlib
D='/home/claude/data/'
p=pd.read_parquet(D+'play_by_play_2026.parquet')
sn=pd.read_parquet(D+'snap_counts_2026.parquet')
ro_all=pd.read_parquet(D+'roster_2026.parquet')
ro=ro_all[ro_all.week==ro_all.week.max()].copy()
NSIM=40000
# ---------- league constants (weeks 1-10) ----------
rush=p[(p.rush_attempt==1)&(p.qb_kneel==0)&(p.two_point_attempt==0)].copy()
qbids=set(ro_all[ro_all.position=='QB'].gsis_id)
rush['isqb']=rush.rusher_player_id.isin(qbids)
LG_YPC=rush.yards_gained.mean(); LG_QB_YPC=rush[rush.isqb].yards_gained.mean()
db=p[(p.pass_attempt==1)&(p.qb_spike==0)&(p.two_point_attempt==0)].copy()   # dropbacks incl sacks (pilot definition)
LG_YPA=db.yards_gained.mean(); LG_YPA_GROSS=db.passing_yards.fillna(0).mean()
rush_emp=rush.yards_gained.values.astype(float); qbr_emp=rush[rush.isqb].yards_gained.values.astype(float)
pass_emp=db.yards_gained.values.astype(float); pass_emp_gross=db.passing_yards.fillna(0).values.astype(float)
opp_ypc=rush.groupby('defteam').yards_gained.mean(); opp_ypa=db.groupby('defteam').yards_gained.mean(); opp_ypa_g=db.groupby('defteam').passing_yards.apply(lambda s:s.fillna(0).mean())
pts=p.groupby('game_id').agg(h=('total_home_score','max'),a=('total_away_score','max')).sum().sum()
LAMBDA_PER_PT=db.pass_touchdown.sum()/pts
print('LG ypc %.3f qb %.3f ypa %.3f gross %.3f lam/pt %.4f'%(LG_YPC,LG_QB_YPC,LG_YPA,LG_YPA_GROSS,LAMBDA_PER_PT))
# ---------- roster/name mapping ----------
def norm(s): return re.sub(r'[^a-z ]','',re.sub(r'\b(jr|sr|ii|iii|iv)\b','',s.lower().replace('.','').replace("'",''))).strip()
ro['n']=ro.full_name.map(norm)
def find(name,team):
    n=norm(name); c=ro[(ro.team==team)&(ro.n==n)]
    if len(c)==0:
        ln=n.split()[-1]; c=ro[(ro.team==team)&(ro.n.str.split().str[-1]==ln)]
        if len(c)>1: c=c[c.n.str[0]==n[0]]
    if len(c)==0: raise KeyError((name,team))
    if len(c)>1: print('AMBIG',name,c[['full_name','position']].values.tolist()); c=c.iloc[:1]
    return c.iloc[0]
# ---------- per player-game logs ----------
snap=sn.merge(ro[['pfr_id','gsis_id']].drop_duplicates(),left_on='pfr_player_id',right_on='pfr_id',how='left')
def logs(gid,team):
    t=p[(p.posteam==team)]
    weeks=sorted(t.week.unique())
    # snaps
    s=snap[(snap.gsis_id==gid)&(snap.team==team)].groupby('week').offense_snaps.sum()
    tg=t[(t.pass_attempt==1)&(t.sack==0)&(t.two_point_attempt==0)&(t.receiver_player_id==gid)]
    rc=t[(t.rush_attempt==1)&(t.qb_kneel==0)&(t.two_point_attempt==0)&(t.rusher_player_id==gid)]
    pb=t[(t.pass_attempt==1)&(t.qb_spike==0)&(t.two_point_attempt==0)&(t.passer_player_id==gid)]
    rows=[]
    for w in weeks:
        a=tg[tg.week==w]; r=rc[rc.week==w]; q=pb[pb.week==w]
        sp=int(s.get(w,0))
        inv=len(a)+len(r)+len(q)
        if sp>0 or inv>0:
            rows.append(dict(week=w,snaps=sp,tgt=len(a),rec=int(a.complete_pass.sum()),recyd=float(a.receiving_yards.fillna(0).sum()),
                car=len(r),rushyd=float(r.yards_gained.sum()),att=len(q),pyd=float(q.yards_gained.sum()),pyd_g=float(q.passing_yards.fillna(0).sum())))
    return pd.DataFrame(rows)
def ew(x,hl=3):
    x=np.asarray(x,float); n=len(x)
    if n==0: return 0.0
    w=0.5**((n-1-np.arange(n))/hl); return float((w*x).sum()/w.sum())
def nb(rng,m,r,size):
    m=max(m,1e-9); return rng.negative_binomial(r,r/(r+m),size)
def adj(opp,lg,on=True): return 1+0.5*(opp/lg-1) if on else 1.0
def seed_for(*a): return zlib.crc32('|'.join(map(str,a)).encode())
PRIOR={'WR':.62,'TE':.72,'RB':.78,'FB':.78}
# ---- simulators; each returns P(Over L) given settings ----
def sim_rec(lg_,pos,L,vol=1.0,rmult=1.0,last2=False,prior_k=15,seed=0):
    rng=np.random.default_rng(seed)
    tg=lg_.tgt.values; rc=lg_.rec.values
    mu=(tg[-2:].mean() if last2 else ew(tg))*vol
    pr=PRIOR.get(pos,.65); catch=(rc.sum()+prior_k*pr)/(tg.sum()+prior_k)
    t=nb(rng,mu,13.5*rmult,NSIM); r=rng.binomial(t,catch)
    return float((r>L).mean()),mu,catch
def sim_rush(lg_,isqb,L,opp,vol=1.0,rmult=1.0,last2=False,noopp=False,qbdist=False,seed=0):
    rng=np.random.default_rng(seed)
    c=lg_.car.values; mu=(c[-2:].mean() if last2 else ew(c))*vol
    base=LG_QB_YPC if isqb else LG_YPC
    ypc=(lg_.rushyd.sum()+50*base)/(c.sum()+50)
    a=adj(opp_ypc[opp],LG_YPC,not noopp)
    n=nb(rng,mu,8.1*rmult,NSIM); mx=int(n.max()) if n.max()>0 else 1
    emp=qbr_emp if (isqb and qbdist) else rush_emp
    sc=ypc/(LG_QB_YPC if (isqb and qbdist) else LG_YPC)*a
    draws=rng.choice(emp,(NSIM,mx))*sc
    mask=np.arange(mx)[None,:]<n[:,None]
    tot=(draws*mask).sum(1)
    return float((tot>L).mean()),mu,ypc,a
def sim_pass(lg_,L,opp,vol=1.0,rmult=1.0,last2=False,noopp=False,gross=False,seed=0):
    rng=np.random.default_rng(seed)
    at=lg_.att.values; mu=(at[-2:].mean() if last2 else ew(at))*vol
    yds=(lg_.pyd_g if gross else lg_.pyd).sum()
    lg=LG_YPA_GROSS if gross else LG_YPA
    ypa=(yds+100*lg)/(at.sum()+100)
    a=adj((opp_ypa_g if gross else opp_ypa)[opp],lg,not noopp)
    n=nb(rng,mu,26.3*rmult,NSIM); mx=int(n.max())
    emp=pass_emp_gross if gross else pass_emp
    draws=rng.choice(emp,(NSIM,mx))*(ypa/lg*a)
    mask=np.arange(mx)[None,:]<n[:,None]
    return float(((draws*mask).sum(1)>L).mean()),mu,ypa,a
from scipy.stats import poisson
def p_ptd(pts_,L,lamscale=1.0,ptsadj=0.0):
    lam=LAMBDA_PER_PT*(pts_+ptsadj)*lamscale
    return float(1-poisson.cdf(int(L),lam)),lam
def imp(price): return 100/(price+100) if price>0 else -price/(-price+100)
def evalprop(P,over_price,under_price):
    # P = list of (label, pOver) ; first is base
    be_o,be_u=imp(over_price),imp(under_price)
    base=P[0][1]
    side='Over' if base-be_o>(1-base)-be_u else 'Under'
    def edge(po): return (po-be_o) if side=='Over' else ((1-po)-be_u)
    edges=[(lab,100*edge(po)) for lab,po in P]
    mn=min(edges,key=lambda x:x[1])
    pb=base if side=='Over' else 1-base
    return dict(side=side,p_over=100*base,p_best=100*pb,be=100*(be_o if side=='Over' else be_u),base_edge=edges[0][1],min_edge=mn[1],min_lab=mn[0])
