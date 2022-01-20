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
        String imagesRepo = folder + "/imageNet";
        String backgroundImage = folder + "/src/main/java/MemoryGame/model/background.png";
        MemoryBoard mb = new MemoryBoard(GameView.BOARDSIZE, imagesRepo, backgroundImage);
        GameController gc = new GameController(mb);

        port(8080);

        ServerClass server = new ServerClass(gc);

        get("/hello", (req, res) -> "Hello World");
        get("/turnCard/:card", (req, res) -> server.turnCard(req, res, req.params(":card")));
        get("/isPair/:pair", (req, res) -> server.isPair(req, res, req.params(":pair")));
        get("/getBoard", (req, res) -> server.getBoard(req, res));

    }
}

class ServerClass {

    private GameController gc;

    public ServerClass(GameController gc) {
        this.gc = gc;
    }

    public String turnCard(Request req, Response res, String card) {
        System.out.println("In turnpair");
        Integer[] cardIndexes = parseCard(card);
        try {
            gc.turnCard(cardIndexes[0], cardIndexes[1]);
        } catch (Exception e) {
            e.printStackTrace();

        }
        res.status(200);
        return "";
    }

    public String isPair(Request req, Response res, String pair) {
        Integer[] pairs = parsePair(pair);
        boolean result = false;
        try {
            result = gc.checkPair(pairs[0], pairs[1], pairs[2], pairs[3]);
        } catch (IOException e) {
            e.printStackTrace();
        }
        res.body(Boolean.toString(result));
        return Boolean.toString(result);
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

    private Integer[] parseCard(String card) {
        Integer[] parsedCards = new Integer[2];
        try {
            parsedCards[0] = Integer.parseInt(card.substring(0, 1));
            parsedCards[1] = Integer.parseInt(card.substring(1, 2));
        } catch (Exception e) {
            e.printStackTrace();
        }
        return parsedCards;
    }

    public Response getBoard(Request req, Response res) {
        byte[] bytes = null;
        try {
            bytes = Files
                .readAllBytes(Paths.get(System.getProperty("user.dir") + "/board.jpg"));
        } catch (Exception e) {
            e.printStackTrace();
        }
        

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
