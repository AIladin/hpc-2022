import logging
import os
import os.path as osp
from typing import Optional

import numpy as np
from fire import Fire
from mpi4py import MPI

from image_processing import downscale_image
from utils import timing


def worker(
    comm,
    output_folder: str,
    data: Optional[list[np.ndarray]],
    im_size: tuple[int, int] = (64, 64),
):
    rank = comm.Get_rank()
    file_paths: np.ndarray = comm.scatter(data, root=0)
    with timing(f"Rank: {rank}; processing {len(file_paths)} images."):
        for file_path in file_paths:
            filename: str = osp.splitext(osp.basename(file_path))[0]
            output_path = osp.join(output_folder, filename + ".png")
            downscale_image(file_path, output_path, im_size)


def producer(comm, listing_path: str, output_folder: str) -> list[np.ndarray]:
    with open(listing_path, "r") as f:
        filenames = f.read().splitlines()
    if not osp.exists(output_folder):
        os.mkdir(output_folder)

    logging.info(f"Total images: {len(filenames)}")

    nprocs = comm.Get_size()
    batches = np.array_split(filenames, nprocs)

    return batches


def main(
    output_folder: str = "data/rescaled_dataset",
    image_list: str = "data/image_list.txt",
    im_size: tuple[int, int] = (32, 32),
):

    logging.basicConfig(level=logging.INFO)
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    data: Optional[list[np.ndarray]] = None
    if rank == 0:
        data = producer(comm, image_list, output_folder)
    worker(comm, output_folder, data, im_size)


if __name__ == "__main__":
    Fire(main)
