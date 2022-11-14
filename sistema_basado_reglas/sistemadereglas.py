from sistema_basado_reglas.reglas import *

class sistemadereglas(KnowledgeEngine): 

    @Rule(AND(reglas(resp_abdominal = "Si")), (reglas(resp_diarrea = "Si")), (reglas(resp_estrenimiento = "No")), (reglas(resp_acidez= "No")), (reglas(resp_vomitos= "Si")))
    def m1 (self):
        return "lo lograste bb"