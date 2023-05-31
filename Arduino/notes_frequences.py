freq = [261.626, 293.665, 329.628, 349.228, 391.995, 440, 493.883, 523.251, 587.33, 659.255, 698.456, 783.991, 880,
        987.767, 1046.5, 277.183, 311.127, 369.994, 415.305, 466.164, 554.365, 622.254, 739.989, 830.609, 932.328]

# l_notes = ['Do3', 'Do#3', 'Re3', 'Re#3', 'Mi3', 'Fa3', 'Fa#3', 'Sol3', 'Sol#3', 'La3', 'La#3', 'Si3'
#            'Do4', 'Do#4', 'Re4', 'Re#4', 'Mi4', 'Fa4', 'Fa#4', 'Sol4', 'Sol#4', 'La4', 'La#4', 'Si4', 'Do5']

notes = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5', 'D5', 'E5', 'F5', 'G5', 'A5', 'B5', 'C6', 'Db4', 'Eb4', 'Gb4',
         'Ab4', 'Bb4', 'Db5', 'Eb5', 'Gb5', 'Ab5', 'Bb5']


def id_note_from_frequency(frequency):
    """
    Donne l'identifiant de la note en fonction de la fréquence
    """
    ecart_min, id_note = float("inf"), -1
    for i in range(len(freq)):
        ecart = abs(freq[i] - frequency)

        if ecart < ecart_min:
            ecart_min = ecart
            id_note = i

    return id_note


def note_from_id_note(id_note):
    """
    Donne la note en fonction de son identifiant
    """
    return notes[id_note]


def note_from_frequency(frequency):
    """
    Donne la note en fonction de la fréquence
    """
    return note_from_id_note(id_note_from_frequency(frequency))
