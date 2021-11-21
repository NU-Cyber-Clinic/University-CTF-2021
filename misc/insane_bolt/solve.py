#!/usr/bin/env python3
'''
Modified version of https://gist.github.com/Tak31337/5314032
Altered to solve mazes from a netcat session for the HTB Uni CTF 2021
'''

'''
This program will first analyze the maze and fill out a two dimensional list with elements
contained within the input file, making note of the start point

The program will then explore neighboring cells from the start location starting with the right cell
by passing the location to a method which will process the cell, and mark it as explored, or maze solved.

The program will make note if there is more than one exploratory juxtaposing cell, and store the cell 
location into a list ordered latest found to earliest found, then note cells explored after this into
a list. If a dead end is hit the location jumps to the location of the top of the list. 
if a jump is made the dead end path is marked with x's by going over explored cells and then wiping the explored
list.

When the program lands on the end cell, it prints out the full path and maze complete.

Every jump the program prints out the entire maze by feeding the multidimensional list into a method which 
will interpret it and print it to stdout. The multidimensional list will actually be a class I create because
python doesn't allow you to initialize a multidimensional array without specific boundaries.

******Note******
This code should actually work with any ASCII maze that contains spaces for open paths, and a S, and E for 
start and ending points. characters representing borders are redundant. 

@version: 1.0a
@author: tak
'''

path = ""

'''
Main method in which the program starts
'''
def solve(maze):
    location = [] #list to hold the location we are at in the maze
    hasNoEnd = True

    #slightly different than I had planned.
    for y in range(0, len(maze)):
        for x in range(0, len(maze[y])):
            if maze[y][x] == 'S':
                location = [y, x]
            elif maze[y][x] == 'E':
                hasNoEnd = False
    if len(location) == 0:
        raise Exception("No start cell found, check your input file")
    if hasNoEnd:
        raise Exception("Maze has no end, unsolvable.")
    
    tick(maze, location[0], location[1])

'''
My origional plan had too many if statements :/

Whenever I see more than 5 if statements, i know something is wrong.

Recursive method which solves the maze.

@param maze: the maze matrix
@param y: the y location
@param x: the x location
'''
def tick(maze, y, x):
    global path
    # dump(maze)
    # print("\n")
    if maze[y][x] in (' ', 'S'):
        maze[y][x] = 'x'
        #check right, down, left, up
        right = tick(maze, y, x+1)
        down = False
        left = False
        up = False

        if (right):
            path += "R"
        else:
            down = tick(maze, y-1, x)
            if (down):
                path += ""
            else:
                left = tick(maze, y, x-1)
                if (left):
                    path += "L"
                else:
                    up = tick(maze, y+1, x)
                    if (up):
                        path += "D"

        if (right or down or left or up):
            maze[y][x] = '.'
            return True
    elif maze[y][x] == 'E':
        return True #start peeling back.
    return False


# CTF code \/

from pwn import *

conn = remote('167.172.57.255', 30458)
print(conn.recvline().decode('utf-8'))
conn.recvuntil(b'>', drop=True)

conn.send(b'2\n')
while (True):
    # Read the maze from the server
    maze = conn.recvuntil(b'>').decode('utf-8')
    print(maze)

    # Clean up the contents and do some replacement for the solver
    maze = maze.replace('>', '').strip()
    maze = maze.replace(" ", "").replace("🤖", "S").replace("💎", "E").replace("🔩", " ").replace(b'\xef\xb8\x8f'.decode('utf-8'), '')
    
    # Split it up and solve
    mazedata = [list(row) for row in maze.splitlines()]
    solve(mazedata)
    
    # Reverse and print the path
    path = path[::-1]
    print(path)
    
    # Send the path to the server
    conn.send(path.encode('utf-8') + b'\n')

    # Dump out the last few lines before the next maze
    print(conn.recvline().decode('utf-8'))
    print(conn.recvline().decode('utf-8'))
    lastline = conn.recvline().decode('utf-8')
    print(lastline)

    # If we got a congrats string then dump the rest of the session and close
    if ('Congratulations!' in lastline):
        print(conn.recvall().decode('utf-8'))
        break

    path = ''
    