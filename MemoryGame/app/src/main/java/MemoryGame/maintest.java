package MemoryGame;

import java.io.IOException;

import static spark.Spark.*;

import spark.Request;
import spark.Response;

import java.util.UUID;

import javax.servlet.http.HttpServletResponse;

import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpRequest.BodyPublishers;
import java.net.http.HttpResponse;
import java.net.http.HttpResponse.BodyHandlers;

import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

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
        post("/turnPair/:pair", (req, res) -> server.turnPair(req, res, req.params(":pair")));
        get("/isPair/:pair", (req, res) -> server.isPair(req, res, req.params(":pair")));
        get("/getBoard", (req, res) -> server.getBoard(req, res));

    }
}

class ServerClass {

    private GameController gc;

    public ServerClass(GameController gc) {
        this.gc = gc;
    }

    public String turnPair(Request req, Response res, String pair) {
        Integer[] pairs = parsePair(pair);
        System.out.println(pairs.toString());
        try {
            gc.turnPair(pairs[0], pairs[1], pairs[2], pairs[3]);
        } catch (Exception e) {
            e.printStackTrace();

        }
        res.status(200);
        return "";
    }

    public String isPair(Request req, Response res, String pair) {
        Integer[] pairs = parsePair(pair);
        gc.checkPair(pairs[0], pairs[1], pairs[2], pairs[3]);
        return "";
    }

    private Integer[] parsePair(String pair) {
        Integer[] parsedPairs = new Integer[4];
        try {
            parsedPairs[0] = Integer.parseInt(pair.substring(0, 1));
            parsedPairs[1] = Integer.parseInt(pair.substring(1, 2));
            parsedPairs[2] = Integer.parseInt(pair.substring(2, 3));
            parsedPairs[3] = Integer.parseInt(pair.substring(3, 4));
        } catch (Exception e) {
            e.printStackTrace();
        }
        return parsedPairs;
    }

    public Response getBoard(Request req, Response res) {
        String folder = System.getProperty("user.dir");
        byte[] bytes = Files
                .readAllBytes(Paths.get(folder.substring(0, folder.length() - 14) + "/Detection/board.jpg"));

        HttpServletResponse raw = res.raw();
        res.header("Content-Disposition", "attachment; filename=image.jpg");
        res.type("application/force-download");
        try {
            raw.getOutputStream().write(bytes);
            raw.getOutputStream().flush();
            raw.getOutputStream().close();
        } catch (Exception e) {

            e.printStackTrace();
        }
        return res;

    }

}
