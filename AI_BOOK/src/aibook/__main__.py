"""
Command Line Interface voor het AI Book project.
"""

import argparse
import sys
from . import __version__
from .builder import BookBuilder
from .server import BookServer

def main():
    """Hoofdfunctie voor de command line interface."""
    parser = argparse.ArgumentParser(description="AI Book Generator")
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
    
    subparsers = parser.add_subparsers(dest='command', help='Beschikbare commando\'s')
    
    # Build commando
    build_parser = subparsers.add_parser('build', help='Bouw het boek')
    build_parser.add_argument('--output', '-o', default='dist',
                            help='Output directory (default: dist)')
    
    # Serve commando
    serve_parser = subparsers.add_parser('serve', help='Start de development server')
    serve_parser.add_argument('--port', '-p', type=int, default=8000,
                             help='Port nummer (default: 8000)')
    serve_parser.add_argument('--host', default='localhost',
                             help='Host adres (default: localhost)')
    
    args = parser.parse_args()
    
    if args.command == 'build':
        builder = BookBuilder(output_dir=args.output)
        builder.build()
    elif args.command == 'serve':
        server = BookServer(host=args.host, port=args.port)
        server.serve()
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == '__main__':
    main() 