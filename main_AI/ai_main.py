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


# Card classification status
class Status(Enum):
    UNKNOWN = "unknown"
    LABELED = "labeled"
    VALID = "valid"

# Card information
class Card():
    def __init__(self,index:int,card_by_line:int):
        self.status = Status.UNKNOWN
        self.index = index
        self.position = [int(index/card_by_line),index%card_by_line]
        self.label = "unknown"
        self.numpy_image = None
        self.predictions = None

    def addPredictions(self,predictions):
        self.predictions = predictions
        self.label = predictions[0]['class']
        self.status = Status.LABELED

    def removeGuess(self):
        for class_id in self.predictions:
            if(class_id['class']==self.label):
                self.predictions.remove(class_id)
        self.label = self.predictions[0]['class']

# AI
class Main_AI():
    def __init__(self,nb_cards:int,card_by_line:int,verbose:bool=True):
        if(nb_cards%2!=0): # Check if the number of cards is even 
            raise Exception("Invalid number of cards (nb_cards={}), must be an even number".format(nb_cards))
        
        self.nb_cards = nb_cards
        self.memory=[Card(number,card_by_line) for number in range(nb_cards)]
        self.verbose = verbose

    def getListIndexUnknown(self): # Return List of unknown cards
        return [card.index for card in self.memory if(card.status==Status.UNKNOWN)]
    def getListIndexRemaining(self): # Return List of remaining cards
        return [card.index for card in self.memory if(card.status!=Status.VALID)]
    def getListIndexLabeled(self): # Return List of labeled cards
        return [card.index for card in self.memory if(card.status==Status.LABELED)]
    def getListIndexValid(self): # Return List of labeled cards
        return [card.index for card in self.memory if(card.status==Status.VALID)]
    
    
    def getListCardTurned(self):
        return [card for card in self.memory if(card.status==Status.VALID or card.index in self.cards_turned)]

    # Return True if the num (corresponding to index of array of returned card) is valid
    def checkNumValid(self,num,image):
        list_card_turned = self.getListCardTurned()
        if(num>=np.size(list_card_turned)):
            print("Problem detection ...")
            plt.imshow(image)
            plt.show()
            return True
        if(list_card_turned[num].status==Status.VALID):
            return True
        else: return False
    
    
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

    # Communication with the memory Game    
    # Ask to the real game (ie java) to send the current board
    def receiveBoard(self): 
        response = requests.get("http://localhost:8080/getBoard")
        board_image_byte  = response.content
        board_image = Image.open(io.BytesIO(board_image_byte))
        plt.imshow(board_image)
        plt.show()
        return board_image_byte
    
    # Ask to the real game (ie java) if the pair is valid 
    def check(self,i_card1,i_card2):
        card1 = self.memory[i_card1]
        card2 = self.memory[i_card2]
        response = requests.get("http://localhost:8080/isPair/{}{}{}{}".format(card1.position[0],card1.position[1],card2.position[0],card2.position[1]))
        b_response = response.content
        if(b_response==b'true'):
            check = True
        else:
            check = False
        return check
    
     # Ask game ie Java to turn a card
    def turnCard(self, index_card_to_turn:int): 
        self.cards_turned.append(index_card_to_turn)
        self.cards_turned = sorted(self.cards_turned)

        card = self.memory[index_card_to_turn]

        requests.get("http://localhost:8080/turnCard/{}{}".format(card.position[0],card.position[1]))
        
    # Communication with classification API
    # Call the service of classification for each image in images_list, save the predictions, return the labeled class
    def classifyImages(self,images_list): 
        
        labels_predicted = []

        for i,image_data in enumerate(images_list):
            card = self.memory[self.cards_turned[i]] # Retrieve card object 
            #card.numpy_image = image

            # Calling the API
            buf = io.BytesIO()
            image = Image.fromarray(np.array(image_data).astype('uint8'), 'RGB')
            

            image.save(buf, format='JPEG')
            byte_im = buf.getvalue()
            files={"file": ("filename",byte_im, "image/jpeg")}
            r = requests.post("http://localhost:5000/predict",files=files)
            
            predictions = r.json()['predictions']
            label_predicted = predictions[0]['class']

            card.addPredictions(predictions)
            labels_predicted.append(predictions)

        return labels_predicted
    
    # Communication with detection API
    # Call detection to get all returned cards
    def detection(self,board_image_byte): 
        buf = io.BytesIO()
        file={"file": ("filename",board_image_byte, "image/jpg")}
        r = requests.post("http://localhost:5001/detection",files=file)
        r=r.json()

        images_card_turned = []
        num = 0
        for (data,n) in zip(r["detection"],range(len(r["detection"]))):
            image = data[f"image{n:04d}"]
            if(not(self.checkNumValid(num,image))):
                plt.imshow(image)
                plt.show()
                images_card_turned.append(image)
            num +=1

        return images_card_turned
            
    # Check if there is the same class than index given
    def checkMatch(self,index:int): 
        if(self.memory[index].status==Status.LABELED):
            for class_id in self.memory[index].predictions:
                class_name = class_id['class']
                for i,card in enumerate(self.memory):
                    if(i!=index and card.status==Status.LABELED):
                        for class_id_2 in card.predictions:
                            class_name_2 = class_id_2['class']
                            if(class_name_2==class_name):
                                card.label = class_name
                                self.memory[index].label = class_name
                                if self.verbose: print("AI think that there is a match between {} and {} ({})".format(index,i,class_name))
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
            return self.chooseRandomUnknownCard(),False
        else: # There is a possibility of a match
            
            return index1,True
    
    # Logic for choosing the second card (possibility that no unknown card remaining)
    def chooseSecondCard(self): 
        index1 = self.cards_turned[0]
        index2 = self.checkMatch(index1)
        if(index2==-1): # No match yet > Choosing a random card
            # Check if it remains unknown
            if((np.size(self.getListIndexUnknown()) != 0)): # Choosing a random unknown card
                return self.chooseRandomUnknownCard(),False
            else: # Choosing a random labeled card
                return self.chooseRandomLabeledCard(),False
        else: # There is a possibility of a match 
            return index2,True

    def stepWhenImagesLabeled(self):
        #Real implementation not implemented, random try
        list_index_remaining = self.getListIndexRemaining().copy()
        index1 = list_index_remaining[0]
        list_index_remaining.remove(index1)
        index2 = random.choice(list_index_remaining)
        while(index2 in self.tested_choice):
            index2 = random.choice(list_index_remaining)
        
        self.tested_choice.append(index2)
        return index1,index2
    
    # Print the current state of the memory (ie assumption of the AI)
    def printCurrentMemory(self):
        for i,card in enumerate(self.memory):
            print("{}: {} - {}".format(i,card.label,card.status))
    
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
        
        last_card_turned = None
        while(not classification_finished): # Looping until there is no unknown card
            if self.verbose:print(f'\n\n---------------- Step {step} ----------------\n')
            self.cards_turned = []
            # --- FIRST CARD ---

            # Choose first card
            index_card_to_turn_1,found = self.chooseFirstCard()
            if(self.verbose): print("AI decided to return card {}".format(index_card_to_turn_1))
            self.turnCard(index_card_to_turn_1)
            
            if(not(found)):
                # Ask for board
                board_image_byte = self.receiveBoard()
                images = self.detection(board_image_byte)

                # Classify it 
                labels_predicted = self.classifyImages(images)
        
                if self.verbose:
                    print("The prediction for the first card {} is :".format(index_card_to_turn_1))
                    print("{}\n".format(labels_predicted[0]))

            # --- SECOND CARD ---

            # Choose second card
            index_card_to_turn_2,found = self.chooseSecondCard()
            if(self.verbose): print("AI decided to return card {}".format(index_card_to_turn_2))
            self.turnCard(index_card_to_turn_2)
            
            
            if(not(found)):
                # Ask for board 
                board_image = self.receiveBoard()
                images = self.detection(board_image)
                
                # Classify it 
                labels_predicted = self.classifyImages(images)
            
                if self.verbose:
                    print("The predictions are : ")
                    print("{} : {}".format(self.cards_turned[0],labels_predicted[0]))
                    print("{} : {}\n".format(self.cards_turned[1],labels_predicted[1]))

            # --- CHECKER --- (check if the 2 cards are the same)

            # Check if the cards have the same class
            if(self.check(index_card_to_turn_1,index_card_to_turn_2)):
                self.memory[index_card_to_turn_1].status = Status.VALID
                self.memory[index_card_to_turn_2].status = Status.VALID
                if self.verbose:
                    print("Checker find that images {} are from same class\n".format(self.cards_turned))
                    if(not(found)):
                        print("Find a pair randomly")
            elif(found):
                self.memory[index_card_to_turn_1].removeGuess()
                self.memory[index_card_to_turn_2].removeGuess()
                if self.verbose: print("It was an incorrect prediction")

            # --- update informations ---
            step += 1
            classification_finished = (np.size(self.getListIndexUnknown()) == 0 and self.checkForAnyMatch()==(-1,-1))
            if self.verbose:self.printCurrentMemory()

        
        
        
        
        
        
        
        
        
        
        # TO IMPROVE - Finishing game randomly if no relation between prediction can be found
        list_index_remaining = self.getListIndexRemaining()
        if(np.size(list_index_remaining)!=0):

            nb_images_remaining = np.size(list_index_remaining)-2
            steps_before = step
            if self.verbose:
                print("\n\n Classification went wrong, we have to search for new label for remaining UNVALID pictures ...")
                print("Indexes remaining to correctly classify : ")
                print(list_index_remaining)
                print("\n\n")

            finished = (np.size(list_index_remaining) == 0)
            self.tested_choice = []
            while(not finished):
                
                if self.verbose:print(f'\n\n---------------- Step {step} ----------------\n')
                # TODO : Create an 
                if(np.size(list_index_remaining)==2): # It must be a pair
                    index_card_to_turn_1 = list_index_remaining[0]
                    index_card_to_turn_2 = list_index_remaining[1]
                    if self.verbose:print("Only 2 images remaining, must be the same")
                else : # Try with predictions information (Improvement : try with other classifier)
                    index_card_to_turn_1,index_card_to_turn_2 = self.stepWhenImagesLabeled()

                self.turnCard(index_card_to_turn_1)
                self.turnCard(index_card_to_turn_2)
                
                if self.verbose:print("Turning card {} and {}".format(index_card_to_turn_1,index_card_to_turn_2))
                # Check if the cards have the same class
                if(self.check(index_card_to_turn_1,index_card_to_turn_2)):
                    self.memory[index_card_to_turn_1].status = Status.VALID
                    self.memory[index_card_to_turn_2].status = Status.VALID
                    self.tested_choice = []
                    if self.verbose:print("\nChecker find that image are from same class")

                # Update informations
                if self.verbose:self.printCurrentMemory()
                list_index_remaining = self.getListIndexRemaining()
                finished = (np.size(list_index_remaining) == 0)
                step+=1
        else:
            nb_images_remaining = 0
            steps_before = step

        if self.verbose:print("\n{} images correctly classified in {} steps \n(after it was random guess)\n".format(self.nb_cards-nb_images_remaining,steps_before))
    
        if self.verbose:print("\n\nGame finished in {} steps".format(step))   
	    
        return(self.nb_cards-nb_images_remaining)

