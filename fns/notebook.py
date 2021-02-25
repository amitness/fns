from typing import List


def print_markdown(markdown):
    from IPython.display import Markdown, display
    display(Markdown(markdown))


def print_bullets(lines: List[str]):
    bullet_points = '\n'.join(f'- `{line}`' for line in sorted(lines))
    print_markdown(bullet_points)


def print_header(text: str,
                 level: int = 2):
    print_markdown(f'{"#" * level} {text}')
