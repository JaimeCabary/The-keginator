# #!/usr/bin/env python3
# """
# Keginator CLI - Data cleaning + Solana blockchain integration
# """
# import click
# import requests
# import os
# from pathlib import Path
# from typing import Optional
# import json
# from rich.console import Console
# from rich.table import Table
# from rich.progress import Progress, SpinnerColumn, TextColumn

# console = Console()

# # Default API endpoint
# API_URL = os.getenv("KEGINATOR_API_URL", "http://localhost:8000")


# @click.group()
# @click.version_option(version="1.0.0")
# def cli():
#     """
#     🔧 Keginator CLI - Clean datasets & commit to Solana
    
#     Examples:
#       keginator upload data.csv --user-id alice
#       keginator history alice
#       keginator verify <hash>
#     """
#     pass


# @cli.command()
# @click.argument('file', type=click.Path(exists=True))
# @click.option('--user-id', required=True, help='Your user identifier')
# @click.option('--commit/--no-commit', default=False, help='Auto-commit to Solana')
# @click.option('--output', '-o', help='Output file path for cleaned data')
# def upload(file: str, user_id: str, commit: bool, output: Optional[str]):
#     """
#     Upload and clean a dataset
    
#     Supports: CSV, JSON, XLSX
#     """
#     file_path = Path(file)
    
#     if not file_path.exists():
#         console.print(f"[red]❌ File not found: {file}[/red]")
#         return
    
#     console.print(f"[cyan]📤 Uploading {file_path.name}...[/cyan]")
    
#     with Progress(
#         SpinnerColumn(),
#         TextColumn("[progress.description]{task.description}"),
#         console=console
#     ) as progress:
#         task = progress.add_task("Processing...", total=None)
        
#         try:
#             with open(file_path, 'rb') as f:
#                 files = {'file': (file_path.name, f)}
#                 params = {
#                     'user_id': user_id,
#                     'auto_commit': commit
#                 }
                
#                 response = requests.post(
#                     f"{API_URL}/upload",
#                     files=files,
#                     params=params,
#                     timeout=300
#                 )
#                 response.raise_for_status()
                
#                 result = response.json()
#                 progress.update(task, completed=True)
        
#         except requests.exceptions.ConnectionError:
#             console.print(f"[red]❌ Cannot connect to API at {API_URL}[/red]")
#             console.print("[yellow]💡 Is the backend running? Try: uvicorn app.main:app[/yellow]")
#             return
#         except requests.exceptions.HTTPError as e:
#             console.print(f"[red]❌ Upload failed: {e.response.text}[/red]")
#             return
#         except Exception as e:
#             console.print(f"[red]❌ Error: {str(e)}[/red]")
#             return
    
#     # Display results
#     console.print("\n[green]✅ Dataset cleaned successfully![/green]\n")
    
#     table = Table(show_header=True, header_style="bold magenta")
#     table.add_column("Metric", style="cyan")
#     table.add_column("Value", style="green")
    
#     table.add_row("Dataset ID", result['dataset_id'])
#     table.add_row("Dataset Hash", result['dataset_hash'][:16] + "...")
#     table.add_row("Original Rows", str(result['original_rows']))
#     table.add_row("Cleaned Rows", str(result['cleaned_rows']))
#     table.add_row("Columns", str(len(result['columns'])))
    
#     if result.get('committed_to_solana'):
#         table.add_row("Solana Status", "✅ Committed")
#         table.add_row("Transaction", result['solana_signature'][:16] + "...")
#     else:
#         table.add_row("Solana Status", "⏸️ Not committed")
    
#     console.print(table)
    
#     # Show cleaning report
#     if result.get('cleaning_report'):
#         console.print("\n[bold]📊 Cleaning Report:[/bold]")
#         report = result['cleaning_report']
        
#         for op in report.get('operations', []):
#             step = op.get('step', 'unknown')
#             console.print(f"  • {step}")
    
#     # Download cleaned file
#     if output or True:
#         output_path = Path(output) if output else Path(f"cleaned_{file_path.name}")
        
#         console.print(f"\n[cyan]💾 Downloading cleaned dataset...[/cyan]")
        
#         download_url = f"{API_URL}{result['download_url']}"
#         dl_response = requests.get(download_url)
        
