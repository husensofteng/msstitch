from app.actions.mzidtsv import quant as prep
from app.drivers.mzidtsv import MzidTSVDriver


class TSVQuantDriver(MzidTSVDriver):
    lookuptype = 'quant'
    outsuffix = '_quant.tsv'
    command = 'addquant'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.precursor = kwargs.get('precursor', False)
        self.isobaric = kwargs.get('isobaric', False)

    def get_psms(self):
        """Creates iterator to write to new tsv. Contains input tsv
        lines plus quant data for these."""
        self.header, isob_header = prep.get_full_and_isobaric_headers(
            self.oldheader, self.lookup, self.isobaric, self.precursor)
        self.psms = prep.generate_psms_quanted(self.lookup, self.fn,
                                               isob_header, self.oldheader,
                                               self.isobaric, self.precursor)
