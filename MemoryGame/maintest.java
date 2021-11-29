package MemoryGame;

import java.awt.FlowLayout;
import java.io.IOException;
import javax.swing.ImageIcon;
import javax.swing.JFrame;
import javax.swing.JLabel;
import java.awt.*;

public class maintest {

    public static void main(String[] args) throws IOException {
        MemoryBoard mb = new MemoryBoard(4,
                "/Users/ebbarickard/2021:2022/INSA/Projet integrateur/Data sets/small_fruit_set/test_zip/test");
        showBoard(mb);
        displayImage(mb.getCard(4, 4).getImage());

    }

    public static void displayImage(Image image) throws IOException {
        ImageIcon icon = new ImageIcon(image);
        JFrame frameImage = new JFrame();
        frameImage.setLayout(new FlowLayout());
        frameImage.setSize(800, 800);
        JLabel lbl = new JLabel();
        lbl.setIcon(icon);
        frameImage.add(lbl);
        frameImage.setVisible(true);
        frameImage.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    }

    public static void showBoard(MemoryBoard mb) throws IOException {
        JFrame frameBoard = new JFrame();
        frameBoard.setLayout(new GridLayout(8, 8));
        frameBoard.setSize(800, 800);
        for (int r = 0; r < mb.getSize(); r++) {
            for (int c = 0; c < mb.getSize(); c++) {
                ImageIcon icon = new ImageIcon(mb.getCard(r, c).getImage());
                JLabel lbl = new JLabel();
                lbl.setIcon(icon);
                frameBoard.add(lbl, r + c);
            }
        }
        System.out.println("here");
        frameBoard.setVisible(true);
        frameBoard.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    }
}
