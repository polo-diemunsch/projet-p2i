l_freq = [261.626, 277.183, 293.665, 311.127, 329.628, 349.228, 369.994, 391.995, 415.305, 440, 466.164, 493.883, 
          523.251, 554.365, 587.33, 622.254, 659.255, 698.456, 739.989, 783.991, 830.609, 880, 932.328, 987.767, 1046.5] 

l_notes = ['Do3', 'Do#3', 'Re3', 'Re#3', 'Mi3', 'Fa3', 'Fa#3', 'Sol3', 'Sol#3', 'La3', 'La#3', 'Si3'
           'Do4', 'Do#4', 'Re4', 'Re#4', 'Mi4', 'Fa4', 'Fa#4', 'Sol4', 'Sol#4', 'La4', 'La#4', 'Si4', 'Do5']

notes = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5', 'D5', 'E5', 'F5', 'G5', 'A5', 'B5', 'C6', 'Db4', 'Eb4', 'Gb4', 'Ab4', 'Bb4', 'Db5', 'Eb5', 'Gb5', 'Ab5', 'Bb5']


def idNote_from_frequency(frequency):
    """
    Donne l'identifiant de la note en fonction de la fréquence
    """
    ecart, indice = 1000, 0
    for i in range(len(l_freq) - 1):
        if l_freq[i] <= frequency and l_freq[i+1] >= frequency:
            ecart = min(abs(l_freq[i] - frequency), abs(l_freq[i+1] - frequency))
            if abs(l_freq[i] - frequency):
                indice = i
            else:
                indice = i+1
    return indice


def note_from_idNote(idNote):
    """
    Donne la note en fonction de son identifiant
    """
    return l_notes[idNote - 1]


def note_from_frequency(frequency):
    """
    Donne la note en fonction de la fréquence
    """
    return note_from_idNote(idNote_from_frequency(frequency))


frequency = 440
