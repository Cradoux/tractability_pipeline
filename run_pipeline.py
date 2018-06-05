from ot_tractability_pipeline.buckets import *
import pandas as pd
import argparse


def main(ensembl_id_list, database_url, out_file_name):

    # Assign tractability buckets
    setup = Pipeline_setup(ensembl_id_list)

    sm = Small_molecule_buckets(setup, database_url=database_url)
    sm_out_buckets = sm.assign_buckets()

    print(sm_out_buckets.groupby('Top_bucket')['ensembl_gene_id'].count())

    ab = Antibody_buckets(setup,database_url=database_url,sm_output=sm_out_buckets)
    out_buckets = ab.assign_buckets()
    print(out_buckets.groupby('Top_bucket_ab')['ensembl_gene_id'].count())

    # Antibody output also includes Small
    out_buckets.to_csv('ab_out_buckets.csv')


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Assess tractability of gene list')
    parser.add_argument('genes',
                        help='A file of Ensembl Gene IDs, one per line and no header')
    parser.add_argument('--db',
                        help='Address to your local ChEMBL installation', default=None)
    parser.add_argument('--out_file', default='tractability_buckets.csv',
                        help='Name of output csv file')


    args = parser.parse_args()

    # Get a unique list of Gene IDs from OT
    gene_list = pd.read_csv(args.genes, encoding='utf-8', header=None, names=['ensembl_gene_id'],usecols=[0])
    ensembl_id_list = list(gene_list['ensembl_gene_id'].unique())
    print(ensembl_id_list)

    # URL to local ChEMBL database
    database_url = args.db
    main(ensembl_id_list,database_url, out_file_name=args.out_file)
