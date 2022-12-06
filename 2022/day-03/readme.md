# Day 3: Rucksack Reorganization
## Part One
One Elf has the important job of loading all of the rucksacks with supplies for the jungle journey. Unfortunately, that Elf didn't quite follow the packing instructions, and so a few items now need to be rearranged.

Each rucksack has two large compartments. All items of a given type are meant to go into exactly one of the two compartments. The Elf that did the packing failed to follow this rule for exactly one item type per rucksack.

The Elves have made a list of all of the items currently in each rucksack (your puzzle input), but they need your help finding the errors. Every item type is identified by a single lowercase or uppercase letter (that is, a and A refer to different types of items).

The list of items for each rucksack is given as characters all on a single line. A given rucksack always has the same number of items in each of its two compartments, so the first half of the characters represent items in the first compartment, while the second half of the characters represent items in the second compartment.

For example, suppose you have the following list of contents from six rucksacks:

```
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
```
- The first rucksack contains the items `vJrwpWtwJgWrhcsFMMfFFhFp`, which means its first compartment contains the items `vJrwpWtwJgWr`, while the second compartment contains the items `hcsFMMfFFhFp`. The only item type that appears in both compartments is lowercase `p`.
- The second rucksack's compartments contain `jqHRNqRjqzjGDLGL` and `rsFMfFZSrLrFZsSL`. The only item type that appears in both compartments is uppercase L.
- The third rucksack's compartments contain `PmmdzqPrV` and `vPwwTWBwg`; the only common item type is uppercase `P`.
- The fourth rucksack's compartments only share item type `v`.
- The fifth rucksack's compartments only share item type `t`.
- The sixth rucksack's compartments only share item type `s`.

To help prioritize item rearrangement, every item type can be converted to a priority:

Lowercase item types `a` through `z` have priorities 1 through 26.
Uppercase item types `A` through `Z` have priorities 27 through 52.
In the above example, the priority of the item type that appears in both compartments of each rucksack is 16 (`p`), 38 (`L`), 42 (`P`), 22 (`v`), 20 (`t`), and 19 (`s`); the sum of these is 157.

Find the item type that appears in both compartments of each rucksack. What is the sum of the priorities of those item types?

### Solution
First of all, let's define a function that computes the priority of an item:


```python
def priority(item: str) -> int:
    assert len(item) == 1
    if item.isupper():
        return ord(item) - ord("A") + 27
    return ord(item) - ord("a") + 1
```

To compute the total priorities, we can iterate over the lines of the input file (which represents the rucksacks), split the rucksack in half (getting the two compartments) and then compute the intersection between the compartments (leveraging Python's built-in `set`). For each common item, we compute the priority and add it to the total.


```python
total_priorities = 0
with open("input.txt", "r") as input_file:
    for rucksack in input_file:
        compartment1, compartment2 = rucksack[:len(rucksack)//2], rucksack[len(rucksack)//2:]
        common_items = set(compartment1) & set(compartment2)
        total_priorities += sum(priority(i) for i in common_items)
print(total_priorities)
```

    8109


## Part Two
As you finish identifying the misplaced items, the Elves come to you with another issue.

For safety, the Elves are divided into groups of three. Every Elf carries a badge that identifies their group. For efficiency, within each group of three Elves, the badge is the only item type carried by all three Elves. That is, if a group's badge is item type B, then all three Elves will have item type B somewhere in their rucksack, and at most two of the Elves will be carrying any other item type.

The problem is that someone forgot to put this year's updated authenticity sticker on the badges. All of the badges need to be pulled out of the rucksacks so the new authenticity stickers can be attached.

Additionally, nobody wrote down which item type corresponds to each group's badges. The only way to tell which item type is the right one is by finding the one item type that is common between all three Elves in each group.

Every set of three lines in your list corresponds to a single group, but each group can have a different badge item type. So, in the above example, the first group's rucksacks are the first three lines:

```
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
```
And the second group's rucksacks are the next three lines:

```
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
```
In the first group, the only item type that appears in all three rucksacks is lowercase `r`; this must be their badges. In the second group, their badge item type must be `Z`.

Priorities for these items must still be found to organize the sticker attachment efforts: here, they are 18 (`r`) for the first group and 52 (`Z`) for the second group. The sum of these is 70.

Find the item type that corresponds to the badges of each three-Elf group. What is the sum of the priorities of those item types?

### Solution
To keep track of the three-Elf groups, we can buffer the rucksacks while we iterate; when in our buffer we have three rucksacks, we compute their intersection and compute the priority for the element in common, and then we empty the buffer and keep going until the rucksacks are over. Finally, we add it to the total priorities count.


```python
total_priorities = 0
group = []
with open("input.txt", "r") as input_file:
    for i, rucksack in enumerate(input_file):
        group.append(rucksack.strip())
        if i % 3 != 2:
            continue
        common_item = set(group[0]) & set(group[1]) & set(group[2])
        total_priorities += priority(list(common_item)[0])
        group.clear()
print(total_priorities)
```

    2738

