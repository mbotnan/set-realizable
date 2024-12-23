# Set-Realizable
This repository contains code for determining whether a vector-valued representation of a finite category is in the additive image of the free functor. Details can be found in our accompanying paper.

### `set-real-routines.g`
- Format: GAP file.
- **Requirements:**
  - Install [GAP](https://www.gap-system.org/).
  - Load the [QPA](https://github.com/homalg-project/QPA) package.
- **Main Functionality:**
  - **`IsInduced`**: Checks if a representation `M` of a bound quiver is in the additive image of the free functor. 
    - **Input Example**: The file `7-star.g` (representation drawn in our paper) demonstrates input formatting.
    - **Performance:** While the code is slow, it runs for GF(2) on 7-star.g in a few seconds.
  - **`TestFromProjectives`**:
    - **Purpose:**
      - Takes an algebra of the form  kQ/relations, where Q is a quiver.
      - Starts with the projective modules and explores a specified number of steps ("depth") into the Auslander-Reiten (AR) quiver from each projective.
      - Uses the transpose of the dual of 'M'.
    - **Output:**
      - If a representation that is not additively set-realizable is found, its dimension vector is output.
      - Can be modified to output the representation itself.
    - **Example:**
      - Input formatting is demonstrated in the file `Ladder.g`.
  - **`TestQuiet`**:
    - Similar to `TestFromProjectives`, but with reduced output.
    - **Return Values:**
      - `0`: Not additively set-realizable.
      - `1`: All representations are additively realizable, and the full AR quiver has been explored.
      - `2`: Inconclusive (full AR quiver not explored, no counterexamples found).

### `add_surjective.py`
- **Purpose:**
  - Takes a quiver (without relations) and examines all its orientations to determine additive set-realizability.
  - Leverages reflection functors for speed-up (see paper).
- **Output:**
  - For Dynkin types A and D, classifications of the additive image are provided in the paper.
  - For type E, checks were performed for GF(2) using this algorithm (see paper).
  - Outputs a plot of each orientation and indicates whether the free functor is additively surjective.
  - For type E8, the algorithm terminates in approximately 40 minutes on a MacBook.



