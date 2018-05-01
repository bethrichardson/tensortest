package edu.bethrichardson.tensortest.api

import static edu.bethrichardson.tensortest.api.RestClientARandom.aRandom

class BadFormBuilder extends Form.FormBuilder {

    BadFormBuilder() {
        super.id(aRandom.uuid())
                .environmentId(aRandom.text(5))
                .name("bad form")
                .constituentCode(aRandom.businessName())
                .formType(aRandom.text(10))
    }
}
