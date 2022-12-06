# Day 2: Rock Paper Scissors
## Part One
The Elves begin to set up camp on the beach. To decide whose tent gets to be closest to the snack storage, a giant Rock Paper Scissors tournament is already in progress.

Rock Paper Scissors is a game between two players. Each game contains many rounds; in each round, the players each simultaneously choose one of Rock, Paper, or Scissors using a hand shape. Then, a winner for that round is selected: Rock defeats Scissors, Scissors defeats Paper, and Paper defeats Rock. If both players choose the same shape, the round instead ends in a draw.

Appreciative of your help yesterday, one Elf gives you an encrypted strategy guide (your puzzle input) that they say will be sure to help you win. "The first column is what your opponent is going to play: A for Rock, B for Paper, and C for Scissors. The second column--" Suddenly, the Elf is called away to help with someone's tent.

The second column, you reason, must be what you should play in response: X for Rock, Y for Paper, and Z for Scissors. Winning every time would be suspicious, so the responses must have been carefully chosen.

The winner of the whole tournament is the player with the highest score. Your total score is the sum of your scores for each round. The score for a single round is the score for the shape you selected (1 for Rock, 2 for Paper, and 3 for Scissors) plus the score for the outcome of the round (0 if you lost, 3 if the round was a draw, and 6 if you won).

Since you can't be sure if the Elf is trying to help you or trick you, you should calculate the score you would get if you were to follow the strategy guide.

For example, suppose you were given the following strategy guide:
```
A Y
B X
C Z
```
This strategy guide predicts and recommends the following:

In the first round, your opponent will choose Rock (A), and you should choose Paper (Y). This ends in a win for you with a score of 8 (2 because you chose Paper + 6 because you won).
In the second round, your opponent will choose Paper (B), and you should choose Rock (X). This ends in a loss for you with a score of 1 (1 + 0).
The third round is a draw with both players choosing Scissors, giving you a score of 3 + 3 = 6.
In this example, if you were to follow the strategy guide, you would get a total score of 15 (8 + 1 + 6).

What would your total score be if everything goes exactly according to your strategy guide?

### Solution

The core part of the problem is defining a function capable of computing the points earned in a game. In order to do that, we need to define first a function which returns the outcome of a game given the choices of the two players.\
Putting it in math terms, given the set of possible choices
$$C := \{ \text{rock},\text{paper},\text{scissors} \}$$
and the set of outcomes
$$O := \{ \text{draw}, \text{first}, \text{second} \}$$
where $\text{first}$ means that the first player wins and $\text{second}$ means that the second player wins, we need to implement a function $o$ (outcome) which takes two choices and returns the outcome of a game
$$o: C^2 \mapsto O$$
following the basic rules of Rock Paper Scissors.

A lot of possible approaches can be used. The most naif approach is the one that requires using a sequence of `if` statements dealing with each case. Ew. That stinks. We could do definitely better than that!

In a more abstract way, the rules of Rock Paper Scissors can be synthesized as follows:
- two equal choices lead to a draw;
- if we define an order relation on the set $C$ such as $\text{rock} < \text{paper} < \text{scissors}$:
    - if two choices are consecutive according to our ordering, the greater one beats the smaller one ($\text{paper}$ beats $\text{rock}$, $\text{scissors}$ beats $\text{paper}$)
    - if two choices are not consecutive, the smaller one beats the greater one ($\text{rock}$ beats $\text{scissors}$)

We need to find a mathematical function which respects these properties.\
Let's start by assigning a numerical value to each choice as suggested by the prompt:
$$g: C \mapsto \mathbb{Z}$$
$$g(c) = \begin{cases}
1 & \text{if } c = \text{rock}\\
2 & \text{if } c = \text{paper}\\
3 & \text{if } c = \text{scissors}\\
\end{cases}$$


```python
from enum import Enum


class Choice(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3
```

We can immediately notice that this mapping follows the theoretical order relation we were just talking about. Nice!

