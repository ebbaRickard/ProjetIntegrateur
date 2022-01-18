package MemoryGame.model;

import java.io.File;

// class should return an image of the board consisting of size x size memory bricks
// takes the board size as input
// keeps track of the status of the board (flipped cards, pairs already made)

public class MemoryBoard {

    private MemoryImage[][] board;
    private String[][] labels;
    private MemoryImage background;
    private boolean[][] boardStatus;
    private int size;

    public MemoryBoard(int size, String fileDirectoryName, String backgroundImageFileName) {
        this.size = size;

        board = new MemoryImage[size][size];
        boardStatus = new boolean[size][size];
        labels = new String[size][size];

        boardStatus[0][0] = true;
        boardStatus[0][1] = true;
        boardStatus[0][2] = true;
        boardStatus[1][1] = true;
        boardStatus[2][2] = true;

        addImages(fileDirectoryName);
        background = new MemoryImage(backgroundImageFileName);

    }

    private void addImages(String fileDirectoryName) {
        File fileDirectory = new File(fileDirectoryName);
        if (fileDirectory.isDirectory()) {
            int r = 0;
            int c = 0;
            int count = 0;
            while (r < size - 1 && c < size - 1) {
                for (File folder : fileDirectory.listFiles()) {
                        for (File file : folder.listFiles()) {
                            if (isImage(file.getName())) {
                                
                                if (count == 2) {
                                    count = 0;
                                    break;
                                }
                                MemoryImage img = new MemoryImage(file.getPath());
                                board[r][c] = img;
                                labels[r][c] = folder.getName();
                                System.out.println(folder.getName());

                                if (r < size - 1) {
                                    r++;
                                } else if (c < size - 1) {
                                    r = 0;
                                    c++;
                                }
                                count++;
                            
                        }
                    }
                }

            }
        }
    }

    // To find the labels in the fruit data set
    private String findLabel(String filepath) {
        return filepath.split("_")[0];
    }

    private boolean isImage(String fileName) {
        int i = fileName.lastIndexOf('.');
        String extension = "";
        if (i > 0) {
            extension = fileName.substring(i + 1);
        }
        return extension.equals("JPEG");
    }

    public int getSize() {
        return size;
    }

    public MemoryImage getCard(int r, int c) {
        return board[r][c];
    }

    public MemoryImage getBackGround() {
        return background;
    }

    public void flipCard(int r, int c) {
        boardStatus[r][c] = !boardStatus[r][c];
    }

    public boolean isFlipped(int r, int c) {
        return boardStatus[r][c];
    }

    public boolean isPair(int r1, int c1, int r2, int c2) {
        System.out.println(labels[r1][c1]);
        System.out.println(labels[r2][c2]);
        return labels[r1][c1].equals(labels[r2][c2]);
    }

}