package MemoryGame;


import MemoryGame.model.MemoryBoard;

public class GameController {
    private boolean[][] boardStatus;
    private GameView gv;

    public GameController(MemoryBoard mb) {
        gv = new GameView(mb);
    }

}
