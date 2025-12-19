# CampNum-Ninja
Ninja is a Python game built on Python with OpenCV and Mediapipe. 

## Installation & usage
Download the repo with `git` using:

```bash
git clone git@github.com:ThibaultLaunois/CampNum-Ninja.git
```

Once you have downloaded the repository, create the conda environment using the `requirement.txt` file.

```bash
conda create --name <env> --file requirements.txt
```

Then, activate the virtual environment:
```bash
conda activate <env>
```

And launch the game with:
```bash
python -m Ninja
```

## Game rules & features
Winter is here, snow flakes are falling from the sky! Catch them all with your hands to gather points and get the best score possible. Each snow flake you catch gives you a base +5 pts, increased by your current multiplier. One game lasts one minute!

To increase your multiplier, simply don't miss a single flake! As you catch more and more without missing, your combo increases. Here's the relationship between combo and multiplier:

| Combo       | Multiplier  |
| ----------- | ----------- |
| 0 - 4       | x1          |
| 5 - 9       | x2          |
| 10 - 14     | x3          |
| 15+         | x4          |

You can set the difficulty from 1 to 5. It will affect the spawn probability of snow flakes. Less snow flakes means it is easier to maintain your combo, but your max score is capped lower.

Have fun and merry christmas! ❄️

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)