#         if dl_response.status_code == 200:
#             with open(output_path, 'wb') as f:
#                 f.write(dl_response.content)
#             console.print(f"[green]✅ Saved to: {output_path}[/green]")
#         else:
#             console.print(f"[yellow]⚠️ Could not download file[/yellow]")
    
#     console.print(f"\n[dim]Dataset ID: {result['dataset_id']}[/dim]")


# @cli.command()
# @click.argument('user_id')
# @click.option('--limit', default=10, help='Number of records to show')
# def history(user_id: str, limit: int):
#     """
#     View your dataset history
#     """
#     try:
#         response = requests.get(
#             f"{API_URL}/history/{user_id}",
#             params={'limit': limit}
#         )
#         response.raise_for_status()
#         data = response.json()
        
#     except requests.exceptions.ConnectionError:
#         console.print(f"[red]❌ Cannot connect to API at {API_URL}[/red]")
#         return
#     except Exception as e:
#         console.print(f"[red]❌ Error: {str(e)}[/red]")
#         return
    
#     if data['total_datasets'] == 0:
#         console.print(f"[yellow]No datasets found for user: {user_id}[/yellow]")
#         return
    
#     console.print(f"\n[bold cyan]📜 History for {user_id}[/bold cyan]")
#     console.print(f"[dim]Total datasets: {data['total_datasets']}[/dim]\n")
    
#     table = Table(show_header=True, header_style="bold magenta")
#     table.add_column("Date", style="cyan")
#     table.add_column("File", style="white")
#     table.add_column("Rows", justify="right")
#     table.add_column("Hash", style="yellow")
#     table.add_column("Solana", justify="center")
    
#     for dataset in data['datasets'][:limit]:
#         date = dataset['created_at'][:10]
#         filename = dataset['original_filename']
#         rows = f"{dataset['rows_cleaned']}"
#         hash_short = dataset['dataset_hash'][:12] + "..."
#         solana_status = "✅" if dataset['committed_to_solana'] else "⏸️"
        
#         table.add_row(date, filename, rows, hash_short, solana_status)
    
#     console.print(table)


# @cli.command()
# @click.argument('dataset_id')
# @click.argument('user_id')
# def commit(dataset_id: str, user_id: str):
#     """
#     Commit a dataset hash to Solana blockchain
#     """
#     console.print(f"[cyan]📡 Committing to Solana...[/cyan]")
    
#     try:
#         response = requests.post(
#             f"{API_URL}/commit",
#             params={
#                 'dataset_id': dataset_id,
#                 'user_id': user_id
#             }
#         )
#         response.raise_for_status()
#         result = response.json()
        
#         console.print(f"[green]✅ Committed to Solana![/green]\n")
#         console.print(f"Hash: {result['dataset_hash']}")
#         console.print(f"Signature: {result['solana_signature']}")
#         console.print(f"\n[cyan]View on explorer:[/cyan]")
#         console.print(result['explorer_url'])
        
#     except requests.exceptions.HTTPError as e:
#         console.print(f"[red]❌ Commit failed: {e.response.text}[/red]")
#     except Exception as e:
#         console.print(f"[red]❌ Error: {str(e)}[/red]")


# @cli.command()
# @click.argument('dataset_hash')
# def verify(dataset_hash: str):
#     """
#     Verify if a dataset hash exists on Solana
#     """
#     console.print(f"[cyan]🔍 Verifying hash on Solana...[/cyan]")
    
#     try:
#         response = requests.get(f"{API_URL}/verify/{dataset_hash}")
#         response.raise_for_status()
#         result = response.json()
        
#         if result['exists_on_chain']:
#             console.print(f"[green]✅ Hash verified on Solana![/green]\n")
            
#             table = Table(show_header=False)
#             table.add_column("Property", style="cyan")
#             table.add_column("Value", style="white")
            
#             table.add_row("Hash", dataset_hash)
#             table.add_row("Status", "✅ On-chain")
            
#             if result.get('timestamp'):
#                 from datetime import datetime
#                 dt = datetime.fromtimestamp(result['timestamp'])
#                 table.add_row("Committed At", dt.strftime("%Y-%m-%d %H:%M:%S"))
            
#             console.print(table)
#         else:
#             console.print(f"[yellow]⚠️ Hash not found on Solana[/yellow]")
#             console.print(f"Hash: {dataset_hash}")
        
#     except Exception as e:
#         console.print(f"[red]❌ Verification failed: {str(e)}[/red]")


