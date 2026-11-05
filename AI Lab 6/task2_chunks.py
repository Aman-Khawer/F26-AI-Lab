import re


# 1. Three synthetic documents

docs = {

    "handbook": """University assignments should normally be submitted through the learning portal before the deadline shown on the course page. Late submissions are normally penalized, but students who become ill before a deadline may request an extension if they contact the coordinator before the deadline and provide medical evidence. The illness exception does not automatically approve an extension, and students should wait for written confirmation before relying on a new date. If the portal is unavailable, students should take a screenshot of the error and email the course coordinator with the assignment attached before the deadline. The coordinator can confirm whether the submission time will be adjusted. Students should keep the original assignment file and the confirmation email until the result is recorded. Files should be uploaded as PDF unless the instructor has specified another format. The file name should include the course code and student ID, but passwords and private account details must never be included. Students can check the portal receipt to confirm that an upload was successful. If no receipt appears, they should contact the help desk promptly. These instructions are synthetic examples for a classroom exercise and are not actual university policy.""",

    "it_help": """Students who cannot access their learning account should first check that the username is typed correctly and that the internet connection is working. A forgotten password can be reset by selecting the recovery link on the sign-in page and following the instructions sent to the registered email address. The recovery link is intended for the account owner and should not be forwarded to another person. If the registered email address is no longer available, the student should contact the IT help desk and provide the required identity information through the approved support process. Never send a password, one-time code, or recovery code in an ordinary email or chat message. The help desk may ask for the student's name, course code, and a short description of the problem, but it should not ask the student to reveal their password. During a service outage, students should wait for the official status update and avoid repeatedly submitting password requests. When access is restored, users should sign in and check that their profile details are correct. These steps are synthetic teaching material. They demonstrate how an instruction and its safety exception should remain together when a document is divided into smaller chunks.""",

    "printer_guide": """A printer that produces blank pages may have an empty ink or toner supply, an incorrectly installed cartridge, or a blocked print head. First, check the printer display for a supply warning and confirm that the paper is loaded correctly. If the supply is low, follow the device manual before replacing any cartridge. Next, use the printer's built-in cleaning utility and print one test page to check whether the problem has improved. Do not open electrical covers or touch hot internal parts while the printer is operating. If the test page is still blank, check that the correct printer is selected in the computer's print settings and that the document itself contains visible text. For a shared printer, ask the equipment supervisor before changing network or administrator settings. Record the printer model and the error message before requesting support. A long troubleshooting sentence can contain several connected conditions, so a simple sentence splitter may need to divide it when it exceeds the selected word budget. This guide is synthetic classroom data and does not replace the manufacturer's instructions."""
}


# 2. Find the position of every word

def word_spans(text):

    spans = []

    for match in re.finditer(r"\S+", text):
        spans.append((match.start(), match.end()))

    return spans


# 3. Fixed word chunks

def windows(text, size=40, overlap=0, offset=0):

    if size <= 0 or overlap < 0 or overlap >= size:
        raise ValueError("Invalid size or overlap")

    spans = word_spans(text)

    chunks = []

    step = size - overlap

    for i in range(0, len(spans), step):

        j = min(i + size, len(spans))

        start = offset + spans[i][0]
        end = offset + spans[j - 1][1]

        chunks.append((start, end))

        if j == len(spans):
            break

    return chunks


# 4. Sentence-aware chunking

def sentence_chunks(text, size=40):

    if size <= 0:
        raise ValueError("Size must be positive")

    cuts = [0]

    # Find sentence boundaries
    for match in re.finditer(r"[.!?]\s+", text):
        cuts.append(match.end())

    cuts.append(len(text))

    chunks = []

    pending = None
    count = 0

    for a, b in zip(cuts, cuts[1:]):

        sentence = text[a:b]
        words = len(sentence.split())

        if words == 0:
            continue

        # Split a sentence if it is longer than 40 words
        if words > size:

            if pending is not None:
                chunks.append(pending)

            chunks.extend(windows(sentence, size, 0, a))

            pending = None
            count = 0

        # Add sentence to the current chunk if space is available
        elif pending is not None and count + words <= size:

            pending = (pending[0], b)
            count = count + words

        else:

            if pending is not None:
                chunks.append(pending)

            pending = (a, b)
            count = words

    if pending is not None:
        chunks.append(pending)

    return chunks