A good starting point could be focusing on the simplest case: the draw. We must have
$$o(\text{rock}, \text{rock}) = o(\text{paper}, \text{paper}) = o(\text{scissors}, \text{scissors}) = \text{draw}$$
A suitable operation for having something similiar could be the subtraction. If we define $o$ in such a way:
$$o(c_1, c_2) = h(g(c_1) - g(c_2))$$
where $h: \mathbb{Z} \mapsto O$ is a function that maps integers back to outcomes, the previous equation would become
$$\begin{align*}
o(\text{rock}, \text{rock}) &= h(1 - 1)\\
= o(\text{paper}, \text{paper}) &= h(2 - 2)\\
= o(\text{scissors}, \text{scissors}) &= h(3 - 3)\\
\text{draw} &= h(0)
\end{align*}$$
This could work. Let's keep it for now.\
Let's try and define the mapping $h$ between numbers and outcomes. According to the function we've just found, we know that we should assign the number $0$ to the outcome $\text{draw}$. A possible mapping could be

$$h: \{0, 1, 2\} \mapsto O$$
$$h(n) = \begin{cases}
\text{draw} & \text{if } n = 0\\
\text{first} & \text{if } n = 1\\
\text{second} & \text{if } n = 2\\
\end{cases}$$

It becomes immediately clear, though, that our definition of $o$ is still incomplete. It deals correctly with the draws, but the win/lost outcomes are still undefined according to our definition of $h$.
$$o(\text{rock}, \text{paper}) = h(g(\text{rock}) - g(\text{paper})) = h(1 - 2) = h(-1) = ?$$
We should keep the input of $h$ in the set $\{0, 1, 2\}$. Modular arithmetic seems perfect for this purpose!\
We can use the ring of integers modulo 3 as the domain of the function $h$
$$\frac{\mathbb{Z}}{3 \mathbb{Z}} = \{0, 1, 2\}$$
such as now $h$ is defined as
$$h: \frac{\mathbb{Z}}{3\mathbb{Z}} \mapsto O$$
$$h(n) = \begin{cases}
\text{draw} & \text{if } n = 0\\
\text{first} & \text{if } n = 1\\
\text{second} & \text{if } n = 2\\
\end{cases}$$


```python
class Outcome(Enum):
    DRAW = 0
    FIRST = 1
    SECOND = 2

outcomes: dict[int, Outcome] = {
    v.value: v for v in Outcome.__members__.values()
}
```

Let's redefine $o$ accordingly, to always feed $h$ a number in the ring of integers modulo 3:

$$o(c_1, c_2) = h((g(c_1) - g(c_2)) \mod 3)$$


```python
def outcome(first: Choice, second: Choice) -> Outcome:
    return outcomes[(first.value - second.value) % 3]
```

Ok, with the modulo operation now we're guaranteed that $h$ always takes a valid input. But are the results meaningful just by taking the result of the modulo operation or do we have to further improve $o$? Let's think about that for a moment.\
The draw case is preserved: $0 \mod 3$ is still $0$, no matter the modulus. Good.\
In case of consecutive choices (i.e. "at distance $1$") where the first choice wins (paper vs rock, scissors vs paper) we always have $1 \mod 3 = 1$. In the opposite case (second choice wins, rock vs paper or paper vs scissors), we always have $-1 \mod 3 = 2$. Good!\
In case of non-consecutive choices (i.e. "at distance $2$") where the first choice wins (rock vs scissors), we have $-2 \mod 3 = 1$ and, on the contrary (second choice winning), we have $2 \mod 3 = 2$. It seems perfect!

$$o(\text{paper}, \text{rock}) = h(2 - 1 \mod 3) = h(1) = \text{first}$$
$$o(\text{rock}, \text{paper}) = h(1 - 2 \mod 3) = h(-1 \mod 3) = h(2) = \text{second}$$
$$o(\text{scissors}, \text{paper}) = h(3 - 2 \mod 3) = h(1) = \text{first}$$
$$o(\text{paper}, \text{scissors}) = h(1 - 2 \mod 3) = h(-1 \mod 3) = h(2) = \text{second}$$
$$o(\text{rock}, \text{scissors}) = h(1 - 3 \mod 3) = h(-2 \mod 3) = h(1) = \text{first}$$
$$o(\text{scissors}, \text{rock}) = h(3 - 1 \mod 3) = h(2) = \text{second}$$


```python
print(outcome(Choice.PAPER, Choice.ROCK))
print(outcome(Choice.ROCK, Choice.PAPER))
print(outcome(Choice.SCISSORS, Choice.PAPER))
print(outcome(Choice.PAPER, Choice.SCISSORS))
print(outcome(Choice.ROCK, Choice.SCISSORS))
print(outcome(Choice.SCISSORS, Choice.ROCK))
```

    Outcome.FIRST
    Outcome.SECOND
    Outcome.FIRST
    Outcome.SECOND
    Outcome.FIRST
    Outcome.SECOND


