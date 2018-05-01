package edu.bethrichardson.tensortest.api

import static edu.bethrichardson.tensortest.api.RestClientARandom.aRandom

class RandomFormBuilder extends Form.FormBuilder {
    RandomFormBuilder() {
        super.id(aRandom.uuid())
                .environmentId(aRandom.environmentId())
                .name(aRandom.businessName())
                .lastModifiedDate(aRandom.dateInPastDays(15).atStartOfDay())
                .createdDate(aRandom.dateInPastDays(365).atStartOfDay())
                .constituentCode(aRandom.text(10))
                .formType(aRandom.text(10))
    }
}
