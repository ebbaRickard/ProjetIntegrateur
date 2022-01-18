package MemoryGame;

import java.io.IOException;

import MemoryGame.model.MemoryBoard;

public class GameController {
    private MemoryBoard mb;
    private GameView gv;


    public GameController(MemoryBoard mb) throws IOException {
        this.mb = mb;
        gv = new GameView(mb);
    }

    public void turnPair(int r1, int c1, int r2, int c2) throws IOException {
        if (!mb.isFlipped(r1, c1) && !mb.isFlipped(r2, c2)) {
            mb.flipCard(r1, c1);
            mb.flipCard(r2, c2);
        }
        gv.updateWindow(mb);
    }

    public void turnCard(int r1, int c1) throws IOException {
        if (!mb.isFlipped(r1, c1)) {
            mb.flipCard(r1, c1);
        }
        gv.updateWindow(mb);
    }

    // Called when the AI thinks it turned two cards that make a pair
    // If the AI doesn't think it is a pair, it just flips them back
    public boolean checkPair(int r1, int c1, int r2, int c2) throws IOException {
        // If not pair, flip back to tell AI that it was wrong
        boolean isPair = true;
        if (!mb.isPair(r1, c1, r2, c2)) {
            if (mb.isFlipped(r1, c1)) {
                mb.flipCard(r1, c1);
            }
            if (mb.isFlipped(r2, c2)) {
                mb.flipCard(r2, c2);
            }

            isPair = false;
        }

        gv.updateWindow(mb);

        return isPair;
    }


}
