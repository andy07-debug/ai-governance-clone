import sys,json
for l in sys.stdin:
    if l.startswith('ERRS') or 'Error' in l or 'Trace' in l: print(l[:600]); continue
    tag,_,j=l.partition(' {')
    try: r=json.loads('{'+j)
    except: print(l[:300]); continue
    print(tag, r['state'], r['hash'], 'inst',r['nInst'],'cv',r['nCanvas'], [(c['id'],c.get('ymax'),round(c.get('cssW',0)),c.get('bw'),c.get('chartH'),c.get('painted')) for c in r['charts']])
