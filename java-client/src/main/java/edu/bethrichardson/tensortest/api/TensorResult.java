package edu.bethrichardson.tensortest.api;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class TensorResult {

    String expectation;
    String prediction;
    float probability;

}
