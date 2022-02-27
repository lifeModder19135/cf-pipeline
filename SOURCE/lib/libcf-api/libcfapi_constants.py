from invoke import run
CFAPI_NAMESPACE = 'CFAPI_'
CFP_CONTEXT_DIR = '~/.local/lib/cfpipeline-context'
CFAPI_DATA_DIR = 
CFAPI_DATA_SUBDIR = 'problemset'
CFAPI_PROBSLIST_DEFAULT = '/'.join(CFAPI_DATA_DIR, CFAPI_DATA_SUBDIR, 'problemset.problems')
CFAPI_PROBSLIST__OBJ_PERLINE = '/cf_probslist.json/'

CFAPI_PROBSLIST_INIT= run(f'wget https://codeforces.com/api/problemset.problems && cat {} | sed "s/},{/},\n{/g" | tee . | less')