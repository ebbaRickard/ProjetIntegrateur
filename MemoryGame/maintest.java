package MemoryGame;

import java.awt.FlowLayout;
import java.io.IOException;

import javax.swing.*;
import javax.swing.ImageIcon;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import java.awt.BorderLayout;


import java.awt.*;

public class maintest {

    public static void main(String[] args) throws IOException {
        MemoryBoard mb = new MemoryBoard(4,
                "/Users/ebbarickard/2021:2022/INSA/Projet integrateur/test");
        showBoard(mb);
        //displayImage(mb.getCard(3, 3).getImage());

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
        JPanel frameBoard = new JPanel(new GridLayout(4, 4, 10, 10));
        frameBoard.setBorder(BorderFactory.createEmptyBorder(5, 5, 5, 5));
        frameBoard.setBackground(Color.MAGENTA);
        for (int r = 0; r < mb.getSize(); r++) {
            for (int c = 0; c < mb.getSize(); c++) {
                ImageIcon icon = resizeImageIcon(new ImageIcon(mb.getCard(r, c).getImage()));
                JLabel lbl = new JLabel();
                lbl.setIcon(icon);
                frameBoard.add(lbl, r + c);
            }
        }
        System.out.println("here");

        JFrame frame = new JFrame("Memory");
        frame.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        frame.getContentPane().add(frameBoard);
        frame.pack();
        frame.setLocationByPlatform(true);
        frame.setVisible(true);
    }

    public static ImageIcon resizeImageIcon(ImageIcon imageIcon) {
        Image image = imageIcon.getImage(); 
        Image newimg = image.getScaledInstance(150, 150,  java.awt.Image.SCALE_SMOOTH); 
        return new ImageIcon(newimg);
    }
}