Bingo! 😎

The final part is pretty straightforward: we have to define a function $p$ that returns the points earned by each game.
It's as easy as taking the integer value of our choice and summing it to a predefined constant depending on the outcome of the game. Let's assume that we're always the first player, so the outcome $\text{first}$ corresponds to a win.

$$m: O \mapsto \mathbb{Z}$$
$$m(o) = \begin{cases}
0 & \text{if } o = \text{second}\\
3 & \text{if } o = \text{draw}\\
6 & \text{if } o = \text{first}
\end{cases}$$


```python
points_by_outcome: dict[Outcome, int] = {
    Outcome.SECOND: 0,
    Outcome.DRAW: 3,
    Outcome.FIRST: 6,
}
```

Now we can implement the function that returns the points earned in a game

$$p: C^2 \mapsto \mathbb{Z}$$
$$p(c_1, c_2) = g(c_1) + m(o(c_1, c_2))$$


```python
def earned_points(me: Choice, opponent: Choice) -> int:
    return me.value + points_by_outcome[outcome(me, opponent)]
```

Let's build a mapping between the letters of the input file and the actual choice for convenience.


```python
letter_to_choice_map: dict[str, Choice] = {
    "A": Choice.ROCK,
    "X": Choice.ROCK,
    "B": Choice.PAPER,
    "Y": Choice.PAPER,
    "C": Choice.SCISSORS,
    "Z": Choice.SCISSORS,
}
```

Finally, we iterate through all the matches and compute the total score.


```python
total_score = 0
with open("input.txt", "r") as input_file:
    for match in input_file:
        opponent, me = [letter_to_choice_map[c.strip()]
                        for c in match.split(maxsplit=2)]
        total_score += earned_points(me, opponent)

print(total_score)
```

    12679


## Part Two
The Elf finishes helping with the tent and sneaks back over to you. "Anyway, the second column says how the round needs to end: X means you need to lose, Y means you need to end the round in a draw, and Z means you need to win. Good luck!"

The total score is still calculated in the same way, but now you need to figure out what shape to choose so the round ends as indicated. The example above now goes like this:

In the first round, your opponent will choose Rock (A), and you need the round to end in a draw (Y), so you also choose Rock. This gives you a score of 1 + 3 = 4.
In the second round, your opponent will choose Paper (B), and you choose Rock so you lose (X) with a score of 1 + 0 = 1.
In the third round, you will defeat your opponent's Scissors with Rock for a score of 1 + 6 = 7.
Now that you're correctly decrypting the ultra top secret strategy guide, you would get a total score of 12.

Following the Elf's instructions for the second column, what would your total score be if everything goes exactly according to your strategy guide?

### Solution

This time we have to build a function which takes the opponent's choice and the outcome of the game and returns "our" choice that produced the given outcome.

$$k: (C, O) \mapsto C$$

Let's tinker with the numbers corresponding to choices and outcomes according to the functions we defined in the previous part. Quick recall:
$$g(c) = \begin{cases}
1 & \text{if } c = \text{rock}\\
2 & \text{if } c = \text{paper}\\
3 & \text{if } c = \text{scissors}\\
\end{cases}
\quad
h(n) = \begin{cases}
\text{draw} & \text{if } n = 0\\
\text{first} & \text{if } n = 1\\
\text{second} & \text{if } n = 2\\
\end{cases}$$

Let's define $g^{-1}$, the inverse of $g$

$$g^{-1}: \{1, 2, 3\} \mapsto C$$
$$g^{-1}(n) = \begin{cases}
\text{rock} & \text{if } n = 1\\
\text{paper} & \text{if } n = 2\\
\text{scissors} & \text{if } n = 3\\
\end{cases}$$


```python
choices: dict[int, Choice] = {
    c.value: c for c in Choice.__members__.values()
}
```

and $h^{-1}$, the inverse of $h$

$$h^{-1}(o): O \mapsto \frac{\mathbb{Z}}{3\mathbb{Z}}$$
$$h^{-1}(o) = \begin{cases}
0 & \text{if } n = \text{draw}\\
1 & \text{if } n = \text{first}\\
2 & \text{if } n = \text{second}\\
\end{cases}$$

The simplest case to start with is always the draw: given a choice and a draw as the outcome, the function should return the same choice as the input one. A draw behaves like a neutral element, from an algebraic perspective. The numerical value previously associated with a draw is 0. It seems a pretty convenient choice now... do you know any binary operation whose neutral element is 0? 🤔\
Yes, the sum operation seems a good starting point! Let's define $k$ as
$$k(c, o) = g^{-1}(g(c) + h^{-1}(o))$$

