package edu.bethrichardson.tensortest.api

import static edu.bethrichardson.tensortest.api.RestClientARandom.aRandom

class ReallyBadFormBuilder extends Form.FormBuilder {

    ReallyBadFormBuilder() {
        super.id(aRandom.uuid())
                .environmentId(aRandom.text(5))
                .name(aRandom.businessName())
                .constituentCode("broken")
                .formType(aRandom.text(10))
    }
}
