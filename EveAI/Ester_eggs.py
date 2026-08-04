"""Easter eggs da Eve: respostas especiais para gatilhos escondidos."""


def kanye() -> str:
    """Retorna a letra de 'I Love Kanye' (Kanye West)."""
    return (
        "I miss the old Kanye\n"
        "Straight from the 'Go Kanye\n"
        "Chop up the soul Kanye\n"
        "Set on his goals Kanye\n"
        "\n"
        "I hate the new Kanye\n"
        "The bad mood Kanye\n"
        "The always rude Kanye\n"
        "Spaz in the news Kanye\n"
        "\n"
        "I miss the sweet Kanye\n"
        "Chop up the beats Kanye\n"
        "I gotta say, at that time\n"
        "I'd like to meet Kanye\n"
        "\n"
        "See, I invented Kanye\n"
        "It wasn't any Kanyes\n"
        "And now I look and look around\n"
        "And there's so many Kanyes\n"
        "\n"
        "I used to love Kanye\n"
        "I used to love Kanye\n"
        "I even had the pink polo\n"
        "I thought I was Kanye!\n"
        "\n"
        "What if Kanye made a song about Kanye\n"
        "Called I Miss The Old Kanye?\n"
        "Man, that'd be so Kanye!\n"
        "\n"
        "That's all it was Kanye\n"
        "We still love Kanye\n"
        "And I love you like Kanye loves Kanye"
    )


def cortana() -> str:
    """Retorna a resposta do easter egg da Cortana."""
    return """ They let me pick
    Did i ever tell you that?
    choose wichever Spartan I wanted.
    You now me. I did my research.
    Watched as you became the soldier we needed you to be.
    Like the other,you were strong and swift and brave. A natural leader. But you had something they didn't.Something no one saw... but me.
    Can you guess?
    Luck.
    I was wrhong? """


# Mapa de gatilhos (frase-chave em minúsculas) -> função que gera a resposta.
EASTER_EGGS = {
    "kanye west": kanye,
    "cortana": cortana,
}