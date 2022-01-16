package MemoryGame.model;

import javax.imageio.ImageIO;

import java.awt.*;
import java.io.File;
import java.io.IOException;

public class MemoryImage {
    private Image image;

    public MemoryImage(String fileName) {
        try {
            image = ImageIO.read(new File(fileName));
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public Image getImage() {
        return image;
    }
}