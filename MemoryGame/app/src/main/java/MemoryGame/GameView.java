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

    private JPanel frameBoard;
    private JFrame frame;

    public GameView(MemoryBoard mb) throws IOException {
        createWindow();
        updateWindow(mb);
    }

    public void createWindow() {
        frameBoard = new JPanel(new GridLayout(BOARDSIZE, BOARDSIZE, 10, 10));
        frameBoard.setBorder(BorderFactory.createEmptyBorder(PADDING, PADDING, PADDING, PADDING));
        frameBoard.setBackground(Color.MAGENTA);
        frame = new JFrame("Memory");
        frame.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        frame.getContentPane().add(frameBoard);
        frame.pack();
        frame.setLocationByPlatform(true);
        
    }

    public void updateWindow(MemoryBoard mb) throws IOException {
        frameBoard.removeAll();
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

        
        frame.pack();
        frame.setVisible(true);

        SaveBoardImage(frameBoard);
    }

    private ImageIcon resizeImageIcon(ImageIcon imageIcon) {
        Image image = imageIcon.getImage();
        Image newimg = image.getScaledInstance(150, 150, java.awt.Image.SCALE_SMOOTH);
        return new ImageIcon(newimg);
    }

    public void SaveBoardImage(JPanel component) {
        Dimension d = component.getSize();
        BufferedImage image = new BufferedImage(d.width, d.height, BufferedImage.TYPE_INT_RGB);
        Graphics2D g2d = image.createGraphics();
        component.print(g2d);
        g2d.dispose();
        try {
            boolean result = ImageIO.write(image, "jpg",
                    new File("../../../../../../board.jpg"));
            System.out.println(result);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private void displayImage(Image image) throws IOException {
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
