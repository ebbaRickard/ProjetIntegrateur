# Import
import requests
import io
import random
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from os import listdir
from os.path import isfile, join
import os
from enum import Enum
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array

 # Create a Virtual board (no detection required)
def tempCreateRandomBoard(nb_cards:int):
    if(nb_cards%2!=0): # Check if the number of cards is even 
        raise Exception("Invalid number of cards (nb_cards={}), must be an even number".format(nb_cards))
    
    path_dir = "imageNet"

    labels_name = []
    board = []

    infos = [d for d in os.walk(path_dir)] # list all directory in given directory

    dirs = infos[0][1]
    
    for i in range(int(nb_cards/2)):
        # Selecting a random class/dir
        random_dir = random.choice(dirs)
        labels_name.append(random_dir)

        files = [f for f in listdir(f'{path_dir}/{random_dir}') if isfile(join(f'{path_dir}/{random_dir}', f))] # list all file in given directory

        # Selecting a random image
        random_file_1 = random.choice(files)
        picture1 = load_img(f'{path_dir}/{random_dir}/{random_file_1}', target_size=(224, 224))  # Extract image data
        board.append({'image':picture1,'label':random_dir})
        files.remove(random_file_1)
        
        # Selecting an another random image (the pair)
        random_file_2 = random.choice(files)
        picture2 = load_img(f'{path_dir}/{random_dir}/{random_file_2}', target_size=(224, 224))  # Extract image data
        board.append({'image':picture2,'label':random_dir})        
        files.remove(random_file_2)

        dirs.remove(random_dir)

    
    np.random.shuffle(board)
    
    print("Simulated board :\n")
    print("index : class")
    for i,card in enumerate(board): 
        print("{} : {}".format(i,card['label']))
    
    return board, labels_name

# Card classification status
class Status(Enum):
    UNKNOWN = "unknown"
    LABELED = "labeled"
    VALID = "valid"

# Card information
class Card():
    def __init__(self,index:int):
        self.status = Status.UNKNOWN
        self.index = index
        self.label = "unknown"
        self.numpy_image = None
        self.predictions = None

    def addPredictions(self,predictions):
        self.predictions = predictions
        self.label = predictions[0]['class']
        self.status = Status.LABELED
