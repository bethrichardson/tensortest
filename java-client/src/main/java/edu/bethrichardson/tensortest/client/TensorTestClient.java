package edu.bethrichardson.tensortest.client;

import edu.bethrichardson.tensortest.api.TensorResult;
import edu.bethrichardson.tensortest.api.TensorTrainResult;
import feign.Headers;
import feign.Param;
import feign.RequestLine;

@Headers({
        "Accept: text/plain,application/json",
        "Content-Type: application/json"
})
public interface TensorTestClient {

    @RequestLine("GET " + "/test/run?status={status}&name={name}&environment={environment}&type={type}&code={code}&api={api}")
    TensorResult runTest(@Param("status") String status, @Param("name") int name, @Param("environment") int environment,
                         @Param("type") int type, @Param("code") int code, @Param("api") String api);

    @RequestLine("GET " + "/train?status={status}&name={name}&environment={environment}&type={type}&code={code}&api={api}")
    TensorTrainResult train(@Param("status") int status, @Param("name") int name, @Param("environment") int environment,
                            @Param("type") int type, @Param("code") int code, @Param("api") String api);
}