# @cli.command()
# def status():
#     """
#     Check API health status
#     """
#     try:
#         response = requests.get(f"{API_URL}/health", timeout=5)
#         response.raise_for_status()
#         data = response.json()
        
#         console.print("[green]✅ API is healthy[/green]")
#         console.print(f"Status: {data['status']}")
#         console.print(f"Solana: {'✅ Connected' if data['solana_connected'] else '❌ Disconnected'}")
        
#     except requests.exceptions.ConnectionError:
#         console.print(f"[red]❌ Cannot connect to API at {API_URL}[/red]")
#     except Exception as e:
#         console.print(f"[red]❌ Error: {str(e)}[/red]")


# if __name__ == '__main__':
#     cli()





#!/usr/bin/env python3
"""
Keginator CLI - Data cleaning + Solana blockchain integration
"""
import click
import requests
import os
import json
from pathlib import Path
from typing import Optional, Dict, Any
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from datetime import datetime # Required for verify command

console = Console()

# Default API endpoint
API_URL = os.getenv("KEGINATOR_API_URL", "http://localhost:8000")


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """
    🔧 Keginator CLI - Clean datasets & commit to Solana
    
    Examples:
      keginator upload data.csv --user-id alice
      keginator history alice
      keginator verify <hash>
    """
    pass

def _format_cleaning_report(report: Dict[str, Any]) -> str:
    """Formats the complex nested cleaning report for rich console display."""
    
    if not report or not report.get('cleaning_operations'):
        return "[dim]No cleaning report available.[/dim]"

    parts = []
    
    # 1. Cleaning Operations Summary
    parts.append("[bold underline]Cleanup Operations:[/bold underline]")
    for op in report.get('cleaning_operations', {}).get('operations', []):
        step = op.get('step', 'N/A').replace('_', ' ').title()
        details = ""
        
        if step == "Remove Empty":
            details = f"Rows removed: {op.get('rows_removed', 0)}, Cols removed: {op.get('columns_removed', 0)}"
        elif step == "Remove Duplicates":
            details = f"Duplicates removed: {op.get('duplicates_removed', 0)}"
        elif step == "Ai Recommendations":
            details = f"Actions: {len(op.get('actions', []))}"
        elif step == "Scaling Encoding":
            details = f"Scaled: {len(op.get('scaled_columns', []))}, Encoded: {len(op.get('encoded_columns', []))}"
        elif step == "Text Embedding":
            details = f"Embedded: {len(op.get('embedded_columns', []))} columns ({report.get('preprocessing_details', {}).get('embedding_summary', {}).get('vector_size', 384)} dim vectors)"
        
        parts.append(f"[cyan]  • {step}:[/cyan] [white]{details}[/white]")

    # 2. Preprocessing Details (Maps)
    parts.append("\n[bold underline]Preprocessing Details (Maps):[/bold underline]")
    details = report.get('preprocessing_details', {})
    
    if details.get('scaling_maps'):
        parts.append(f"[magenta]  • Numerical Scaling:[/magenta] {len(details['scaling_maps'])} columns scaled.")
    if details.get('encoding_maps'):
        parts.append(f"[magenta]  • Label Encoding:[/magenta] {len(details['encoding_maps'])} columns encoded.")
    if details.get('embedding_summary') and isinstance(details['embedding_summary'], dict) and details['embedding_summary'].get('vector_size'):
        parts.append(f"[yellow]  • Text Embedding:[/yellow] {details['embedding_summary']['vector_size']} dimensions.")

    
    # 3. AI Insights
    ai_insights = report.get('cleaning_operations', {}).get('ai_insights', [])
    if ai_insights:
        parts.append("\n[bold underline]Gemini AI Insights:[/bold underline]")
        for insight in ai_insights:
            if isinstance(insight, dict) and insight.get('quality_score'):
                 parts.append(f"[yellow]  • Final Quality Score:[/yellow] [bold]{insight['quality_score']}[/bold]")
                 parts.extend([f"[dim]    - Suggestion:[/dim] {s}" for s in insight.get('suggestions', [])])
            elif isinstance(insight, str):
                 parts.append(f"[yellow]  • {insight}[/yellow]")
    
    return "\n".join(parts)

