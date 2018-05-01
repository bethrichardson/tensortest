package edu.bethrichardson.tensortest.api;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;
import java.util.UUID;

@Data
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class Form {
    UUID id;
    String name;
    String environmentId;
    String formType;
    String constituentCode;
    LocalDateTime lastModifiedDate;
    LocalDateTime createdDate;
}
