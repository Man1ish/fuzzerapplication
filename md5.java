import com.google.gson.JsonObject;

public class Main {
    public static JsonObject main(JsonObject args) {
        // if a value for name is provided, use it else use a default
        String input = args.has("name") ? args.get("name").getAsString() : "stranger";

        int output = hash(input);

        // construct the response JSON object
        JsonObject response = new JsonObject();
        response.addProperty("result", output);
        response.addProperty("latency", 1);

        return response;
    }

    public static int hash(String input) {
        int hash = 0;

        for (int i = 0; i < input.length(); i++) {
            hash = (hash << 5) - hash + input.charAt(i);
            hash &= hash;
        }

        return hash;
    }
}
