exec(open('/home/claude/work/model.py').read())
pd.set_option('display.width',250); pd.set_option('display.max_columns',40); pd.set_option('display.max_rows',500)
PTS={'SEA':23.5,'LV':17.0,'LA':23.75,'ARI':14.75,'SF':29.75,'DAL':25.75}
OPP={'SEA':'LV','LV':'SEA','LA':'ARI','ARI':'LA','SF':'DAL','DAL':'SF'}
GAME={'SEA':'SEA@LV','LV':'SEA@LV','LA':'LAR@ARI','ARI':'LAR@ARI','SF':'SF@DAL','DAL':'SF@DAL'}
REC=[('SEA','Jaxon Smith-Njigba',7.5,105,-135),('SEA','Cooper Kupp',1.5,-185,140),('SEA','Rashid Shaheed',1.5,-185,140),('SEA','Tory Horton',0.5,-220,160),('SEA','AJ Barner',2.5,-125,-105),('SEA','Zach Charbonnet',1.5,-145,110),('SEA','Jadarian Price',1.5,-130,100),
('LV','Brock Bowers',5.5,-105,-125),('LV','Ashton Jeanty',4.5,125,-160),('LV','Michael Mayer',2.5,-145,110),('LV','Tre Tucker',2.5,-110,-120),('LV','Jalen Nailor',1.5,110,-140),('LV','Jack Bech',0.5,-190,140),
('LA','Tyler Higbee',3.5,-130,100),('LA','Colby Parkinson',3.5,-120,-110),('LA','Kyren Williams',2.5,-160,125),('LA','Tutu Atwell',2.5,110,-140),('LA','Konata Mumpfield',2.5,115,-150),('LA','Davis Allen',1.5,105,-135),('LA','CJ Daniels',1.5,120,-155),('LA','Blake Corum',1.5,130,-170),
('ARI','Trey McBride',6.5,-105,-125),('ARI','Elijah Higgins',2.5,-110,-120),('ARI','Reggie Virgil',2.5,125,-160),('ARI','Tyler Allgeier',2.5,135,-185),('ARI','Bam Knight',1.5,-110,-120),('ARI','Devin Duvernay',1.5,115,-150),('ARI','Simi Fehoko',1.5,125,-165),
('SF','George Kittle',5.5,120,-155),('SF','Christian McCaffrey',4.5,115,-145),('SF','Deebo Samuel',3.5,115,-145),('SF','Keenan Allen',2.5,110,-140),('SF','Demarcus Robinson',2.5,120,-160),('SF','Jordan Watkins',1.5,105,-135),('SF','Kyle Juszczyk',0.5,-220,155),
('DAL','CeeDee Lamb',7.5,115,-145),('DAL','George Pickens',4.5,-105,-125),('DAL','Ryan Flournoy',3.5,115,-150),('DAL','Javonte Williams',2.5,-155,120),('DAL','Brevyn Spann-Ford',2.5,-145,110)]
RUSH=[('SEA','Zach Charbonnet',63.5,-115,-115,0),('SEA','Jadarian Price',41.5,-115,-115,0),('SEA','Drew Lock',5.5,-115,-115,1),
('LV','Ashton Jeanty',36.5,-115,-115,0),('LV','Michael Washington',25.5,-110,-120,0),('LV','Fernando Mendoza',15.5,-120,-110,1),
('LA','Kyren Williams',66.5,-115,-115,0),('LA','Blake Corum',58.5,-115,-115,0),('LA','Matthew Stafford',0.5,135,-180,1),
('ARI','Tyler Allgeier',34.5,-120,-110,0),('ARI','Bam Knight',33.5,-115,-115,0),('ARI','Carson Beck',10.5,-120,-110,1),
('SF','Christian McCaffrey',63.5,-115,-115,0),('SF','Kaelon Black',36.5,-115,-115,0),('SF','Brock Purdy',21.5,-115,-115,1),('SF','Deebo Samuel',6.5,-115,-115,0),
('DAL','Javonte Williams',60.5,-115,-115,0),('DAL','Dak Prescott',9.5,-115,-115,1)]
PASS=[('SEA','Drew Lock',198.5,-115,-115),('LV','Fernando Mendoza',183.5,-115,-115),('LA','Matthew Stafford',209.5,-120,-110),('ARI','Carson Beck',175.5,-115,-115),('SF','Brock Purdy',260.5,-115,-115),('DAL','Dak Prescott',270.5,-115,-115)]
PTD=[('SEA','Drew Lock',1.5,120,-155),('LV','Fernando Mendoza',0.5,-230,165),('LA','Matthew Stafford',1.5,100,-130),('ARI','Carson Beck',0.5,-155,120),('SF','Brock Purdy',2.5,160,-225),('DAL','Dak Prescott',1.5,-195,145)]
out=[]; hist={}
def H(lg_,col,n=8): return list(lg_[col].astype(int).values[-n:])
for team,name,L,po,pu in REC:
    r=find(name,team); lg_=logs(r.gsis_id,team); s=seed_for(name,'rec')
    if len(lg_)==0:
        out.append(dict(game=GAME[team],team=team,player=name,pos=r.position,mkt='rec',line=L,over=po,under=pu,g=0,side='NA',note='no current-team sample')); continue
    base,mu,c=sim_rec(lg_,r.position,L,seed=s)
    P=[('base',base)]
    for lab,kw in [('vol-15',dict(vol=.85)),('vol+15',dict(vol=1.15)),('disp x.5',dict(rmult=.5)),('disp x2',dict(rmult=2)),('last2',dict(last2=True)),('catch5',dict(prior_k=5)),('catch30',dict(prior_k=30))]:
        P.append((lab,sim_rec(lg_,r.position,L,seed=s,**kw)[0]))
    e=evalprop(P,po,pu)
    out.append(dict(game=GAME[team],team=team,player=name,pos=r.position,mkt='rec',line=L,over=po,under=pu,g=len(lg_),mu=mu,catch=c,**e,hist_rec=H(lg_,'rec'),hist_tgt=H(lg_,'tgt'),snaps=H(lg_,'snaps'),weeks=H(lg_,'week')))
