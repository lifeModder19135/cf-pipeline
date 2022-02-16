#
##
#####   PYTHON3
##
#


##>._  ~ Invoke Module ~ _.<## 

from:
    class Invoke.runners.Runner()


``handle_stdin(input_, output, echo)``

    Read local stdin, copying into process’ stdin as necessary.
    Intended for use as a thread target.

    Note:
        Because real terminal stdin streams have no well-defined “end”, if such a stream is detected 
        (based on existence of a callable .fileno()) this method will wait until program_finished is set, 
        before terminating. When the stream doesn’t appear to be from a terminal, the same semantics as 
        handle_stdout are used
        - the stream is simply read() from until it returns an empty value.

    Parameters:	
        input – Stream (file-like object) from which to read.
        output – Stream (file-like object) to which echoing may occur.
        echo (bool) – User override option for stdin-stdout echoing.
    Returns: None.


# Terminal Commands

    # wgets a list
$ wget https://codeforces.com/api/problemset.problems && \
cat ./problemset.problems | sed 's/},{/},\n{/g' | tee ./cf_probslist.json | less
