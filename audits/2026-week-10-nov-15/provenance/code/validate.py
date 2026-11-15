exec(open('/home/claude/work/model.py').read())
def rec_row(name,team,L,po,pu):
    r=find(name,team); lg_=logs(r.gsis_id,team); 
    pb,mu,c=sim_rec(lg_,r.position,L,seed=seed_for(name,'rec'))
    print(name,'g',len(lg_),'tgtEW %.1f catch %.2f'%(mu,c),'P(over) %.1f'%(100*pb), evalprop([('base',pb)],po,pu))
rec_row('Bijan Robinson','ATL',3.5,-165,125)
rec_row('Kyle Pitts','ATL',3.5,-150,115)
rec_row('Deion Burks','IND',1.5,-160,125)
r=find('Bryce Young','CAR'); lg_=logs(r.gsis_id,'CAR')
pb,mu,ypc,a=sim_rush(lg_,True,9.5,'NO',seed=1); print('Young carEW %.2f ypc %.2f adj %.3f P(over) %.1f'%(mu,ypc,a,100*pb), 'prior card: .8, 5.80, 1.053, 18.5')
print(lg_[['week','car','rushyd']].T)
r=find('Penix','ATL') if False else find('Michael Penix','ATL'); lg_=logs(r.gsis_id,'ATL')
pb,mu,ypa,a=sim_pass(lg_,219.5,'KC',seed=2); print('Penix attEW %.1f ypa %.2f adj %.3f P(over) %.1f'%(mu,ypa,a,100*pb),'prior card: 30.0 6.55 .971 32.0')
