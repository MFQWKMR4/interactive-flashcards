# import argparse
from __future__ import print_function

import os
import random
import textwrap

import yaml
from recognition import AudioInput
from future.builtins.misc import input

MAX_WIDTH = 120
MIN_CONTENT_HEIGHT = 6
BORDER = '*'


class Flashcard:
    """Representation of a flashcard.

    It has two states.
    First a placeholder is displayed, and the user is requested
    to press a key to continue.
    Second, the content is shown, and the user is requested to press
    a key to shown next flashcard or to finish.
    """

    def __init__(self, topic, content, previous_answer=None, max_card_width=MAX_WIDTH,
                 min_content_height=MIN_CONTENT_HEIGHT):
        self.max_card_width = max_card_width
        self.min_content_height = min_content_height
        self.topic = topic
        self.content = content
        self.previous_answer = previous_answer

    def format_raw(self, line, max_length):
        """Processes raw data.

        :param line: contains raw data which may include tabs, new lines, etc.
        :type line: str
        :param max_length: max length of each element of the array generated.
        :type max_length: int
        :returns: formated data.
        :rtype: list
        """

        line = ' '.join(line.split())
        words_in_line = line.replace('\n', ' ').replace('\t', ' ')

        return textwrap.wrap(words_in_line, max_length - 5)

    def style_on_line(self, line, max_length, border=BORDER):
        """Add border and center a given line.

        :param line: the pre formatted string.
        :type line: str
        :param max_length: used to calculate extra whitespaces and borders.
        :type max_length: int
        :param border: representation of the border.
        :type border: str

        :returns: styled string
        :rtype: str
        """

        return line.center(max_length - 2, ' ').center(max_length, border)

    def clean(self):
        """Clear the terminal on which the flashcard is gonna be displayed."""

        if os.name == 'posix':
            os.system('clear')
        else:
            os.system('cls')

    def get_topic(self, topic):
        """Generate the topic lines ready to be displayed.

        :returns: lines ready to be shown.
        :rtype: list
        """

        topic_lines = ['']
        topic_lines += self.format_raw(topic, self.max_card_width)
        topic_lines += ['']
        return [self.style_on_line(l, self.max_card_width) for l in topic_lines]

    def get_content(self, content):
        """Generate the content lines ready to be displayed.

        :returns: lines ready to be shown.
        :rtype: list
        """

        content_lines = ['']
        formatted_content = self.format_raw(content, self.max_card_width)

        content_lines += formatted_content

        content_lines += ['']

        current_height = len(content_lines)
        expected_height = len(formatted_content)
        min_height = self.min_content_height
        height = 0
        if expected_height > min_height:
            height = expected_height
        else:
            height = min_height

        if current_height > height:
            height = current_height

        content_lines += [''] * (height - current_height)

        return [self.style_on_line(l, self.max_card_width)
                for l in content_lines]

    def get_previous_answer(self):
        """Generate the previous_answer lines ready to be displayed.

        :returns: lines ready to be shown.
        :rtype: list
        """

        topic_lines = ['']
        topic_lines += self.format_raw(self.previous_answer,
                                       self.max_card_width)
        topic_lines += ['']
        return [self.style_on_line(l, self.max_card_width) for l in topic_lines]

    def get_lines_to_draw(self, show_placeholder=False,
                          border=BORDER, inverted=False):
        """Central connection where all the lines generated are unified.

        :returns: lines to be shown
        :rtype: list
        """

        lines = ['\n']  # starts with a new line

        # generate border line
        horizontal_border = border * self.max_card_width

        lines.append(horizontal_border)

        topic = self.get_topic(self.topic)
        content = self.get_content(self.content)

        if show_placeholder:
            placeholder = 'Answer and Press [Enter] to submit'
            if inverted:
                topic = self.get_topic(placeholder)
            else:
                content = self.get_content(placeholder)

        lines += topic
        lines.append(horizontal_border)
        lines.append(horizontal_border)
        lines += content

        if self.previous_answer:
            lines.append(horizontal_border)
            lines.append(horizontal_border)
            lines += self.get_previous_answer()

        lines.append(horizontal_border)
        return lines

    def draw(self, show_placeholder=False, inverted=False):
        """Draw the generated lines."""
        self.clean()
        lines = self.get_lines_to_draw(
            inverted=inverted, show_placeholder=show_placeholder)
        for line in lines:
            print(line)

    def run(self, inverted=False, w=False, s=False, ai=None):
        """Execute the flashcard.

        It will transition between this states:
        1) Content shows the placeholder and will wait for an input to continue.
        2) Content is shown and will wait for an input to continue.
        """

        if (not w) and (not s):
            self.draw(show_placeholder=True, inverted=inverted)
            input()
            self.draw()
            input()
        else:
            if w:
                self.draw(show_placeholder=True, inverted=inverted)
                ans = input("( ´ゝ`) Write ...)")
                self.previous_answer = ans
                self.draw()
                input()
            else:
                self.draw(show_placeholder=True, inverted=inverted)
                input("Press [Enter] if you're ready")
                ans = ai.run()
                self.previous_answer = ans
                input()
                self.draw()
                input()


def run_flashcards(flashcards, ordered, inverted, w, s):
    if not ordered:
        random.shuffle(flashcards)
    ai = None
    if s:
        ai = AudioInput()
    for fc in flashcards:
        fc.run(inverted=inverted, w=w, s=s, ai=ai)


def start(args):
    file_names = args.file_names
    ordered = args.ordered
    inverted = args.inverted
    writing = args.writing
    speaking = args.speaking

    flashcards = []

    for file_name in file_names:
        with open("./yaml/" + file_name) as stream:
            # no exception handling here, let yaml exceptions do their job
            parsed_file = yaml.load(stream, Loader=yaml.Loader)
            for data in parsed_file:
                fc = Flashcard(**data)
                flashcards.append(fc)

    run_flashcards(flashcards, ordered, inverted, writing, speaking)
    if writing or speaking:
        updated = list(map(lambda x: {
                       "topic": x.topic, "content": x.content, "previous_answer": x.previous_answer}, flashcards))
        with open("./yaml/" + file_name, "w", encoding="utf-8") as yf:
            yaml.dump(updated, yf, default_flow_style=False,
                      encoding='utf-8', allow_unicode=True)
