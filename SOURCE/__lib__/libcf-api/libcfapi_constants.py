from invoke import run

CFAPI_NAMESPACE = 'CFAPI_'
CFP_CONTEXT_DIRECTORY_BASE = '~/.local/share/'
CFP_CONTEXT_DIRECTORY_NAME='cfpipeline_context'
CFP_CTX = ''.join(CFP_CONTEXT_DIRECTORY_BASE, CFP_CONTEXT_DIRECTORY_NAME)
CFAPI_DATA_DIR_BASE = 
CFAPI_DATA_DIR_NAME = 
CFAPI_DATA_SUBDIR = 'problemset'
CFAPI_PROBSLIST_DEFAULT = '/'.join(CFAPI_DATA_DIR, CFAPI_DATA_SUBDIR, 'problemset.problems')
CFAPI_PROBSLIST__OBJ_PERLINE = '/cf_probslist.json/'

CFAPI_PROBSLIST_INIT= run(f'wget https://codeforces.com/api/problemset.problems && cat {} | sed "s/},{/},\n{/g" | tee . | less'
