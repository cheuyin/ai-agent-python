from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich import box as rich_box

console = Console()


def print_banner():
    console.print()
    console.print(
        Panel(
            "[bold bright_cyan]AI Agent[/]  [dim]powered by Google Gemini[/]",
            box=rich_box.ROUNDED,
            border_style="bright_cyan",
            padding=(0, 2),
        )
    )
    console.print()


def get_user_input() -> str:
    text = console.input("\n[bold bright_cyan]❯[/] ")
    if text.strip():
        console.print(
            Panel(
                text,
                title="[bold bright_cyan]You[/]",
                border_style="bright_cyan",
                box=rich_box.ROUNDED,
            )
        )
    return text


def print_agent_response(text: str):
    console.print(
        Panel(
            Markdown(text),
            title="[bold bright_green]Agent[/]",
            border_style="bright_green",
            box=rich_box.ROUNDED,
        )
    )


def print_tool_call(name: str, args: dict, result: str):
    def fmt_val(v: str) -> str:
        return v[:40] + "…" if len(v) > 40 else v

    args_str = ", ".join(f"{k}={fmt_val(repr(v))}" for k, v in args.items())
    result_preview = result.replace("\n", " ")
    result_preview = result_preview[:100] + "…" if len(result_preview) > 100 else result_preview
    console.print(f"  [dim]· {name}({args_str}) → {result_preview}[/dim]")


def print_stats(stats: dict):
    model = stats.get("model", "unknown")
    prompt_tokens = stats.get("prompt_tokens", 0)
    token_limit = stats.get("token_limit", 0)
    total_cost = stats.get("total_cost", 0.0)

    content = (
        f"[dim]model:[/] {model}   "
        f"[dim]context:[/] {prompt_tokens:,} / {token_limit:,} tokens   "
        f"[dim]cost:[/] ${total_cost:.6f}"
    )
    console.print(
        Panel(
            content,
            border_style="dim",
            box=rich_box.SIMPLE,
            padding=(0, 1),
        )
    )


def print_warning(text: str):
    console.print(f"\n[bold yellow]⚠  {text}[/bold yellow]")


def print_error(text: str):
    console.print(f"\n[bold red]✗  {text}[/bold red]")
