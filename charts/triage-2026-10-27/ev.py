import json,datetime as dt
S={}
for f in ['w2.json','e1.json','e2.json','e3.json']:
    d=json.load(open(f))
    for e in d['data']['entities']:
        k=e['entity_id'].split('.')[-1]
        if f not in('w2.json',) or k not in('sigen_plant_battery_power','sigen_plant_pv_power','sigen_plant_grid_active_power','sigen_inverter_dc_charger_output_power'):
            S.setdefault(k,[]).extend((dt.datetime.fromisoformat(s['last_changed']),s['state']) for s in e['states'])
        if f!='w2.json': print(f,k,e['total_count'],e['count'])
for k in S: S[k].sort()
short={'sigen_plant_battery_power':'BESS','sigen_plant_pv_power':'PV','sigen_plant_grid_active_power':'grid','sigen_inverter_dc_charger_output_power':'EV','sigen_inverter_dc_charger_running_state':'rs','garage_sigen_inverter_dc_charger_max_charging_power_limit':'dcC','garage_sigen_inverter_dc_charger_max_discharging_power_limit':'dcD','sigen_plant_grid_export_limitation':'expL','amber_v2x_amber_purcell_id_au_optimiser_decision':'dec','sigen_plant_ems_work_mode':'mode','sigen_plant_battery_state_of_charge':'soc','m3p_t_battery_level':'evsoc'}
def at(k,t):
    v=None
    for tt,s in S[k]:
        if tt<=t: v=s
        else: break
    return v
import sys
t=dt.datetime.fromisoformat(sys.argv[1]); t1=dt.datetime.fromisoformat(sys.argv[2]); st=int(sys.argv[3])
ks=list(short)
print('time     '+' '.join(f'{short[k]:>7}' for k in ks))
while t<=t1:
    row=[]
    for k in ks:
        v=at(k,t)
        try: row.append(f'{float(v):7.1f}')
        except: row.append(f'{str(v)[:7]:>7}')
    print(t.strftime('%H:%M:%S'),' '.join(row)); t+=dt.timedelta(seconds=st)
