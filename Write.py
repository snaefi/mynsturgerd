import numpy as np

def with_komma(letter, size = "small"):
    """
    Adds a komma to a letter. The letter is a numpy array.
    size="small" adds a small komma, size="big" adds a large komma.
    """
    if size=="big":
        komma = np.array([
                    [0,0,1],
                    [0,1,1],
                    [1,1,0],
                    [0,0,0]
                    ])
    else:
        komma = np.array([
                        [0,0,1],
                        [0,1,0],
                        [0,0,0]
                        ])
        
    m = letter.shape[1]
    if m//2 != 0:
        w = int((m-3)/2)
        boarder = np.zeros((komma.shape[0],w))
        komma = np.hstack((boarder,komma,boarder))
    else:
        w = int((m-3-1)/2)
        komma = np.hstack((np.zeros((komma.shape[0],w)),komma,np.zeros((komma.shape[0],w+1))))
    
    letter = np.vstack((komma,letter))
    return letter



def write(letters, str, align="left",newline="˚", letter_spacing=0):
    """
    Use: write_matrix = write(letters,str, align, newline)
    Pre: str is the string to be written out, letters is a dictionary where each
         symbol in str is a key and its value is a numpy matrix of the letter.
         align can either be "left" or "middle" and determines the way the text is aligned.
         newline is the symbol that defines a new line in text i.e. in str each symbol after
         a newline symbol is written in the next line.
    Post: write_matrix is a pattern matrix where the string str has been written out with the font 
          provided in the letters dictionary.
    """
    max_height = 0
    for k in letters.keys():
        if letters[k].shape[0] > max_height:
            max_height = letters[k].shape[0]

    written = np.zeros((max_height,1))
    keep = np.zeros((max_height,1))
    for i in str:
        if i == newline:
            if keep.shape[0] == 1 :
                keep = written
            else: 
                l = keep.shape[1]
                k = written.shape[1]
                if l > k:
                    if align=="middle":
                        if (l-k)%2 == 0:
                            boarder = np.zeros((written.shape[0],int((l-k)/2)))
                            written = np.hstack((boarder,written,boarder))
                        else: 
                            boarder_l = np.zeros((written.shape[0],int((l-k-1)/2)))
                            boarder_r = np.zeros((written.shape[0],int((l-k-1)/2+1)))
                            written = np.hstack((boarder_l,written,boarder_r))
                    else:
                        written = np.hstack((written,np.zeros((written.shape[0],l-k))))
                if k > l:
                    if align=="middle":
                        if (k-l)%2 == 0:
                            boarder =np.zeros((keep.shape[0],int((k-l)/2)))
                            keep = np.hstack((boarder,keep,boarder))
                        else:
                            boarder_l = np.zeros((keep.shape[0],int((k-l-1)/2)))
                            boarder_r = np.zeros((keep.shape[0],int((k-l-1)/2+1)))
                            keep = np.hstack((boarder_l,keep,boarder_r))
                    else:

                        keep = np.hstack((keep,np.zeros((keep.shape[0],k-l))))

                keep = np.vstack((keep,np.zeros((2,keep.shape[1])),written))

            written = np.zeros((max_height,1))
        else:
            add_height = max_height - letters[i].shape[0]
            letter = np.vstack((np.zeros((add_height,letters[i].shape[1])),letters[i]))
            if letter_spacing > 0:
                letter = np.hstack((np.zeros((letter.shape[0],letter_spacing)),letter))
            written = np.hstack((written,letter))
    
    if np.any(keep):
        written = keep

    written = np.hstack((written,np.zeros((written.shape[0],1))))
    return written
