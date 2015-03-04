from app.lookups.sqlite.base import DatabaseConnection


class QuantDB(DatabaseConnection):
    def create_quantdb(self, workdir):
        self.create_db(workdir, ['mzml', 'isobaric_quant', 'ms1_quant'],
                       foreign_keys=True)

    def store_isobaric_quants(self, quants):
        self.store_many(
            'INSERT INTO isobaric_quant(mzmlfilename, retention_time, '
            'quantmap, intensity) VALUES (?, ?, ?, ?)', quants)

    def store_mzmls(self, spectra):
        self.store_many(
            'INSERT INTO mzml(mzmlfilename, scan_nr, retention_time) '
            'VALUES (?, ?, ?)', spectra)

    def store_ms1_quants(self, quants):
        self.store_many(
            'INSERT INTO ms1_quant(mzmlfilename, retention_time, mz, '
            'charge, intensity) VALUES (?, ?, ?, ?, ?)', quants)

    def store_many(self, sql, values):
        cursor = self.get_cursor()
        cursor.executemany(sql, values)
        self.conn.commit()

    def index_mzml(self):
        self.index_column('mzmlfn_index', 'mzml', 'mzmlfilename')
        self.index_column('scan_index', 'mzml', 'scan_nr')
        self.index_column('rt_index', 'mzml', 'retention_time')

    def index_isobaric_quants(self):
        pass

    def index_precursor_quants(self):
        self.index_column('charge_index', 'ms1_quant', 'charge')
        self.index_column('mz_index', 'ms1_quant', 'mz')

    def lookup_retention_time(self, spectrafile, scannr):
        cursor = self.get_cursor()
        cursor.execute(
            'SELECT retention_time FROM mzml '
            'WHERE mzmlfilename=? AND scan_nr=?',
            (spectrafile, scannr))
        return cursor.fetchall()

    def lookup_isobaric_quant(self, spectrafile, scannr):
        cursor = self.get_cursor()
        cursor.execute(
            'SELECT iq.quantmap, iq.intensity '
            'FROM mzml AS mz '
            'JOIN isobaric_quant AS iq USING(retention_time) '
            'WHERE mz.mzmlfilename=? AND mz.scan_nr=?', (spectrafile, scannr))
        return cursor.fetchall()

    def lookup_precursor_quant(self, spectrafile, charge, minrt, maxrt,
                               minmz, maxmz):
        # FIXME check if this is slow since it has two BETWEEN in it
        # we could replace the mz BETWEEN by filtering in python
        cursor = self.get_cursor()
        return cursor.execute(
            'SELECT mz, intensity '
            'FROM ms1_quant '
            'WHERE mzmlfilename=? AND charge=? AND '
            'retention_time BETWEEN ? AND ? AND mz BETWEEN ? AND ?',
            (spectrafile, charge, minrt, maxrt, minmz, maxmz))

    def get_all_quantmaps(self):
        cursor = self.get_cursor()
        cursor.execute(
            'SELECT DISTINCT quantmap FROM isobaric_quant')
        return cursor.fetchall()