def _display_tabular_result(result: Dict[str, Any], file_path: Path):
    """Displays results for tabular data processing."""
    console.print("\n[green]✅ Dataset cleaned and processed successfully![/green]\n")

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("Dataset Type", "[bold]Tabular (CSV/JSON/XLSX)[/bold]")
    table.add_row("Original File", file_path.name)
    table.add_row("Original Rows", str(result['original_rows']))
    table.add_row("Cleaned Rows", str(result['cleaned_rows']))
    table.add_row("Final Columns", str(len(result['columns'])))
    table.add_row("Original Size", result['file_size'])
    table.add_row("Cleaned Size", result['cleaned_size'])
    
    console.print(table)
    
    # Detailed Preprocessing Report (New JSON Structure)
    report_panel = Panel.fit(
        _format_cleaning_report(result.get('cleaning_report')),
        title="[bold blue]📊 Cleaning & Preprocessing Report[/bold blue]",
        border_style="blue"
    )
    console.print(report_panel)

def _display_audio_result(result: Dict[str, Any]):
    """Displays results for audio data transcription."""
    audio_report = result.get('audio_report', {})
    
    console.print("\n[green]✅ Audio transcribed and committed successfully![/green]\n")

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("Dataset Type", "[bold yellow]Audio (Transcription)[/bold yellow]")
    table.add_row("Original File", audio_report.get('file_name', 'N/A'))
    table.add_row("Duration", f"{audio_report.get('duration_seconds', 0)} seconds")
    table.add_row("Transcript Hash", result.get('transcript_hash', '')[:16] + "...")
    table.add_row("Confidence Avg", f"{audio_report.get('confidence_score_avg', 0):.4f}")
    table.add_row("Processing Time", f"{audio_report.get('processing_time_s', 0):.2f}s")

    console.print(table)
    
    # Display Transcription
    transcript_panel = Panel(
        audio_report.get('transcript_text', 'No transcript available.'),
        title="[bold blue]🎙️ Transcription Output[/bold blue]",
        border_style="yellow"
    )
    console.print(transcript_panel)


@cli.command()
@click.argument('file', type=click.Path(exists=True))
@click.option('--user-id', required=True, help='Your user identifier')
@click.option('--commit/--no-commit', default=False, help='Auto-commit hash to Solana')
@click.option('--output', '-o', help='Output file path for cleaned data (Tabular only)')
def upload(file: str, user_id: str, commit: bool, output: Optional[str]):
    """
    Upload and process a dataset (Tabular: CSV/JSON/XLSX or Audio: MP3/WAV)
    """
    file_path = Path(file)
    file_name = file_path.name
    
    supported_extensions = ['.csv', '.json', '.xlsx', '.xls', '.mp3', '.wav']
    if file_path.suffix.lower() not in supported_extensions:
        console.print(f"[red]❌ Unsupported file format: {file_path.suffix}. Supports: {', '.join(supported_extensions)}[/red]")
        return
    
    console.print(f"[cyan]📤 Uploading {file_name} for processing...[/cyan]")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Processing data pipeline...", total=None)
        
        try:
            with open(file_path, 'rb') as f:
                files = {'file': (file_name, f)}
                params = {
                    'user_id': user_id,
                    'auto_commit': commit
                }
                
                response = requests.post(
                    f"{API_URL}/upload",
                    files=files,
                    params=params,
                    timeout=300
                )
                response.raise_for_status()
                
                result = response.json()
                progress.update(task, completed=True)
        
        except requests.exceptions.ConnectionError:
            progress.update(task, completed=True)
            console.print(f"[red]❌ Cannot connect to API at {API_URL}[/red]")
            console.print("[yellow]💡 Is the backend running? Try: uvicorn app.main:app[/yellow]")
            return
        except requests.exceptions.HTTPError as e:
            progress.update(task, completed=True)
            error_details = e.response.json().get('detail', e.response.text)
            console.print(f"[red]❌ Upload failed ({e.response.status_code}): {error_details}[/red]")
            return
        except Exception as e:
            progress.update(task, completed=True)
            console.print(f"[red]❌ Error: {str(e)}[/red]")
            return
    
    # --- Display Logic based on file type ---
    if result.get('type') in ['tabular', 'tabular_duplicate']:
        _display_tabular_result(result, file_path)
        
        # Download cleaned file (Tabular only)
        if result.get('download_url'):
            # Determine output path, defaulting to cleaned_originalfilename.csv
            output_path = Path(output) if output else Path(f"{file_path.stem}_cleaned.csv")
            
            console.print(f"\n[cyan]💾 Downloading cleaned dataset...[/cyan]")
            
            download_url = f"{API_URL}{result['download_url']}"
            dl_response = requests.get(download_url)
            
            if dl_response.status_code == 200:
                with open(output_path, 'wb') as f:
                    f.write(dl_response.content)
                console.print(f"[green]✅ Saved cleaned data to: {output_path.resolve()}[/green]")
            else:
                console.print(f"[yellow]⚠️ Could not download file[/yellow]")

    elif result.get('type') == 'audio':
        _display_audio_result(result)
    
    else:
        # Catch unexpected types
        console.print("[red]❌ Error: Received unexpected response type from API.[/red]")

    # --- Solana Commit Status (Unified) ---
    if result.get('solana_signature'):
        console.print(f"\n[bold magenta]🔗 Solana Transaction:[/bold magenta]")
        console.print(f"  [white]Signature:[/white] [dim]{result['solana_signature']}[/dim]")
        console.print(f"  [cyan]Explorer:[/cyan] https://explorer.solana.com/tx/{result['solana_signature']}?cluster=devnet")
    elif commit and result.get('type') not in ['tabular_duplicate', 'audio']: # Avoid double-warnings for audio if commit failed inside processor
        console.print("[yellow]⚠️ Auto-commit failed or was skipped.[/yellow]")
    
    if result.get('dataset_id'):
        console.print(f"\n[dim]Dataset ID: {result['dataset_id']}[/dim]")
    elif result.get('transcript_hash'):
         console.print(f"\n[dim]Transcript Hash (Source of Truth): {result['transcript_hash']}[/dim]")


