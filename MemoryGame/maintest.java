package MemoryGame;

import java.io.IOException;

import MemoryGame.model.MemoryBoard;

public class maintest {


    public static void main(String[] args) throws IOException {
        MemoryBoard mb = new MemoryBoard(GameView.BOARDSIZE,
                "/Users/ebbarickard/2021:2022/INSA/Projet integrateur/test");
        GameController gc = new GameController(mb);
        // GameView gv = new GameView(mb);
        // showBoard(mb);
        // displayImage(mb.getCard(3, 3).getImage());

    }

}
