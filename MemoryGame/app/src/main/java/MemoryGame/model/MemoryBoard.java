package MemoryGame.model;

import java.io.File;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Arrays;
import java.util.List;

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

        addImages(fileDirectoryName);
        background = new MemoryImage(backgroundImageFileName);

    }

    public class PairImageLabel{
        private MemoryImage image;
        private String label;

        public PairImageLabel(MemoryImage image, String label) {
            this.image = image;
            this.label = label;
        }

        public MemoryImage getImage(){
            return this.image;
        }
        public String getLabel(){
            return this.label;
        }
    }

    private void addImages(String fileDirectoryName) {
        File fileDirectory = new File(fileDirectoryName);
        ArrayList<PairImageLabel> l_image_label = new ArrayList<PairImageLabel>();
        int total_images_remaining = size*size;
        int count = 0;
        // Select random images from random directories (2 by files)
        //System.out.println("Folder open :");
        if (fileDirectory.isDirectory()) {
            List<File> folders = Arrays.asList(fileDirectory.listFiles());
            Collections.shuffle(folders);
            //File [] folders_shuffled = intList.toArray()
            for (File folder : folders) {
                //System.out.println(folder.getName());
                
                List<File> files = Arrays.asList(folder.listFiles());
                Collections.shuffle(files);
                //File [] file_shuffled = intList.toArray(Collections.shuffle(Arrays.asList()))
                count = 0;
                for (File file : files) {
                    if (isImage(file.getName())) {
                        MemoryImage img = new MemoryImage(file.getPath());
                        PairImageLabel pair_image_label = new PairImageLabel(img, folder.getName());
                        l_image_label.add(pair_image_label);
                        count++;
                    }
                    if(count>1){
                        total_images_remaining=total_images_remaining-count;
                        break;
                    }
                    
                    
                }
                if(total_images_remaining<1){
                    break;
                }
                    
            }
        }
        // Shuffle the list
        int r = 0;
        int c = 0;
        Collections.shuffle(l_image_label);
        //System.out.println("\nLabel in game order :");
        for (PairImageLabel image_label : l_image_label){
            board[r][c] = image_label.getImage();
            labels[r][c] = image_label.getLabel();
            //System.out.println(image_label.getLabel());
            if (r < size - 1) {
                r++;
            } else if (c < size - 1) {
                r = 0;
                c++;
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