# 5. Create chunks with IDs and source information

def make_chunks(docs, strategy):

    result = []

    for doc_id, text in docs.items():

        if strategy == "0":
            spans = windows(text, 40, 0)

        elif strategy == "10":
            spans = windows(text, 40, 10)

        elif strategy == "sentence":
            spans = sentence_chunks(text, 40)

        else:
            raise ValueError("Invalid chunking strategy")

        for i, (start, end) in enumerate(spans):

            chunk = {
                "id": doc_id + ":" + str(i),
                "doc": doc_id,
                "source": doc_id + ".txt",
                "start": start,
                "end": end,
                "text": text[start:end]
            }

            result.append(chunk)

    return result


# 6. Check document word counts

print("DOCUMENT WORD COUNTS")

for doc_id, text in docs.items():

    total_words = len(text.split())

    print(doc_id, ":", total_words, "words")

    assert 150 <= total_words <= 250


# 7. Compare all three chunking methods

for strategy in ["0", "10", "sentence"]:

    chunks = make_chunks(docs, strategy)

    print("\n")
    print("STRATEGY:", strategy)
    print("Total chunks:", len(chunks))

    for doc_id, text in docs.items():

        doc_chunks = [c for c in chunks if c["doc"] == doc_id]

        original_words = len(text.split())

        chunk_words = sum(
            len(c["text"].split()) for c in doc_chunks
        )

        repeated_words = chunk_words - original_words

        sizes = [len(c["text"].split()) for c in doc_chunks]

        print("\nDocument:", doc_id)
        print("Chunk count:", len(doc_chunks))
        print("Smallest chunk:", min(sizes))
        print("Largest chunk:", max(sizes))
        print("Repeated words:", repeated_words)

    # Display chunk details

    for chunk in chunks:

        print("\nChunk ID:", chunk["id"])
        print("Source:", chunk["source"])
        print("Start:", chunk["start"])
        print("End:", chunk["end"])
        print("Text:", chunk["text"])


# 8. Check rule and exception

evidence = (
    "Late submissions are normally penalized, but students who become "
    "ill before a deadline may request an extension if they contact "
    "the coordinator before the deadline and provide medical evidence."
)

print("\nRULE AND EXCEPTION TEST")

for strategy in ["0", "10", "sentence"]:

    chunks = make_chunks(docs, strategy)

    found = False

    for chunk in chunks:

        if evidence in chunk["text"]:
            found = True
            break

    print(strategy, ":", found)


# 9. Edge-case tests

print("\nEDGE CASE TESTS")

# Empty text
print("Empty text:", windows(""))

# Short document
print("Short document:", windows("This is a short document."))

# Invalid overlap
try:

    windows("one two three", 40, 40)

except ValueError:

    print("Invalid overlap test passed.")


# Long sentence
long_sentence = " ".join(["word"] * 95) + "."

long_chunks = sentence_chunks(long_sentence, 40)

print("Long sentence chunks:", len(long_chunks))

for start, end in long_chunks:

    print("Words:", len(long_sentence[start:end].split()))


# 10. Check sentence splitting limitation

example = "Dr. Aman submitted the assignment. The teacher checked it."

print("\nABBREVIATION TEST")

for start, end in sentence_chunks(example, 40):

    print(repr(example[start:end]))


# 11. Final automatic checks

print("\nFINAL CHECKS")

for strategy in ["0", "10", "sentence"]:

    chunks = make_chunks(docs, strategy)

    for chunk in chunks:

        original = docs[chunk["doc"]]

        # Check source offsets
        assert chunk["text"] == original[chunk["start"]:chunk["end"]]

        # Check chunk size
        assert len(chunk["text"].split()) <= 40

        # Check that chunks are not empty
        assert chunk["text"].strip() != ""

print("All chunking tests passed.")