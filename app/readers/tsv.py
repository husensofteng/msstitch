import itertools
from hashlib import md5
from app.dataformats import mzidtsv as mzidtsvdata


def get_tsv_header(tsvfn):
    with open(tsvfn) as fp:
        return next(fp).strip().split('\t')


def generate_tsv_lines_multifile(fns, header):
    return itertools.chain.from_iterable([generate_tsv_psms(fn, header)
                                          for fn in fns])


def generate_tsv_psms(fn, header):
    """Returns dicts with header-keys and psm statistic values"""
    for line in generate_tsv_psms_line(fn):
        yield {x: y for (x, y) in zip(header, line.strip().split('\t'))}


def generate_tsv_psms_line(fn):
    with open(fn) as fp:
        next(fp)  # skip header
        for line in fp:
            yield line


def get_proteins_from_psm(line):
    """From a line, return list of proteins reported by Mzid2TSV. The line
    should not be unrolled."""
    proteins = line[mzidtsvdata.HEADER_PROTEIN].split(';')
    outproteins = []
    for protein in proteins:
        try:
            outproteins.append(protein[:protein.index('(')].strip())
        except ValueError:
            outproteins.append(protein)
    return outproteins


def get_psm_id_from_line(line):
    return md5('{0}{1}'.format(line[mzidtsvdata.HEADER_SPECFILE],
                               line[mzidtsvdata.HEADER_SCANNR])
               .encode('utf-8')).hexdigest()


def get_pepproteins(line, unroll=False):
    """From a line, generate a psm_id (MD5 of specfile and scannr).
    Returns that id with the peptide sequence and protein accessions.
    Return values:
        specfn          -   str
        scan            -   str
        psm_id          -   str
        peptideseq      -   str
        proteins        -   list of str
    """
    specfn = line[mzidtsvdata.HEADER_SPECFILE]
    scan = line[mzidtsvdata.HEADER_SCANNR]
    score = line[mzidtsvdata.HEADER_MSGFSCORE]
    psm_id = get_psm_id_from_line(line)
    peptideseq = line[mzidtsvdata.HEADER_PEPTIDE]
    if unroll and '.' in peptideseq:
        peptideseq = peptideseq.split('.')[1]
    proteins = get_proteins_from_psm(line)
    return specfn, scan, psm_id, peptideseq, score, proteins
