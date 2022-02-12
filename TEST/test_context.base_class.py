from cfpipeline.SOURCE.modules.cfp_context import *

def test__Context_base_init_01():
    description("ensure that new Context objs are created with")
    ctx = Context("TEST_CTX_", "example", {})
    assert ctx.namespace == "TEST_CTX_" 
    
def test__Context_base_init_02():
    ctx = Context("TEST_CTX_", "example", {"wrd1":"Hello ", "wrd2":"world!"})
    assert ctx.env_dict["wrd1"] == "Hello " 
    
def test__Context_base_init_03():
    ctx = Context("TEST_CTX_", "example", {})
    assert ctx.ctx_type =="example"
    
def test_Context_base_init_04():
    ctx = Context("TEST_CTX_", "example", {"wrd1":"Hello ", "wrd2":"world!"})
    assert ctx.env_dict["wrd2"] == "world!"
    