# AI
class Main_AI():
    def __init__(self,nb_cards:int,model_name:str="model_trained"):
        if(nb_cards%2!=0): # Check if the number of cards is even 
            raise Exception("Invalid number of cards (nb_cards={}), must be an even number".format(nb_cards))
        
        self.nb_cards = nb_cards
        self.memory=[Card(number) for number in range(nb_cards)]
            
    def getListIndexUnknown(self): # Return List of unknown cards
        return [card.index for card in self.memory if(card.status==Status.UNKNOWN)]
    def getListIndexRemaining(self): # Return List of remaining cards
        return [card.index for card in self.memory if(card.status!=Status.VALID)]
    def getListIndexLabeled(self): # Return List of labeled cards
        return [card.index for card in self.memory if(card.status==Status.LABELED)]
    
    # Return random index of an unknown card
    def chooseRandomUnknownCard(self): 
        unknown_list = self.getListIndexUnknown()
        if(np.size(unknown_list)==0):
            raise Exception("Error : No unknown cards remaining, can't choose one")
        return random.choice(unknown_list)

    # Return random index of an labeled card
    def chooseRandomLabeledCard(self): 
        labeled_list = self.getListIndexLabeled()
        if(np.size(labeled_list)==0):
            raise Exception("Error : No labeled cards remaining, can't choose one")
        return random.choice(labeled_list)
    
    def receiveBoard(self): # TO_IMPLEMENT Ask to the real game (ie java) to send the current board
        pass
    
     # TO_CHANGE (ask to the real game ie Java) Check if cards are the same 
    def check(self,board,card1,card2):
        return board[card1]['label'] == board[card2]['label']
                
    def turnCard(self, index_card_to_turn:int, board):  # TO_CHANGE (ask to the real game and do not show the card) Turn a card
        self.cards_turned.append(index_card_to_turn)
        self.cards_turned =  sorted(self.cards_turned)

        # TO REMOVE
        plt.imshow(board[index_card_to_turn]['image'])
        plt.show()

        # TO ADD 
        # Sending to the game
    
    # Call the service of classification for each image in images_list, save the predictions, return the labeled class
    def classifyImages(self,images_list): 
        
        labels_predicted = []

        for i,image in enumerate(images_list):
            card = self.memory[self.cards_turned[i]] # Retrieve card object 
            #card.numpy_image = image

            # Calling the API
            buf = io.BytesIO()
            image.save(buf, format='JPEG')
            byte_im = buf.getvalue()
            files={"file": ("filename",byte_im, "image/jpeg")}
            r = requests.post("http://0.0.0.0:5000/predict",files=files)
            
            predictions = r.json()['predictions']
            label_predicted = predictions[0]['class']

            card.addPredictions(predictions)
            labels_predicted.append(label_predicted)

            
            
        return labels_predicted
                
    # TO_CHANGE (Do detection instead) Return image currently turned (simule detection)
    def tempGetImages(self,board): 
        return [board[card]['image'] for card in self.cards_turned]
            
    # Check if there is the same class than index given
    def checkMatch(self,index:int): 
        if(self.memory[index].status==Status.LABELED):
            class_name = self.memory[index].label
            for i,card in enumerate(self.memory):
                if(i!=index and self.memory[i].label==class_name):
                    return i
            return -1

    # Check if there is a pair among all memory
    def checkForAnyMatch(self): 
        # Remarks : Could be optimize by only looking further in checkMatch, but checkMatch can be use by itself
        match_found = False
        for i,card in enumerate(self.memory):
            if(card.status==Status.LABELED):
                match = self.checkMatch(i)
                if(match!=-1):
                    return i,match
        return -1,-1

    # Logic for choosing the first card
    def chooseFirstCard(self): 
        index1,index2 = self.checkForAnyMatch()
        if(index1==-1): # No match yet > Choosing a random card
            return self.chooseRandomUnknownCard()
        else: # There is a possibility of a match
            print("AI think that there is a match between {} and {}".format(index1,index2))
            return index1
    
    # Logic for choosing the second card (possibility that no unknown card remaining)
    def chooseSecondCard(self): 
        index1 = self.cards_turned[0]
        index2 = self.checkMatch(index1)
        if(index2==-1): # No match yet > Choosing a random card
            # Check if it remains unknown
            if((np.size(self.getListIndexUnknown()) != 0)): # Choosing a random unknown card
                return self.chooseRandomUnknownCard()
            else: # Choosing a random labeled card
                return self.chooseRandomLabeledCard()
        else: # There is a possibility of a match 
            print("AI think that there is a match between {} and {}".format(index1,index2))
            return index2

    def stepWhenImagesLabeled(self):
        #Real implementation not implemented, random try
        list_index_remaining = self.getListIndexRemaining().copy()
        index1 = random.choice(list_index_remaining)
        list_index_remaining.remove(index1)
        index2 = random.choice(list_index_remaining)
        return index1,index2
    
    # Print the current state of the memory (ie assumption of the AI)
    def printCurrentMemory(self,board):
        for i,card in enumerate(self.memory):
            print("{}: {} instead of {} - {}".format(i,card.label,board[i]['label'],card.status))
    
    # TO_CHANGE (update with game and detection parts) Define how AI have to behave with the game
    def run(self): 
        """
        Function that define how the AI have to behave
        @desc 
            - 
        @echues remaining 
            - If 2 cards are labeled identique but they aren't the ai will try to return them infinitly (it never happen with our class/image)
            - Not connected with the game
            - Not connected with the detection
        """
        classification_finished = (np.size(self.getListIndexUnknown()) == 0)
        step = 0
        
        board,labels_name = tempCreateRandomBoard(self.nb_cards) # Create a random board
        last_card_turned = None
        while(not classification_finished): # Looping until there is no unknown card
            print(f'\n\n---------------- Step {step} ----------------\n')
            self.cards_turned = []
            
            # --- FIRST CARD ---

            # Choose first card
            index_card_to_turn_1 = self.chooseFirstCard()
            self.turnCard(index_card_to_turn_1,board)
            
            # Ask for board 
            images = self.tempGetImages(board)

            # Classify it 
            labels_predicted = self.classifyImages(images)
            print("The prediction for the first card({}) is {}".format(index_card_to_turn_1,labels_predicted[0]))

            # --- SECOND CARD ---

            # Choose second card
            index_card_to_turn_2 = self.chooseSecondCard()
            self.turnCard(index_card_to_turn_2,board)
            
            # Ask for board 
            images = self.tempGetImages(board)
            
            # Classify it 
            labels_predicted = self.classifyImages(images)
            
            print("The prediction for cards({} and {}) are {} and {}\n".format(index_card_to_turn_1,index_card_to_turn_2,labels_predicted[0],labels_predicted[1]))

            # --- CHECKER --- (check if the 2 cards are the same)

            # Check if the cards have the same class
            if(self.check(board,index_card_to_turn_1,index_card_to_turn_2)):
                self.memory[index_card_to_turn_1].status = Status.VALID
                self.memory[index_card_to_turn_2].status = Status.VALID
                print("Checker find that image are from same class\n")

            # --- FINISHING STEP --- (update informations)
            step += 1
            classification_finished = (np.size(self.getListIndexUnknown()) == 0)
            self.printCurrentMemory(board)
            if(self.cards_turned==last_card_turned): # Fixing infinite loop problem (it never happens)
                raise Exception("Error : Classification is looping into the same cards, interruption of the program... ")
            last_card_turned = self.cards_turned
        
        list_index_remaining = self.getListIndexRemaining()
        if(np.size(list_index_remaining)!=0):

            nb_images_remaining = np.size(list_index_remaining)-2
            steps_before = step
            print("\n\n Classification went wrong, we have to search for new label for remaining UNVALID pictures ...")
            print("Indexes remaining to correctly classify : ")
            print(list_index_remaining)
            print("\n\n")

            finished = (np.size(list_index_remaining) == 0)

            while(not finished):
                print(f'\n\n---------------- Step {step} ----------------\n')

                if(np.size(list_index_remaining)==2): # It must be a pair
                    index_card_to_turn_1 = list_index_remaining[0]
                    index_card_to_turn_2 = list_index_remaining[1]
                    print("Only 2 images remaining, must be the same")
                else : # Try with predictions information (Improvement : try with other classifier)
                    index_card_to_turn_1,index_card_to_turn_2 = self.stepWhenImagesLabeled()

                self.turnCard(index_card_to_turn_1,board)
                self.turnCard(index_card_to_turn_2,board)
                
                print("Turning card {} and {}".format(index_card_to_turn_1,index_card_to_turn_2))
                # Check if the cards have the same class
                if(self.check(board,index_card_to_turn_1,index_card_to_turn_2)):
                    self.memory[index_card_to_turn_1].status = Status.VALID
                    self.memory[index_card_to_turn_2].status = Status.VALID
                    print("\nChecker find that image are from same class")

                # Update informations
                self.printCurrentMemory(board)
                list_index_remaining = self.getListIndexRemaining()
                finished = (np.size(list_index_remaining) == 0)
                step+=1
        else:
            nb_images_remaining = 0
            steps_before = step

        print("\n{} images correctly classified in {} steps \n(after it was random guess)\n".format(self.nb_cards-nb_images_remaining,steps_before))
    
        print("\n\nGame finished in {} steps".format(step))    

