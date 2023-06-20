from hashtable import Hashtable
import math


HASH_CELLS = 57
TOO_FULL = 0.5
GROWTH_RATIO = 2


class Markov:
    def __init__(self, k, text, use_hashtable):
        """
        Construct a new k-order markov model using the text 'text'.
        """
        self.k = k
        self.text = text
        self.use_hashtable = use_hashtable
        self.model = self.build_model()
        # Get S in likelihood calculation formula
        self.unique_char = len(set(text))

    def build_model(self):
        '''Build the model table based on given text, k and use_hashtable'''
        if self.use_hashtable:
            # use_hashtable is true, use customized Hashtable type
            model = Hashtable(HASH_CELLS, 0, TOO_FULL, GROWTH_RATIO)
        else:
            # use_hashtable is false, use built in dict
            model = {}

        text_length = len(self.text)
        extended_text = self.text + self.text[:self.k]
        for i in range(text_length):
            # Generate K, K+1 String starts from index i.
            j = i + self.k
            k_string = extended_text[i:j]
            kplus1_string = k_string + extended_text[j]
            # Update k string occurence count in model
            if k_string in model:
                model[k_string] += 1
            else:
                model[k_string] = 1
            # Update k+1 string occurence count in model.
            if kplus1_string in model:
                model[kplus1_string] += 1
            else:
                model[kplus1_string] = 1
        return model

    def log_probability(self, s):
        """
        Get the log probability of string "s", given the statistics of
        character sequences modeled by this particular Markov model
        This probability is *not* normalized by the length of the string.
        """
        result = 0
        s_length = len(s)
        extended_s = s + s[:self.k]
        for i in range(s_length):
            # Generate K, K+1 String starts from index i.
            j = i + self.k
            k_string = extended_s[i:j]
            kplus1_string = k_string + extended_s[j]
            # Get M in likelihood calculation formula
            if self.use_hashtable is False and kplus1_string not in self.model:
                m = 0
            else:
                m = self.model[kplus1_string]
            # Get N in likelihood calculation formula
            if self.use_hashtable is False and k_string not in self.model:
                n = 0
            else:
                n = self.model[k_string]
            # Calculate probability using formula log((M + 1)/(N + S))
            result += math.log((m + 1)/(n + self.unique_char))
        return result


def identify_speaker(speech1, speech2, speech3, k, use_hashtable):
    """
    Given sample text from two speakers (1 and 2), and text from an
    unidentified speaker (3), return a tuple with the *normalized* log
    probabilities
    of each of the speakers uttering that text under a "order" order
    character-based Markov model, and a conclusion of which speaker
    uttered the unidentified text based on the two probabilities.
    """
    # Generate models for speech 1 and 2.
    model1 = Markov(k, speech1, use_hashtable)
    model2 = Markov(k, speech2, use_hashtable)
    # Obtain normalized log probabilities.
    normal_1 = model1.log_probability(speech3) / len(speech3)
    normal_2 = model2.log_probability(speech3) / len(speech3)
    # Compare and get result.
    if normal_1 > normal_2:
        possible_speaker = "A"
    else:
        possible_speaker = "B"
    return (normal_1, normal_2, possible_speaker)
