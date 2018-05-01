package edu.bethrichardson.tensortest;

import com.blackbaud.testsupport.BaseTestConfig;
import edu.bethrichardson.tensortest.client.TensorTestClient;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class ComponentTestConfig extends BaseTestConfig {

    @Autowired
    private HackedTestClientSupport hackedTestClientSupport;

    @Bean
    public HackedTestClientSupport hackedTestClientSupport() {
        return new HackedTestClientSupport();
    }

    @Bean
    public TensorTestClient tensorTestClient() {
        return hackedTestClientSupport.createClientWithBbAuthToken(TensorTestClient.class);
    }

}
