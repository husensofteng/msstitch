from app.drivers.pycolator import base
from app.actions.pycolator import filters as preparation


class FilterPeptideLength(base.PycolatorDriver):
    """Filters on peptide length, to be specified in calling. Outputs to
    multiple files if multiple file input is given. No PSMs will be
    outputted."""
    outsuffix = '_filt_len.xml'
    command = 'filterlen'

    def __init__(self, **kwargs):
        super(FilterPeptideLength, self).__init__(**kwargs)
        self.minlength = kwargs.get('minlength', 0)
        self.maxlength = kwargs.get('maxlength', None)

    def set_features(self):
        # FIXME psm filter len too!
        self.features = {
            'psm': preparation.filter_peptide_length(
                self.allpsms, 'psm', self.ns, self.minlength, self.maxlength),
            'peptide': preparation.filter_peptide_length(
                self.allpeps, 'pep', self.ns, self.minlength, self.maxlength)
        }


class FilterUniquePeptides(base.PycolatorDriver):
    """This class processes multiple percolator runs from fractions and
    filters out the best scoring peptides."""
    outsuffix = '_filtuniq.xml'
    command = 'filteruni'

    def __init__(self, **kwargs):
        super(FilterUniquePeptides, self).__init__(**kwargs)
        self.score = kwargs.get('score')
        if self.score is None:
            self.score = 'svm'

    def get_all_psms(self):
        """Override parent method so it returns strings instead"""
        return self.get_all_psms_strings()

    def set_features(self):
        uniquepeps = preparation.filter_unique_peptides(self.allpeps,
                                                        self.score,
                                                        self.ns)
        self.features = {'psm': self.allpsms, 'peptide': uniquepeps}


class FilterKnownPeptides(base.PycolatorDriver):
    """This class processes multiple percolator runs from fractions and
    filters out first peptides that are found in a specified searchspace. Then
    it keeps the remaining best scoring unique peptides."""
    outsuffix = '_filtknown.xml'
    lookuptype = 'searchspace'
    command = 'filterknown'

    def __init__(self, **kwargs):
        super(FilterKnownPeptides, self).__init__(**kwargs)
        self.db = kwargs.get('database')
        self.falloff = kwargs.get('falloff')

    def set_features(self):
        self.features = {
            'peptide': preparation.filter_known_searchspace(self.allpeps,
                                                            'pep',
                                                            self.lookup,
                                                            self.ns,
                                                            self.falloff),
            'psm': preparation.filter_known_searchspace(self.allpsms,
                                                        'psm',
                                                        self.lookup,
                                                        self.ns,
                                                        self.falloff),
        }
