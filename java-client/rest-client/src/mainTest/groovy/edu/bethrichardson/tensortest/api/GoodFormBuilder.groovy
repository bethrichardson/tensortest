package edu.bethrichardson.tensortest.api

import static edu.bethrichardson.tensortest.api.RestClientARandom.aRandom

class GoodFormBuilder extends Form.FormBuilder {

    GoodFormBuilder() {
        super.id(aRandom.uuid())
                .environmentId(aRandom.text(50))
                .name(aRandom.businessName())
                .constituentCode(aRandom.text(10))
                .formType(aRandom.text(10))
    }
}
