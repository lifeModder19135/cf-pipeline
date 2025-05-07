#! /usr/bin/env bash

# USAGE:
#       testv  TEST_INPUTFILE   PYTHON_SOURCEFILE   TEST_EXPECTSFILE

INFILE="${1}"
OUTFILE=$(set_context)
python3 "${2}" <"${INFILE}" 1>"${OUTFILE}" || echo "ERROR: !!!" && exit 1
echo 'EXPECTED:'
echo ''
cat "${3}"
echo ''
echo 'RECIEVED:'
echo ''
cat "${OUTFILE}"

set_context () {
    if [ -n "${CFS_PREFIX}" ];  then
        if [ ! -d "${CFS_PREFIX}" ]; then
            echo 'Something went wrong. Make sure that CFS_PREFIX is a set to a directory path.'
            exit 1
        else
            CFS_OUTPREF="${CFS_PREFIX}"
            sed 's/\/ //g' "${CFS_OUTPREF} " # ensure that string doesn't already end with "/"'
            CFS_OUTPREF="${CFS_OUTPREF}/" # add one "/" to the end of the string.
        fi
    else
        CFS_OUTPREF=~/.local/share/
    fi
    if [ -n "${CFS_DIRNAME}" ];  then
        if [ ! -d "${CFS_DIRNAME}" ]; then
            echo 'Something went wrong. Make sure that CFS_PREFIX is a set to a directory path.'
            exit 1
        else
            CFS_OUTDIR="${CFS_DIRNAME}" 
            sed 's/\///g' "${CFS_OUTDIR}" # ensure that string doesn't contain "/"'  
            CFS_OUTDIR="${CFS_OUTDIR}/" # add one "/" to the end of the string.
        fi
    else
        CFS_OUTDIR="cfpipeline"
    fi
    CFS_CONTEXT="${CFS_OUTPREF}${CFS_OUTDIR}"
    mkdir -p "${CFS_CONTEXT}" && echo -e "${CFS_CONTEXT}" ||\
    echo "Something went wrong. Ensure you can write to /usr/local/share/" && exit 1
}