import re

# SENTENCE_PATTERN_REGEX = "(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|!|\")\s"  # a whitespace character which follows the pattern (?<=\.|\?|!|\") and does not follow (?<!\w\.\w.)(?<![A-Z][a-z]\.)
SENTENCE_PATTERN_REGEX = "(?<=\.|\?|!|\")\s"
FULL_STOP_WITH_NO_SPACE_PATTERN = "(?<=\w)(\.)(?=[^\d])"
QUESTION_MARK_WITH_NO_SPACE_PATTERN = "(?<=\w)(\?)(?=\w)"
FULL_STOP_LEFT_QUOTE_PATTERN = "(?<=\w)(\.“)(?=\w)"                 # for example: this year.“Of the total  (left quote opens quotation)
FULL_STOP_RIGHT_QUOTE_PATTERN = "(?<=\w)(\.”)(?=\w)"                 # for example: Gobabis.”Katjizeu also expressed  (right quote closes quotation)
RIGHT_QUOTE_FULL_STOP_PATTERN = "(?<=\w)(”\.)(?=\w)"                 # for example: the country”.So far  (right quote closes quotation)
FULL_STOP_PARENTHESES_PATTERN = "(?<=\w)(\)\.)(?=\w)"                 # for example: Union (NAFWU).The basic
QUESTION_MARK_LEFT_QUOTE_PATTERN = "(?<=\w)(\?“)(?=\w)"
QUESTION_MARK_RIGHT_QUOTE_PATTERN = "(?<=\w)(\?”)(?=\w)"

PROBLEMATIC_CHARS_SET = {"ǂ", "ǁ", "ǀ", "ǃ", "!", "?", "/", "\\", '"', "*", ":", "<", ">", "|", "î", "â", "ā", "Ô", "Â",
                         "Û", "ē", "ū", "%", "ô", ";", "Î", "ō", "ī", "Ā", "Ō", "Ī", "Ē", "Ū", "&", "^", "~", ",", ".",
                         u"\u00A0", u'\xad', "\n", "\r", "\t"}
NON_BREAKING_SPACE_UNICODE = u"\u00A0"
SOFT_HYPHEN = u'\xad'
SPACE_CHAR = " "


class ArticlesParser:

    def _create_article_id(self, title, date=None):
        first_word = title.split()[0]
        for char in PROBLEMATIC_CHARS_SET:
            if char in first_word:
                first_word = first_word.replace(char, "")               # cleaning out problematic chars
        return first_word

    def _sentences_to_lines(self, txt_str):
        """
        :param txt_str: txt of an article
        :return: the required separated str
        """
        article_txt = txt_str.replace(SOFT_HYPHEN, "")
        article_txt = article_txt.replace(NON_BREAKING_SPACE_UNICODE, "")
        article_txt = re.sub(FULL_STOP_WITH_NO_SPACE_PATTERN, ". ", article_txt)            # add space after full stops which don't precede a space
        article_txt = re.sub(QUESTION_MARK_WITH_NO_SPACE_PATTERN, "? ", article_txt)        # add space after question marks which don't precede a space
        article_txt = re.sub(FULL_STOP_LEFT_QUOTE_PATTERN, ". “", article_txt)
        article_txt = re.sub(FULL_STOP_RIGHT_QUOTE_PATTERN, "”. ", article_txt)
        article_txt = re.sub(RIGHT_QUOTE_FULL_STOP_PATTERN, "”. ", article_txt)
        article_txt = re.sub(FULL_STOP_PARENTHESES_PATTERN, "). ", article_txt)
        article_txt = re.sub(QUESTION_MARK_LEFT_QUOTE_PATTERN, "? “", article_txt)
        article_txt = re.sub(QUESTION_MARK_RIGHT_QUOTE_PATTERN, "?“. ", article_txt)
        sentences_list = re.split(SENTENCE_PATTERN_REGEX, article_txt)
        for i in range(len(sentences_list)):
            sentences_list[i] = sentences_list[i].strip()                            # cut all unnecessary spaces
        return sentences_list

    def _clean_quotes(self, str_to_clean):
        str_to_clean = str_to_clean.replace('"', '“')
        return str_to_clean.replace("'", "’")
