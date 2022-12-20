#!/usr/bin/env python3

import argparse
import numpy as np
from .ppp_particle_file import ParticleFile
from .ppp_result_file import ResultsFile
from .ppp_grid import HorizontalGrid, VerticalGrid
from .ppp_quantity import Concentration, Counts


def plot(args):
    print("Plotting")
    filename = args.source
    result_filename = args.out_file
    raise NotImplementedError("Plotting not implemented yet")


def process(args):
    print("Processing")
    overwrite = args.overwrite
    filename = args.source
    result_filename = args.out_file
    topo_filename = args.topo
    resolution = args.resolution
    id_list = args.id_list
    # Default should be a list of all options (loop and compute all)
    sort_by = args.sort
    ini_file = args.ini_file
    last_positions = args.last

    result_file = ResultsFile(result_filename, filename)

    if (result_file.exists and overwrite == False):
        raise Exception("Results file already exists. Use -O to overwrite")

    particle_file = ParticleFile(filename, id_list)
    grid = HorizontalGrid(topo_filename, resolution)
    result_file.initialize(grid)

    counts = grid.get_counts(particle_file, sort_by)

    # Compute measures
    OrdinaryCounter = Counts(grid)
    data = OrdinaryCounter.run(counts)
    result_file.append(data)

    ConcentrationCounter = Concentration(grid)
    data = ConcentrationCounter.run(counts)
    result_file.append(data)

    # Save results
    result_file.write()

    return


def main():

    global_parser = argparse.ArgumentParser(add_help=True)
    subparsers = global_parser.add_subparsers(
        help="Subcommands", dest="subcommand")

    plot_parser = subparsers.add_parser(
        "plot", help="Plot particle distribution")
    plot_parser.add_argument(
        "-s", "--source", help="Path to data file", type=str, required=True)
    plot_parser.add_argument(
        "-o", "--out-file", help="Results file", type=str, required=False, default="counts.nc")
    plot_parser.set_defaults(func=plot)

    process_parser = subparsers.add_parser(
        "process", help="Process particle file")
    process_parser.add_argument(
        "-O", "--overwrite", help=f"Overwrite results file", action='store_true')
    process_parser.add_argument(
        "-s", "--source", help="Path to data file", type=str, required=True)
    process_parser.add_argument(
        "-o", "--out-file", help="Results file", type=str, required=False, default="counts.nc")
    process_parser.add_argument(
        "--topo", help="Topography (grid) file", type=str, required=False, default="topo.nc")
    process_parser.add_argument(
        "-dx", "--resolution", help="Resolution of grid (meters)", type=float)
    process_parser.add_argument("--sort", help="Sort particles",
                                choices=["id", "state"], type=str, required=False, default=None)
    process_parser.add_argument(
        "--id-list", help="List of particle IDs to use in processing", nargs="+", type=float)
    process_parser.add_argument(
        "--ini-file", help="Initial particle position file", type=str, required=False)
    process_parser.add_argument(
        "--last", help=f"Use only last active position", action='store_true')
    process_parser.set_defaults(func=process)

    args = global_parser.parse_args()

    args.func(args)

    return


if __name__ == "__main__":
    main()
