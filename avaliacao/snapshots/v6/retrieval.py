import math, re, unicodedata
from collections import Counter
from nltk.stem.snowball import PortugueseStemmer
STEM = PortugueseStemmer()
STOP = set('a o as os de do da dos das e em um uma que para com por no na nos nas se ao é ou como qual quais quem pode devo precisa quero meu minha este esse esta isso mais fazer ser tem tenho'.split())
def words(text):
    raw=re.findall(r'[a-záàâãéêíóôõúç0-9]+',text.lower())
    result=[unicodedata.normalize('NFKD',STEM.stem(t)).encode('ascii','ignore').decode() for t in raw if t not in STOP and len(t)>2]
    aliases={'esquent':'quent', 'falh':'vici', 'validad':'val'}
    return [aliases.get(t,t) for t in result]
def rank(question, base, method='tfidf', k=3):
    docs=[Counter(words(x['texto'])) for x in base]; q=Counter(words(question)); n=len(docs)
    df=Counter(t for d in docs for t in d); avg=sum(sum(d.values()) for d in docs)/n
    def vector(c):return {t:(1+math.log(v))*(1+math.log((n+1)/(df[t]+1))) for t,v in c.items()}
    qv=vector(q); qn=math.sqrt(sum(v*v for v in qv.values()))
    found=[]
    for row,d in zip(base,docs):
        if method=='bm25':
            length=sum(d.values()); score=sum(math.log(1+(n-df[t]+.5)/(df[t]+.5))*(d[t]*2.2)/(d[t]+1.2*(.25+.75*length/avg)) for t in q if d[t])
        else:
            dv=vector(d); dn=math.sqrt(sum(v*v for v in dv.values())); score=sum(v*dv.get(t,0) for t,v in qv.items())/(qn*dn) if qn and dn else 0
        found.append({**row,'score':score})
    return sorted(found,key=lambda x:(-x['score'],x['id']))[:k]
