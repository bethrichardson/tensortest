package edu.bethrichardson.tensortest.form.resources

import edu.bethrichardson.tensortest.ComponentTest
import edu.bethrichardson.tensortest.api.Form
import edu.bethrichardson.tensortest.api.TensorResult
import edu.bethrichardson.tensortest.api.TensorTrainResult
import edu.bethrichardson.tensortest.client.TensorTestClient
import org.apache.commons.lang.StringUtils
import org.springframework.beans.factory.annotation.Autowired
import spock.lang.Specification

import static edu.bethrichardson.tensortest.core.CoreARandom.aRandom

@ComponentTest
class TensorTestSpec extends Specification {
    @Autowired
    TensorTestClient tensorClient

    def "should run a good test against TensorTest"() {
        given:
        Form form = aRandom.form().build()

        when:
        TensorResult result = tensorClient.runTest("200", form.name.hashCode(), form.environmentId.hashCode(),
                                                   form.formType.hashCode(), form.constituentCode.hashCode(), "form")

        then:
        result.expectation.equals("200")
        !StringUtils.isBlank(result.prediction)
        result.prediction.equals("200")
        result.probability > 0
    }

    def "should run a bad test against TensorTest"() {
        given:
        Form form = aRandom.badForm().build()

        when:
        TensorResult result = tensorClient.runTest("400", form.name.hashCode(), form.environmentId.hashCode(),
                                                   form.formType.hashCode(), form.constituentCode.hashCode(), "form")

        then:
        result.expectation.equals("400")
        !StringUtils.isBlank(result.prediction)
        result.prediction.equals("400")
        result.probability > 0
    }

    def "should run a really bad test against TensorTest"() {
        given:
        Form form = aRandom.reallyBadForm().build()

        when:
        TensorResult result = tensorClient.runTest("500", form.name.hashCode(), form.environmentId.hashCode(),
                                                   form.formType.hashCode(), form.constituentCode.hashCode(), "form")

        then:
        result.expectation.equals("500")
        !StringUtils.isBlank(result.prediction)
        result.prediction.equals("500")
        result.probability > 0
    }

    def "should get an error when sending bad training data to TensorTest"() {
        given:
        Form form = aRandom.form().build()

        when:
        tensorClient.train(200, form.name.hashCode(), form.environmentId.hashCode(),
                                                   form.formType.hashCode(), form.constituentCode.hashCode(), "form")

        then:
        thrown(Exception)
    }


    def "should send a training event to TensorTest"() {
        given:
        Form form = aRandom.form().build()

        when:
        TensorTrainResult result = tensorClient.train(0, form.name.hashCode(), form.environmentId.hashCode(),
                                                             form.formType.hashCode(), form.constituentCode.hashCode(), "form")

        then:
        result.acknowledged
        StringUtils.isNotBlank(result.id)
    }

//    @Ignore
    def "should send a lot of training events to TensorTest"() {
        given:
        int numGoodEvents = 150
        int numBadEvents = 150
        int numReallyBadEvents = 150

        when:
        numGoodEvents.times {
            Form form = aRandom.form().build()
            tensorClient.train(0, form.name.hashCode(), form.environmentId.hashCode(),
                                                          form.formType.hashCode(), form.constituentCode.hashCode(), "form")
        }

        numBadEvents.times {
            Form form = aRandom.badForm().build()
            tensorClient.train(1, form.name.hashCode(), form.environmentId.hashCode(),
                               form.formType.hashCode(), form.constituentCode.hashCode(), "form")
        }

        numReallyBadEvents.times {
            Form form = aRandom.reallyBadForm().build()
            tensorClient.train(2, form.name.hashCode(), form.environmentId.hashCode(),
                               form.formType.hashCode(), form.constituentCode.hashCode(), "form")
        }


        then:
        noExceptionThrown()
    }
}
