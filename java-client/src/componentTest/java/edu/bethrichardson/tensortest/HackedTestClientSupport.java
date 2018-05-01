package edu.bethrichardson.tensortest;

import com.blackbaud.feign.JacksonFeignBuilder;
import com.blackbaud.identity.token.BbAuthJwtBuilder;
import com.blackbaud.rest.client.AbstractClientBuilder;
import com.blackbaud.rest.client.CrudClientRequest;
import com.blackbaud.rest.client.request.ClientRequest;
import com.blackbaud.rest.client.request.ClientRequestBuilder;
import com.blackbaud.testsupport.TestTokenSupport;
import groovyx.net.http.RESTClient;
import org.springframework.beans.factory.annotation.Autowired;

import java.net.URISyntaxException;
import java.util.UUID;

public class HackedTestClientSupport {

    private String port = "5000";
    @Autowired
    private TestTokenSupport testTokenSupport;

    public RESTClient createRestClientWithTestToken() throws URISyntaxException {
        RESTClient restClient = new RESTClient("http://localhost:" + port + "/");
        testTokenSupport.setTestToken(restClient);
        return restClient;
    }

    public <T> T createClientWithTestToken(AbstractClientBuilder<T, ?> builder) {
        return (T) builder.baseUrl("http://localhost:" + port + "/")
                .authorizationHeaderProvider(testTokenSupport.createTestTokenAuthorizationHeaderProvider())
                .build();
    }

    public <T> T createClientWithTestToken(Class<T> apiType) {
        return createClientWithTestToken(new JacksonFeignBuilder<T>().apiType(apiType));
    }

    public <T> T createClientWithTestToken(JacksonFeignBuilder<T> builder) {
        return builder.baseUrl("http://localhost:" + port + "/")
                .requestInterceptor(testTokenSupport.createTestTokenAuthorizationRequestInterceptor())
                .target();
    }

    public <T> T createClientWithTestToken(AbstractClientBuilder<T, ?> builder, UUID userId, UUID tenantId) {
        return (T) builder.baseUrl("http://localhost:" + port + "/")
                .authorizationHeaderProvider(testTokenSupport.createTestTokenAuthorizationHeaderProvider(userId, tenantId))
                .build();
    }

    public <T> T createClientWithTestToken(Class<T> apiType, UUID userId, UUID tenantId) {
        return createClientWithTestToken(new JacksonFeignBuilder<T>().apiType(apiType), userId, tenantId);
    }

    public <T> T createClientWithTestToken(JacksonFeignBuilder<T> builder, UUID userId, UUID tenantId) {
        return builder.baseUrl("http://localhost:" + port + "/")
                .requestInterceptor(testTokenSupport.createTestTokenAuthorizationRequestInterceptor(userId, tenantId))
                .target();
    }

    public <T> T createClientWithStaticToken(AbstractClientBuilder<T, ?> builder, String token) {
        return (T) builder.baseUrl("http://localhost:" + port + "/")
                .authorizationHeaderProvider(testTokenSupport.createStaticAuthorizationHeaderProvider(token))
                .build();
    }

    public <T> T createClientWithStaticToken(Class<T> apiType, String token) {
        return createClientWithStaticToken(new JacksonFeignBuilder<T>().apiType(apiType), token);
    }

    public <T> T createClientWithStaticToken(JacksonFeignBuilder<T> builder, String token) {
        return builder.baseUrl("http://localhost:" + port + "/")
                .requestInterceptor(testTokenSupport.createStaticAuthorizationRequestInterceptor(token))
                .target();
    }

    public <T> CrudClientRequest<T> createCrudClientRequestWithTestToken(Class<T> type) {
        ClientRequest clientRequest = new ClientRequestBuilder()
                .luminateNextGenDefaults()
                .baseUrl("http://localhost:" + port + "/")
                .authorizationHeaderProvider(testTokenSupport.createTestTokenAuthorizationHeaderProvider())
                .build();
        return new CrudClientRequest<>(clientRequest, type);
    }

    public <T> T createClientWithBbAuthToken(AbstractClientBuilder<T, ?> builder) {
        return (T) builder.baseUrl("http://localhost:" + port + "/")
                .authorizationHeaderProvider(testTokenSupport.createBbAuthTokenAuthorizationHeaderProvider())
                .build();
    }

    public <T> T createClientWithBbAuthToken(Class<T> apiType) {
        return createClientWithBbAuthToken(new JacksonFeignBuilder<T>().apiType(apiType));
    }

    public <T> T createClientWithBbAuthTokenWithFormEncoding(Class<T> apiType) {
        return createClientWithBbAuthToken(new JacksonFeignBuilder<T>().apiType(apiType).enableFormEncoding());
    }

    public <T> T createClientWithBbAuthToken(JacksonFeignBuilder<T> builder) {
        return builder.baseUrl("http://localhost:" + port + "/")
                .requestInterceptor(testTokenSupport.createBbAuthTokenAuthorizationRequestInterceptor())
                .target();
    }

    public <T> T createClientWithBbAuthToken(JacksonFeignBuilder<T> builder, BbAuthJwtBuilder authJwtBuilder) {
        return builder.baseUrl("http://localhost:" + port + "/")
                .requestInterceptor(testTokenSupport.createBbAuthTokenAuthorizationRequestInterceptor(authJwtBuilder))
                .target();
    }

    public <T> T createClientWithSasToken(AbstractClientBuilder<T, ?> builder, String realm) {
        return (T) builder.baseUrl("http://localhost:" + port + "/")
                .authorizationHeaderProvider(testTokenSupport.createSasTokenAuthorizationHeaderProvider(realm))
                .build();
    }

    public <T> T createClientWithSasToken(Class<T> apiType, String realm) {
        return createClientWithSasToken(new JacksonFeignBuilder<T>().apiType(apiType), realm);
    }

    public <T> T createClientWithSasToken(JacksonFeignBuilder<T> builder, String realm) {
        return builder.baseUrl("http://localhost:" + port + "/")
                .requestInterceptor(testTokenSupport.createSasTokenAuthorizationRequestInterceptor(realm))
                .target();
    }

}
