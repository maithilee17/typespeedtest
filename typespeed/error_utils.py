import difflib

def highlight_word_errors(expected_word, typed_word):
    matcher = difflib.SequenceMatcher(None, expected_word, typed_word)
    highlighted_expected = ""
    highlighted_typed = ""
    mistake_positions = []

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'equal':
            highlighted_expected += expected_word[i1:i2]
            highlighted_typed += typed_word[j1:j2]
        elif tag == 'replace':
            mistake_positions.extend(list(range(i1 + 1, i2 + 1)))
            highlighted_expected += f"**{expected_word[i1:i2]}**"
            highlighted_typed += f"**{typed_word[j1:j2]}**"
        elif tag == 'delete':
            mistake_positions.extend(list(range(i1 + 1, i2 + 1)))
            highlighted_expected += f"**{expected_word[i1:i2]}**"
        elif tag == 'insert':
            mistake_positions.append(i1 + 1)
            highlighted_typed += f"**{typed_word[j1:j2]}**"

    return mistake_positions, highlighted_expected, highlighted_typed


def generate_user_friendly_errors(expected_sentence, typed_sentence):
    expected_words = expected_sentence.split()
    typed_words = typed_sentence.split()
    errors = []
    total_errors = 0
    extra_words = []

    for i, (expected_word, typed_word) in enumerate(zip(expected_words, typed_words)):
        if expected_word != typed_word:
            positions, he, ht = highlight_word_errors(expected_word, typed_word)
            total_errors += len(positions)

            if len(positions) == 1:
                error_msg = (
                    f'Mistake at "{expected_word}" at character {positions[0]}:\n'
                    f'Expected: {he}\n'
                    f'Typed:    {ht}\n'
                )
            else:
                pos_list = ', '.join(f'character {p}' for p in positions)
                error_msg = (
                    f'Mistake at "{expected_word}" at {pos_list}:\n'
                    f'Expected: {he}\n'
                    f'Typed:    {ht}\n'
                )
            errors.append(error_msg)

    if len(typed_words) > len(expected_words):
        extra = typed_words[len(expected_words):]
        extra_words.extend(extra)
        errors.append(f"✱ Extra words added: {' '.join(extra)}")
        total_errors += len(extra)
    elif len(typed_words) < len(expected_words):
        missing = expected_words[len(typed_words):]
        errors.append(f"✱ Missing words: {' '.join(missing)}")
        total_errors += len(missing)

    summary = f"Total Mistakes: {total_errors}\n"
    return summary + "\n" + "\n".join(errors)
