"""Fast Search - CLI Interface."""
import click
import time
from pathlib import Path
from backend.database.database import Database
from backend.indexer.indexer import FileIndexer
from backend.search.search_engine import SearchEngine
from backend.config.config import Config


@click.group()
def cli():
    """Fast Local Desktop Search Tool."""
    pass


@cli.command()
@click.argument('directories', nargs=-1, type=click.Path(exists=True))
@click.option('--clear', is_flag=True, help='Clear existing index before indexing')
def index(directories, clear):
    """Index one or more directories."""
    if not directories:
        directories = Config.DEFAULT_DIRECTORIES
        click.echo(f"No directories specified. Using defaults: {', '.join(directories)}")
    
    db = Database()
    
    if clear:
        click.echo("Clearing existing index...")
        db.clear_index()
    
    indexer = FileIndexer()
    total_indexed = 0
    
    start_time = time.time()
    
    with click.progressbar(
        indexer.index_directories(list(directories)),
        label='Indexing files',
        item_show_func=lambda x: f"{total_indexed} files indexed" if x else ""
    ) as batches:
        for batch in batches:
            inserted = db.insert_files(batch)
            total_indexed += inserted
    
    elapsed = time.time() - start_time
    
    click.echo(f"\n✓ Indexed {total_indexed} files in {elapsed:.2f} seconds")
    click.echo(f"  Database: {db.db_path}")
    
    db.close()


@cli.command()
@click.argument('query')
@click.option('--limit', default=10, help='Maximum number of results')
def search(query, limit):
    """Search for files by name."""
    db = Database()
    
    # Load index
    files = db.get_all_files()
    
    if not files:
        click.echo("No files indexed. Run 'index' command first.")
        db.close()
        return
    
    # Perform search
    start_time = time.time()
    engine = SearchEngine(files)
    results = engine.search(query)
    elapsed = (time.time() - start_time) * 1000  # Convert to ms
    
    # Display results
    click.echo(f"\nFound {len(results)} results in {elapsed:.1f}ms:\n")
    
    for i, result in enumerate(results[:limit], 1):
        click.echo(f"{i}. {result.name} (score: {result.score:.1f})")
        click.echo(f"   {result.path}")
        click.echo()
    
    db.close()


@cli.command()
def stats():
    """Show index statistics."""
    db = Database()
    
    file_count = db.get_file_count()
    
    click.echo(f"\n📊 Index Statistics")
    click.echo(f"   Database: {db.db_path}")
    click.echo(f"   Total files: {file_count:,}")
    
    if file_count > 0:
        # Get some sample data
        files = db.get_all_files()
        extensions = {}
        for f in files:
            ext = f['extension'] or 'no extension'
            extensions[ext] = extensions.get(ext, 0) + 1
        
        click.echo(f"\n   Top file types:")
        for ext, count in sorted(extensions.items(), key=lambda x: x[1], reverse=True)[:5]:
            click.echo(f"     {ext}: {count:,}")
    
    db.close()


@cli.command()
@click.argument('query')
@click.option('--iterations', default=100, help='Number of search iterations')
def benchmark(query, iterations):
    """Benchmark search performance."""
    db = Database()
    files = db.get_all_files()
    
    if not files:
        click.echo("No files indexed. Run 'index' command first.")
        db.close()
        return
    
    engine = SearchEngine(files)
    
    click.echo(f"Running {iterations} searches for '{query}'...")
    
    times = []
    for _ in range(iterations):
        start = time.time()
        engine.search(query)
        elapsed = (time.time() - start) * 1000
        times.append(elapsed)
    
    times.sort()
    avg = sum(times) / len(times)
    p50 = times[len(times) // 2]
    p95 = times[int(len(times) * 0.95)]
    p99 = times[int(len(times) * 0.99)]
    
    click.echo(f"\n⚡ Performance Results:")
    click.echo(f"   Average: {avg:.2f}ms")
    click.echo(f"   Median (p50): {p50:.2f}ms")
    click.echo(f"   p95: {p95:.2f}ms")
    click.echo(f"   p99: {p99:.2f}ms")
    click.echo(f"   Min: {min(times):.2f}ms")
    click.echo(f"   Max: {max(times):.2f}ms")
    
    if p95 < 100:
        click.echo(f"\n✓ Performance target met! (p95 < 100ms)")
    else:
        click.echo(f"\n⚠ Performance target not met (p95 >= 100ms)")
    
    db.close()


@cli.command()
@click.argument('directories', nargs=-1, type=click.Path(exists=True))
def watch(directories):
    """Watch directories for changes and update index in real-time."""
    from backend.search.search_service import SearchService
    
    if not directories:
        directories = Config.DEFAULT_DIRECTORIES
        click.echo(f"No directories specified. Using defaults: {', '.join(directories)}")
    
    # Check if directories exist
    valid_dirs = [d for d in directories if Path(d).exists()]
    if not valid_dirs:
        click.echo("Error: No valid directories to watch")
        return
    
    click.echo(f"\n🔍 Starting file watcher...")
    click.echo(f"   Watching {len(valid_dirs)} directories")
    
    # Create service with watcher enabled
    service = SearchService(enable_watcher=True)
    
    try:
        # Start watching
        service.start_watching(valid_dirs)
        
        click.echo(f"\n✓ File watcher is running!")
        click.echo(f"   Press Ctrl+C to stop\n")
        
        # Keep running
        while True:
            time.sleep(1)
    
    except KeyboardInterrupt:
        click.echo(f"\n\n⏹ Stopping file watcher...")
        service.close()
        click.echo(f"✓ Stopped")


if __name__ == '__main__':
    cli()