Since the domain of k is $\{1, 2, 3\}$, we must guarantee that its input stays valid. To keep the value of the sum $\in \{1, 2, 3\}$, we can use again the magic of the modular arithmetic to stay in $\mathbb{Z}/3\mathbb{Z}$... and then just add $1$ to "shift" the result!
$$k(c, o) = g^{-1}((g(c) + h^{-1}(o) \mod 3) + 1)$$

Okay! Now at least we're guaranteed to provide $g^{-1}$ admissible values.

Now that we are sure that the expression is "syntactically" correct, let's focus on its "semantics".\
Let's verify if our current definition of $k$ returns the right result.

Let's consider again the draw case: our opponent played $\text{rock}$ and the outcome must be $\text{draw}$, so our choice must be $\text{rock}$ too.

$$\begin{align*}
    k(\text{rock}, \text{draw}) &= g^{-1}((g(\text{rock}) + h^{-1}(\text{draw}) \mod 3) + 1)\\
    &= g^{-1}((1 + 0 \mod 3) + 1)\\
    &= g^{-1}(2) = \text{paper} \neq \text{rock}
\end{align*}$$

Looks like we fixed the syntax but broke the semantics! The error is quite trivial though. Since we're always adding $1$ after the modulo operation, our result is "shifted"! To compensate, we should simply subtract $1$ to the operand of the modulo.
$$k(c, o) = g^{-1}((g(c) + h^{-1}(o) - 1 \mod 3) + 1)$$


```python
def choice_by_outcome(opponent: Choice, outcome: Outcome) -> Choice:
    return choices[(opponent.value + outcome.value - 1) % 3 + 1]
```

Let's verify again with the previous example and let's do also another couple of checks:
$$\begin{align*}
    k(\text{rock}, \text{draw}) &= g^{-1}((g(\text{rock}) + h^{-1}(\text{draw}) - 1 \mod 3) + 1)\\
    &= g^{-1}((1 + 0 - 1 \mod 3) + 1)\\
    &= g^{-1}(1) = \text{rock}
\end{align*}$$
$$\begin{align*}
    k(\text{rock}, \text{first}) &= g^{-1}((g(\text{rock}) + h^{-1}(\text{first}) - 1 \mod 3) + 1)\\
    &= g^{-1}((1 + 1 - 1\mod 3) + 1)\\
    &= g^{-1}(2) = \text{paper}
\end{align*}$$
$$\begin{align*}
    k(\text{scissors}, \text{second}) &= g^{-1}((g(\text{scissors}) + h^{-1}(\text{second}) - 1 \mod 3) + 1)\\
    &= g^{-1}((3 + 2 - 1\mod 3) + 1)\\
    &= g^{-1}((4 \mod 3) + 1)\\
    &= g^{-1}(1 + 1) = g^{-1}(2) = \text{paper}
\end{align*}$$


```python
print(choice_by_outcome(Choice.ROCK, Outcome.DRAW))
print(choice_by_outcome(Choice.ROCK, Outcome.FIRST))
print(choice_by_outcome(Choice.SCISSORS, Outcome.SECOND))
```

    Choice.ROCK
    Choice.PAPER
    Choice.PAPER


Nailed it 😎
Now let's redefine the function to compute the earned points
$$p: (C, O) \mapsto \mathbb{Z}$$
$$p(c, o) = g(k(c, 0)) + m(o)$$


```python
del earned_points
def earned_points(opponent: Choice, outcome: Outcome) -> int:
    return choice_by_outcome(opponent, outcome).value \
        + points_by_outcome[outcome]

```

Let's build a mapping between the letters of the input file and the outcome for convenience.


```python
letter_to_outcome_map: dict[str, Outcome] = {
    "X": Outcome.SECOND,
    "Y": Outcome.DRAW,
    "Z": Outcome.FIRST,
}
```

Finally, we iterate through all the matches and compute the total score.


```python
total_score = 0
with open("input.txt", "r") as input_file:
    for match in input_file:
        match = match.split(maxsplit=2)
        opponent = letter_to_choice_map[match[0].strip()]
        outcome = letter_to_outcome_map[match[1].strip()]
        total_score += earned_points(opponent, outcome)

print(total_score)
```

    14470

