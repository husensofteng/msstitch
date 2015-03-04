from app.lookups.sqlite.base import DatabaseConnection


class SpectraDB(DatabaseConnection):
    def add_tables(self):
        self.create_tables(['mzml'])

    def get_mzmlfile_map(self):
        cursor = self.get_cursor()
        cursor.execute('SELECT mzmlfile_id, mzmlfilename FROM mzmlfiles')
        return cursor.fetchall()

    def store_mzmls(self, spectra):
        self.store_many(
            'INSERT INTO mzml(mzmlfile_id, scan_nr, retention_time) '
            'VALUES (?, ?, ?)', spectra)

    def index_mzml(self):
        self.index_column('mzmlfnid_index', 'mzml', 'mzmlfile_id')
        self.index_column('scan_index', 'mzml', 'scan_nr')
        self.index_column('rt_index', 'mzml', 'retention_time')
