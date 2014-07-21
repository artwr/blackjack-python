## Design Comments

### Cards module

The idea to just refactor the code for `Card`, `CardCollection`, `Hand` and `Deck` into a different module made sense, since the code was starting to be long enough. The module can be reused to program another card game , e.g. [War](http://en.wikipedia.org/wiki/War_%28card_game%29) or [Sevens](http://en.wikipedia.org/wiki/Sevens_%28card_game%29). Of course, the rank of the aces would have to be considered carefully depending on the game, but this could be dealt with by creating `__eq__()` and `__gt__()` for the `Card` object. 

`CardCollection` was created mostly to illustrate inheritance for both Hand and Deck.

### Card.value()

I had originally thought of a map/reduce approach, but you need the total hand value without the aces before assigning a value of 1 or 11. My original code (still available in the prototypes folder) would return the correct value in all but one case: a hand containing n aces (n>1) and other cards such that the total counting one ace as 11 would be 22, e.g. A,A,K, or A,A,A,9. The first check would let the ace go to 11, ending in a bust, when it should have been counted as one.

In the end, I opted for a list comprehension which seemed more compact than trying to force it into a map/filter.


### Deck

The deck is designed as an extension of CardCollection. Note that the order is of importance here, and the `pop()` method used returns the last card of the internal list. The deck could have been implemented as a `deque` from the `collections` module, but in this instance, it seemed unnecessary. The only detail to carefully consider was printing the deck in the right order.

### blackjack.py

Obviously, there are more features I wish I would have implemented. I started the work for splitting, and I am investigating saving the state of the game through a `pickle` object.