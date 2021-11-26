# Contributing

Thank you for considering Pycordia as your next place for contribution. Your efforts keep this library alive.

Pycordia has a set of contributing guidelines to keep readability, ease of use, and accessibility in place.

Your contribution should maintain a balance between the 3 core principles below:

- **Readability**: Keep code clean and readable, both for the end user and for the average maintainer, so that even a user with no experience in Discord bot development can understand.
- **Ease of Use**: Make Pycordia easy to use, make it enjoyable to work with.
- **Accessibility**: Make Pycordia accessible to all people, both bot developers and our contributors. Keep code organized, with in-depth documentation and coherent examples.

## Prerequisites

Due to the nature of this library, it is recommended you have a decent understanding of intermediate Python concepts (async, sockets, classes, packages, etc).

You're also expected to have some knowledge in Git and Github, and if you're directly contributing to documentation, have basic knowledge of ReStructuredText and Markdown.

You also may want to read our Wiki section as it outlines the reason of some of our design decisions as well as useful resources for contributors.

While not required, this helps us maintain our principles and makes it more likely for your pull request to be merged.

## Setup Before Contribution

First, you have to fork the repository and proceed to clone it. We recommend you clone it into a virtual environment so that the requirements are only installed to that environment.

> Make sure that you're running one of the supported versions for Pycordia -- so 3.7 or later

- Create your virtual environment and activate it

```sh
python -m venv your_venv_name
cd your_venv_name & .\Scripts\activate 
```

- Clone the repository and install from `requirements.txt`

```sh
git clone https://github.com/<YOUR_USERNAME>/pycordia
pip install -r requirements.txt
```

Now you're ready to make your contribution. Make sure you're in the `main` branch
before contributing your changes. The `gh-pages` branch should not be touched as the changes will likely be overwritten by the documentation creation action.

## Contributing - Style Guidelines

### Docstrings

Docstrings should use the style preferred by the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html#docstrings)

### Code

Code should mostly adhere to the [PEP8 style guide](https://www.python.org/dev/peps/pep-0008/)

Line lengths can exceed the set limit of 80, but should not exceed 100 characters.

### Markdown

Markdown should adhere to [Markdownlint](https://github.com/DavidAnson/markdownlint).

### Github

Commits should use [Gitmoji](https://gitmoji.dev/). This is to maintain organization throughout the repository and it also adds a nice touch to it.

## Before Making a PR

- Make sure the code runs and show that what you have implemented works correctly.
- Document the code so that both our developers and other users can understand it.