@cli.command()
@click.argument('user_id')
@click.option('--limit', default=10, help='Number of records to show')
def history(user_id: str, limit: int):
    """
    View your dataset history
    """
    try:
        response = requests.get(
            f"{API_URL}/history/{user_id}",
            params={'limit': limit}
        )
        response.raise_for_status()
        data = response.json()
        
    except requests.exceptions.ConnectionError:
        console.print(f"[red]❌ Cannot connect to API at {API_URL}[/red]")
        return
    except Exception as e:
        console.print(f"[red]❌ Error: {str(e)}[/red]")
        return
    
    if data['total_datasets'] == 0:
        console.print(f"[yellow]No datasets found for user: {user_id}[/yellow]")
        return
    
    console.print(f"\n[bold cyan]📜 History for {user_id}[/bold cyan]")
    console.print(f"[dim]Total datasets: {data['total_datasets']}[/dim]\n")
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Date", style="cyan")
    table.add_column("File", style="white")
    table.add_column("Status", style="magenta", justify="center")
    table.add_column("Hash", style="yellow")
    table.add_column("Solana", justify="center")
    
    for dataset in data['datasets'][:limit]:
        date = dataset['timestamp'][:10]
        filename = dataset['filename']
        hash_short = dataset['hash'][:12] + "..."
        solana_tx_short = dataset['solanaTx'][:12] + "..." if dataset['solanaTx'] else "N/A"
        
        status_icon = "✅" if dataset['status'] == 'completed' else "⏳"
        
        table.add_row(date, filename, status_icon, hash_short, solana_tx_short)
    
    console.print(table)


@cli.command()
@click.argument('dataset_hash')
def verify(dataset_hash: str):
    """
    Verify if a dataset hash exists on Solana
    """
    console.print(f"[cyan]🔍 Verifying hash on Solana...[/cyan]")
    
    try:
        response = requests.get(f"{API_URL}/verify/{dataset_hash}")
        response.raise_for_status()
        result = response.json()
        
        if result['exists_on_chain']:
            console.print(f"[green]✅ Hash verified on Solana![/green]\n")
            
            table = Table(show_header=False)
            table.add_column("Property", style="cyan")
            table.add_column("Value", style="white")
            
            table.add_row("Hash", dataset_hash)
            table.add_row("Status", "[green]✅ On-chain[/green]")
            
            if result.get('timestamp'):
                # Convert UNIX timestamp (seconds) to datetime object
                dt = datetime.fromtimestamp(result['timestamp'])
                table.add_row("Committed At", dt.strftime("%Y-%m-%d %H:%M:%S"))
            
            console.print(table)
        else:
            console.print(f"[yellow]⚠️ Hash not found on Solana[/yellow]")
            console.print(f"Hash: {dataset_hash}")
        
    except Exception as e:
        console.print(f"[red]❌ Verification failed: {str(e)}[/red]")


