package MemoryGame;

import MemoryGame.model.MemoryBoard;

import java.awt.*;
import java.awt.FlowLayout;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;

import javax.imageio.ImageIO;

import javax.swing.*;
import javax.swing.ImageIcon;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;

public class GameView {
    public static int PADDING = 10;
    public static int LINEWIDTH_MEMORYCARD = 3;
    public static int BOARDSIZE = 3;

    public GameView(MemoryBoard mb) {

        try {
            showBoard(mb);
        } catch (IOException e) {
            e.printStackTrace();
        }

    }

    public static void showBoard(MemoryBoard mb) throws IOException {
        JPanel frameBoard = new JPanel(new GridLayout(BOARDSIZE, BOARDSIZE, 10, 10));
        frameBoard.setBorder(BorderFactory.createEmptyBorder(PADDING, PADDING, PADDING, PADDING));
        frameBoard.setBackground(Color.MAGENTA);

        ImageIcon icon = new ImageIcon();

        for (int r = 0; r < mb.getSize(); r++) {
            for (int c = 0; c < mb.getSize(); c++) {
                if (mb.isFlipped(r, c)) {
                    icon = resizeImageIcon(new ImageIcon(mb.getCard(r, c).getImage()));
                } else {
                    icon = resizeImageIcon(new ImageIcon(mb.getBackGround().getImage()));
                }
                JLabel lbl = new JLabel();
                lbl.setBorder(BorderFactory.createMatteBorder(LINEWIDTH_MEMORYCARD, LINEWIDTH_MEMORYCARD,
                        LINEWIDTH_MEMORYCARD, LINEWIDTH_MEMORYCARD, Color.BLACK));
                lbl.setIcon(icon);
                frameBoard.add(lbl, BOARDSIZE*r + c);  // Här blir det konstigt
            }
        }
        System.out.println("here");

        JFrame frame = new JFrame("Memory");
        frame.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        frame.getContentPane().add(frameBoard);
        frame.pack();
        frame.setLocationByPlatform(true);
        frame.setVisible(true);

        SaveBoardImage(frameBoard);
    }

    public static ImageIcon resizeImageIcon(ImageIcon imageIcon) {
        Image image = imageIcon.getImage();
        Image newimg = image.getScaledInstance(150, 150, java.awt.Image.SCALE_SMOOTH);
        return new ImageIcon(newimg);
    }

    public static void SaveBoardImage(JPanel component) {
        Dimension d = component.getSize();
        BufferedImage image = new BufferedImage(d.width, d.height, BufferedImage.TYPE_INT_RGB);
        Graphics2D g2d = image.createGraphics();
        component.print(g2d);
        g2d.dispose();
        try {
            boolean result = ImageIO.write(image, "jpg",
                    new File("/Users/ebbarickard/2021:2022/INSA/Projet integrateur/board.jpg"));
            System.out.println("Should have saved image");
            System.out.println(result);
        } catch (IOException e) {
            e.printStackTrace();
        }
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

}
