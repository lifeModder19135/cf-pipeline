CFAPI_NAMESPACE = 'CFAPI_'
CFAPI_PROBSLIST_INIT= 'wget https://codeforces.com/api/problemset.problems && cat ./problemset.problems | sed "s/},{/},\n{/g" | tee ./cf_probslist.json | less'