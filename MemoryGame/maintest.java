package MemoryGame;

import java.io.IOException;

import MemoryGame.model.MemoryBoard;

public class maintest {

    public static void main(String[] args) throws IOException {
        String imagesRepo = "/Users/ebbarickard/2021:2022/INSA/Projet integrateur/test";
        String backgroundImage = "/Users/ebbarickard/2021:2022/INSA/Projet integrateur/MemoryGame/model/background.png";
        MemoryBoard mb = new MemoryBoard(GameView.BOARDSIZE, imagesRepo, backgroundImage);
        GameController gc = new GameController(mb);

    }

}
