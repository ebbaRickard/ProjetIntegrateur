package MemoryGame;

import java.io.IOException;

import static spark.Spark.*;

import spark.Request;
import spark.Response;

import java.util.UUID;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpRequest.BodyPublishers;
import java.net.http.HttpResponse;
import java.net.http.HttpResponse.BodyHandlers;

import MemoryGame.model.MemoryBoard;

public class maintest {

    public static void main(String[] args) throws IOException {
        String folder = System.getProperty("user.dir");
        String imagesRepo = folder + "/src/main/java/MemoryGame/model/data/test";
        String backgroundImage = folder + "/src/main/java/MemoryGame/model/background.png";
        MemoryBoard mb = new MemoryBoard(GameView.BOARDSIZE, imagesRepo, backgroundImage);
        GameController gc = new GameController(mb);

        port(8080);


        ServerClass server = new ServerClass(gc);

        get("/hello", (req, res) -> "Hello World");
        post("/flipcard/:row1/:col1/:row2/:col2", (req, res) -> server.turnPair(req, res, req.params(":row1"), req.params(":col1"), req.params(":row2"), req.params(":col2") )  );


}}

class ServerClass {

    private GameController gc;

    public ServerClass(GameController gc) {
        this.gc = gc;
    }

    public String turnPair(Request req, Response res, String row1, String col1, String row2, String col2) {
        System.out.println(row1);
        System.out.println(col2);
        System.out.println(row1);
        System.out.println(col2);
        try {
            gc.turnPair(Integer.parseInt(row1),Integer.parseInt(col1),Integer.parseInt(row2),Integer.parseInt(col2));
        } catch (Exception e) {
            e.printStackTrace();

        }
        res.status(200);
        return "";
    }

}