for team,name,L,po,pu,isqb in RUSH:
    r=find(name,team); lg_=logs(r.gsis_id,team); s=seed_for(name,'rush'); opp=OPP[team]
    if len(lg_)==0 or lg_.car.sum()==0:
        out.append(dict(game=GAME[team],team=team,player=name,pos=r.position,mkt='rush',line=L,over=po,under=pu,g=len(lg_),side='NA',note='no carries in sample')); continue
    base,mu,ypc,a=sim_rush(lg_,bool(isqb),L,opp,seed=s); P=[('base',base)]
    pert=[('vol-15',dict(vol=.85)),('vol+15',dict(vol=1.15)),('disp x.5',dict(rmult=.5)),('disp x2',dict(rmult=2)),('last2',dict(last2=True)),('noopp',dict(noopp=True))]
    if isqb: pert.append(('qbdist',dict(qbdist=True)))
    for lab,kw in pert: P.append((lab,sim_rush(lg_,bool(isqb),L,opp,seed=s,**kw)[0]))
    e=evalprop(P,po,pu)
    out.append(dict(game=GAME[team],team=team,player=name,pos=r.position,mkt='rush',line=L,over=po,under=pu,g=len(lg_),mu=mu,ypc=ypc,adj=a,**e,hist_car=H(lg_,'car'),hist_yd=H(lg_,'rushyd'),snaps=H(lg_,'snaps'),weeks=H(lg_,'week')))
for team,name,L,po,pu in PASS:
    r=find(name,team); lg_=logs(r.gsis_id,team); s=seed_for(name,'pass'); opp=OPP[team]
    if len(lg_)==0 or lg_.att.sum()==0: out.append(dict(game=GAME[team],team=team,player=name,mkt='pass',line=L,side='NA',g=len(lg_),note='no attempts')); continue
    base,mu,ypa,a=sim_pass(lg_,L,opp,seed=s); P=[('base',base)]
    for lab,kw in [('vol-15',dict(vol=.85)),('vol+15',dict(vol=1.15)),('disp x.5',dict(rmult=.5)),('disp x2',dict(rmult=2)),('last2',dict(last2=True)),('noopp',dict(noopp=True))]:
        P.append((lab,sim_pass(lg_,L,opp,seed=s,**kw)[0]))
    e=evalprop(P,po,pu)
    # diagnostic: official gross passing-yard definition (sack yards not subtracted)
    gb=sim_pass(lg_,L,opp,seed=s,gross=True)[0]; eg=evalprop([('base',gb)],po,pu)
    out.append(dict(game=GAME[team],team=team,player=name,pos='QB',mkt='pass',line=L,over=po,under=pu,g=len(lg_),mu=mu,ypa=ypa,adj=a,**e,gross_p_over=100*gb,gross_side=eg['side'],gross_edge=eg['base_edge'],hist_att=H(lg_,'att'),hist_pyd_net=H(lg_,'pyd'),hist_pyd_gross=H(lg_,'pyd_g'),weeks=H(lg_,'week')))
for team,name,L,po,pu in PTD:
    pts_=PTS[team]; base,lam=p_ptd(pts_,L); P=[('base',base),('lam-15',p_ptd(pts_,L,.85)[0]),('lam+15',p_ptd(pts_,L,1.15)[0]),('tot-3',p_ptd(pts_,L,ptsadj=-1.5)[0]),('tot+3',p_ptd(pts_,L,ptsadj=1.5)[0])]
    e=evalprop(P,po,pu); r=find(name,team); lg_=logs(r.gsis_id,team)
    if len(lg_)==0 or 'att' not in lg_: e['note']='no NFL sample for QB (model P is points-only)'
    out.append(dict(game=GAME[team],team=team,player=name,pos='QB',mkt='pass_td',line=L,over=po,under=pu,g=len(lg_),lam=lam,pts=pts_,**e,hist_att=(H(lg_,'att') if len(lg_) else [])))
df=pd.DataFrame(out); df.to_pickle('board.pkl')
cols=['game','player','mkt','line','over','under','side','p_best','be','base_edge','min_edge','min_lab','g']
for m in ['rec','rush','pass','pass_td']:
    d=df[df.mkt==m]
    print('\n=====',m); print(d[[c for c in cols if c in d]].round(1).to_string(index=False))
