package MemoryGame;

import java.io.File;

public class MemoryBoard {

    private MemoryImage[][] board;
    private int size;

    public MemoryBoard(int size, String fileDirectoryName) {
        this.size = size;
        board = new MemoryImage[size][size];
        addImages(fileDirectoryName);
    }

    private void addImages(String fileDirectoryName) {
        File fileDirectory = new File(fileDirectoryName);
        if (fileDirectory.isDirectory()) {
            int r = 0;
            int c = 0;
            while (r < size - 1 && c < size - 1) {
                for (File file : fileDirectory.listFiles()) {
                    if (isImage(file.getName())) {
                        System.out.println(file.getPath());
                        MemoryImage img = new MemoryImage(file.getPath());
                        board[r][c] = img;

                        if (r < size - 1) {
                            r++;
                        } else if (c < size - 1) {
                            r = 0;
                            c++;
                        }
                        System.out.println(r);
                        System.out.println(c);
                    }
                }
            }

        }
    }

    private boolean isImage(String fileName) {
        int i = fileName.lastIndexOf('.');
        String extension = "";
        if (i > 0) {
            extension = fileName.substring(i + 1);
        }
        return extension.equals("jpg");
    }

    public int getSize() {
        return size;
    }

    public MemoryImage getCard(int r, int c) {
        return board[r][c];
    }

}