from ...sourcepy.modules.cfp_context import *

def test__Context_base_init_01():
    ctx = Context("TEST_CTX_", "example", {})
    assert ctx.namespace == "TEST_CTX" 
    
def test__Context_base_init_02():
    ctx = Context("TEST_CTX_", "example", {"wrd1":"Hello ", "wrd2":"world!"})
    assert ctx.env_dict["wrd1"] == "Hello " 
    
def test__Context_base_init_01():
    ctx = Context("TEST_CTX_", "example", {})
    assert ctx.ctx_type =="example"
    
def test_Context_base_init_02():
    ctx = Context("TEST_CTX_", "example", {"wrd1":"Hello ", "wrd2":"world!"})
    assert ctx.env_dict["wrd2"] == "world!"