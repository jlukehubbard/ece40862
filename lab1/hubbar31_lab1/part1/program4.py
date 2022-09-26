#!/usr/bin/env python3

def main():
    birthdays = {"Albert Einstein": "04/14/1879", "Benjamin Franklin": "01/17/1706", "Ada Lovelace": "10/10/1815", "Bill Clinton": "08/19/1946" , "James Hubbard": "04/25/2002"}
    s = input("""Welcome to the birthday dictionary. We know the birthdays of:
    Albert Einstein
    Benjamin Franklin
    Ada Lovelace
    Bill Clinton
    James Hubbard
    Whose birthday do you want to look up?
    """)
    try:
        print(s, "'s birthday is ", birthdays[s], sep='')
    except KeyError:
        print("We don't know that birthday, try another.")

if __name__ == '__main__':
    main()
