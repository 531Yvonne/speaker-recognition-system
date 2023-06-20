import sys
from markov import identify_speaker

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print(
            f"Usage: python3 {sys.argv[0]} <filenameA> <filenameB> <filenameC> <k> <hashtable-or-dict>"
        )
        sys.exit(1)

    # extract parameters from command line & convert types
    filenameA, filenameB, filenameC, k, hashtable_or_dict = sys.argv[1:]
    k = int(k)
    if hashtable_or_dict not in ("hashtable", "dict"):
        print("Final parameter must either be 'hashtable' or 'dict'")
        sys.exit(1)

    # open files & read text
    with open(filenameA, "r") as f1:
        text1 = f1.read()

    with open(filenameB, "r") as f2:
        text2 = f2.read()

    with open(filenameC, "r") as f3:
        text3 = f3.read()

    # call identify_speaker & print results
    if hashtable_or_dict == "hashtable":
        result = identify_speaker(text1, text2, text3, k, True)
    else:
        result = identify_speaker(text1, text2, text3, k, False)

    # Output resembles (values will differ based on inputs):

    # Speaker A: -2.1670591295191572
    # Speaker B: -2.2363636778055525

    # Conclusion: Speaker A is most likely

    print(f"Speaker A: {result[0]}")
    print(f"Speaker B: {result[1]}")
    print()
    print(f"Conclusion: Speaker {result[2]} is most likely")
