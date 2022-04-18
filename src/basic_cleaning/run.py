#!/usr/bin/env python
"""
Download from W&B the raw dataset and apply some basic data cleaning, exporting the result to a new artifact
"""
import argparse
import logging
import wandb
import pandas as pd


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    # artifact_local_path = run.use_artifact(args.input_artifact).file()

    ######################
    # YOUR CODE HERE     #
    ######################
    artifact_local_path = run.use_artifact(args.input_artifact).file()
    df = pd.read_csv(artifact_local_path)
    logger.info("Input artifact loaded")

    idx = df['price'].between(args.min_price, args.max_price)
    df = df[idx].copy()
    logger.info("Price outliers dropped")

    df['last_review'] = pd.to_datetime(df['last_review'])
    logger.info("last_review converted to datetime")

    df.to_csv("clean_sample.csv", index=False)

    logger.info("Creating output artifact")
    artifact = wandb.Artifact(
     args.output_artifact,
     type=args.output_type,
     description=args.output_description,
    )
    artifact.add_file("clean_sample.csv")

    logger.info("Logging output artifact")
    run.log_artifact(artifact)

    # This makes sure that the output artifact is uploaded 
    # before the tempfile is destroyed
    artifact.wait()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="A very basic data cleaning")


    parser.add_argument(
        "--input_artifact", 
        type=str,
        help="Input artifact name to be cleaned",
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type=str,
        help="Output artifact name cleaned",
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str,
        help="Type for the output artifact",
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type=str,
        help="Description for the otuput artifact",
        required=True
    )

    parser.add_argument(
        "--min_price", 
        type=float,
        help="Minimum accepted price",
        required=True
    )

    parser.add_argument(
        "--max_price", 
        type=float,
        help="Maximum accepted price",
        required=True
    )


    args = parser.parse_args()

    go(args)