@cli.command()
@click.option('--email', required=True, help='User email for Paystack')
@click.option('--amount', required=True, type=int, help='Amount in kobo (e.g., 50000)')
@click.option('--plan', required=True, help='The plan being purchased (e.g., "professional")')
@click.option('--user-id', required=True, help='User ID for payment metadata')
def payment_initialize(email: str, amount: int, plan: str, user_id: str):
    """
    Initialize a Paystack payment and get the authorization URL.
    """
    console.print(f"[cyan]💳 Initializing Paystack payment for {plan} plan...[/cyan]")
    
    try:
        response = requests.post(
            f"{API_URL}/payment/initialize",
            params={
                'email': email,
                'amount_kobo': amount,
                'plan': plan,
                'user_id': user_id
            }
        )
        response.raise_for_status()
        result = response.json()
        
        if result['success']:
            console.print(f"[green]✅ Payment initialized successfully![/green]\n")
            console.print(Panel(
                f"[bold magenta]Reference:[/bold magenta] {result['reference']}\n"
                f"[bold cyan]URL:[/bold cyan] {result['authorization_url']}\n\n"
                f"[yellow]Use the URL above to complete the payment.[/yellow]",
                title="[bold]Transaction Details[/bold]",
                border_style="green"
            ))
        else:
            console.print(f"[red]❌ Initialization failed: {result.get('message', 'Unknown error')}[/red]")
            
    except requests.exceptions.HTTPError as e:
        console.print(f"[red]❌ HTTP Error ({e.response.status_code}): {e.response.json().get('detail', e.response.text)}[/red]")
    except Exception as e:
        console.print(f"[red]❌ Error: {str(e)}[/red]")


@cli.command()
@click.argument('reference')
@click.option('--user-id', required=True, help='User ID for Authorization (Must be authenticated user)')
def payment_verify(reference: str, user_id: str):
    """
    Verify a completed Paystack payment using the reference.
    Note: Requires a valid JWT Token for the authenticated user.
    """
    console.print(f"[cyan]🔎 Verifying Paystack transaction reference {reference}...[/cyan]")
    
    # We must obtain the JWT token to satisfy the backend's `get_current_user` dependency.
    token = console.input(f"[yellow]Enter JWT Token for User ID '{user_id}' (Required by API auth):[/yellow] ")
    if not token:
        console.print("[red]❌ JWT Token is required for API authorization and user lookup.[/red]")
        return
        
    try:
        response = requests.get(
            f"{API_URL}/payment/verify/{reference}",
            headers={'Authorization': f'Bearer {token}'}
        )
        response.raise_for_status()
        result = response.json()
        
        if result['success']:
            console.print(f"\n[green]✅ Payment Verification Successful![/green]\n")
            console.print(Panel(
                f"[bold magenta]Plan Upgraded:[/bold magenta] {result['plan'].upper()}\n"
                f"[bold cyan]Amount Paid:[/bold cyan] ₦{result['amount_paid_kobo'] / 100:.2f} (Kobo converted to Naira)\n"
                f"[bold]User ID:[/bold] {result['user_id']}",
                title="[bold]Subscription Status[/bold]",
                border_style="green"
            ))
        else:
            console.print(f"[yellow]⚠️ Verification Status: {result.get('status', 'N/A')}[/yellow]")
            console.print(f"[red]❌ Verification failed: {result.get('message', 'Unknown error')}[/red]")
            
    except requests.exceptions.HTTPError as e:
        error_details = e.response.json().get('detail', e.response.text)
        console.print(f"[red]❌ HTTP Error ({e.response.status_code}): {error_details}[/red]")
    except Exception as e:
        console.print(f"[red]❌ Error: {str(e)}[/red]")


@cli.command()
def status():
    """
    Check API health status
    """
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        response.raise_for_status()
        data = response.json()
        
        console.print("[green]✅ API is healthy[/green]")
        console.print(f"Status: [cyan]{data['status']}[/cyan]")
        console.print(f"Solana: {'[green]✅ Connected[/green]' if data['solana_connected'] else '[red]❌ Disconnected[/red]'}")
        
    except requests.exceptions.ConnectionError:
        console.print(f"[red]❌ Cannot connect to API at {API_URL}[/red]")
    except Exception as e:
        console.print(f"[red]❌ Error: {str(e)}[/red]")


if __name__ == '__main__':
    cli()