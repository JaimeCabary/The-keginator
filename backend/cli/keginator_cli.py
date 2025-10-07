#!/usr/bin/env python3
"""
Keginator CLI - Data cleaning + Solana blockchain integration
"""
import click
import requests
import os
from pathlib import Path
from typing import Optional
import json
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

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


@cli.command()
@click.argument('file', type=click.Path(exists=True))
@click.option('--user-id', required=True, help='Your user identifier')
@click.option('--commit/--no-commit', default=False, help='Auto-commit to Solana')
@click.option('--output', '-o', help='Output file path for cleaned data')
def upload(file: str, user_id: str, commit: bool, output: Optional[str]):
    """
    Upload and clean a dataset
    
    Supports: CSV, JSON, XLSX
    """
    file_path = Path(file)
    
    if not file_path.exists():
        console.print(f"[red]❌ File not found: {file}[/red]")
        return
    
    console.print(f"[cyan]📤 Uploading {file_path.name}...[/cyan]")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Processing...", total=None)
        
        try:
            with open(file_path, 'rb') as f:
                files = {'file': (file_path.name, f)}
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
            console.print(f"[red]❌ Cannot connect to API at {API_URL}[/red]")
            console.print("[yellow]💡 Is the backend running? Try: uvicorn app.main:app[/yellow]")
            return
        except requests.exceptions.HTTPError as e:
            console.print(f"[red]❌ Upload failed: {e.response.text}[/red]")
            return
        except Exception as e:
            console.print(f"[red]❌ Error: {str(e)}[/red]")
            return
    
    # Display results
    console.print("\n[green]✅ Dataset cleaned successfully![/green]\n")
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("Dataset ID", result['dataset_id'])
    table.add_row("Dataset Hash", result['dataset_hash'][:16] + "...")
    table.add_row("Original Rows", str(result['original_rows']))
    table.add_row("Cleaned Rows", str(result['cleaned_rows']))
    table.add_row("Columns", str(len(result['columns'])))
    
    if result.get('committed_to_solana'):
        table.add_row("Solana Status", "✅ Committed")
        table.add_row("Transaction", result['solana_signature'][:16] + "...")
    else:
        table.add_row("Solana Status", "⏸️ Not committed")
    
    console.print(table)
    
    # Show cleaning report
    if result.get('cleaning_report'):
        console.print("\n[bold]📊 Cleaning Report:[/bold]")
        report = result['cleaning_report']
        
        for op in report.get('operations', []):
            step = op.get('step', 'unknown')
            console.print(f"  • {step}")
    
    # Download cleaned file
    if output or True:
        output_path = Path(output) if output else Path(f"cleaned_{file_path.name}")
        
        console.print(f"\n[cyan]💾 Downloading cleaned dataset...[/cyan]")
        
        download_url = f"{API_URL}{result['download_url']}"
        dl_response = requests.get(download_url)
        
        if dl_response.status_code == 200:
            with open(output_path, 'wb') as f:
                f.write(dl_response.content)
            console.print(f"[green]✅ Saved to: {output_path}[/green]")
        else:
            console.print(f"[yellow]⚠️ Could not download file[/yellow]")
    
    console.print(f"\n[dim]Dataset ID: {result['dataset_id']}[/dim]")


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
    table.add_column("Rows", justify="right")
    table.add_column("Hash", style="yellow")
    table.add_column("Solana", justify="center")
    
    for dataset in data['datasets'][:limit]:
        date = dataset['created_at'][:10]
        filename = dataset['original_filename']
        rows = f"{dataset['rows_cleaned']}"
        hash_short = dataset['dataset_hash'][:12] + "..."
        solana_status = "✅" if dataset['committed_to_solana'] else "⏸️"
        
        table.add_row(date, filename, rows, hash_short, solana_status)
    
    console.print(table)


@cli.command()
@click.argument('dataset_id')
@click.argument('user_id')
def commit(dataset_id: str, user_id: str):
    """
    Commit a dataset hash to Solana blockchain
    """
    console.print(f"[cyan]📡 Committing to Solana...[/cyan]")
    
    try:
        response = requests.post(
            f"{API_URL}/commit",
            params={
                'dataset_id': dataset_id,
                'user_id': user_id
            }
        )
        response.raise_for_status()
        result = response.json()
        
        console.print(f"[green]✅ Committed to Solana![/green]\n")
        console.print(f"Hash: {result['dataset_hash']}")
        console.print(f"Signature: {result['solana_signature']}")
        console.print(f"\n[cyan]View on explorer:[/cyan]")
        console.print(result['explorer_url'])
        
    except requests.exceptions.HTTPError as e:
        console.print(f"[red]❌ Commit failed: {e.response.text}[/red]")
    except Exception as e:
        console.print(f"[red]❌ Error: {str(e)}[/red]")


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
            table.add_row("Status", "✅ On-chain")
            
            if result.get('timestamp'):
                from datetime import datetime
                dt = datetime.fromtimestamp(result['timestamp'])
                table.add_row("Committed At", dt.strftime("%Y-%m-%d %H:%M:%S"))
            
            console.print(table)
        else:
            console.print(f"[yellow]⚠️ Hash not found on Solana[/yellow]")
            console.print(f"Hash: {dataset_hash}")
        
    except Exception as e:
        console.print(f"[red]❌ Verification failed: {str(e)}[/red]")


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
        console.print(f"Status: {data['status']}")
        console.print(f"Solana: {'✅ Connected' if data['solana_connected'] else '❌ Disconnected'}")
        
    except requests.exceptions.ConnectionError:
        console.print(f"[red]❌ Cannot connect to API at {API_URL}[/red]")
    except Exception as e:
        console.print(f"[red]❌ Error: {str(e)}[/red]")


if __name__ == '__main__':
    cli()