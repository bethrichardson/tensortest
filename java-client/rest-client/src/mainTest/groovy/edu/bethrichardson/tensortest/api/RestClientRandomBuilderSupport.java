package edu.bethrichardson.tensortest.api;

public class RestClientRandomBuilderSupport {
    public RandomFormBuilder form() {
        return new RandomFormBuilder();
    }

    public BadFormBuilder badForm() {
        return new BadFormBuilder();
    }

    public ReallyBadFormBuilder reallyBadForm() {
        return new ReallyBadFormBuilder();
    }
}
