from blacklist import word_list
import re
import emoji


def get_msg_list():
    """open chat.txt file and return array of all lines in file"""
    msg_file = open("./chat.txt", "r")
    msg_arr = []
    for msg in msg_file:
        msg_arr.append(msg.strip())
    msg_file.close()
    return msg_arr


def remove_emoji(emoji_text):
    """Returns emoji-less string"""
    chars = [str for str in emoji_text]
    emoji_list = [c for c in chars if c in emoji.UNICODE_EMOJI]
    clean = ' '.join([str for str in emoji_text.split()
                      if not any(i in str for i in emoji_list)])
    return clean


def remove_url(message):
    """removes urls from message"""
    return re.sub(r'http\S+', '<Message Redacted>', message)


def requires_redaction(message):
    """Checks if message content needs to be redacted"""
    temp = message.split(":")
    msg_length = len(temp[len(temp) - 1])
    for word in word_list:
        # if msg_length is 0, message has alredy been cleaned due to sanitization
        if (word in message or msg_length == 0):
            return True
    return False


def sanitize_message(message):
    """removes urls, emojis and lower case converts message"""
    sanitized = remove_emoji(message)
    sanitized = remove_url(sanitized)
    sanitized = sanitized.lower()
    return sanitized


def create_redacted_file():
    """creates new text file with sensitive information sanitized and redacted"""
    r_file = open("chat_history.txt", "w")
    msg_list = get_msg_list()
    for msg in msg_list:
        content = sanitize_message(msg)
        if (requires_redaction(content)):
            chunks = msg.split(" - ")
            chunks[len(chunks) - 1] = "<message redacted>"
            content = ' - '.join([str(x) for x in chunks])
        r_file.write(content + "\n")


if __name__ == '__main__':
    create_redacted_file()
